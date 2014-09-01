#!/usr/bin/env python

import xml.etree.ElementTree as ET
import string
import re
import os,sys
import cx_Oracle
import traceback
import copy

# Process the xml file
def Process_xml(file_name): 

    tree = ET.parse(file_name)

    # SLL_NAME and eSM Table name mapping
    Dict1={}

    # SLL_NAME and the eSM column mapping 
    Dict3={}

    # SLL_NAME and the SLL data item mapping 
    Dict5={}

    # SLL_NAME and the eSM data item mapping 
    Dict7={}
    
    List_dict=[]

    # Processing the normal table
    for table in tree.iter('TABLE'):
    
    # Skipping the RTDB table processing
        m=re.search('RTDB',table.get('NAME'))
        if m is not None:
            continue 

        #print '%d %s' %(i,table.get('SLL_NAME'))
        Dict1.setdefault(table.get('SLL_NAME'),table.get('NAME'))

        # The data item list for each table
        List_tb=[]
        List_tb_sll=[]
        List_tb_esm=[]  
        for data in table.iter('DATA_ITEM'):

            mash=data.get('AGGRTYPE')
            if mash is not None:

                mash_data=data.get('AGGRINFO')

                # The list for AGGRTYPE data 
                List_mash_data=mash_data.split(',')
                List_mash_data.insert(0,data.get('NAME'))
                List_tb.append(List_mash_data)
                List_tb_sll.append(data.get('SLL_NAME'))    
                List_tb_esm.append(data.get('NAME'))
    
            else:
                List_tb.append(data.get('NAME'))    
                List_tb_sll.append(data.get('SLL_NAME'))    
                List_tb_esm.append(data.get('NAME'))

        #print List_tb
        #print List_tb_sll
        Dict3.setdefault(table.get('SLL_NAME'),List_tb)
        Dict5.setdefault(table.get('SLL_NAME'),List_tb_sll)
        Dict7.setdefault(table.get('SLL_NAME'),List_tb_esm)

    # Processing the global table 
    flag_1 = 'Server' 
    for table in tree.iter('NON_TABLE'):
        
        m=re.search('global_static|global_rc',table.get('NAME'))
        if m is not None and flag_1 == 'Server' :
            Dict1.setdefault('global_server',table.get('NAME'))
            flag_1 = 'Client' 
            
            List_tb=[]
            List_tb_sll=[]
            for data in table.iter('DATA_ITEM'):
                List_tb.append(data.get('NAME'))
                List_tb_sll.append(data.get('SLL_NAME'))
            Dict3.setdefault('global_server',List_tb)
            Dict5.setdefault('global_server',List_tb_sll)
            Dict7.setdefault('global_server',List_tb)
        elif m is not None and flag_1 == 'Client': 
            Dict1.setdefault('global_client',table.get('NAME'))

            List_tb=[]
            List_tb_sll=[]
            for data in table.iter('DATA_ITEM'):
                List_tb.append(data.get('NAME'))
                List_tb_sll.append(data.get('SLL_NAME'))
            Dict3.setdefault('global_client',List_tb)
            Dict5.setdefault('global_client',List_tb_sll)
            Dict7.setdefault('global_client',List_tb)
            

    List_dict.append(Dict1) 
    List_dict.append(Dict3) 
    List_dict.append(Dict7)
    List_dict.append(Dict5) 


    #j=1
    #for key in sorted(Dict1):
    #   print '%d key=%s, value=%s' %(j,key,Dict1[key])
    #   j+=1

    #j=1
    #for key in sorted(Dict3):
    #   print '%d key=%s, value=%s' %(j,key,Dict3[key])
    #   j+=1

    #j=1
    #for key in sorted(Dict7):
    #   print '%d key=%s, value=%s' %(j,key,Dict7[key])
    #   j+=1
    #j=1
    #for key in sorted(Dict5):
    #   print '%d key=%s, value=%s' %(j,key,Dict5[key])
    #   j+=1

    return List_dict    

#print '==================================================='

# SLL_Name and SPA table mapping
def Process_sym(file_name):
    
    # SPA table name and eSM table name mapping
    Dict2={}

    # SPA table name and eSM column mapping
    Dict4={}    

    # SPA table name and SPA column mapping
    Dict6={}    

    List_item_esm=[]    
    List_item_spa=[]
    spa_tb=''

    List_dict=[]


    f_sym = open(file_name,'r')
    for line in f_sym:
        line = line.strip()

        if line.startswith('//'):
            continue
        elif line.startswith('SPA'):
            aList=re.split(';|\s',line)
            spa_tb=aList[0]
            # filter the normal table
            if re.search('tbl',aList[-1]) is not None:
                Dict2.setdefault(aList[0],aList[-1])
            elif re.search('server global;rc$',line) is not None:
                Dict2.setdefault(aList[0],'global_server')
            elif re.search('client global;rc$',line) is not None:
                Dict2.setdefault(aList[0],'global_client')
        elif len(line):
            if re.search('\[\]',line) is not None:
                col_esm=re.search('].(.+)',line.split(';')[1]).group(1)
                col_spa=line.split(';')[-2]
            else:
                #print line
                col_esm=line.split(';')[1]
                col_spa=line.split(';')[-2]
            List_item_esm.append(col_esm)
            List_item_spa.append(col_spa)
        elif not len(line) and spa_tb != '':
            Dict4.setdefault(spa_tb,List_item_esm)
            Dict6.setdefault(spa_tb,List_item_spa)
            List_item_esm=[]
            List_item_spa=[]
            spa_tb=''


    f_sym.close()
    
    List_dict.append(Dict2)
    List_dict.append(Dict4)
    List_dict.append(Dict6)

    #k=1
    #for key in sorted(Dict2):
    #   print '%d key=%s, value=%s' %(k,key,Dict2[key])
    #   k+=1
    #k=1
    #for key in sorted(Dict4):
    #   print '%d key=%s, value=%s' %(k,key,Dict4[key])
    #   k+=1
    #k=1
    #for key in sorted(Dict6):
    #   print '%d key=%s, value=%s' %(k,key,Dict6[key])
    #   k+=1

    return List_dict 

#print '==================================================='

def Conn_DB(tb_eSM,service):

    
    conn = cx_Oracle.connect("sms", "nsms123", "NSMS")
    cur = conn.cursor()

    #tb_eSM = 'Subscriber_Num_Val_N'

    # Get table name in Oracle database 
    #sql_eSM_tb_name = "select dbtblname from svcdatatype where svcname='SUREPAY' and sdtname like '"+tb_eSM+"%'"
    sql_eSM_tb_name = "select dbtblname from svcdatatype where svcname='"+service+"' and sdtname like '"+tb_eSM+"'"

    cur.execute(sql_eSM_tb_name)
    rows = cur.fetchone() 
    for row in rows: 
        #eSM_tb_name_cut = re.match('[A-Za-z0-9]+_(\w+)',row).group(1) 
        tb_eSM_Oracle=row
        #print eSM_tb_name_cut 
        #print tb_eSM_Oracle
        
        #if tb_eSM != 'global_static':
        if re.search('global_static|global_rc',tb_eSM) is None:
            # Get the svcname and sotname of the table
            #sql_svc_sot_eSM = "select svcname,sotname from sottosdtsetmap where sdtsetname='"+eSM_tb_name_cut+"'"
            sql_svc_sot_eSM = "select svcname,sotname from sottosdtsetmap where svcname='"+service+"' and sdtsetname='"+tb_eSM+"'"
            #print sql_svc_sot_eSM
    
            cur.execute(sql_svc_sot_eSM)
            rows = cur.fetchone() 
            #print rows
            svc_name=rows[0]
            sot_name=rows[1]
        elif service == 'SUREPAY' and tb_eSM == 'global_static':
            svc_name = 'SUREPAY'
            sot_name = 'Global SurePay'
        elif service == 'AUDIT' and tb_eSM == 'global_static':
            svc_name = 'AUDIT'
            sot_name = 'Global'
        elif service == 'DROUTER' and tb_eSM == 'global_rc':
            svc_name = 'DROUTER'
            sot_name = 'Global Parameters'
        elif service == 'EPPSM' and tb_eSM == 'global_rc':
            svc_name = 'EPPSM'
            sot_name = 'Global EPPSM'
    
        # Get the soid and sogid of the table
        sql_soid_sogid_eSM = "select soid,sogid from svcobj where svcname= '"+ svc_name + "' and sotname= '" + sot_name+ "'"        
        #print sql_soid_sogid_eSM 
        try:
            cur.execute(sql_soid_sogid_eSM)
            rows = cur.fetchone()
            soid=rows[0]
            sogid=rows[1]
        except TypeError,e:
            print 'No soid and sogid found!'
            
    cur.close()
    conn.commit()
    conn.close()

    List_eSM_DB=[tb_eSM_Oracle,soid,sogid]      
    return List_eSM_DB 

#print '==================================================='

def Check_soid():
    spa_dict = {
        'Global SurePay':'SUREPAY',
#       'MNP SurePay':'SUREPAY',
        'Provider':'SUREPAY',
#       'Scratch Card SurePay':'SUREPAY',
        'Subscriber_Access':'SUREPAY',
#       'User SurePay':'SUREPAY',
#       'Account SurePay':'SUREPAY',
        'Class of Service':'SUREPAY',
        'Diameter Network':'SUREPAY',
        'GPRSLDAP':'SUREPAY',
#       'Global RTDB':'SUREPAY',
        'Subscriber_Access':'AUDIT',
        'Global':'AUDIT',
        'GPRSLDAP':'AUDIT',
        'Audit':'AUDIT',
        'Class of Service':'NWTPPS',
        'Global PrePaid':'NWTPPS',
        'Billing':'NWTPPS',
        'Network':'NWTPPS',
        'Numbering Plan':'NWTPPS',
        'Provider':'NWTPPS',
        'Rating':'NWTPPS',
        'SCP Specific':'NWTPPS',
        'Scratch Card':'NWTPPS',
        'Network':'NWTCOM',
        'Numbering Plan':'NWTCOM',
#       'Public RTDB':'NWTCOM',
        'Screening':'NWTCOM',
        'Announcement':'NWTCOM',
        'NWTGSM':'NWTGSM',
#       'DROUTER Access':'DROUTER',
        'Global Parameters':'DROUTER',
        'Protocol And Network':'DROUTER',
#       'SERVER Access':'DROUTER',
        'Server Maintenance':'DROUTER',
        'Service Configuration':'DROUTER',
#       'Subscriber_Access':'DROUTER',
#       'ROUTSIM':'DUMMY',
#       'ROUTSIM IMSI':'DUMMY',
        'CDB SurePay':'EPPSM',
        'Global EPPSM':'EPPSM',
#       'Service Access':'EPPSM',
#       'User EPPSM':'EPPSM'
    }
    
    conn = cx_Oracle.connect("sms", "nsms123", "NSMS")
    cur = conn.cursor()

    for key in spa_dict:  
        sotname = key
        svcname = spa_dict[key]
        #print '[svcname=%s,sotname=%s]' %(svcname,sotname) 
        # Get the soid and sogid of the table
        sql_soid_sogid_eSM = "select soid,sogid from svcobj where svcname= '"+ svcname + "' and sotname= '" + sotname+ "'"      
        #print sql_soid_sogid_eSM 
        cur.execute(sql_soid_sogid_eSM)
        rows = cur.fetchone()
        soid=rows[0]
        sogid=rows[1]
        
        #print '[svcname=%s,sotname=%s]=[%s,%s]' %(svcname,sotname,soid,sogid)

    cur.close()
    conn.commit()
    conn.close()
    
def List_Col_Pro(List_str_2,List_Dict_spa_sll_col,List_Dict_sll_sll_col,List_Dict_sll_esm_col,List_Dict_sll_esm_col_mapping):
    
    # the SLL Name and eSM Name mapping in xml
    Dict_sll_esm_col_mapping = {}
    Dict_spa_item = {}
    Dict_esm_item = {}

    List_Dict_sll_esm_col_tmp = copy.deepcopy(List_Dict_sll_esm_col)
    List_Dict_sll_esm_col_mapping_tmp = copy.deepcopy(List_Dict_sll_esm_col_mapping)

    for i in range(len(List_Dict_sll_sll_col)):
        Dict_sll_esm_col_mapping.setdefault(List_Dict_sll_sll_col[i],List_Dict_sll_esm_col[i])
    for item in List_Dict_spa_sll_col:
        Dict_spa_item.setdefault(item,List_str_2.pop(0))
    for item in Dict_spa_item: 
        if item in Dict_sll_esm_col_mapping:
            Dict_esm_item.setdefault(Dict_sll_esm_col_mapping[item],Dict_spa_item[item])
    
    for item_2 in List_Dict_sll_esm_col_mapping_tmp:
        if isinstance(item_2,list):
            print item_2
            #print Dict_esm_item.get(item_2.pop(0))
            Index_val = Dict_esm_item.get(item_2.pop(0))
            print Index_val
            if Index_val.find(':') != -1:
                List_Index_val = Index_val.split(':')
                i=0
                for item in List_Index_val:
                    if i == 0:
                        List_Index_val[i] = item + "'"
                    elif i == len(List_Index_val)-1:
                        List_Index_val[i] = "'" + item
                    else:
                        List_Index_val[i] = "'" + item + "'"
                    i+=1

                if len(List_Index_val) == len(item_2):
                    for i in range(len(item_2)):
                        Dict_esm_item.setdefault(item_2[i],List_Index_val[i])   
                else:
                    print 'SPA data less than eSM data!' 
            elif len(item_2) == 1:
                Dict_esm_item.setdefault(item_2[0],Index_val)   
    
            else:
                print 'Invalid data!'   
                break
    index=0
    for item_3 in List_Dict_sll_esm_col_tmp:
        List_Dict_sll_esm_col_tmp[index]=Dict_esm_item[item_3] 
        index+=1
    if not len(List_str_2):
        List_str_2.extend(List_Dict_sll_esm_col_tmp)
    else:
        print 'Error_1'
    return List_str_2

            
#print '==================================================='
         
        
    
def Process_sql(spa_sql,esm_sql,Dict_sll_esm,Dict_sll_esm_col_mapping,Dict_sll_esm_col,Dict_sll_sll_col,Dict_spa_sll,Dict_spa_sll_col,service):

    Dict1=Dict_sll_esm
    Dict3=Dict_sll_esm_col
    Dict2=Dict_spa_sll
    Dict4=Dict_spa_sll_col  

    f_sql = open(spa_sql,'r')
    f_esm_sql = open(esm_sql,'w')

    
    #List_str_2_tmp = []

    for line in f_sql:
        line = line.strip() 
        if not len(line) or not re.search('SPA|spa\w+',line): 
            continue
        tb_SPA=re.search('SPA\w+|spa\w+',line).group()
        tb_SPA_ori=copy.deepcopy(tb_SPA)
        tb_SPA=tb_SPA.upper()

        str_4 = ''  
        str_5 = ''
        print tb_SPA    
        if tb_SPA in Dict2: 
            if Dict2[tb_SPA] in Dict1:
                List_DB=Conn_DB(Dict1[Dict2[tb_SPA]],service)
                if re.search('SPA\w+',line) is not None:
                    print '--->%s' %tb_SPA
                    str_1=line.replace(tb_SPA,List_DB[0])
                elif re.search('spa\w+',line) is not None:
                    print '--->%s' %tb_SPA_ori
                    str_1=line.replace(tb_SPA_ori,List_DB[0])
                    
                soid=str(List_DB[1])
                sogid=str(List_DB[2])
                print str_1 
                print List_DB

                match_1=re.search('\((.+)\)',str_1) 
                if match_1 is None:
                    #print str_1
                    f_esm_sql.write('%s%s' %(str_1,os.linesep))
                    continue    
                str_2=match_1.group(1).strip()
                print str_2 
                match_2=re.match('(.+)\(',str_1).group(1)
                #print match_2
                List_str_2 = str_2.split(',')
                if Dict2[tb_SPA] == 'global_server':
                    Dict_server={}
                    for item in Dict_spa_sll_col[tb_SPA]:
                        Dict_server.setdefault(item,List_str_2.pop(0))
                        
                    #for key in sorted(Dict_server):        
                    #   print "key=%s,value=%s" %(key,Dict_server[key])

                    index=0
                    for item in Dict_sll_sll_col['global_server']:
                        Dict_sll_sll_col['global_server'][index]=Dict_server[item]
                        index+=1
                elif Dict2[tb_SPA] == 'global_client':
                    Dict_client={}
                    for item in Dict_spa_sll_col[tb_SPA]:
                        Dict_client.setdefault(item,List_str_2.pop(0))

                    #for key in sorted(Dict_client):        
                    #   print "key=%s,value=%s" %(key,Dict_client[key])

                    index=0
                    for item in Dict_sll_sll_col['global_client']:
                        Dict_sll_sll_col['global_client'][index]=Dict_client[item]
                        index+=1
                    if not len(List_str_2):
                        List_str_2.extend(Dict_sll_sll_col['global_client'])
                        List_str_2.extend(Dict_sll_sll_col['global_server'])
                    
                        List_str_2.insert(0,soid)
                        List_str_2.insert(1,sogid)

                        str_3='('   
                        count=1
                        for val in List_str_2:
                            if count!=len(List_str_2):  
                                str_3=str_3+val+',' 
                                count+=1
                            else:
                                str_3=str_3+val

                        str_3=str_3+')'
                        str_4=match_2+str_3+';'
                    
                        #print str_4 
                        print '**********'  
                        print str_4 
                        print '**********'  
                        if len(str_4)>2499:
                            index=2400
                            while (str_4[:index].endswith(',') == False):
                                index+=1
                            f_esm_sql.write('%s%s'%(str_4[:index],os.linesep))  
                            f_esm_sql.write('%s%s'%(str_4[index:],os.linesep))  
                        
                        else:
                            f_esm_sql.write('%s%s'%(str_4,os.linesep))
                            str_4=''
                    else:
                        print 'Error_2'

                else:   

                    List_eSM_col=Dict_sll_esm_col[Dict_spa_sll[tb_SPA]]
                    List_eSM_col_mapping=Dict_sll_esm_col_mapping[Dict_spa_sll[tb_SPA]]
                    #print len(List_str_2),len(List_eSM_col_mapping)
                    #print Dict4[tb_SPA]
                    print List_str_2,List_eSM_col_mapping 
                    #print len(Dict_spa_sll_col[tb_SPA]),len(Dict_sll_sll_col[Dict_spa_sll[tb_SPA]])
                    #print Dict_spa_sll_col[tb_SPA],Dict_sll_sll_col[Dict_spa_sll[tb_SPA]]
                
                    #for item in List_str_2:
                    #   print item  
                
                    if len(List_str_2) == len(List_eSM_col):    
                        Dict_spa_item = {}
                        for item in Dict_spa_sll_col[tb_SPA]:
                            Dict_spa_item.setdefault(item,List_str_2.pop(0))
                        #for key in Dict_spa_item:
                        #   print 'key=%s,value=%s' %(key,Dict_spa_item[key])

                        List_sll_sll_col = copy.deepcopy(Dict_sll_sll_col[Dict_spa_sll[tb_SPA]])    

                        #print '---------------------------' 
                        #print List_sll_sll_col
                        #print Dict_sll_sll_col[Dict_spa_sll[tb_SPA]] 
                        #print '---------------------------' 
                        index=0
                        for item in List_sll_sll_col: 
                            List_sll_sll_col[index]=Dict_spa_item[item]
                            index+=1
                        if not len(List_str_2):
                            List_str_2.extend(List_sll_sll_col) 
                            List_str_2.insert(0,soid)
                            List_str_2.insert(1,sogid)
                            str_3='('   
                            count=1
                            for val in List_str_2:
                                if count!=len(List_str_2):  
                                    str_3=str_3+val+',' 
                                    count+=1
                                else:
                                    str_3=str_3+val

                            str_3=str_3+')'
                            str_4=match_2+str_3+';'
                        else:
                            print 'Error_3'
                    else:
                        List_str_4=List_Col_Pro(List_str_2,Dict_spa_sll_col[tb_SPA],Dict_sll_sll_col[Dict_spa_sll[tb_SPA]],Dict_sll_esm_col[Dict_spa_sll[tb_SPA]],Dict_sll_esm_col_mapping[Dict_spa_sll[tb_SPA]])
                        List_str_4.insert(0,soid)
                        List_str_4.insert(1,sogid)

                        str_3='('   
                        count=1
                        for val in List_str_4:
                            if count!=len(List_str_4):  
                                str_3=str_3+val+',' 
                                count+=1
                            else:
                                str_3=str_3+val

                        str_3=str_3+')'
                        str_4=match_2+str_3+';'
                
                


                    print '**********'  
                    print str_4 
                    print '**********'  
                    if len(str_4)>2499:
                        index=2400
                        while (str_4[:index].endswith(',') == False):
                            index+=1
                        #print index    
                        f_esm_sql.write('%s%s'%(str_4[:index],os.linesep))  
                        f_esm_sql.write('%s%s'%(str_4[index:],os.linesep))  
                        
                    else:
                        f_esm_sql.write('%s%s'%(str_4,os.linesep))
                        str_4=''


    f_esm_sql.close()
    f_sql.close()


menu = """

        menu

----------------------------------------------
    1: AUDIT
    2: DROUTER
    3: EPPSM
    4: NWTCOM
    5: NWTGSM
    6: NWTPPS
    7: SUREPAY
    c: SOID Check
    h: Help
    m: Print menu
    q: Quit

-----------------------------------------------
    
"""

menu_dict={
    '1':'AUDIT',
    '2':'DROUTER',  
    '3':'EPPSM',
    '4':'NWTCOM',   
    '5':'NWTGSM',   
    '6':'NWTPPS',   
    '7':'SUREPAY',  
    }

def commands(args):
    cmd = menu_dict.get(args)
    return cmd

def Find_file(root_dir):
    List_dirs = os.walk(root_dir)
    List_conf = ['sym_path','xml_path','sql_path']  
    for root,dirs,files in List_dirs:
        for f in files:
            if f.split('.')[-1] == 'sym':
                List_conf[0]=os.path.join(root,f)
            elif f.split('.')[-1] == 'xml':
                List_conf[1]=os.path.join(root,f)
            elif f.split('.')[-1] == 'sql':
                List_conf[-1]=os.path.join(root,f)

    return List_conf

if __name__ == '__main__':
    os.system('clear')  
    print menu
    
    # SLL Name and eSM Name mapping 
    Dict_sll_esm = {}

    # SLL Name and eSM data mapping 
    Dict_sll_esm_col_mapping = {}

    # SLL Name and eSM Column mapping 
    Dict_sll_esm_col = {}

    # SLL Name and SLL Column mapping 
    Dict_sll_sll_col = {}

    # SPA Name and SLL mapping 
    Dict_spa_sll = {}

    # SPA Name and SLL Column mapping 
    Dict_spa_sll_col = {}

    # SPA Name and SPA Column mapping 
    Dict_spa_spa_col = {}

    while True:
        cmd = raw_input("Selec the SPA to Process:")
        if cmd != 'q':
            os.system('clear')
            #if True:
            try:
                print menu
                if cmd == 'c':
                    Check_soid()
                elif cmd == 'm':
                    os.system('clear')
                    print menu
                elif cmd == 'h':
                    os.system('clear')
                    print '''
***************************************************************************************

    Copy the sym and xml file to the corresponding SPA directory before running this script'
                            
****************************************************************************************
'''         

                elif commands(cmd) != None:
                    spa = commands(cmd)
                    print spa
                    dir =  os.path.dirname(os.path.abspath(sys.argv[0]))    
                    # input file (sym,xml and sql file) path    
                    conf_path = os.path.join(os.path.join(dir,'conf'),spa)
                    List_conf=Find_file(conf_path)

                    # output file path 
                    output_path = os.path.join(os.path.join(dir,'sql_eSM'),os.path.basename(List_conf[-1]))
                    #print 'sym file:%s,xml file:%s,sql file:%s' %(List_conf[0],List_conf[1],List_conf[-1])
                    
                    List_dict = Process_xml(List_conf[1])   
                    Dict_sll_esm = List_dict[0]
                    Dict_sll_esm_col_mapping = List_dict[1]
                    Dict_sll_esm_col = List_dict[2]
                    Dict_sll_sll_col = List_dict[3]
                    
                    #i=1    
                    #for key in Dict_sll_esm:
                    #   print '%d:key:%s,value:%s' %(i,key,Dict_sll_esm[key])
                    #   i+=1

                    #print '==========================================='

                    #i=1    
                    #for key in Dict_sll_sll_col:
                    #   print '%d:key:%s,value:%s' %(i,key,Dict_sll_sll_col[key])
                    #   i+=1
                         
                    List_dict_sym = Process_sym(List_conf[0])
                    Dict_spa_sll = List_dict_sym[0]
                    Dict_spa_sll_col = List_dict_sym[1]
                    Dict_spa_spa_col = List_dict_sym[2]

                    #print '==========================================='
                    #i=1    
                    #for key in Dict_spa_sll:
                    #   print '%d:key:%s,value:%s' %(i,key,Dict_spa_sll[key])
                    #   i+=1

                    #print '==========================================='
                    #i=1    
                    #for key in Dict_spa_esm_col:
                    #   print '%d:key:%s,value:%s' %(i,key,Dict_spa_esm_col[key])
                    #   i+=1

                    #print '==========================================='
                    #i=1    
                    #for key in Dict_spa_spa_col:
                    #   print '%d:key:%s,value:%s' %(i,key,Dict_spa_spa_col[key])
                    #   i+=1
                    
                    #print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'     
                    # AUDIT
                    #print Dict_spa_sll_col.get('SPA_EPPSA29D_111') 
                    #print Dict_spa_sll_col.get('SPA_EPPSA29D_115') 
                    #print Dict_sll_sll_col.get('global_server')  
                    #print Dict_sll_sll_col.get('global_client')  
                    # EPAY
                    #print Dict_spa_sll_col.get('SPA_EPAY29D_0')    
                    #print Dict_spa_sll_col.get('SPA_EPAY29D_237')  
                    #print Dict_sll_sll_col.get('global_server')  
                    #print Dict_sll_sll_col.get('global_client')  
                    #print len(Dict_spa_esm_col.get('SPA_EPPSA29D_111'))                    
                    #print len(Dict_spa_esm_col.get('SPA_EPPSA29D_115'))
                    # EPAY
                    #print len(Dict_spa_sll_col.get('SPA_EPAY29D_0'))                   
                    #print len(Dict_spa_sll_col.get('SPA_EPAY29D_237'))
                    #print len(Dict_sll_sll_col.get('global_server'))
                    #print len(Dict_sll_sll_col.get('global_client'))
                    #print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'     

                    Process_sql(List_conf[-1],output_path,Dict_sll_esm,Dict_sll_esm_col_mapping,Dict_sll_esm_col,Dict_sll_sll_col,Dict_spa_sll,Dict_spa_sll_col,spa)    

                else:
                    print "Input is Wrong!\n"

            except Exception,e:
            #except IndexError,e:
                print menu
                print '==========='
                print e
                traceback.print_exc()
                print '==========='

        else: 
            print "Exit the menu\n"
            sys.exit()
