# __main__.py

# This file acts as an entry point to the package.

import argparse
import github
import json

parser = argparse.ArgumentParser(
		description="Query GitHub and BitBucket's online endpoints."
		)
requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('--provider', metavar='v', type=str, required=True,
					help='The repository provider [GITHUB|BITBUCKET].')
requiredArgs.add_argument('--user', metavar='u', type=str, required=True,
					help='Your username.')
requiredArgs.add_argument('--token', metavar='t', type=str, required=True,
					help='Your authentication token.')
requiredArgs.add_argument('--endpoint', metavar='e', type=str, required=True,
					help='The endpoint you want to query.')
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

scraper = github.Scraper(args['user'], args['token'], target=target)
scraper.query(endpoint, parameters=parameters, method=method)

if target == "WEB":
	print(scraper.result)

if output == "JSON" and target == "API":
	print(json.dumps(scraper.result))