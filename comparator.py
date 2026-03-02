"""
Uses Python's standard library difflib.
Returns both:
- full diff text
- number of changed lines
"""

from __future__ import annotations

import difflib   #similar to git diff
from dataclasses import dataclass


@dataclass(frozen=True)  #frozen
class DiffResult:
    diff_text: str
    changed_lines: int


def build_unified_diff(
    original_text: str,
    enhanced_text: str,
    from_name: str = "original",
    to_name: str = "enhanced",
    context_lines: int = 3,
) -> DiffResult:
    """
    Building a unified diff of the og and the enhanced 
    Returns:
      DiffResult.diff_text: the final diff as a single string
      DiffResult.changed_lines: count of lines in diff that indicate changes
    """
    original_lines = original_text.splitlines(keepends=True)
    enhanced_lines = enhanced_text.splitlines(keepends=True)

    diff_iter = difflib.unified_diff(
        original_lines,
        enhanced_lines,
        fromfile=from_name,
        tofile=to_name,
        n=context_lines,
    )
    diff_text = "".join(diff_iter)

    # Count only actual line changes not headers
    changed_lines = 0
    for line in diff_text.splitlines():
        if line.startswith(("---", "+++", "@@")):
            continue
        if line.startswith(("+", "-")):
            changed_lines += 1

    return DiffResult(diff_text=diff_text, changed_lines=changed_lines)