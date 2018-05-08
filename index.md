# What is GitSherlock?

GitSherlock is a way I came up with a while back to make my life easier when scraping data off the GitHub API.
What GitSherlock does is essentially the following:
1. You give GitSherlock an endpoint you want to query (along with a selection of parameters)
2. GitSherlock sends a request to the GitHub API on your behalf, and retrieves the data returned by the GitHub API.
3. GitSherlock then formats the data in the format you've requested, and then returns that to you.

## Required External Libraries

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

# How do I use it?

You can use GitSherlock in two main ways:
- The terminal/command line (depending on which OS you use)
  - As part of a shell script
  - As a standalone executable
- As a python module in one of your python scripts

Examples for both use cases are given below.

## Usage Examples

### Terminal/Command Line or Executable

```bash
gitsherlock --user <your_github_username> --token <your github_token> --endpoint <api_or_html_endpoint>
```

### Python Script

```python
from gitsherlock import GitSherlock

scraper = GitSherlock(user=GITHUB_USER, token=GITHUB_TOKEN)
scraper.query(endpoint)
print(scraper.result)
```
