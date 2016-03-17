# coding:utf-8
import requests
import json
import logging
import urllib
import urllib2

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
        #q=urllib.urlencode(msgstring.encode('utf8'))
        msgstring = urllib2.quote(msgstring.encode("utf-8"))
        url = "https://api.apigw.smt.docomo.ne.jp/knowledgeQA/v1/ask?APIKEY=%s&q=%s" % (self.APIKEY ,msgstring)
        #logging.debug("getAIAsk Url: " + url)
        # jsondata = requests.get(url);
        response = urllib2.urlopen(url)
        dataHtml = response.read()
        jsonResult = json.loads(dataHtml)
        # jsonResult = json.loads(dataHtml)['results'][0]
        resultCode = jsonResult['code']
        if 'S0' in resultCode:
            returnStr =jsonResult['message']['textForDisplay'] + "\n" + jsonResult['answers'][0]['answerText']
            if jsonResult['answers'][0]['linkText']!="":
                returnStr+="\n参考リンク：%s \n(%s)"%(jsonResult['answers'][0]['linkText'],jsonResult['answers'][0]['linkUrl'])
            return returnStr
            #logging.debug("getAIAsk: " +
            #jsonResult['message']['textForDisplay'])
        else:
            return self.getAITalk(msg)

        return  ""
     