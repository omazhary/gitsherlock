#!/usr/bin/env python

"""
Checks the github API for projects within a certain set that do not use CI
tools.
"""

import requests
import argparse
import json
import time
from urllib import urlencode


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

    def query(self, endpoint, parameters=dict(), method="GET", data_type="std"):
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
        gh_uri = "%s?%s" % (gh_query, urlencode(parameters))
        header_type = ''
        if data_type.lower() == "diff":
            header_type = 'application/vnd.github.diff'
        elif data_type.lower() == "patch":
            header_type = 'application/vnd.github.patch'
        else:
            header_type = 'application/vnd.github+json'
        gh_json_result = requests.request(
                method, gh_uri, auth=(self.user, self.token),
                headers={'Accept': header_type}
                )
        if self.target == "WEB":
            self.result = gh_json_result.status_code
        else:
            if data_type.lower() == 'std':
                self.result = json.loads(gh_json_result.content)
            else:
                self.result = gh_json_result.content
        self.requests += 1
        time.sleep(1)

if __name__ == "__main__":
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

    scraper = GitSherlock(args['user'], args['token'], target=target)
    scraper.query(endpoint, method=method)

    if target == "WEB":
        print(scraper.result)

    if output == "JSON" and target == "API":
        print(json.dumps(scraper.result))
