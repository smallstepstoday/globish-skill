#!/usr/bin/env python3
"""
check_globish_on_write.py — PostToolUse hook for the globish plugin.

Fires automatically after Claude writes or edits a file. If the file looks
like prose (.md, .markdown, .txt, .mdx) and isn't part of the plugin's own
bundled reference material, it runs the Globish compliance checker against
it and prints a short summary.

This is a report, not a gate: it always exits 0. Claude Code / Cowork
surfaces PostToolUse hook output as context, which is enough for Claude to
notice flagged issues and offer to fix them in the same turn, without
blocking the write itself. That matches the skill's own stated philosophy —
the checker informs, it doesn't refuse.

Input: the tool-call event as JSON on stdin, per the Claude Code / Cowork
hooks contract (reads tool_input.file_path).
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PROSE_EXTENSIONS = {".md", ".markdown", ".txt", ".mdx"}

# Paths (relative to the plugin root) that are the plugin's own bundled
# material, not a user document — checking these against themselves would
# just be noise (the word list itself isn't "prose").
EXCLUDED_SUBSTRINGS = (
    "/skills/globish/references/",
    "/skills/globish/scripts/",
    "/hooks/",
)


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (event.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    path = Path(file_path)
    if path.suffix.lower() not in PROSE_EXTENSIONS:
        return 0

    normalized = str(path).replace(os.sep, "/")
    if any(marker in normalized for marker in EXCLUDED_SUBSTRINGS):
        return 0

    if not path.exists():
        return 0

    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not plugin_root:
        # Fall back to resolving relative to this script's own location.
        plugin_root = str(Path(__file__).resolve().parent.parent)

    checker = Path(plugin_root) / "skills" / "globish" / "scripts" / "check_globish.py"
    if not checker.exists():
        return 0

    try:
        result = subprocess.run(
            [sys.executable, str(checker), str(path)],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0

    output = result.stdout or ""
    if "Total issues to review:" in output:
        # Pull just the counts, not the full word-by-word dump, to keep the
        # hook's context footprint small. Claude can re-run the checker
        # directly for the full report if it decides to act on this.
        summary_lines = [
            line for line in output.splitlines()
            if line.startswith(("Words not on", "Sentences over", "Forbidden tenses", "Idioms", "Total issues"))
        ]
        print(f"[globish] {path.name} was just written and is not fully Globish-compliant:")
        for line in summary_lines:
            print(f"  {line.strip()}")
        print("  Run the checker for details: "
              f"python3 {checker} {path}")
    # "Draft is clean." case: say nothing, don't clutter the transcript.

    return 0


if __name__ == "__main__":
    sys.exit(main())
