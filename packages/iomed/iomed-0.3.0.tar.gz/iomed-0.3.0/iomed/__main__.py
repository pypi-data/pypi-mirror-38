#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys

import crayons

from .mel import MEL
from .logs import logger

MSG_NO_KEY = """Error: missing api key.
You can either set the environment variable IOMED_MEL_KEY or pass the key with --key.
Please visit https://console.iomed.es to obtain your api key."""

MSG_CLI_DESCRIPTION = """
Command line interface to IOMED Medical Language API (MEL).

- Visit https://console.iomed.es to obtain your api key.
- Visit https://docs.iomed.es to learn more about MEL.
"""


def main():

    parser = argparse.ArgumentParser(
        description=MSG_CLI_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )

    # parser.add_argument('-i', '--input',
    #                     dest = "infile",
    #                     action = "store",
    #                     default = None,
    #                     help = "Input ENCODE formatted file")

    parser.add_argument('-t', '--test',
                        dest="test",
                        action="store_true",
                        default=False,
                        help="Use the testing platform instead of production.")

    parser.add_argument('-p', '--pretty-print',
                        dest="pretty_print",
                        action="store_true",
                        default=False,
                        help="Instead of full json, print nice output.")

    parser.add_argument('-u', '--url',
                        dest="url",
                        action="store",
                        default=None,
                        help="API url (by default https://api.iomed.es).")

    parser.add_argument('-k', '--key',
                        dest="key",
                        action="store",
                        default=None,
                        help="API key (get it at https://console.iomed.es).")

    parser.add_argument('text')

    # if no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()

    options = parser.parse_args()

    if options.test and options.url:
        logger.error(
            'Only one of --test and --url can be specified at a time.')
        exit(1)

    if not options.key:
        try:
            apikey = os.environ['IOMED_MEL_KEY']
        except KeyError:
            logger.error(MSG_NO_KEY)
            exit(1)
    else:
        apikey = options.key

    url = options.url
    if url and not url.endswith('annotation'):
        url = '{}/annotation'.format(url)
    if url and not url.startswith('http'):
        url = 'http://{}'.format(url)
    mel = MEL(apikey, test=options.test, url=url)
    result = mel.parse(options.text, as_json=True)

    if not options.pretty_print:
        print(result)

    else:
        parsed = json.loads(result)
        if not parsed['annotations']:
            print(crayons.white('No concepts found.', bold=True))
            exit(0)

        print(crayons.white('Concepts:', bold=True))
        for concept in parsed['annotations']:
            neg = 'negative' in concept['characteristics']
            type_ = concept['type'].get('iomed', concept['type'].get('umls'))
            color = crayons.cyan if not neg else crayons.red
            string = '"'
            string += color(concept['match']['text'], bold=True)
            string += '"'
            string += crayons.green(' <')
            string += crayons.green(type_, bold=True)
            string += ':'
            string += crayons.magenta(concept['code']['umls'], bold=True)
            string += ':'
            string += crayons.yellow(
                '"' + concept['match']['preferred_term'] + '"'
            )
            string += crayons.green('>')
            print(string)

        print()
        if not parsed['relations']:
            print(crayons.white('No relations found.', bold=True))
            exit(0)
        print(crayons.white('Relations:', bold=True))
        id_to_conc = {c['id']: c for c in parsed['annotations']}
        for relation in parsed['relations']:
            src = id_to_conc[relation['from']]['match']['text']
            target = id_to_conc[relation['to']]['match']['text']
            rel = relation['rel']
            string = crayons.yellow('(' + src + ') ', bold=True)
            string += crayons.magenta('-[{}]->'.format(rel), bold=True)
            string += crayons.yellow(' (' + target + ')', bold=True)
            print(string)

    exit(0)


if __name__ == '__main__':
    main()
