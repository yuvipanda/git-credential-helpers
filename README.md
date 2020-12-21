# git-credential-helpers

Collection of [git-credential](https://git-scm.com/docs/gitcredentials) helpers,
focused on interacting with private repos.

## Installation

`git-credential-helpers` is available on PyPI, and can be installed with `pip`.

```bash
python3 -m pip install git-credential-helpers
```

A number of scripts with names of form `git-credential-$NAME` will now be in
`$PATH`.

## Configuration

You must configure git to use the helpers appropriately by adding an entry
in [gitconfig](https://git-scm.com/docs/git-config). 

### github-app helper

In your `gitconfig` file, add the following section:

```ini
[credential "https://github.com"]
  helper = !git-credential-github-app --app-key-file <path-to-your-app-rsa-key-file> --app-id <id-of-your-github-app>
  useHttpPath = true
```

If you are doing this in a docker container, I'd recommend putting this under `/etc/gitconfig`.
Else, try `~/.gitconfig`
