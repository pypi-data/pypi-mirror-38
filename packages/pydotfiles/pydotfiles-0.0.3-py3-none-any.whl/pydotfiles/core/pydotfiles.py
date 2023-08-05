import os.path
from pydotfiles.utils import PrettyPrint, symlink_file, unsymlink_file, is_linked
import sys
import argparse


class Symlink:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def __str__(self):
        return f"{self.origin} -> {self.destination}"

    def link(self):
        symlink_file(self.origin, self.destination)

    def unlink(self):
        unsymlink_file(self.origin, self.destination)

    def is_linked(self):
        return is_linked(self.origin, self.destination)


class Dotfiles:
    """
    Logical class to represent the dotfiles
    as a singular unit
    """
    def __init__(self, dotfiles_directory='~/.dotfiles'):
        self.dotfiles_directory = dotfiles_directory
        self.git_remote_link_file = os.path.expanduser(f"{dotfiles_directory}/.dotfile_link")
        self.xcode_accepted_file = os.path.expanduser(f"{dotfiles_directory}/.xcode_accepted")
        self.symlinks_directory = os.path.expanduser(f"{dotfiles_directory}/symlinks")
        self.git_remote_link = self.get_git_remote_link()
        self.symlinks = self.get_symlinks()

    def download(self):
        # TODO P0: Implement
        pass

    def install(self):
        # Installs all symlinks
        for symlink in self.symlinks:
            if not symlink.is_linked():
                symlink.link()

    def uninstall(self):
        # Uninstalls all symlinks
        for symlink in self.symlinks:
            if symlink.is_linked():
                symlink.unlink()

    def update(self):
        # TODO P0: Implement
        pass

    def upgrade(self):
        # TODO P0: Implement
        pass

    def clean(self):
        # TODO P0: Implement
        pass

    def get_git_remote_link(self):
        with open(self.git_remote_link_file, 'r') as git_remote_link_file:
            return git_remote_link_file.read()

    def get_symlinks(self):
        return [Symlink(f"{self.symlinks_directory}/{symlink}", os.path.expanduser(f"~/.{symlink.replace('.symlink', '')}")) for symlink in os.listdir(self.symlinks_directory)]


class Dispatcher:
    """
    # TODO P0: Add in nested argsparse helper menus for all the options
    """
    def __init__(self):
        self.dotfiles = Dotfiles()

    def dispatch(self):
        parser = argparse.ArgumentParser(description="Python Dotfiles Manager")
        parser.add_argument("command", help="Runs the command given", choices=['download', 'install', 'uninstall', 'update', 'upgrade', 'clean'])
        args = parser.parse_args()

        # Dynamically dispatches to the relevant method
        getattr(self, args.command)()

    def download(self):
        self.dotfiles.download()

    def install(self):
        self.dotfiles.install()

    def uninstall(self):
        self.dotfiles.uninstall()

    def update(self):
        self.dotfiles.update()

    def upgrade(self):
        self.dotfiles.upgrade()

    def clean(self):
        self.dotfiles.clean()

def main():
    dispatcher = Dispatcher()
    dispatcher.dispatch()


if __name__ == '__main__':
    main()

"""
nano: set constantshow
"""


"""
dotfiles install <-- Installs everything in one go
dotfiles update <-- git update and package manager update, then uninstall & re-install
dotfiles upgrade <-- runs the upgrade() command
dotfiles clean <-- cleans out the cache directory
dotfiles uninstall <-- uninstalls all the symlinks that it's managing


Here's the flow:


-------------------- from setup onwards ---------
1.) we run a command in our command line to install the dotfiles
2.) the command will grab the installation script from github and run it
    a.) the script will accept the xcode license if it exists
    b.) the script will install pyenv
    c.) the script will install pyenv python 3.6.3 (or latest, as long as its python 3.6+)
    d.) the script will install pyenv virtualenv laptop-3.6.3 (or latest)
    e.) the script will set the global pyenv to be laptop-3.6.3
    f.) the script will download the dotfiles to ~/.dotfiles
    g.) the script will run `pip install pydotfiles`
    h.) the script will run `dotfiles install`

3.) The installation will provide the binary `dotfiles` when in
    the laptop-3.6.3 virtualenv
---------------- end of setup


------------- to update ----------
`dotfiles update` will:
1.) git update the ~/.dotfiles directory
2.) run the update() command, which abstracts away
    updating the package manager


--------------- end of update


------------------ to upgrade --------------------
`dotfiles upgrade` will:
1.) run the package manager upgrade command, and install
    new packages that have been added to the .ini that
    weren't installed before

---------------------- end of upgrade

"""





"""
Setup functions
"""

def setup_git():
    # TODO P0: Implement
    pass

def setup_editors():
    # TODO P0: Implement
    pass



def setup_ssh():
    # TODO P0: Implement
    pass
