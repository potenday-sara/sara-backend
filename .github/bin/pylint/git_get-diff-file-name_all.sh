#!/bin/bash
DIR_PATH=`dirname $0`
BASE_BRANCH=$1

(sh ./${DIR_PATH}/git_get-diff-file-name_staged.sh ${BASE_BRANCH} & sh ./${DIR_PATH}/git_get-diff-file-name_unstaged.sh) | tr '\n' ' '
