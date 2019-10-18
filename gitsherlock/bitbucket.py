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

    def __init__(self, authFile, target="API"):
        if authFile is None:
            raise Exception("No authentication file provided!!")
        if target == "API":
            self.bbRequest = "https://api.bitbucket.org/2.0/"
        elif target == "WEB":
            self.bbRequest = "https://bitbucket.org/"
        self.parameters = dict()
        self.target = target
        token = json.load(open(authFile))
        self.user = token['user']
        self.token = token['token']


    def query(self, endpoint, parameters=dict(), method="GET"):
        """
        Queries the desired endpoint using the given parameters.
        :param endpoint: The BitBucket endpoint to be queried.
        :param parameters: A dictionary containing the endpoint's parameters.
        :param data_type: The type of data queried by the user
            (diff, patch, std)
        :return: The result in the requested format.
        """

        result = None
        # Perform the request:
        bbQuery = self.bbRequest + endpoint
        header_type = ''
        if self.target == "API":
            bbUri = "%s?%s" % (bbQuery, urlencode(parameters))
            bbJsonResult = requests.request(
                    method, bbUri, auth=(self.user, self.token),
                    headers={'Accept': header_type}
                    )
            content = bbJsonResult.content.decode('utf-8')
            if content is not None and not content == '':
                result = json.loads(content)
            else:
                result = json.loads('{"message": "No result returned"}')
        elif self.target == "WEB":
            bbUri = "%s" % (bbQuery)
            bbResult = requests.get(bbUri)
            soup = BeautifulSoup(bbResult.text.encode("utf8"), 'html.parser')
            result = soup
        time.sleep(1)
        return result
