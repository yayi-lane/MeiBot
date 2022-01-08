from nonebot import on_command ,on_keyword
from nonebot.adapters import Bot ,Event
from nonebot.rule import to_me ,regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message , GroupMessageEvent
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from lxml import etree
from aiohttp import ClientSession
import re
import random


async def url():

    url_list = []

    

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    try:

        url_ = "https://zh.joyhentai3.com/rank/day"
        async with ClientSession() as session:      
            async with await session.get(url=url_,headers=headers) as response_a:
                response_ = await response_a.text()

                num = random.choice(range(1,45))
                tree = etree.HTML(response_)

                x = f'//*[@id="main-contents"]/div[1]/div/ul[2]/li[{num}]/div/a/@href'

                slist_list = tree.xpath(x)[0]
                url = "https://zh.joyhentai3.com" + slist_list

    except:

        url_ = "https://zh.joyhentai.com/rank/day"
        async with ClientSession() as session:      
            async with await session.get(url=url_,headers=headers) as response_a:
                response_ = await response_a.text()

                num = random.choice(range(1,45))
                tree = etree.HTML(response_)
                x = f'//*[@id="main-contents"]/div[1]/div/ul[2]/li[{num}]/div/a/@href'
                slist_list = tree.xpath(x)[0]
                url = "https://zh.joyhentai.com" + slist_list

    async with ClientSession() as session:
        async with await session.get(url=url,headers=headers) as response_b:
            response = await response_b.text()

            tree_ = etree.HTML(response)
            slist = tree_.xpath('//*[@id="main-contents"]/div[1]/div[5]/div[1]/div/img')

    for n in slist:

        url = n.xpath('./@data-src')[0]
        url_list.append(url)
        
    return url_list

class Email_send:

    def __init__(self) -> None:
        pass

    def email_bz(self,id,url_list):

        email = str(id) +"@qq.com"

        smtp_obj = SMTP_SSL(host ="smtp.qq.com")
        smtp_obj.ehlo(name ="smtp.qq.com")
        smtp_obj.login("iuioiui@qq.com","evysvaukctgjgfcg")

        mail_contet = """<h1 align="center">芽衣爱你呦!</h1><h1 align="center"><font size="2">图片加载可能有点慢请耐心等待</font></h1>"""

        for u in  url_list:

            mail_contet += f"""<p align="center"><img style="width: ;height: 100%;" src="{u}"></p>"""

        # 纯文本
        # msg = MIMEText("Hello","plain","utf-8")
        msg =   MIMEMultipart()
        msg["From"] = Header("可爱的芽衣酱","utf-8")
        msg["To"] = Header("亲","utf-8")
        msg["Subject"] = Header("芽衣偷偷塞给你的本子","utf-8")
        msg.attach(MIMEText(mail_contet,"html"))

        smtp_obj.sendmail("iuioiui@qq.com",email,msg.as_string())

        smtp_obj.quit()

    def email_sends(self,*num_list):
        
        email_list = []

        for num in num_list:

            email = str(num) +"@qq.com"
            email_list.append(email)

        smtp_obj = SMTP_SSL(host = "smtp.qq.com")
        smtp_obj.ehlo(name = "smtp.qq.com")
        smtp_obj.set_debuglevel(1)
        smtp_obj.login("iuioiui@qq.com","evysvaukctgjgfcg")

        url = ""
        mail_contet = """<p align="center"><img  style="width: ;height: 100%;" src="{}"></p><h1 align="center">芽衣爱你呦!</h1>""".format(url)

        # 纯文本
        # msg = MIMEText("Hello","plain","utf-8")
        msg =   MIMEMultipart()
        msg["From"] = Header("芽衣","utf-8")
        msg["To"] = Header("亲","utf-8")
        msg["Subject"] = Header("芽衣的信","utf-8")
        msg.attach(MIMEText(mail_contet,"html"))

        smtp_obj.sendmail("iuioiui@qq.com",email_list,msg.as_string())

        smtp_obj.quit()



email = on_keyword(["本子" ,"今日本子"] ,rule= regex(regex= r"(芽衣)|(@芽衣)" ,flags= re.M|re.I) ,priority=25)

@email.handle()
async def h_r(bot:Bot,event:GroupMessageEvent,state:T_State):

    id =str(event.get_user_id())

    await bot.call_api("send_group_msg",group_id=event.group_id,message="正在获取请稍后...")

    email_send = Email_send()
    try:
        url_list = await url()
    except:
         return await email.finish(Message("[CQ:at,qq={}]".format(id) +"冷却中请稍后..."))

    email_send.email_bz(id,url_list)

    return await email.finish(Message("[CQ:at,qq={}]".format(id) +"注意查收邮箱哦~"))