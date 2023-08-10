import git

repo = git.Repo(".")
repo.git.add(".")
repo.git.commit(m = "Add demofile for playing with gitpython")
repo.git.push()
