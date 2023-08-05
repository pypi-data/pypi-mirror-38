from django.core.management.base import BaseCommand  # , CommandError
from Atheneum import models
from Atheneum.physio import e4
from ._patharg import PathType
from . import _empatica_connect
import os
import requests
import tempfile


class Command(BaseCommand):
    help = 'Import an E4 zip'

    def add_arguments(self, parser):
        parser.add_argument(
            '--e4-zipfile',
            nargs='*',
            type=PathType(exists=True, type=None),
            default=[])
        parser.add_argument(
            '--empatica-id', nargs='*', help='Empatica IDs to import')
        parser.add_argument(
            '--userid', type=str, help='Empatica user id (if known)')

    def handle(self, *args, **options):
        e4_zipfiles = options['e4_zipfile']

        with tempfile.TemporaryDirectory() as tmp_dir:
            if options['empatica_id']:
                with requests.Session() as req_session:
                    _empatica_connect.login(req_session)
                    sessions_list = _empatica_connect.get_sessions(
                        req_session, json_cache=None, **options)
                    sessions = sessions_list.loc[sessions_list['id'].isin(
                        options['empatica_id'])]
                    for _, session_info in sessions.iterrows():
                        fname = os.path.join(
                            tmp_dir, '{}.zip'.format(session_info['id']))
                        _empatica_connect.download_session(
                            session_info, req_session, local_filename=fname)
                        e4_zipfiles.append(fname)

            for zipfilename in e4_zipfiles:
                session = models.Physio_Session.objects.create()
                session_reader = e4.Session(zipfilename)
                session.e4_import(session_reader)
                session.save()

                self.stdout.write(
                    self.style.SUCCESS('Successfully imported "%s"' %
                                       os.path.basename(zipfilename)))
