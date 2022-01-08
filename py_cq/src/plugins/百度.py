from nonebot import on_keyword ,on_command
from nonebot.adapters import Bot ,Event
from nonebot.rule import regex ,to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message ,GroupMessageEvent
from lxml import etree
from aiohttp import ClientSession
import re


baidu = on_keyword(["百度" ,""] ,rule= regex(regex= r"(芽衣)|(@芽衣)" ,flags= re.M|re.I) ,priority=40)

@baidu.handle()
async def handle_city(bot: Bot ,event:GroupMessageEvent ,state: T_State):

    args = str(event.get_message()).strip()
    args = re.sub(r'(百度)|(芽衣)|(@芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I).strip()

    if args =="":
        args = "芽衣"
    
    if args:
        state["content"] = args

@baidu.got("content", prompt="什么都不的说~芽衣也不知道要怎么办呢~")
async def handle_content(bot: Bot ,event:GroupMessageEvent ,state: T_State):

    content_ = state["content"]

    url_ = "https://baike.baidu.com/item/" + content_
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"}

    async with ClientSession() as session:       
        async with await session.get(url=url_,headers=header) as response:
            response_ = await response.text()

    img = etree.HTML(response_)
    page = img.xpath('/html/head/meta[4]/@content')

    if page == []:
        page = "词条暂无"
    else:
        page = page[0]
    id =str(event.get_user_id())

    return await baidu.finish(Message("[CQ:at,qq={}]".format(id)+ page))