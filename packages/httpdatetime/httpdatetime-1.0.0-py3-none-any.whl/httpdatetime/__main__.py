#!/usr/bin/env python3
# encoding:utf-8


from pathlib import Path

from httpdatetime.getdatetime import HttpDateTime


def main():
    if not Path('/tmp/datetime_updated.txt').is_file():
        HttpDateTime.set_os_datetime()


if __name__ == '__main__':
    main()
