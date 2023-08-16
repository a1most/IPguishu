#!/usr/bin/env python
#coding=utf8
import requests,openpyxl,re,os,json,time
from multiprocessing import Pool

thread=20

url = 'http://ip.zxinc.org/api.php?type=json&ip='
header={
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.1) Gecko/20100101 Firefox/78.0',
'Host':'ip.zxinc.org',
}
def query(ip):
    #ip=ip.strip()
    try:
        r = requests.post(url+ip,headers=header,timeout=10)
        r.encoding = 'utf-8'
        regex=re.findall('location":"(.*?)"',r.text)
        print (ip,regex[0])
        return str(regex[0])
    except:
        return ['None']
def main():
    e=os.getcwd()
    in_file=input("请输入IP文件绝对路径：")
    f=open(in_file,'r')
    wb=openpyxl.Workbook()
    ws=wb.active
    ws.cell(1,1).value='源IP'
    ws.cell(1,2).value='ip归属地'
    line=f.readline().strip()
    pool=Pool(thread)
    time_start=time.time()
    i=2
    while line:
        guishu=pool.map(query,[line])
        #print (guishu[0])
        ws.cell(i,1).value=str(line)
        ws.cell(i,2).value=str(guishu[0])
        i=i+1
        line=f.readline().strip()
    pool.close()
    pool.join()
    f.close()
    wb.save(e+'\\'+'IP归属.xlsx')
    print ('归属地查询用时：%.2f' %(time.time()-time_start)+'s')
if __name__=='__main__':
    main()