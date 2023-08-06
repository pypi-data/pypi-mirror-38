# -*- coding:utf-8 -*-

import execjs
import urllib
import re
import requests
from lxml import etree


class googleTranApi:

    def __init__(self):
        pass

    def getTkkValue(self):
        url = "https://translate.google.cn/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"}
        tkkHtml = requests.get(url, headers=headers)
        if tkkHtml.status_code == 200:
            tkkHtml.encoding = "utf-8"
            tkkHtmlCont = tkkHtml.content
        else:
            print("获取网页源码错误，请检查程序")
            return None
        tkkEtree = etree.HTML(tkkHtmlCont)
        # 这里返回一个list/ This is a list
        tkkScript = tkkEtree.xpath(".//*[@id='gt-c']/script[1]")[0]
        tkkValue01 = re.search("TKK=\'\d*\.\d*'", tkkScript.text).group()
        tkk = re.search("\d*\.\d*", tkkValue01).group()
        if tkk is not None:
            return tkk
        else:
            print("tkk提取错误，请检查程序")
            return None


    def get_tk(self, query):
        tkk = self.getTkkValue()
        tk_value = execjs.compile(
            open(r"./Tkk.js").read()).call(
            'tk', query, tkk)
        return tk_value

    def test(self, text):
        len_text = len(text)
        tk = self.get_tk(text)
        text = urllib.parse.quote(
            text, safe='/', encoding='utf-8', errors=None)
        return tk, text, len_text


    def url(self, text):
        (tk, text, len_text) = self.test(text)
        url = "https://translate.google.cn/translate_tts?ie=UTF-8&q=%s&tl=ja&total=1&idx=0&textlen=%d&tk=%s" \
              "&client=t&prev=input" % (text, len_text, tk)
        return url


    def downloadMedia(self, url, path):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}

            media = requests.get(url, stream=True, headers=headers)

            with open(path, 'ab') as file:
                file.write(media.content)
                file.flush()
        except Exception as e:
            print(e)


    def API(self):
        data = []
        for i in range(1, 10000):
            text = input("请输入你的第%d个短语或单词,输入end结束:" % i)
            if text != "end":
                data.append(text)
                print("第%d个输入保存完毕" % i)
            else:
                print("输入结束")
                break

        nominal_path = input("请输入您的音频保存路径,格式如：C://media")

        for txt in data:
            path = nominal_path + "//%s.mp3" % txt
            url = self.url(txt)
            self.downloadMedia(url, path)
            print("音频%s保存完毕" % txt)
        print("所有的文件均以保存在您的路径中，请查收。晚安，亲爱的。")
