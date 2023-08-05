#!/usr/bin/env python
import argparse
import dateutil.parser
from empatican.interface import connect
import sys


def add_parser():
    help = 'Search and Download E4 Sessions from Empatica Connect'
    parser = argparse.ArgumentParser(description=help)
    add_arguments(parser)
    return parser


def add_arguments(parser):
    subparsers = parser.add_subparsers(dest='action')
    list_parser = subparsers.add_parser('list')
    download_parser = subparsers.add_parser('download')
    add_query_args(list_parser)
    add_query_args(download_parser)

    list_parser.add_argument(
        '--table-fmt',
        default='tab',
        choices=['tab', 'csv'],
        help=('Display table as tab-separated (nice on screen) '
              'or csv (useful for saving output)'))

    download_parser.add_argument(
        '--template', '-t', help='Output template to use when saving zipfiles')


def add_query_args(parser):
    # parser.add_argument('action', choices=['download', 'list'])
    parser.add_argument(
        '--device-assignment', help='Participant->Device sheet as csv')

    description = 'Arguments used to filter or query specific sessions'
    group = parser.add_argument_group(title='query arguments', description=description)
    group.add_argument(
        '--device-id', '-d', nargs='*', help='Restrict to Device ID', type=str)
    group.add_argument(
        '--empatica-id',
        nargs='*',
        help='Space-separated list of Empatica Connect website session IDs')
    group.add_argument(
        '--participant-id',
        nargs='+',
        help='Space-separated list of Participant IDs to restict',
    )
    group.add_argument(
        '--n-recent', metavar='N', type=int, help='Number of recent sessions')
    group.add_argument(
        '--start-date',
        type=dateutil.parser.parse,
        metavar='YYYY-MM-DD',
        help='Date of earliest session')
    group.add_argument(
        '--end-date',
        type=dateutil.parser.parse,
        metavar='YYYY-MM-DD',
        help='Date of latest session')

    # parser.add_argument(
    #     '--userid', type=str, help='Optional Empatica user id (for performance)')


def main():
    parser = add_parser()
    args = parser.parse_args(sys.argv[1:])
    connect.search_or_download(vars(args))
