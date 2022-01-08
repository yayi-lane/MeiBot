<<<<<<< HEAD
from nonebot import on_command , on_keyword
from nonebot.adapters import Bot , Event
from nonebot.rule import to_me , regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message , GroupMessageEvent
=======
from nonebot import on_command ,on_keyword
from nonebot.adapters import Bot ,Event
from nonebot.rule import to_me ,regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message ,GroupMessageEvent
>>>>>>> 85f013a (first commit)
from aiohttp import ClientSession
import re


<<<<<<< HEAD
weather = on_keyword(["天气", "查天气" ,"今天天气"], rule= regex(regex= "芽衣", flags= re.M|re.I),priority= 5)

@weather.handle()
async def handle_city(bot: Bot, event:GroupMessageEvent , state: T_State):

    args = str(event.get_message()).strip()
    args = re.sub(r'(天气)|(查天气)|(芽衣)|(今天天气)', "", args, count=0, flags= re.M|re.I)
=======
weather = on_keyword(["天气" ,"查天气" ,"今天天气","天气怎么样"] ,rule= regex(regex= r"芽衣|(@芽衣)" ,flags= re.M|re.I) ,priority= 5)

@weather.handle()
async def handle_city(bot: Bot, event:GroupMessageEvent ,state: T_State):

    args = str(event.get_message()).strip()
    args = re.sub(r'(天气)|(查天气)|(芽衣)|(今天天气)|(天气怎么样)|(@芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I).strip()
>>>>>>> 85f013a (first commit)

    if args:
        state["city"] = args
        state["id"] = 0

@weather.got("city", prompt="呐~呐~欧尼酱~你想查询哪个城市的天气呢？")
<<<<<<< HEAD
async def handle_city(bot: Bot, event:GroupMessageEvent , state: T_State):

    id =str(event.get_user_id())
    city = state["city"]

=======
async def handle_city(bot: Bot, event:GroupMessageEvent ,state: T_State):

    id =str(event.get_user_id())

    city = state["city"]

    city = str(city).strip()

    city = re.sub(r'(天气)|(查天气)|(芽衣)|(今天天气)|(天气怎么样)|(@芽衣)' ,"" ,city ,count=0 ,flags= re.M|re.I).strip()
>>>>>>> 85f013a (first commit)
    
    url = "https://www.tianqiapi.com/api"
    payload = "?unescape=1&appid=61754919&appsecret=FVT6Q77I&city="+city
    async with ClientSession() as sess:
        async with sess.post(url+payload) as response:
            res_payload = await response.json()
            
            if city == res_payload['city']:

                res = f"{res_payload['city']}  {res_payload['data'][0]['date']}  {res_payload['data'][0]['week']}\n"\
                    f"天气: {res_payload['data'][0]['wea']}\n"\
                    f"温度: {res_payload['data'][0]['tem2']}到{res_payload['data'][0]['tem']}\n"\
                    f"风向: {res_payload['data'][0]['win'][0]}  风力: {res_payload['data'][0]['win_speed']}\n"\
                    f"{res_payload['data'][0]['air_tips']}"

                await weather.finish(Message("[CQ:at,qq={}]".format(id)+"\n"+res))

            else:

                if state["id"] == 0:

                    state["id"] = 1
                    await weather.reject(Message("[CQ:at,qq={}]".format(id)+"\n"+f"真是奇怪呢~芽衣居然找不到{city}这个地方,换个别的地方再试试嘛~"))

                elif state["id"] == 1:

                    state["id"] = 0
                    await weather.finish(Message("[CQ:at,qq={}]".format(id)+"\n"+f"芽衣居然也找不到{city}这个地方,芽衣自闭了"))