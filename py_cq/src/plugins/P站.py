from os import name
from nonebot import on_keyword ,on_command
from nonebot.adapters import Bot ,Event
from nonebot.rule import regex ,to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message ,GroupMessageEvent
import re
from aiohttp import ClientSession
import datetime
from lxml import etree
from urllib.parse import urlencode
from urllib import parse
from pydantic.networks import url_regex
import random


# 请求模块
async def pzapi(url_):

    print(url_)
    url_list = []
    id_list = []
    title_list = []

    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"}

    async with ClientSession() as session:       
        async with await session.get(url=url_,headers=header) as response:
            response_ = await response.json()

            for sx in response_["rows"]:
                
                id = sx["id"]
                title = sx["title"]
                regular_url =sx["regular_url"]

                url = re.sub(r'regular' ,"original" ,regular_url ,count=0 ,flags= re.M|re.I)
                url = re.sub(r'_master(.*)',".png",url ,count=0 ,flags= re.M|re.I)

                url_list.append(url)
                id_list.append(id)
                title_list.append(title)  
            return (url_list,id_list,title_list)


# 获取昨日日期
def rq_z():

    date = datetime.datetime.now()
    date = str(re.sub(r'(..:..:.........)|-' ,"" ,str(date) ,count=0 ,flags= re.M|re.I).strip())
    date_2 = int(date[6:8]) - 1

    if date_2 == 0:

        if date[4:6] == "05" or  "07" or "10":
            date = date[0:4]+"0"+str(int(date)[4:6]-1)+"30"

        elif date[4:6] == "01":
            date = str(int(date[0:4])-1)+"1231" 

        elif date[4:6] == "03":
            if int(date[0:4]) % 4 == 0:
                if int(date[0:4]) % 40 == 0:
                    if int(date[0:4]) % 400 == 0:
                            date = date[0:4]+"0229"
            else:
                date_2 = date[0:4]+"0228"

        elif date[4:6] == "08":
            date = date[0:4]+"0731"

        elif date[4:6] == "11":
            date = date[0:4]+"1031"

        elif date[4:6] == "12":
            date = date[0:4]+"1130"
     
        else:     
            date = date[0:4]+"0"+str(int(date)[4:6]-1)+"31"
    else:
        if date_2 < 10:
            date_2 = "0"+str(date_2) 

        date = date[0:6] + str(date_2)
    
    return date


pz = on_keyword(["今日图片","美图"] ,rule= regex(regex= r"(美图)|(今日图片)" ,flags= re.M|re.I) ,priority=10)

@pz.handle()
async def handle_city(bot: Bot ,event:GroupMessageEvent ,state: T_State):
    
    
    date = rq_z()
    limit = "5"
    url_ = f"https://www.vilipix.com/api/illust?mode=daily&date={date}&limit={limit}&offset=0"

    await bot.call_api("send_group_msg",group_id=event.group_id,message=f"榜首日期:{date}")

    (url,a,b) = await pzapi(url_)
    for send in url:
        try:
            await bot.call_api("send_group_msg",group_id=event.group_id,message=f"[CQ:image,file={send},id=40000]")
        except:
            send = re.sub(r'.png' ,".jpg",send ,count=0 ,flags= re.M|re.I)
            await bot.call_api("send_group_msg",group_id=event.group_id,message=f"[CQ:image,file={send},id=40000]")

pz_b = on_keyword(["榜首","榜首图片"] ,rule= regex(regex= r"(榜首)|(榜首图片)" ,flags= re.M|re.I) ,priority=10)

@pz_b.handle()
async def handle_city(bot: Bot ,event:GroupMessageEvent ,state: T_State):
    
    args = str(event.get_message()).strip()
    date = re.sub(r'(榜首)|(榜首)|(@芽衣)|(芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I).strip()

    try:

        if int(len(str(date))) != 8:

            return await bot.call_api("send_group_msg",group_id=event.group_id,message=f"请输入八位日期,例如20200101")
            
        date = str(date)

    except:
        return await bot.call_api("send_group_msg",group_id=event.group_id,message=f"请输入八位日期,例如20200101")

    limit = "5"
    url_ = f"https://www.vilipix.com/api/illust?mode=daily&date={date}&limit={limit}&offset=0"

    await bot.call_api("send_group_msg",group_id=event.group_id,message=f"榜首日期:{date}")

    (url,a,b) = await pzapi(url_)
    for send in url:
        try:
            await bot.call_api("send_group_msg",group_id=event.group_id,message=f"[CQ:image,file={send},id=40000]")
        except:
            send = re.sub(r'.png' ,".jpg",send ,count=0 ,flags= re.M|re.I)
            await bot.call_api("send_group_msg",group_id=event.group_id,message=f"[CQ:image,file={send},id=40000]")


pz_s = on_keyword(["p站","P站","图片"] ,rule= regex(regex= r"" ,flags= re.M|re.I) ,priority=10)

@pz_s.handle()
async def handle_b(bot: Bot ,event:GroupMessageEvent ,state: T_State):
    
    args = str(event.get_message()).strip()
    args = re.sub(r'(p站)|(P站)|(图片)|(@芽衣)|(芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I).strip()

    if args =="":
        args = "芽衣"
        
    args_ = parse.quote(args)
    offset = random.randint(1,20)

    limit = "10"
    url_ = f"https://www.vilipix.com/api/illust/tag/{args_}?limit={limit}&offset={offset}"



    (url,a,b) = await pzapi(url_)

    url_ = random.choice(url)

    try:
        header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"}

        async with ClientSession() as session:      
            async with await session.get(url=url_,headers=header) as response:
                response_ = await response.text()
                send = re.sub(r'.png' ,".jpg",url_ ,count=0 ,flags= re.M|re.I)
                await bot.call_api("send_group_msg",group_id=event.group_id,message=f"[CQ:image,file={send},id=40000]")
    except: 
        await bot.call_api("send_group_msg",group_id=event.group_id,message=f"[CQ:image,file={url_},id=40000]")