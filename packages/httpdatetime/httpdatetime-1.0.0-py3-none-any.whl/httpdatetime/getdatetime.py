#!/usr/bin/env python3
# encoding:utf-8


import http.client
import subprocess
import sys
from pathlib import Path
from subprocess import CalledProcessError


class HttpDateTime:

    @staticmethod
    def get_datetime():
        try:
            conn = http.client.HTTPSConnection('www.google.com', timeout=10)
            conn.request('GET', '/')
            res = conn.getresponse()
            return res.getheader('date')
        except:
            print('Error: Could not get the date and time from the internet.', file=sys.stderr)
            return None

    @classmethod
    def set_os_datetime(cls):
        datetime = cls.get_datetime()
        if datetime is None:
            return None
        try:
            subprocess.run(['date', '-s', datetime], check=True, stdout=subprocess.DEVNULL)
            print('Date and time have been updated successfully')
            Path('/tmp/datetime_updated.txt').touch()
        except CalledProcessError:
            pass
