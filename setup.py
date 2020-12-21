from setuptools import find_packages, setup

setup(
    name='git-credential-helpers',
    version='0.1',
    url='https://github.com/yuvipanda/git-credential-helpers',
    license='3-clause BSD',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    description='Collection of git-credential helpers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    platforms='any',
    install_requires=['github3.py'],
    entry_points={
        'console_scripts': [
            'git-credential-github-app = git_credential_helpers.github_app:main'
        ],
    }
)
