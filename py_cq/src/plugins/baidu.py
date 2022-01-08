#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot import on_command
from nonebot.adapters import Bot , Event
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message , GroupMessageEvent
from aiohttp import ClientSession
from lxml import etree


baidu = on_command("百度",aliases={"百度一下", ""},rule=to_me(), priority=40)

@baidu.handle()
async def handle_city(bot: Bot, event:GroupMessageEvent , state: T_State):
    
    args = str(event.get_message()).strip()  # xx.strip()去除首位字符/空格
    if args:
        state["content"] = args

@baidu.got("content", prompt="什么都不的说~芽衣也不知道要怎么办呢~")
async def handle_content(bot: Bot, event:GroupMessageEvent , state: T_State):

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
    at_ = "[CQ:at,qq={}]".format(id)
    msg = at_ + page
    msg = Message(msg)
    return await baidu.finish(msg)
        


    