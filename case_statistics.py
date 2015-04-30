#!/usr/bin/env python
import sys,os
import re

def get_caselist():
    Dict_case = {}

    patt = re.compile(r'(\w+).*')
    try:
        try:
            caselist_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            f_case_list = open(os.path.join(caselist_dir, 'All.caselist'), 'r')
            for str in f_case_list.readlines():
                if re.match(patt,str) is not None:
                    case_num = re.match(patt,str).group(1)
                    case_title = re.match(patt,str).group()
                    Dict_case.setdefault(case_num,case_title)
            return Dict_case
        finally:
            f_case_list.close()
    except Exception,e:
        print e

def create_log(List_fail_file):
    log_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    try:
        f_fail_case = open(os.path.join(log_dir, 'Failed_Case.list'), 'a')
        for f in List_fail_file:
            case_title = Dict_case[os.path.splitext(f)[0]]
            f_fail_case.writelines('%s%s' % (case_title,os.linesep))
    finally:
        f_fail_case.close()

def find_file(root_dir):
    List_file = []
    List_pass_file = []
    List_fail_file = []
    result_dir = os.path.join(root_dir, 'res')
    pass_dir = os.path.join(root_dir, 'log')
    fail_dir = os.path.join(root_dir, 'faillog')

    for root, dirs, files in os.walk(result_dir):
        for f in files:
            if f.split('.')[-1] == 'result':
                List_file.append(f)

    for root, dirs, files in os.walk(pass_dir):
        for f in files:
            if f.split('.')[-1] == 'log':
                List_pass_file.append(f)

    for root, dirs, files in os.walk(fail_dir):
        for f in files:
            if f.split('.')[-1] == 'log':
                List_fail_file.append(f)

    create_log(List_fail_file)
    total_num = len(List_file)
    pass_num = len(List_pass_file)
    fail_num = len(List_fail_file)
    skip_num = total_num - pass_num - fail_num
    print root_dir.split('/')[-1]
    print 'Total: %s, Pass: %s, Fail: %s, Skip: %s' % (total_num, pass_num, fail_num, skip_num)

if __name__ == '__main__':
    # Usage:
    # python case_statistics.py /l/haixiaoy/Automation/ANSI/R29SUG_20150311/VZWUC/R28SUG
    root_dir = sys.argv[1]
    List_root_dir = []
    Dict_case = get_caselist()
    for sub_dir in os.listdir(root_dir):
        List_root_dir.append(os.path.join(root_dir,sub_dir))
    map(find_file, List_root_dir)