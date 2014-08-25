#!/usr/bin/env python

# Usage: ./replace_sql.py
# Put your data will be processed in the src directory, excute this script, and result data 
# will generated in des directory.
#
# Aug,22,2014
#

import os,sys
import re

def GetHostname():
    sys = os.name
    
    if sys == 'nt':
        hostname = os.getenv('computername')
        return hostname
        print hostname
    elif sys == 'posix':
        hostname = os.getenv('HOSTNAME').split('-')[0]
        return hostname
    else:
        return 'unknow hostname'
        
def Process_sql(src_sql,des_sql):

    head = """psql -h pglocalhost -U scncraft <<!eof
BEGIN;
"""
    tail = """END;
!eof
"""
    
    try:
        f_src_sql = open(src_sql,'r')
        f_des_sql = open(des_sql,'w')
        
        try:        
            patt_head = re.compile(r'psql')
            patt_body = re.compile(r'BEGIN|END')
            patt_tail = re.compile(r'^!eof')
            patt_sub = re.compile(r'SPVM\d{2,3}[A-Z]?')
            repl = GetHostname()         
            
            for line in f_src_sql:
                if re.search(patt_head,line):
                    f_des_sql.write(head)
                elif re.search(patt_body,line):
                    continue
                elif re.search(patt_tail,line):
                    f_des_sql.write(tail)
                elif re.search(patt_sub,line):
                    f_des_sql.write(re.sub(patt_sub,repl,line))
                else:
                    f_des_sql.write(line)
        finally:
            f_src_sql.close()
            f_des_sql.close()
    except IOError:
        print 'file open failed!'
   
def Process_data(src_data,des_data):
    try:
        try:
            f_src_data = open(src_data,'r')
            f_des_data = open(des_data,'w')
            
            patt_sub = re.compile(r'SPVM\d{2,3}[A-Z]?')
            repl = GetHostname()
            
            for line in f_src_data:
                if re.search(patt_sub,line):
                    f_des_data.write(re.sub(patt_sub,repl,line))
                else:
                    f_des_data.write(line)               
        finally:
            f_src_data.close()
            f_des_data.close()     
    except IOError:
        print 'file open failed!'
        
def Find_file(root_dir):

    List_file = []
    for root,dirs,files in os.walk(root_dir):
        for f in files:
            List_file.append(os.path.join(root,f))  
    return List_file

def RemoveFile(path):
    if len(os.listdir(path)) != 0:
        for file in os.listdir(path):
            targetfile = os.path.join(path,file)
            os.remove(targetfile)

if __name__ == '__main__': 

    cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    input_path = os.path.join(cur_dir,'src')
    output_path = os.path.join(cur_dir,'des')
    
    RemoveFile(output_path)

    List_file = Find_file(input_path)
    for file in List_file:
        src_file = file
        des_file = os.path.join(output_path,os.path.basename(file))
        
        print 'Process... %s' %file
        if os.path.basename(file).split('.')[-1] == 'sql': 
            Process_sql(src_file,des_file)
        elif os.path.basename(file).split('.')[-1] == 'data':
            Process_data(src_file,des_file)
