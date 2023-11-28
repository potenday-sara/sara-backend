#!/bin/bash
(sh ../bin/lint_common/git_get-diff-file-name_unstaged.sh) | grep -E '\.py$' | tr '\n' ' '
