#!/usr/bin/env python3
# encoding:utf-8


import os
import sys
from time import sleep

from httpdatetime.getdatetime import HttpDateTime


def main():
    if os.geteuid() == 0:
        while not HttpDateTime.set_os_datetime():
            sleep(30)
    else:
        print('Error: You need to run this program with root privileges.', file=sys.stderr)
    sys.exit()


if __name__ == '__main__':
    main()
