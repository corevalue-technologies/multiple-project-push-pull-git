import os
from github import Github

organization: abc/123
user: abc
password: ''

g = Github(user, password)


for repo in g.get_user().get_repos():
    print(repo.name)

