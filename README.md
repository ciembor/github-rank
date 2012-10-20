github-rank
===========
This script generates ranks of top users and repositories located in specified regions.

## Dependencies
* Python 2,
* [PyGithub](http://github.com/jacquev6/PyGithub).

## Usage
1. Set locations in `config.py`.
2. Generate authorization key (more info here: http://developer.github.com/v3/oauth) and set `oauth` variable in `auth.py`. 
3. Run `python2 main.py`.
4. Open `output` directory, generated files are formated as GitHub Flavored Markdown with embeded HTML.
