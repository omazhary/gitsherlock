# Project Status:
| Branch | Master | Production |
| ------ | :----: | :--------: |
| CI Build Status | [![CircleCI](https://circleci.com/gh/omazhary/gitsherlock/tree/master.svg?style=svg)](https://circleci.com/gh/omazhary/gitsherlock/tree/master) | [![CircleCI](https://circleci.com/gh/omazhary/gitsherlock/tree/production.svg?style=svg)](https://circleci.com/gh/omazhary/gitsherlock/tree/production) |

# What is GitSherlock?

GitSherlock is a way I came up with a while back to make my life easier when scraping data off the GitHub API.
What GitSherlock does is essentially the following:
1. You give GitSherlock an endpoint you want to query (along with a selection of parameters)
2. GitSherlock sends a request to the GitHub API on your behalf, and retrieves the data returned by the GitHub API.
3. GitSherlock then formats the data in the format you've requested, and then returns that to you.

## Requirements
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

# Usage

You can use GitSherlock in two main ways:
1. The terminal/command line (depending on which OS you use)
    1. As part of a shell script
    2. As a standalone executable
2. As a python module in one of your python scripts
