#!/bin/bash

DIR=$(pwd -P)

# Clone into a working repo
git clone ${DIR}/bare working
cd working

# Create a .gitignore
echo "*.pyc" > .gitignore

# Commit and push
git add .gitignore
git commit -m "Initial commit with .gitignore"
git push origin master
