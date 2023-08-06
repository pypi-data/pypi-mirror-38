from tagscraper.scrape import scrape
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument(
    '--url',
    '-u',
    help='URL to start from',
    type=str,
    required=True
)
parser.add_argument(
    '--selector',
    '-s',
    help='CSS selecctor',
    type=str,
    required=True
)
parser.add_argument(
    '--limit',
    '-limit',
    help='The amount of tags to stop at',
    type=int
)
args = parser.parse_args()


def run():
    print(json.dumps(
        scrape(
            [args.url],
            args.selector,
            args.limit
        ),
        indent=4,
        sort_keys=True,
        default=str
    ))
