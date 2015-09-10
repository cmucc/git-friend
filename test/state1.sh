#!/bin/bash

# Remove any previous test repos here
rm -rf bare working

# Create a bare repo and give git-friend AFS permissions
git init --bare bare
cd bare
find . -type d -exec fs sa {} git-friend write \;

# Echo the location of the repo to the user, so they can give it to git-friend
echo -en "\033[0;31m"
pwd -P
echo -en "\033[0m"
