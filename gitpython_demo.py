import git

repo = git.Repo(".")
repo.remotes.origin.set_url("ssh://git@github.com:alchemistbg/forvo-web-scraping.git")
repo.git.add(".")
repo.git.commit(m = "Add demofile for playing with gitpython")
repo.git.push()
