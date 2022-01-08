from nonebot import require
import re
import os


def del_files(path,gs):
      
    for root , dirs, files in os.walk(path):
             
          for name in files:
                              
                if name.endswith(gs):
        
                      os.remove(os.path.join(root, name))
                      print ("Delete File: " + os.path.join(root, name))

#调度程序
ql = require('nonebot_plugin_apscheduler').scheduler

@ql.scheduled_job("cron",hour='*/1',id="masturbation")
async def masturbation():

    lj = re.sub(r'(src\\plugins\\清理.py)' ,"" ,os.path.abspath(__file__) ,count=0 ,flags= re.M|re.I)
    file_lj = re.sub(r'\\' ,"//" ,lj ,count=0 ,flags= re.M|re.I)
    dz = file_lj
    
    del_files(dz,".flv")
    del_files(dz,".png")