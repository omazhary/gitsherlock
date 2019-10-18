# __main__.py

# This file acts as an entry point to the package.

import argparse
import bitbucket
import github
import json

from sys import exit

parser = argparse.ArgumentParser(
		description="Query GitHub and BitBucket's online endpoints."
		)
requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('--provider', metavar='v', type=str, required=True,
					help='The repository provider [GITHUB|BITBUCKET].')
requiredArgs.add_argument('--endpoint', metavar='e', type=str, required=True,
					help='The endpoint you want to query.')
parser.add_argument('--user', metavar='u', type=str,
					help='Your username.')
parser.add_argument('--token', metavar='t', type=str,
					help='Your authentication token.')
parser.add_argument('--authfile', metavar='f', type=str,
					help='The file where you store your credentials.')
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
		exit('You have not provided a valid json string!!')

scraper = None
if args['provider'] == 'BITBUCKET':
	scraper = bitbucket.Scraper(args['authfile'])
elif args['provider'] == 'GITHUB':
	scraper = github.Scraper(args['user'], args['authfile'], target=target)

result =  scraper.query(endpoint, parameters=parameters, method=method)

if target == "WEB":
	print(result)

if output == "JSON" and target == "API":
	print(json.dumps(result))
