#!/bin/bash
(sh .github/bin/lint_common/git_get-diff-file-name_unstaged.sh) | grep -E '\.py$' | tr '\n' ' '
