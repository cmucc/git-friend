# git-friend

A "helpful" IRC bot to walk you through the basics of git.

Created for git workshops by the Carnegie Mellon University Computer Club.

## How to launch

To run `git-friend` on club servers:

```bash
# Ensure a data directory exists
mkdir -p data

# Ensure git-friend has access to all of its directories
find . -type d -exec fs sa {} git-friend write \;

# Become git-friend and authenticate to the cell.
# (You will need the password to the git-friend principal.)
kinit git-friend
aklog club.cc.cmu.edu

# Enter the data directory
cd data

# Run the client
python ../git_friend.py
```

Some time after the workshop, terminate `git-friend` with `Ctrl-c`.
