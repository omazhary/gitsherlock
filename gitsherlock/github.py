"""
Checks the github API for projects within a certain set that do not use CI
tools.
"""

import argparse
import json
import requests
import time

from bs4 import BeautifulSoup
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class Scraper:
    """
    This class scrapes GitHub for information, depending on the specified
    query.
    """

    REQUEST_LIMIT = 2400

    def __init__(self, user, authFile=None, target="API"):
        if authFile is None:
            raise Exception("No authentication file provided!!")
        if target == "API":
            self.gh_request = "https://api.github.com/"
        elif target == "WEB":
            self.gh_request = "https://github.com/"
        self.parameters = dict()
        self.result = dict()
        self.user = user
        self.requests = 0
        self.target = target
        token = json.load(open(authFile))
        self.user = token['user']
        self.token = token['token']

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

        result = None
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
                    result = json.loads(content)
                else:
                    result = json.loads(
                            '{"message": "No result returned"}'
                            )
            else:
                result = gh_json_result.content
        elif self.target == "WEB":
            gh_uri = "%s" % (gh_query)
            gh_result = requests.get(gh_uri)
            soup = BeautifulSoup(gh_result.text.encode("utf8"),
                                 'html.parser')
            result = soup
        self.requests += 1
        time.sleep(1)
        return result
