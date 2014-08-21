#!/usr/bin/env python

import os,sys
import re

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
            repl = 'SPVM118A'
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
    except:

        pass
   

def Find_file(root_dir):

    List_sql = []
    for root,dirs,files in os.walk(root_dir):

        for f in files:
            if f.split('.')[-1] == 'sql':
                List_sql.append(os.path.join(root,f))
    
    return List_sql


if __name__ == '__main__':
    
    cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    input_path = os.path.join(cur_dir,'src_sql')
    output_path = os.path.join(cur_dir,'des_sql')

    List_sql = Find_file(input_path)
    for file in List_sql:
        src_sql = file
        des_sql = os.path.join(output_path,os.path.basename(file))

        Process_sql(src_sql,des_sql)
