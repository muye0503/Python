#!/usr/bin/env python

import os
import sys
import shutil


def remove_file(target_dir):
    for target_file in os.listdir(target_dir):
            target_file = os.path.join(target_dir, target_file)
            os.remove(target_file)


def find_file(target_dir):
    pass_dir = os.path.join(target_dir, 'log')
    fail_dir = os.path.join(target_dir, 'faillog')
    pass_bak_dir = os.path.join(target_dir, 'log_1st')
    fail_bak_dir = os.path.join(target_dir, 'faillog_1st')

    if len(os.listdir(pass_dir)) != 0:
        print "Processing ... %s" % pass_dir
        try:
            shutil.copytree(pass_dir, pass_bak_dir)
            remove_file(pass_dir)
        except Exception, e:
            print e
    if len(os.listdir(fail_dir)) != 0:
        print "Processing ... %s" % fail_dir
        try:
            shutil.copytree(fail_dir, fail_bak_dir)
            remove_file(fail_dir)
        except Exception, e:
            print e


if __name__ == '__main__':
    # Usage:
    # python case_statistics.py /l/haixiaoy/Automation/ANSI/R29SUG_20150311/VZWUC/R28SUG
    root_dir = sys.argv[1]
    List_root_dir = []
    for sub_dir in os.listdir(root_dir):
        List_root_dir.append(os.path.join(root_dir, sub_dir))
    map(find_file, List_root_dir)
