#!/usr/bin/env python

# Usage:
# Only support ATCA, and support data file: .sql, .data, .frm, .frmbk
# copy this script on your ATCA and execute as:
# ./Replace_hostname.py [options] data_file
# data_file can be a file or directory
# By default, the hostname(SPVMxxx) in the data file will be replaced with your hostname
# you can also specify the original hostname with --ori, and the destination
# hostname with --des .
# e.g. $ python Replace_hostname.py --ori=SPVM11A --des=BJRMS1A data_file
# with --help for the detailed usage.
# Apr19,2015
# Report bug to Haixiao.Yan@alcatel-lucent.com

import os
import sys
import glob
import re
import fileinput
import optparse


def get_hostname():

    sys_tpye = os.name

    if sys_tpye == 'nt':
        hostname = os.getenv('computername')
        return hostname
    elif sys_tpye == 'posix':
        try:
            hostname = os.getenv('HOSTNAME').split('-')[0]
        except AttributeError:
            print 'Hostname not exists or is not supported!'
        else:
            return hostname
    else:
        return 'unknow hostname'


def process_sql_file(input_sql_file, old=None, new=None):
    print 'Process ... %s' % os.path.abspath(input_sql_file)
    head = """psql -h pglocalhost -U scncraft <<!eof
BEGIN;
"""
    tail = """END;
!eof
"""
    patt_head = re.compile(r'^psql')
    patt_body = re.compile(r'^(BEGIN|END)')
    patt_tail = re.compile(r'^!eof')

    if old is None:
        patt_sub = re.compile(r'SPVM_?\d*[A-Z]+')
    else:
        patt_sub = re.compile(r'%s' % old)
    if new is None:
        repl = get_hostname()
    else:
        repl = new
    for line in fileinput.input(input_sql_file, inplace=True):
        if re.search(patt_head, line):
            sys.stdout.write(head)
        elif re.search(patt_body, line):
            continue
        elif re.search(patt_tail, line):
            sys.stdout.write(tail)
        elif re.search(patt_sub, line):
            sys.stdout.write(re.sub(patt_sub, repl, line))
        else:
            sys.stdout.write(line)


def process_data_file(input_data_file, old=None, new=None):
    print 'Process ... %s' % os.path.abspath(input_data_file)
    if old is None:
        patt_sub = re.compile(r'SPVM_?\d*[A-Z]+')
    else:
        patt_sub = re.compile(r'%s' % old)
    if new is None:
        repl = get_hostname()
    else:
        repl = new

    for line in fileinput.input(input_data_file, inplace=True):
        if re.search(patt_sub, line):
            sys.stdout.write(re.sub(patt_sub, repl, line))
        else:
            sys.stdout.write(line)


if __name__ == '__main__':

    usage = "usage: %prog [options] data_file"
    parser = optparse.OptionParser(usage)
    parser.add_option('--ori',
                      action="store",
                      dest="ori",
                      help="The original hostname",
                      )
    parser.add_option('--des',
                      action="store",
                      dest="des",
                      help="The new hostname",
                      )
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("No data file to process")
    else:
        data_file = args[0]
        if os.path.isdir(data_file):
            data_dir = os.path.abspath(data_file)
            os.chdir(data_dir)
            sql_file_list = glob.glob('./*.sql')
            data_file_list = glob.glob('./*.data')
            frm_file_list = glob.glob('./*.frm*')

            if len(sql_file_list) > 0:
                for item in sql_file_list:
                    process_sql_file(item, options.ori, options.des)
            if len(data_file_list) > 0:
                for item in data_file_list:
                    process_data_file(item, options.ori, options.des)
            if len(frm_file_list) > 0:
                for item in frm_file_list:
                    process_data_file(item, options.ori, options.des)
        elif os.path.isfile(data_file):
            if os.path.splitext(data_file)[-1] == ".sql":
                process_sql_file(data_file, options.ori, options.des)
            elif os.path.splitext(data_file)[-1] in [".data", ".frm", ".frmbk"]:
                process_data_file(data_file, options.ori, options.des)
