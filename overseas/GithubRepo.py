import git
from covid_19_au_grab.overseas.GlobalBase import \
    GlobalBase


class GithubRepo(GlobalBase):
    def __init__(self, output_dir, github_url):
        GlobalBase.__init__(self, output_dir)
        self.github_url = github_url

    def update(self):
        g = git.cmd.Git(self.output_dir)
        g.pull()
