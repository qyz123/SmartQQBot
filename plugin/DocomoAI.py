# coding:utf-8
import requests
import json
import logging
import urllib
import urllib2
from textwrap import wrap
from urllib import quote
import urllib2 as request

class DocomoAI:
    def __init__(self):
        self.APIKEY = '796a524d706f676a2e46667636314d6a355a56364b414d4f4367546f345975426954654257613734636f30'
        

    def getAITalk(self, msg):
        try:
            url = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=%s" % self.APIKEY
            payload = {
                "utt": msg.content.replace('@にゃ娘',''),
                # "context": "%s" % msg.from_uin,
                # "user":"%s" % msg.from_uin,
                "nickname": "美里",
                "nickname_y": "ミサト",
                "sex": "女",
                "bloodtype": "A",
                "birthdateY": "1997",
                "birthdateM": "6",
                "birthdateD": "24",
                "age": "16",
                "constellations": "蟹座",
                "place": "東京",
                # "t":"20",
                "mode": "dialog",
            }
            jsondata = json.dumps(payload)
            # logging.debug("DocomoAI payload ="+jsondata)
            r = requests.post(url, data=jsondata)
            result = r.json()['utt']
            logging.debug("DocomoAI:  " + result)
            return result
        except:
            return ""

    def getAIAsk(self,msg):
        msgstring = "%s" % msg.content.replace('@にゃ娘','')
        ######################################################
        if '中日:' in msg.content:
            return self.translate(msgstring.replace('中日:',''),'中日')
        elif '日中:' in msg.content:
            return self.translate(msgstring.replace('日中:',''),'日中')
        ######################################################

        msgstring = urllib2.quote(msgstring.encode("utf-8"))
        url = "https://api.apigw.smt.docomo.ne.jp/knowledgeQA/v1/ask?APIKEY=%s&q=%s" % (self.APIKEY ,msgstring)
        response = urllib2.urlopen(url)
        dataHtml = response.read()
        jsonResult = json.loads(dataHtml)
        resultCode = jsonResult['code']
        if 'S0' in resultCode:
            returnStr = jsonResult['message']['textForDisplay'] + "\n" + jsonResult['answers'][0]['answerText']
            if jsonResult['answers'][0]['linkText'] != "":
                returnStr+="\n参考リンク：%s \n(%s)" % (jsonResult['answers'][0]['linkText'],jsonResult['answers'][0]['linkUrl'])
            return returnStr
        else:
            return self.getAITalk(msg)

        return  ""
     

    def translate(self, source,lafromto):
        logging.debug("translate %s" % lafromto) 
        if lafromto=='中日':
            self.from_lang='zh'
            self.to_lang='ja'
        elif lafromto=='日中':
            self.from_lang='ja'
            self.to_lang='zh'
        else:
            return source

        self.source_list = wrap(source, 1000, replace_whitespace=False)
        return ' '.join(self._get_translation_from_google(s) for s in self.source_list)

    def _get_translation_from_google(self, source):
        json5 = self._get_json5_from_google(source)
        data = json.loads(json5)
        translation = data['responseData']['translatedText']
        if not isinstance(translation, bool):
            return translation
        else:
            matches = data['matches']
            for match in matches:
                if not isinstance(match['translation'], bool):
                    next_best_match = match['translation']
                    break
            return next_best_match

    def _get_json5_from_google(self, source):
        escaped_source = quote(source.encode("utf-8"))
        headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                   (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        api_url = "http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s"
        req = request.Request(url=api_url % (escaped_source, self.from_lang, self.to_lang),
                              headers=headers)
        r = request.urlopen(req)
        return r.read().decode('utf-8')
