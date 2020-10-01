#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
必应词典 for goldendict
author: 'oldoldstone'
Created on 2020-9-30 12:04:00
USAGE:
python3 bingdict.py  <text to be translated>
python3 bingdict.py 'hello world!'
"""

import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import quote
import string
HTML_TMPL = """
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>必应词典</title>
<meta http-equiv="content-type" content="text/html;charset=utf-8" />
<meta name="generator" content="Geany 1.36" />
<style type="text/css">html,body,h1,h2,h3,h4,h5,h6,p,img,ol,ul,li,form,table,tr,th,td,blockquote{border:0;border-collapse:collapse;border-spacing:0;list-style:none;margin:5;padding:0}client_def_hd_area{width:100%;overflow:hidden;margin-bottom:15px}.client_def_hd_hd_nw{display:inline-block}.client_def_hd_hd{margin-right:20px;float:left}.client_def_hd_pn_bar{overflow:hidden}.client_def_hd_pn_list{overflow:hidden;float:left;margin-right:10px}.client_def_hd_pn{float:left;margin:5px 5px 0 0;white-space:nowrap}.client_def_hd_hd{font-family:Microsoft YaHei;font-size:20px;color:#000;font-weight:bold}.client_def_hd_pn{font-family:Segoe UI,Arial,Helvetica,Sans-Serif;_font-family:Lucida Sans Unicode,sans-serif;font-size:13px;color:#777}.client_add_newword_f,.client_add_newword_o,.client_add_newword_d,.client_del_newword_f,.client_del_newword_o,.client_del_newword_d,.client_ktv_f,.client_ktv_o,.client_ktv_d,.client_aud_f,.client_aud_o,.client_aud_d,.client_share_f,.client_share_o,.client_share_d .client_copy_f,.client_copy_o,.client_copy_d{width:24px;height:24px;background-image:url("/th?id=OJ.VomR2COqzLF7sg&pid=MSNJVFeeds");background-repeat:no-repeat;_height:15px;_width:338px;_filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src="/th?id=OJ.VomR2COqzLF7sg&pid=MSNJVFeeds",sizingMethod="scale");_background:none;_background-color:#fff;_font-size:0}.client_do_you_mean_list_word,.client_siderbar_list_word,.client_word_change_word,.client_def_en_hover,.client_do_you_mean_word{color:#06a}.client_del_newword_o{_margin-left:-150px;background-position:-150px 0}.client_add_newword_o{_margin-left:-207px;background-position:-207px 0}.client_new_word{display:inline-block;float:left;margin-top:6px}.client_icon_container{width:16px;height:16px;overflow:hidden;cursor:pointer}.client_aud_o{_margin-left:-95px;background-position:-95px 0}.client_def_audio{margin-right:5px;float:left;margin-top:6px}.client_def_container{clear:both;overflow:hidden}.client_def_bar{margin-bottom:5px;clear:both;overflow:hidden}.client_def_title,.client_def_title_web{padding:1px 3px}.client_def_title_web{font-size:13px;background-color:#000;color:#fff;font-family:Segoe UI,Arial;font-weight:bold}.client_def_title{font-size:13px;background-color:#aaa;color:#fff;font-family:Segoe UI,Arial;font-weight:bold}.client_def_title_bar{width:45px;vertical-align:top;float:left}.client_def_list{margin-left:3px;overflow:hidden;_float:left}.client_def_list_item{overflow:hidden;display:block;_display:inline-block;padding-bottom:5px}.client_def_list_word_item{overflow:hidden;_float:left;padding-left:0}.client_def_list_word_bar{overflow:hidden;font-size:13px;color:#000;font-family:Microsoft YaHei,宋体}.client_def_list_word_content{float:left}.client_word_change{float:left;margin-right:10px}.client_word_change_def{overflow:hidden;margin-right:20px}.client_word_change_word{margin-right:10px;cursor:pointer;float:left}.client_word_change{font-size:13px;font-family:Microsoft YaHei,宋体;color:#777}</style>
</head>
<body> 
{{content}}
</body>
</html>
"""


def parse(gwords):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                             Chrome/42.0.2311.90 Safari/537.36"
               }
    # urlstr = 'https://cn.bing.com/dict/search?q=' + keyword
    urlstr = 'https://cn.bing.com/dict/clientsearch?mkt=zh-CN&setLang=zh&form=BDVEHC&ClientVer=BDDTV3.5.1.4320&q='
    url = quote(urlstr, safe=string.printable) + gwords
    try:
        r = requests.post(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print('Connection Error !')
        exit()
    except Exception as e:
        print(e)
        exit()
    return BeautifulSoup(r.text, 'html.parser')  # transfer to html files easy to analyse


if __name__ == '__main__':
    keyword = ' '.join(sys.argv[1:])
    soup = parse(keyword)
    content = u""
    nextNode = soup.find('span', id='anchor0')
    if nextNode is None:
        output = soup.prettify()
    else:
        while True:
            nextNode = nextNode.nextSibling
            if nextNode.attrs == {'id': 'anchor1'} or nextNode.attrs == {'class': ['client_def_image_bar']}:
                break
            content = content + nextNode.prettify()
        output = HTML_TMPL.replace('{{content}}', content)
    print(output)
