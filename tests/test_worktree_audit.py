import os
from pathlib import Path
import subprocess
import tempfile
import unittest


AUDIT = Path(__file__).resolve().parents[1] / ".agents/skills/poteto-mode/scripts/worktree-audit.sh"


class WorktreeAuditTest(unittest.TestCase):
    def test_audit_uses_the_full_worktree_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            repo = root / "main checkout"
            subprocess.run(["git", "init", "-q", str(repo)], check=True)

            def git(*args):
                subprocess.run(["git", "-C", str(repo), *args], check=True)

            (repo / "tracked").write_text("initial\n")
            git("add", "tracked")
            git("-c", "user.name=Test", "-c", "user.email=test@example.org",
                "-c", "commit.gpgsign=false", "commit", "-qm", "initial")
            clean = root / "feature"
            dirty = root / "feature branch"
            recent = root / "feature [review]"
            missing = root / "missing"
            for tree in (clean, dirty, recent, missing):
                git("worktree", "add", "--detach", "-q", str(tree))
            (dirty / "tracked").write_text("uncommitted\n")
            missing.rename(root / "moved")
            transcripts = root / "transcripts"
            transcripts.mkdir()
            (transcripts / "session notes.jsonl").write_text(f'"{recent}/tracked"\n')

            result = subprocess.run(
                [str(AUDIT), "-b", "HEAD", str(dirty)], check=True,
                env={**os.environ, "PSTACK_TRANSCRIPTS_DIR": str(transcripts)},
                capture_output=True, text=True,
            )
            rows = [line.split("\t") for line in result.stdout.splitlines()[2:]]
            self.assertCountEqual(
                [Path(row[8]) for row in rows], [clean, dirty, recent, missing],
            )
            classifications = {row[8]: (row[3], row[7]) for row in rows}
            self.assertEqual(classifications[str(clean)], ("clean", "safe"))
            self.assertEqual(classifications[str(dirty)], ("wip:1", "hold-wip"))
            self.assertEqual(classifications[str(recent)], ("clean", "verify-recent-chat"))
            self.assertEqual(classifications[str(missing)], ("unknown", "review"))


if __name__ == "__main__":
    unittest.main()
