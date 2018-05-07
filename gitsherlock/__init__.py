"""
Checks the github API for projects within a certain set that do not use CI
tools.
"""

import argparse
from bs4 import BeautifulSoup
import json
import requests
import sys
import time
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class GitSherlock:
    """
    This class scrapes GitHub for information, depending on the specified
    query.
    """

    REQUEST_LIMIT = 2400

    def __init__(self, user, token=None, tokenfile=None, target="API"):
        if token is None and tokenfile is None:
            raise Exception("No token or token file provided!!")
        if target == "API":
            self.gh_request = "https://api.github.com/"
        elif target == "WEB":
            self.gh_request = "https://github.com/"
        self.parameters = dict()
        self.result = dict()
        self.token = token
        self.user = user
        self.requests = 0
        self.tokencounter = 0
        self.target = target
        if tokenfile is not None:
            with open(tokenfile) as f:
                self.tokenlist = f.readlines()
                self.tokenlist = [x.strip() for x in self.tokenlist]
                self.token = self.tokenlist[self.tokencounter]
        else:
            self.tokenlist = []
            self.tokenlist.append(self.token)

    def query(self, endpoint, parameters=dict(), method="GET",
              data_type="std"):
        """
        Queries the desired endpoint using the given parameters.
        :param endpoint: The GitHub endpoint to be queried.
        :param parameters: A dictionary containing the endpoint's parameters.
        :param data_type: The type of data queried by the user
            (diff, patch, std)
        :return: The result in the requested format.
        """

        # Check if we need to cycle tokens:
        if self.requests == self.REQUEST_LIMIT:
            self.tokencounter = (self.tokencounter + 1) % len(self.tokenlist)
            self.token = self.tokenlist[self.tokencounter]
            print("## Cycling to token #%d..." % self.tokencounter)
            self.requests = 0
        # Perform the request:
        gh_query = self.gh_request + endpoint
        header_type = ''
        if data_type.lower() == "diff":
            header_type = 'application/vnd.github.diff'
        elif data_type.lower() == "patch":
            header_type = 'application/vnd.github.patch'
        else:
            header_type = 'application/vnd.github+json'
        if self.target == "API":
            gh_uri = "%s?%s" % (gh_query, urlencode(parameters))
            gh_json_result = requests.request(
                    method, gh_uri, auth=(self.user, self.token),
                    headers={'Accept': header_type}
                    )
            if data_type.lower() == 'std':
                content = gh_json_result.content.decode('utf-8')
                if content is not None and not content == '':
                    self.result = json.loads(content)
                else:
                    self.result = json.loads(
                            '{"message": "No result returned"}'
                            )
            else:
                self.result = gh_json_result.content
        elif self.target == "WEB":
            gh_uri = "%s" % (gh_query)
            gh_result = requests.get(gh_uri)
            soup = BeautifulSoup(gh_result.text.encode("utf8"),
                                 'html.parser')
            self.result = soup
        self.requests += 1
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser(
            description="Query GitHub's online endpoints."
            )
    parser.add_argument('--user', metavar='u', type=str, required=True,
                        help='Your GitHub username.')
    parser.add_argument('--token', metavar='t', type=str, required=True,
                        help='Your GitHub authentication token.')
    parser.add_argument('--endpoint', metavar='e', type=str,
                        help='The GitHub endpoint you want to query.')
    parser.add_argument('--method', metavar='m', type=str,
                        help='The HTTP method to use.')
    parser.add_argument('--output', metavar='o', type=str,
                        help='The output data format.')
    parser.add_argument('--target', metavar='r', type=str,
                        help='The request\'s target [API|WEB].')
    parser.add_argument('--params', metavar='p', type=str,
                        help='The request\'s parameters in json.')

    args = vars(parser.parse_args())
    endpoint = ""
    method = ""
    output = ""
    target = "API"
    parameters = dict()

    if args['endpoint'] is None:
        endpoint = ""
    else:
        endpoint = args['endpoint']
    if args['method'] is None:
        method = "GET"
    else:
        method = args['method']
    if args['output'] is None:
        output = "JSON"
    else:
        output = args['output']
    if args['target'] is not None:
        target = args['target']
    if args['params'] is not None:
        try:
            parameters = json.loads(args['params'])
        except ValueError:
            print('You have not provided a valid json string!!')
            sys.exit(1)

    scraper = GitSherlock(args['user'], args['token'], target=target)
    scraper.query(endpoint, parameters=parameters, method=method)

    if target == "WEB":
        print(scraper.result)

    if output == "JSON" and target == "API":
        print(json.dumps(scraper.result))
