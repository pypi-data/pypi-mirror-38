from __future__ import print_function

import argparse
import json
import sys

import jref.version
import jref.reference

from jref.context import CLIContext, LocalContext, RemoteContext


def parse_args():
    cli = argparse.ArgumentParser()
    cli.set_defaults(context_class=CLIContext)

    cli.add_argument(
        '--version', action='version',
        version='%(prog)s v{}'.format(jref.version.version))

    cli.add_argument(
        '--max-recursion', type=int, help='''Maximum recursion depth for
        resolving references (default: {})'''
        .format(jref.reference.MAXIMUM_REFERENCE_RECURSION_DEPTH))
    cli.add_argument(
        '--local-root', default='', help='''Root path for references to the
        local filesystem. Note: remote resources are not allowed to reference
        local paths.''')

    uri_handling = cli.add_mutually_exclusive_group()
    uri_handling.add_argument(
        '--local-only', dest='context_class', action='store_const',
        const=LocalContext, help='''Accept only references to files in the local
        filesystem''')
    uri_handling.add_argument(
        '--remote-only', dest='context_class', action='store_const',
        const=RemoteContext, help='''Accept only references using remote
        URIs''')

    cli.add_argument('reference', nargs='*', help='A JSON Reference to evaluate')

    return cli.parse_args()


def print_reference(ref):
    print(json.dumps(
        ref.expand(), indent=2, separators=(',', ': '), sort_keys=True))


def main():
    config = parse_args()

    if config.max_recursion:
        jref.reference.MAXIMUM_REFERENCE_RECURSION_DEPTH = \
            config.max_recursion

    ctx_args = {}
    if config.local_root:
        ctx_args['root'] = config.local_root
    ctx = config.context_class(**ctx_args)

    for user_ref in config.reference:
        ref = ctx.parse_reference(user_ref)
        print_reference(ref)


if __name__ == '__main__':
    # Don't show __main__.py as executable in usage string
    sys.argv[0] = 'jref'

    main()
