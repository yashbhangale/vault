"""Compatibility entry point: the safe organizer preserves all existing metadata."""
from pathlib import Path
import subprocess
import sys

repo = Path(__file__).resolve().parents[1]
sys.exit(subprocess.call(["node", str(repo / "scripts/knowledgebase/index.mjs"), "refresh"], cwd=repo))
