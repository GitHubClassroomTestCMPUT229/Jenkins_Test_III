#!/bin/bash

# TODO: If these commands can be made to work (requires auth)
#       then we can use the push to notify students of their
#       test-case status.

# How to stop Travis building and entering into an endless loop.
# https://coderwall.com/p/f7fusq/how-to-skip-making-a-build-in-travis-ci
# Scripting in Bash for Git
# https://gist.github.com/mintindeed/4600385
# https://stackoverflow.com/questions/1335815/how-to-slice-an-array-in-bash
# https://stackoverflow.com/questions/7124486/what-to-do-with-commit-made-in-a-detached-head/7124513#7124513
# User: Charles Bailey

# UNAME & PWORD are set within Travis as environment variables
# UNAME & PWORD are used to authenticate with github in order to permit a push

git checkout master
git pull

URL=$(git config remote.origin.url)
AUTH_URL="https://$UNAME:$PWORD@${URL[@]:8}"
cp ./.travis/diagnostics/output ./output

git config user.name "Stuart Hoye (Travis CI response)"
git config push.default simple

git config -l

git add ./output
git commit -m "Responding with test case results. [ci skip]"
git branch tmp
git checkout master
git merge tmp
git branch -d tmp

git push $AUTH_URL


