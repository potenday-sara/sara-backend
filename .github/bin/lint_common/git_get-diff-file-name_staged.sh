#!/bin/bash
BASE_BRANCH=$1

echo "$(git diff ${BASE_BRANCH} --name-only --diff-filter=d)"
