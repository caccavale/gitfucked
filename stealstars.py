import sys
from github import Github

if len(sys.argv) is not 4:
    exit()

g = Github(sys.argv[1], sys.argv[2])
me = g.get_user()
my_stars = me.get_starred()

other = g.get_user(sys.argv[3])
their_stars = other.get_starred()
for repo in their_stars:
    if repo not in my_stars:
        me.add_to_starred(repo)
