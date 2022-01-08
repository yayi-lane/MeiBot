from nonebot import on_keyword ,on_command
from nonebot.adapters import Bot ,Event
from nonebot.rule import regex ,to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot ,Message ,GroupMessageEvent
from aiohttp import ClientSession
from urllib.parse import urlencode
import re
import os



bilibili = on_keyword(["b站" ,"哔站" ,"哔哩哔哩"] ,rule= regex(regex= r"芽衣|(@芽衣)",flags= re.M|re.I) ,priority=5)

@bilibili.handle()
async def handle_city(bot: Bot ,event:GroupMessageEvent ,state: T_State):

    args = str(event.get_message()).strip()
    args = re.sub(r'(b站)|(哔站)|(哔哩哔哩)|(芽衣)|(@芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I).strip()
    
    if args:
        state["content"] = args

@bilibili.got("content", prompt="呐~呐~想问什么呢？")
async def handle_content(bot: Bot, event:GroupMessageEvent , state: T_State):

    content = state["content"]
    name =  state["content"]

    dic ={"keyword": content}
    content = urlencode(dic)
    # UA伪装 referer 防盗链
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','referer': 'https://www.bilibili.com'}
    # 索引api 获取BV
    url = "https://api.bilibili.com/x/web-interface/search/type"
    payload = "?page=1&rder=click&%s&search_type=video" %(content)
    url = url + payload
    # verify_ssl 证书认证
    async with ClientSession() as session:
        response = await session.get(url,verify_ssl= False ,headers= headers)
        res_payload = await response.json()

        bv_1 = res_payload["data"]["result"][0]["bvid"]
        bv = "\nBV:" + bv_1

        bv_author = res_payload["data"]["result"][0]["author"]
        bv_author = "\n制作UP:" + bv_author

        bv_link = res_payload["data"]["result"][0]["arcurl"]
        bv_link = "\n链接: " + bv_link

        name = re.sub(r'(b站)|(哔站)|(哔哩哔哩)|(芽衣)' ,"" ,name ,count=0 ,flags= re.M|re.I)
        bv_name = res_payload["data"]["result"][0]["title"]
        bv_name = re.sub(r"(<.*>)","%s",bv_name) %(name)
        bv_name = "\n名称: "+ bv_name

        bv_pic = res_payload["data"]["result"][0]["pic"]
        bv_pic = "https:"+ bv_pic
        bv_pic = "\n[CQ:image,file=%s]" %(bv_pic)

        res = bv + bv_author + bv_link + bv_name + bv_pic
        # cid api 获取 cid
        url_c = "https://api.bilibili.com/x/player/pagelist?bvid=%s&jsonp=jsonp"% bv_1
        async with ClientSession() as session:
            response = await session.get(url_c,verify_ssl= False ,headers= headers)
            res_payload = await response.json()
        cid = res_payload["data"][0]["cid"]
        # 播放地址 api 获取视频链接
        url_p = "http://api.bilibili.com/x/player/playurl"
        payload = "?bvid=%s&cid=%s&qn=32&fnval=0&fnver=0"% (bv_1,cid)
        url_p = url_p + payload
        async with ClientSession() as session:
            response = await session.get(url_p,verify_ssl= False ,headers= headers)
            res_payload = await response.json()

        d_url = res_payload["data"]["durl"][0]["url"]

        async with ClientSession() as session:
            response = await session.get(d_url,verify_ssl= False ,headers= headers)
            res_payload = await response.read()

        file_name = r"{}.flv".format(bv_1)
        with open(file_name,'wb') as fp:
            fp.write(res_payload)
            fp.close()

        id =str(event.get_user_id())

        lj = re.sub(r'(src\\plugins\\哔站.py)' ,"" ,os.path.abspath(__file__) ,count=0 ,flags= re.M|re.I)
        file_lj = re.sub(r'\\' ,"//" ,lj ,count=0 ,flags= re.M|re.I)
        dz = "%s%s"%(file_lj,file_name)
        
        await bot.call_api("upload_group_file", group_id= str(event.group_id),file=  dz ,name= file_name)

        return await bilibili.finish(Message("[CQ:at,qq={}]".format(id) +res))
            



bilibili_bv = on_keyword(["精准播放" ,"bv播放" ,"Bv播放" ,"BV播放" ,"播放"] ,rule= regex(regex= r"播放",flags= re.M|re.I) ,priority=5)

@bilibili_bv.handle()
async def handle_city(bot: Bot ,event:GroupMessageEvent ,state: T_State):

    bv = str(event.get_message()).strip()
    bv = re.sub(r'(精准播放)|(bv播放)|(Bv播放)|(BV播放)|(播放)|(芽衣)|(@芽衣)' ,"" ,bv ,count=0 ,flags= re.M|re.I).strip()

    bv = re.search(r'BV..........', bv, flags= re.M|re.I).group(0)
    print(bv)

    # UA伪装 referer 防盗链
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','referer': 'https://www.bilibili.com'}

    # cid api 获取 cid
    url_c = "https://api.bilibili.com/x/player/pagelist?bvid=%s&jsonp=jsonp"% bv
    async with ClientSession() as session:
        response = await session.get(url_c,verify_ssl= False ,headers= headers)
        res_payload = await response.json()
    cid = res_payload["data"][0]["cid"]

    # 播放地址 api 获取视频链接
    url_p = "http://api.bilibili.com/x/player/playurl"
    payload = "?bvid=%s&cid=%s&qn=32&fnval=0&fnver=0"% (bv ,cid)
    url_p = url_p + payload
    async with ClientSession() as session:
        response = await session.get(url_p,verify_ssl= False ,headers= headers)
        res_payload = await response.json()

    d_url = res_payload["data"]["durl"][0]["url"]

    async with ClientSession() as session:
        response = await session.get(d_url,verify_ssl= False ,headers= headers)
        res_payload = await response.read()

    file_name = r"{}.flv".format(bv)
    with open(file_name,'wb') as fp:
        fp.write(res_payload)
        fp.close()

    id =str(event.get_user_id())

    lj = re.sub(r'(src\\plugins\\哔站.py)' ,"" ,os.path.abspath(__file__) ,count=0 ,flags= re.M|re.I)
    file_lj = re.sub(r'\\' ,"//" ,lj ,count=0 ,flags= re.M|re.I)
    dz = "%s%s"%(file_lj,file_name)
    
    await bot.call_api("upload_group_file", group_id= str(event.group_id),file=  dz ,name= file_name)

    return await bilibili_bv.finish(Message("[CQ:at,qq={}]".format(id)))




bilibili_t = on_keyword(["b站" ,"哔站" ,"哔哩哔哩"] ,rule= regex(regex= r"(b站)|(哔站)|(哔哩哔哩)",flags= re.M|re.I) ,priority=40)

@bilibili_t.handle()
async def handle_city(bot: Bot ,event:GroupMessageEvent ,state: T_State):

    args = str(event.get_message()).strip()
    args = re.sub(r'(b站)|(哔站)|(哔哩哔哩)|(芽衣)|(@芽衣)' ,"" ,args ,count=0 ,flags= re.M|re.I).strip()


    content = args
    name = args

    dic ={"keyword": content}
    content = urlencode(dic)
    # UA伪装 referer 防盗链
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','referer': 'https://www.bilibili.com'}
    # 索引api 获取BV
    url = "https://api.bilibili.com/x/web-interface/search/type"
    payload = "?page=1&rder=click&%s&search_type=video" %(content)
    url = url + payload
    # verify_ssl 证书认证
    async with ClientSession() as session:
        response = await session.get(url,verify_ssl= False ,headers= headers)
        res_payload = await response.json()

        bv_1 = res_payload["data"]["result"][0]["bvid"]
        bv = "\nBV:" + bv_1

        bv_author = res_payload["data"]["result"][0]["author"]
        bv_author = "\n制作UP:" + bv_author

        bv_link = res_payload["data"]["result"][0]["arcurl"]
        bv_link = "\n链接: " + bv_link

        name = re.sub(r'(b站)|(哔站)|(哔哩哔哩)|(芽衣)' ,"" ,name ,count=0 ,flags= re.M|re.I)
        bv_name = res_payload["data"]["result"][0]["title"]
        bv_name = re.sub(r"(<.*>)","%s",bv_name) %(name)
        bv_name = "\n名称: "+ bv_name

        bv_pic = res_payload["data"]["result"][0]["pic"]
        bv_pic = "https:"+ bv_pic
        bv_pic = "\n[CQ:image,file=%s]" %(bv_pic)

        res = bv + bv_author + bv_link + bv_name + bv_pic
        id =str(event.get_user_id())
        return await bilibili_t.finish(Message("[CQ:at,qq={}]".format(id) +res))