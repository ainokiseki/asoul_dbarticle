import asyncio
import time
import hmac
import base64
import datetime
import requests
import MySQLdb
from urllib.parse import urlparse, quote

from lxml import etree
from pymysql.converters import escape_string
import json
def estr(x):
    return "'"+escape_string(x)+"'"
def fulltext(x):
    return etree.tostring(x,encoding='utf-8').decode('utf-8')

class apiError(Exception):
    pass

def stodt(x):
    return datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S")

cnt=MySQLdb.connect('localhost','**user**','**password**','**database**')
cursor = cnt.cursor()


class DoubanApi:
    @staticmethod
    def _encryption(api: str, method: str, row_data: dict) -> dict:
        """"
        签名算法
        """
        time.sleep(0.2)
        path = urlparse(api).path
        secret = b"bf7dddc7c9cfe6f7"
        timestamp = int(time.time())
        message = "&".join([method, quote(path, safe="")])
        message += "&" + str(timestamp)
        h = hmac.new(secret, message.encode(), digestmod="sha1")
        b = base64.b64encode(h.digest())
        return {**row_data, "apikey": "0dad551ec0f84ed02907ff5c42e8ec70", "_ts": timestamp, "_sig": b.decode()}

    @staticmethod
    def _check(data: dict) -> dict:
        if "localized_message" not in data:
            return data
        else:
            print(data)
            raise apiError(data["localized_message"])

    @classmethod
    def get_new_topics(cls, session, gid,tagid,start):
        """
        获取新的帖子
        """
        api = f"https://frodo.douban.com/api/v2/group/{gid}/topics"
        method = "GET"
        params = cls._encryption(api, method, {
            "start": start,  # 开始位置
            "count": 100,  # 返回条目数
            "topic_tag_id": tagid,  # TagID
        })
        resp=session.get(api, params=params)
        return cls._check(resp.json())

    @classmethod
    def get_topic(cls, session, tid):
        
        """
        获取新的帖子
        """
        api = "https://frodo.douban.com/api/v2/group/topic/{}".format(tid)
        print(api)
        method = "GET"
        params = cls._encryption(api, method, {
        })
        resp=session.get(api, params=params)
        return cls._check(resp.json())
    @classmethod
    def get_com(cls, session, tid,start):
        """
        获取楼主回复
        """
        api = "https://frodo.douban.com/api/v2/group/topic/{}/op_comments".format(tid)
        print(api)
        method = "GET"
        params = cls._encryption(api, method, {
            "start":start,
            "count":100
        })
        resp=session.get(api, params=params)
        return cls._check(resp.json())

def get_paper_list():

    headers = {
        "User-Agent": "api-client/1 com.douban.frodo/7.22.0.beta9(231) Android/23 product/Mate 40 vendor/HUAWEI model/Mate 40 brand/HUAWEI  rom/android  network/wifi  platform/AndroidPad",
    }
    grouplist=[[726457,87879],[720459,73743],[728891,91342],[726499,97461]]
    #嘉晚饭：726457，87879
    #魂组：720459,73743
    #乃贝：728891 ，91342
    #bbj:726499,97461
    session=requests.session()
    session.headers=headers
    newtplist=[]
    for i,j in grouplist:
        ttnum=200
        nnum=0
        cursor.execute('select max(update_time) from asoul_paper where gid=%d'%(i))
        maxtime=cursor.fetchall()[0][0]
        if maxtime==None:
            maxtime=stodt("2020-12-26 00:00:00")
        while nnum<ttnum:
            js=DoubanApi.get_new_topics(session, i,j,nnum)
            target_data=[k for k in js['topics'] if stodt(k['update_time'])>maxtime]
            newtplist+=[int(k['id']) for k in target_data]
            nnum+=100
            ttnum=js['total']
            data1=[[k['id'],i,k['author']['id'],k['author']['name'],k['create_time']] for k in target_data]

            data2=[[k['title'],str(int(k['is_elite'])),k['update_time'],str(k['comments_count']),k['id']] for k in target_data]
            sql="insert ignore into asoul_paper (tid,gid,uid,author,create_time) values (%s,%s,%s,%s,%s)"
            cursor.executemany(sql,data1)
            sql="update asoul_paper set title=%s,elite=%s,update_time=%s,comment_count=%s where tid=%s"
            cursor.executemany(sql,data2)
            if len(target_data)<len(js['topics']):
                break
            
    #print(await DoubanApi.get_group_info(session, g))
    return newtplist
def get_article(xx):

    headers = {
        "User-Agent": "api-client/1 com.douban.frodo/7.22.0.beta9(231) Android/23 product/Mate 40 vendor/HUAWEI model/Mate 40 brand/HUAWEI  rom/android  network/wifi  platform/AndroidPad",
    }
    def handle_json(x):

        y={'name':x['author']['name'],'uid':x['author']['uid'],'text':x['text'],'photos':x['photos'],'create_time':x['create_time']}
        if 'ref_comment' in x:
            z=x['ref_comment']
            zz={'name':z['author']['name'],'uid':z['author']['uid'],'text':z['text']}
            y['ref_comment']=zz
        return json.dumps(y)
        
    session=requests.session()
    session.headers=headers

    for j in xx:
        


        try:
            js=DoubanApi.get_topic(session,j)

            # sql="update asoul_paper set gid=%s,uid=%s,author=%s,title=%s,elite=%s,create_time=%s,update_time=%s,fav_count=%s,comment_count=%s,like_count=%s where tid=%s"
            # cursor.execute(sql,[js['group']['id'],js['author']['id'],js['author']['name'],js['title'],str(int(js['is_elite'])),js['create_time'],js['update_time'],js['collections_count'],js['comments_count'],js['like_count'],str(j)])
            




            sql="update asoul_paper set like_count=%d,fav_count=%d where tid=%d"%(js['like_count'],js['collections_count'],j)
            cursor.execute(sql)
            

            sql="insert into asoul_article (tid,`order`) select %s,0 where not exists (select tid from asoul_article where tid=%s)"
            cursor.execute(sql,[str(j),str(j)])
            sql="update asoul_article set textdata=%s where tid=%s and `order`=0"
            cursor.execute(sql,[js['content'],str(j)])

            cursor.execute('select count(*) from asoul_article where tid=%d'%(j))
            nnum=cursor.fetchall()[0][0]-1
            ttnum=nnum+1
            while nnum<ttnum:
                try:

                    js=DoubanApi.get_com(session,j,nnum)

                    
                    ttnum=js['total']

                    data=[[str(j),str(kk+nnum+1),handle_json(k)] for kk,k in enumerate(js['comments'])]

                    nnum+=100

                    sql="insert into asoul_article (tid,`order`,textdata) values (%s,%s,%s)"
                    cursor.executemany(sql,data)
                    print(nnum,ttnum)
                except apiError as e:
                    print(e)
                    break

        except apiError as e:
            print(e)
            cursor.execute('update asoul_paper set banned=1 where tid=%d'%(j))
        
    #print(await DoubanApi.get_group_info(session, g))
    

def t2():
    headers = {
        "User-Agent": "api-client/1 com.douban.frodo/7.22.0.beta9(231) Android/23 product/Mate 40 vendor/HUAWEI model/Mate 40 brand/HUAWEI  rom/android  network/wifi  platform/AndroidPad",
    }

    session=requests.session()
    session.headers=headers
    js=DoubanApi.get_topic(session,258428877)
    f=open('dp.json','w')
    f.write(json.dumps(js))
    f.close()

    #print(await DoubanApi.get_group_info(session, g))


if __name__ == "__main__":
    while True:
        time.sleep(3600*12)
        x=get_paper_list()
        print(len(x))

        # cursor.execute('select tid from asoul_paper where flag=2')
        # x=[i[0] for i in cursor.fetchall()]
        get_article(x)
        cnt.commit()

    #t2()
    #嘉晚饭：726457，87879
    #魂组：720459,73743
    #乃贝：728891 ，91342
    #bbj:726499,97461