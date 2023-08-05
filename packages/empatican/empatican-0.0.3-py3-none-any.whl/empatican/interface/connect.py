#!/usr/bin/env python
# Simple E4 Downloader
from getpass import getpass
import json
import os
import pandas as pd
import re
import requests
import sys
import zipfile

BASE_URL = 'https://www.empatica.com/connect/'
AUTH_URL = BASE_URL + 'authenticate.php'
DOWNLOAD_URL = BASE_URL + 'download.php'
SESSIONS_URL = BASE_URL + 'connect.php/users/{}/sessions'

if 'EMPATICA_USER' in os.environ.keys():
    USERNAME = os.environ['EMPATICA_USER']
    PASSWORD = os.environ['EMPATICA_PASS']
else:
    USERNAME = input('Empatica Username: ')
    PASSWORD = getpass('Empatica Password: ')


def search_or_download(options):
    '''Simple wrapper to open and use a request session

    Parameters
    -----------
        options : dict
            Dictionary with options from :class:`empatican.cli` list or
            download parser (e.g. participant_id, device_id,
            device_assignment). See the :ref:`commandline-reference` for more
            information.
    '''
    if options['participant_id'] and not options['device_assignment']:
        msg = ('Error: A --device-assignment csv table is required if '
               'specifying --participant-id')
        raise ValueError(msg)

    with requests.Session() as req_session:
        _search_or_download(req_session, options)


def _search_or_download(req_session, options):
    '''Main handler for searching and downloading E4 sessions'''
    # Logs in to the E4 connect site and updates req_session in place
    login(req_session)

    # Get a list of all sessions by querying the econnect site (or cache)
    session_list = get_sessions(req_session, json_cache=None, **options)
    session_df = pd.DataFrame(session_list)

    if options['device_assignment']:
        # If device assignment was provided, add a participant_id column inline
        merge_device_assignment(session_df, options['device_assignment'])

    filtered_df = filter_sessions(session_df, options)

    if options['action'] == 'list':
        if options['table_fmt'] == 'tab':
            table_string = filtered_df.to_string() + '\n'
        elif options['table_fmt'] == 'csv':
            table_string = filtered_df.to_csv()
        else:
            raise ValueError('Format must be either "tab" or "csv"')

        sys.stdout.write(table_string)

    elif options['action'] == 'download':
        for _, row in filtered_df.iterrows():
            try:
                if options['template']:
                    local_filename = build_fname(row, options)
                else:  # Use default within download_session
                    local_filename = None

                download_fname = download_session(
                    row, req_session, local_filename=local_filename)
                sys.stdout.write(
                    'Successfully downloaded "%s"\n' % download_fname)
            except Exception as e:
                sys.stdout.write(
                    'Problem downloading "%s": %s\n' % (row['id'], e))


def filter_sessions(session_df, options):
    # Create a set of filters to restrict sessions
    query = []
    if options['device_id']:
        device_id = options['device_id']
        query.append("device_id == @device_id")
    if options['empatica_id']:
        empatica_id = options['empatica_id']
        query.append("id == @empatica_id")
    if options['participant_id']:
        participant_id = options['participant_id']
        query.append("participant_id == @participant_id")
    if options['start_date']:
        start_date = options['start_date']
        query.append("start_datetime >= @start_date")
    if options['end_date']:
        end_date = options['end_date']
        query.append("start_datetime <= @end_date")

    if options['n_recent']:
        n_recent = options['n_recent']
    else:
        n_recent = session_df.shape[0]  # (don't tail any)

    # Take the filters and apply them once
    if len(query):
        session_df.query(' & '.join(query), inplace=True)

    # Filter n recent sessions in place
    session_df = session_df.iloc[-n_recent:]
    return session_df


def merge_device_assignment(session_df, device_assignment_sheet):
    """Add participant_id from device assignment table

    Expects a sheet with columns *participant_id*, *start_date*, *end_date* and
    *device_serial*

    Dates must be fully-valid dates (e.g. including year), Day-Month aren't
    sufficient."""
    csv_df = pd.read_csv(
        device_assignment_sheet, parse_dates=['start_date', 'end_date'])

    # Initialize 'participant_id' column
    session_df.loc[:, 'participant_id'] = None

    # Add participant_id in session from matching assignment rows.
    for row_idx, row in session_df.iterrows():
        search = ((csv_df['device_serial'] == row['device_name']) &
                  (csv_df['start_date'] <= row['start_datetime'])
                  & (csv_df['end_date'] >= row['start_datetime']))
        device_assignment_rows = csv_df.loc[search]
        if device_assignment_rows.shape[0] > 0:
            cur_participant_id = '_or_'.join(
                device_assignment_rows['participant_id'].astype(str).values)
            session_df.loc[row_idx, 'participant_id'] = cur_participant_id
        else:
            continue


def build_fname(row, options):
    '''Build an output file from a format.'''
    # TODO Add sanity check format, handle errors
    if not options['template'].endswith('.zip'):
        options['template'] += '.zip'

    try:
        fname = options['template'].format(**row)
    except KeyError as e:
        print(e)
        raise FormatError(
            "Problem with your template string. "
            "Be sure to use only the following special values: {}".format(
                row.keys()))
    return fname


def login(req_session, login_info=None):
    if not login_info:
        login_info = dict(username=USERNAME, password=PASSWORD)

    # Login with the session
    response = req_session.post(AUTH_URL, data=login_info)
    if 'dashboard' not in response.url:
        msg = "Couldn't log in {}. Check username/pass and try again.".format(
            login_info['username'])
        raise ValueError(msg)


def get_userid(req_session):
    recent_sessions = req_session.get(BASE_URL + 'sessions.php')
    match = re.search('var userId = (\d+)', recent_sessions.text)
    userid = match.groups()[0]
    return userid


def get_sessions(req_session, json_cache='sessions_list.json', **options):
    '''Download or load from cache a list of session dictionaries.
    To avoid any caching, use json_cache=None'''
    # Determine the userid if not provided explicitly
    # (one fewer REST call if pre-determined)
    if 'userid' not in options.keys() or not options['userid']:
        userid = get_userid(req_session)
        options['userid'] = userid
        # print('Found user as {}'.format(userid))

    # Build the sessions list url and grab the full list of sessions
    sessions_list_url = SESSIONS_URL.format(options['userid'])

    if json_cache:
        if os.path.exists(json_cache):
            with open(json_cache, 'r') as f:
                sessions_list = json.load(f)
        else:
            sessions_list_response = req_session.get(sessions_list_url)
            sessions_list = sessions_list_response.json()
            with open(json_cache, 'w') as f:
                indent = None
                json.dump(sessions_list, f, indent=indent)

    else:
        sessions_list_response = req_session.get(sessions_list_url)
        sessions_list = sessions_list_response.json()

    session_df = pd.DataFrame(sessions_list)

    session_df['start_datetime'] = pd.to_datetime(
        session_df['start_time'], unit='s')
    session_df['_duration'] = session_df['duration'].astype(int).apply(
        _pretty_relative_time)

    # Empatica stores hex device names as ints in their site. For all E4
    # devices, convert the "label" into a 5-padded hex string plus "A" prefix
    session_df['device_name'] = session_df['label'].dropna().astype(int).apply(
        "A{0:05x}".format).str.upper()

    session_df.drop(
        columns=['status', 'exit_code'], inplace=True, errors='ignore')

    return session_df


def download_session(physio_session, requests_session, local_filename=None):
    """Download a single session from Empatica Connect

    Parameters
    -----------
    physio_session : Dictlike, pandas row is acceptable
        Session details with metadata keys from empatica connect site. **id**
        is the only required key, but other information may be provided as
        well to automatically create a `empatica connect`-style zip filename,
        e.g. keys 'start_time' and 'device_id'.

    requests_session : :class:requests.Session
        An open and logged-in ``Session``

    local_filename : str, optional
        An optional filename may be provided. If dirname does not exist, it
        will be created recursively. Leave as ``None`` to infer a standard
        filename from ``options`` as ``{start_time}_{device_id}.zip``.

    Returns
    --------

    local_filename : str, default None
        The filename of the zipfile created, regardless of whether the filename
        was inferred or passed in explicitly.

    """
    if not local_filename:
        local_filename = '{start_time}_{device_id}.zip'.format(
            **physio_session)

    # Recursively create output directory if needed
    local_dirname = os.path.abspath(os.path.dirname(local_filename))
    if not os.path.exists(local_dirname):
        os.makedirs(local_dirname)

    params = dict(id=physio_session['id'])

    if not os.path.exists(local_filename):
        with requests_session.get(
                DOWNLOAD_URL, params=params, stream=True) as stream:
            with open(local_filename, 'wb') as f:
                for chunk in stream.iter_content(chunk_size=512):
                    # if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
            write_metadata(physio_session, local_filename)
    return local_filename


def write_metadata(physio_session, local_filename):
    """Append metadata from download to zip"""
    if isinstance(physio_session, pd.Series):
        meta = physio_session.to_dict()
    else:
        meta = physio_session
    with zipfile.ZipFile(local_filename, 'a') as z:
        z.writestr(
            'metadata.json',
            json.dumps(meta, indent=4, sort_keys=True, default=str),
        )


def download(req_session, **options):
    payload = dict(username=USERNAME, password=PASSWORD)

    # Login with the session
    req_session.post(AUTH_URL, data=payload)

    sessions_list = get_sessions(req_session, options)

    if 'n_recent' in options.keys():
        n_recent = sessions_list.shape[0]

    for _, physio_info in sessions_list.tail(n_recent).iterrows():
        download_session(physio_info, req_session)


def _pretty_relative_time(time_diff_secs):
    '''Originally from: https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    Each tuple in the sequence gives the name of a unit, and the number of
    previous units which go into it.
    '''
    weeks_per_month = 365.242 / 12 / 7
    intervals = [('minute', 60), ('hour', 60), ('day', 24), ('week', 7),
                 ('month', weeks_per_month), ('year', 12)]

    unit, number = 'second', abs(time_diff_secs)
    for new_unit, ratio in intervals:
        new_number = float(number) / ratio
        # If the new number is too small, don't go to the next unit.
        if new_number < 2:
            break
        unit, number = new_unit, new_number
    shown_num = int(number)
    return '{} {}'.format(shown_num, unit + ('' if shown_num == 1 else 's'))


class FormatError(Exception):
    pass
