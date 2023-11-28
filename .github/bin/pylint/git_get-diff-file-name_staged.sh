#!/bin/bash
BASE_BRANCH=$1

(sh .github/bin/lint_common/git_get-diff-file-name_staged.sh ${BASE_BRANCH}) | grep -E '\.py$' | tr '\n' ' '
