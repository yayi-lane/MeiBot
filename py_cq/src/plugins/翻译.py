from nonebot import on_command,on_keyword
from nonebot.adapters import Bot
from nonebot.rule import to_me ,regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message , GroupMessageEvent
from aiohttp import ClientSession
from urllib.parse import urlencode
import hashlib
import time
import re

translate = on_keyword(["翻译","翻译一下"] ,rule= regex(regex= r"" ,flags= re.M|re.I) ,priority=5)

@translate.handle()
async def handle_city(bot: Bot, event:GroupMessageEvent , state: T_State):

    args = str(event.get_message())
    args = re.sub(r'(翻译)|(翻译一下)|(芽衣)|(@芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I)
    
    if args:
        state["content"] = args

# 在python3中使用hashlib模块进行md5操作
def msg(msg_str):
    # 待加密信息
    str = msg_str
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding="utf-8"))
    # hl.hexdingest 获取加密后得字符串
    return hl.hexdigest()


def payload_q(q_):

    q_ = str(q_)
    
    from_ = "auto"
    to_ = "zh"
    appid = "20210315000727962"
    salt = int(time.time())
    salt = str(salt)
    Key = "spzfAEHCz8Dgx62ytNQ0"
    sign = appid + q_ + salt + Key
    sign = msg(sign)

    dic = {"q": q_}
    q_ = urlencode(dic)
 
    payload = "?%s&from=%s&to=%s&appid=%s&salt=%s&sign=%s" % (q_ ,from_ ,to_ ,appid ,salt ,sign )

    return payload

@translate.got("content", prompt="呐~呐~翻译什么呢？")
async def handle_content(bot: Bot, event:GroupMessageEvent , state: T_State):

    content = state["content"]

    payload = payload_q(content)

    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    url = url + payload

    # session get (url , verify_ssl = False)
    async with ClientSession() as session:
        response = await session.get(url,verify_ssl = False)
        res_payload = await response.json()
        translate_2 = res_payload["trans_result"][0]["dst"]
        translate_ = "\n翻译结果:" + translate_2

        id =str(event.get_user_id())
     
        return await translate.finish(Message("[CQ:at,qq={}]".format(id) +"\n" +translate_))
        