#!/usr/bin/env python
import sys
import os
import re

multiple_case = 0


def get_caselist():
    dict_case = {}
    global multiple_case
    patt = re.compile(r'(\w+).*')
    try:
        try:
            caselist_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            f_case_list = open(os.path.join(caselist_dir, 'All.caselist'), 'r')
            # lines = (line for line in f_case_list if not line.startswith('#')) # support from 2.4
            for line in f_case_list:
                line = line.strip()
                if line.startswith('#'):
                    continue
                elif re.match(patt, line) is not None:
                    case_num = re.match(patt, line).group(1)
                    case_title = re.match(patt, line).group()
                    if case_num in dict_case:
                        # print line
                        multiple_case += 1
                    elif case_num not in dict_case:
                        dict_case[case_num] = []
                    dict_case[case_num].append(case_title)
            return dict_case
        finally:
            f_case_list.close()
    except Exception, e:
        print e


def create_log(list_log_file):
    customer = sys.argv[1]
    log_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    try:
        f_fail_case = open(os.path.join(log_dir, 'Failed_Case.list'), 'a')
        for f in list_log_file:
            for case_title in dict_case[f]:
                if case_title.endswith(customer):
                    f_fail_case.writelines('%s%s' % (case_title, os.linesep))
                elif len(dict_case[f]) == 1:
                    print '=' * 10
                    print case_title
                    print 'Case: %s No case title found!' % f
                    print '=' * 10
    finally:
        f_fail_case.close()


def find_file(current_dir):
    list_file = []
    list_pass_file = []
    list_fail_file = []
    result_dir = os.path.join(current_dir, 'res')
    pass_dir = os.path.join(current_dir, 'log')
    fail_dir = os.path.join(current_dir, 'faillog')

    for root, dirs, files in os.walk(result_dir):
        for f in files:
            if f.split('.')[-1] == 'result':
                list_file.append(os.path.splitext(f)[0])

    for root, dirs, files in os.walk(pass_dir):
        for f in files:
            if f.split('.')[-1] == 'log':
                list_pass_file.append(os.path.splitext(f)[0])

    for root, dirs, files in os.walk(fail_dir):
        for f in files:
            if f.split('.')[-1] == 'log':
                list_fail_file.append(os.path.splitext(f)[0])

    list_total_file = [f for f in list_file if f in dict_case]
    total_num = len(list_total_file)
    pass_num = len(list_pass_file)
    fail_num = len(list_fail_file)
    skip_num = total_num - pass_num - fail_num
    list_log_file = [f for f in list_total_file if f not in list_pass_file]
    print current_dir.split('/')[-1]
    print 'Total: %s, Pass: %s, Fail: %s, Skip: %s' % (total_num, pass_num, fail_num, skip_num)
    create_log(list_log_file)

if __name__ == '__main__':
    # Usage:
    # python case_statistics.py VZWUC
    root_dir = os.path.join(sys.argv[1], os.listdir(sys.argv[1])[0])
    list_root_dir = []
    dict_case = get_caselist()
    print 'Total: %s' % (len(dict_case) + multiple_case)
    # for keys in dict_case:
    #    print 'keys= %s, val = %s' %(keys, dict_case[keys])
    for sub_dir in os.listdir(root_dir):
        list_root_dir.append(os.path.join(root_dir, sub_dir))
    map(find_file, list_root_dir)