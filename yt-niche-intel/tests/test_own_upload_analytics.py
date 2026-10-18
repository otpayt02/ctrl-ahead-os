import csv
from contextlib import closing
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "own_upload_analytics.py"


class OwnUploadAnalyticsTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.db = Path(self.folder.name) / "test.db"

    def tearDown(self):
        self.folder.cleanup()

    def run_cli(self, *arguments, success=True):
        environment = dict(os.environ, PYTHONIOENCODING="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--db", str(self.db), *arguments],
            capture_output=True, text=True, encoding="utf-8", env=environment)
        self.assertEqual(result.returncode == 0, success,
                         (result.stdout or "") + (result.stderr or ""))
        return result

    def test_short_checkpoints_derive_swipe_and_reject_early_or_cross_format(self):
        self.run_cli("register", "--video-id", "TEST1234567", "--format", "short",
                     "--title", "=unsafe title", "--published-at", "2026-10-01T12:00:00Z")
        self.run_cli("snapshot", "--video-id", "TEST1234567", "--window", "24h",
                     "--measured-at", "2026-10-01T13:00:00Z", "--viewed-pct", "72",
                     success=False)
        self.run_cli("snapshot", "--video-id", "TEST1234567", "--window", "24h",
                     "--measured-at", "2026-10-02T12:00:00Z", "--ctr-pct", "4",
                     success=False)
        self.run_cli("snapshot", "--video-id", "TEST1234567", "--window", "24h",
                     "--measured-at", "2026-10-02T12:00:00Z", "--viewed-pct", "72",
                     "--shown-in-feed", "1000")
        self.run_cli("snapshot", "--video-id", "TEST1234567", "--window", "24h",
                     "--measured-at", "2026-10-02T13:00:00Z", "--shown-in-feed", "1200")
        with closing(sqlite3.connect(self.db)) as connection:
            row = connection.execute("SELECT viewed_pct, swipe_pct, shown_in_feed FROM own_upload_snapshots").fetchone()
        self.assertEqual(row, (72.0, 28.0, 1200))
        output = Path(self.folder.name) / "export.csv"
        self.run_cli("export", "--output", str(output))
        with output.open(encoding="utf-8", newline="") as source:
            exported = list(csv.DictReader(source))
        self.assertEqual(len(exported), 1)
        self.assertEqual(exported[0]["title"], "'=unsafe title")

    def test_long_metrics_and_snapshot_windows(self):
        self.run_cli("register", "--video-id", "LONG1234567", "--format", "long",
                     "--title", "Long demo", "--published-at", "2026-10-01T12:00:00Z")
        self.run_cli("snapshot", "--video-id", "LONG1234567", "--window", "7d",
                     "--measured-at", "2026-10-08T12:00:00Z", "--ctr-pct", "4.5",
                     "--retention-30s-pct", "68", "--avd-seconds", "180")
        status = self.run_cli("status").stdout
        self.assertIn("24h: DUE", status)
        self.assertIn("48h: DUE", status)
        self.assertIn("7d: RECORDED", status)
        with closing(sqlite3.connect(self.db)) as connection:
            row = connection.execute("SELECT ctr_pct, retention_30s_pct, avd_seconds FROM own_upload_snapshots").fetchone()
        self.assertEqual(row, (4.5, 68.0, 180.0))


if __name__ == "__main__":
    unittest.main()
