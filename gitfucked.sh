#!/bin/bash

git config --global alias.fucked 'git reset $(git commit-tree HEAD^{tree} -m "fucked")'

