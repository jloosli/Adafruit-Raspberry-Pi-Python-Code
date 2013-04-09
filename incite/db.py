#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Database setup
"""

import sys
import os
import traceback
import argparse
import time
import re
import sqlite3
#from pexpect import run, spawn


class Db:

    def __init__(self, dbpath):
        ''' use path relative to this file '''
        theDir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(theDir, dbpath)
        self.conn = sqlite3.connect(dbpath)
        self.c = self.conn.cursor

    
    def getDatasets(self):
        self.c.execute("SELECT Distinct dataset from samples")
        result = self.c.fetchall()
        return result



def main():

    global args
    db = Db('data/samples.db')

    print(db.getDatasets())

if __name__ == '__main__':
    try:
        start_time = time.time()
        # Parser: See http://docs.python.org/dev/library/argparse.html
        parser = argparse.ArgumentParser(description='Database connections')
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_argument('-ver', '--version', action='version', version='1.0')
        args = parser.parse_args()
        if args.verbose:
            print(time.asctime())
        main()
        if args.verbose:
            print(time.asctime())
        if args.verbose:
            print("Total time in minutes: ", end="")
        if args.verbose:
            print((time.time() - start_time) / 60.0)
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
