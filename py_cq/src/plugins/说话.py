from nonebot import on_keyword, on_command
from nonebot.adapters import Bot , Event
from nonebot.rule import regex,to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message , GroupMessageEvent
import re
from nonebot import on_keyword ,on_command
from nonebot.adapters import Bot ,Event
from nonebot.rule import regex ,to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message ,GroupMessageEvent
import random
import re

hallo_2 = on_keyword(["你好", "嗨", "哈喽"], rule= regex(regex= "芽衣", flags= re.M|re.I),priority= 10)

@hallo_2.handle()
async def h_r(bot:Bot,event:GroupMessageEvent,state:T_State):

    id = str(event.get_user_id())
    
    await hallo_2.finish(Message("[CQ:at,qq={}]".format(id) +"你好啊~"))



hallo = on_keyword(["你好" ,"嗨" ,"哈喽"], rule= regex(regex= r"芽衣|(@芽衣)" ,flags= re.M|re.I) ,priority= 35)

@hallo.handle()
async def h_r(bot:Bot ,event:GroupMessageEvent ,state:T_State):

    id = str(event.get_user_id())
    
    await hallo.finish(Message("[CQ:at,qq={}]".format(id) +"你好啊~"))

hallo = on_keyword(["随机数" ,"随机"], rule= regex(regex= r"" ,flags= re.M|re.I) ,priority= 35)
@hallo.handle()
async def h_r(bot:Bot ,event:GroupMessageEvent ,state:T_State):

    id = str(event.get_user_id())

    args = str(event.get_message()).strip()
    args = int(re.sub(r'(随机数)|(随机)|(@芽衣)|(芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I).strip())

    num = random.choice(range(args))
    await hallo.finish(Message("[CQ:at,qq={}]".format(id) +f"数字为:{num}"))


cd = on_keyword(["菜单" ,"功能"], rule= regex(regex= r"芽衣|(@芽衣)" ,flags= re.M|re.I) ,priority= 1)

@cd.handle()
async def h_r(bot:Bot ,event:GroupMessageEvent ,state:T_State):

    id = str(event.get_user_id())

    bb = "\n用法:关键词加信息即可\n"
    cc = "例如:芽衣哈尔滨天气\n"
    bh = "--功能-----用法--\n"
    ah = "需要叫 芽衣 触发的功能\n"
    ch = "天气查询-天气加地区\n"
    dh = "百度词条-百度加信息\n"
    eh = "哔站视频-哔站加名称\n"
    fh = "不需要叫 芽衣 触发的功能\n"
    gh = "精准播放-播放加bv号\n视频信息-哔站加名称\n"
    hh = "今日榜首-今日图片\n图片索引-图片加名称\n榜首图片-榜首加日期\n"
    zh = "百度翻译-翻译加文字\n随机数字-随机加数字\n"
    ih = "其他功能升级中....预计包含qr码"
    age = bb +cc +ah +bh +ch +dh +eh +fh +bh +gh +hh +zh +ih
    await cd.finish(Message("[CQ:at,qq={}]".format(id) +age))




# 彩蛋01
eggshell_a = on_keyword(["二次元" ,"二刺螈" ,"二刺猿"], rule= regex(regex= r"芽衣|(@芽衣)" ,flags= re.M|re.I) ,priority= 35)
@eggshell_a.handle()
async def h_r(bot:Bot,event:GroupMessageEvent,state:T_State):

    send = "诶多~是~同类的~喵呢!那群八嘎 是不会懂的关于二次元的美好的呢! 呐 ~如果说吾的存在有意义的话 ~那一定是因为二次元吧 所以呢~妄图污染这份爱的人类都会被吾~抹杀掉的呢 ~哼唧唧 ~讨厌二次元的八嘎 ~和那些三次元真的是最恶心的呢 魂淡三次元 八嘎八嘎 ~哼唧唧"

    await eggshell_a.finish(Message("[CQ:tts,text={}]".format(send)))
# 彩蛋02
eggshell_b = on_keyword(["媳妇","老婆","达令","宝贝"], rule= regex(regex= r"芽衣|(@芽衣)" ,flags= re.M|re.I) ,priority= 35)
@eggshell_b.handle()
async def h_r(bot:Bot,event:GroupMessageEvent,state:T_State):

    send_mgs = ["老公好~","老公~要亲亲嘛？","怎么了~老公"]
    send = random.choice(send_mgs)

    await eggshell_b.finish(Message("[CQ:tts,text={}]".format(send)))
