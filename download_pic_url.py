#!/bin/python
#coding=utf-8
 
import xlrd
import xlsxwriter
import urllib.request  
from xml.dom import minidom 
import re
import sys
import codecs
import string
from urllib.parse import quote
import os
import urllib
import urllib3
import time
from hashlib import md5
import imghdr
from lxml import etree
import xml.etree.ElementTree as ET
import xml
import urllib.request, urllib.error, urllib.request, urllib.parse
import pprint as pp
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配url模式
pic_file_path = "./pic/"
file_path = "./file/"
replace_pic = "./replace_pic/"

def findfile(start, name):
    for relpath, dirs, files in os.walk(start):
        if name in files:
            return True

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)



class ImageDownLoader:
    """
    图片下载器
    """
    @staticmethod
    def download(url, path):
        """
        这个方法用来下载图片并保存
        :param url:  图片的路径
        :param path: 要保存到的路径
        :return:
        """
        s=requests.Session()
        s.mount('https://', MyAdapter())
        response = urllib.request.urlopen(url)
        url_type = imghdr.what(None, response.read())
        if(url_type):
            #这里用了url算了md5来作为该图片的名字
            url_md5 = md5(url.encode("utf-8")).hexdigest()
            save_name = path + url_md5 + "." + url_type
            pic_name = url_md5 + "." + url_type
            urllib.request.urlretrieve(url, save_name)   
            with open(save_name, 'wb') as img_file:
                print("download a pic name:",save_name)
                img_file.write(response.read())
            return pic_name
        else:
            return ""


def parse_url(url):
    header = { 'Connection': 'close','User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    #请求获取xml数据
    
    url = quote(url, safe=string.printable)
    for i in range(5):
        try:
            s=requests.Session()
            s.mount('https://', MyAdapter())
            conn = urllib.request.urlopen(url)
            save_name = ImageDownLoader.download(url,pic_file_path)
            return save_name
        except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...
        #if this happened, find loacl dictionary if we have this picture
            print('HTTPError: {}'.format(e.code))
            if(re.search(cdn_pattern,url)):
                print("find this 404 cdn:",url)
                pic_name = url.split("/")[-1] + ".jpg"
                if(findfile(replace_pic,pic_name)):
                    print("find this 404 pic in replace_pic:",url)
                    return pic_name
                else:
                    print("Not find this 404 pic in replace_pic:",url)
            break
        except urllib.error.URLError as ee:
            print("other error: ",url)
            break
        except ConnectionResetError as a:
            print("sleep 0.5s")
            time.sleep(0.5)
            continue
        except Exception as b:
            print("other error: ",url)
            break
        else:
            break  
    return ""



def get_url(upload_address, url,file_name):
    header = { 'Connection': 'close','User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    #request url in xml format
    url = quote(url, safe=string.printable)

    #you can use sentence downbelow if you want to download this url
    #urllib.request.urlretrieve(url,file_name)

    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "xml")
    get_cdn = False
    address_dict = {}    
    for tag in soup.find_all(text=re.compile(url_pattern)):
        print("get html a url:",tag.string)
        pic_address = parse_url(tag.string)
        if(pic_address and len(pic_address)>0):
            cdn = upload_address+pic_address
            print("get cdn address: ",cdn)
            tag.string.replace_with(cdn)
            get_cdn = True

    if(get_cdn):
        with open(file_name,"wb") as store_file:
            print("write new file in ", file_name)
            #print(soup.prettify(soup.original_encoding))
            store_file.write(soup)

if __name__ == "__main__":
    #you can read url in file or input as argv
    #upload_address is the picture url in your cdn
    if(re.match(url_pattern,url)):
        get_url(upload_address, url,file_name)
 
 