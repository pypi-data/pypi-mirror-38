from django.core.management.base import BaseCommand  # , CommandError
import pandas as pd
import requests
from . import _empatica_connect


class Command(BaseCommand):
    help = 'Download E4 Sessions from Empatica Connect'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['download', 'list'])
        parser.add_argument(
            '--device-id',
            '-d',
            nargs='*',
            help='Restrict to Device ID',
            type=str)
        parser.add_argument(
            '--empatica-id', nargs='*', help='Restrict to Empatica IDs')
        parser.add_argument(
            '--label', '-l', nargs='*', help='Session Label', type=str)
        parser.add_argument(
            '--n-recent', type=int, help='Number of recent sessions')
        parser.add_argument(
            '--userid', type=str, help='Empatica user id (if known)')

    def handle(self, *args, **options):
        with requests.Session() as req_session:
            _empatica_connect.login(req_session)

            session_list = _empatica_connect.get_sessions(
                req_session, json_cache=None, **options)
            session_df = pd.DataFrame(session_list)

            if options['label']:
                session_df = session_df.loc[session_df['label'].isin(
                    options['label'])]
            if options['device_id']:
                session_df = session_df.loc[session_df['device_id'].isin(
                    options['device_id'])]
            if options['n_recent']:
                n_recent = options['n_recent']
            else:
                n_recent = session_df.shape[0]  # (don't tail any)
            if options['empatica_id']:
                session_df = session_df.loc[session_df['id'].isin(
                    options['empatica_id'])]

            if options['action'] == 'list':
                self.stdout.write(session_df.tail(n_recent).to_string())
            elif options['action'] == 'download':
                for _, row in session_df.tail(n_recent).iterrows():
                    try:
                        download_fname = _empatica_connect.download_session(
                            row, req_session)
                        self.stdout.write(
                            self.style.SUCCESS('Successfully downloaded "%s"' %
                                               download_fname))
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR('Problem downloading "%s": %s' %
                                             (row['id'], e)))
