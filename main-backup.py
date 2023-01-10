# coding=utf-8
# インポートするライブラリ
from flask import Flask, request, abort, render_template, g,jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage,
    ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, FlexSendMessage, PostbackAction,
    MessageAction, URIAction, QuickReplyButton, QuickReply
)


from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
from flask_sqlalchemy import SQLAlchemy

import os
import psycopg2
#import sys
import json
import pya3rt # リクルートの文書を分類するAIのライブラリ（無料）初期値では、求人票の文章から職種を判定する
import testjson
import aians
import zatsudan

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #jason dump defaultの英文字設定をやめて、日本語表示可とする
zd = zatsudan.Zatsudan("函大花子","函大花子","19歳")

# 環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
# 環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/", methods=['GET'])
def index():
	moji = u"こんにちは、ビ研です"

	return render_template("index.html",moji=moji)

@app.route("/test", methods=['POST'])
def test():
	moji = u"こんにちは"
	if request.method == 'GET':
		msg1 = request.args.get('msg1')
		msg2 = request.args.get('msg2')
	elif request.method == 'POST':
		msg1 = request.form['msg1']
		msg2 = request.form['msg2']
		suji1 = int(msg1)
		suji2 = int(msg2)
		kotae = suji1 + suji2

	return render_template("test.html",moji1=msg1,moji2=msg2,kotae=kotae)

@app.route("/read_db", methods=['GET'])
def read_db():
	dsn = os.environ.get('DATABASE_URL')
	conn = psycopg2.connect(dsn)
	cur = conn.cursor()

# データを取得する
	cur.execute('SELECT * FROM studenttbl')
#レコード数を知る方法 これでよいのか？
	record_max = cur.rowcount
#	c_one=cur.fetchone()
	app.logger.debug(type(cur))
	
	res = {}
#	msg = c_one[2]
	msg = ""
	for i in cur:

		msg = msg + "<tr><td>"+str(i[1])+"</td><td>"+i[2]+"</td></tr>"

	kotae = msg
	return render_template("testdb.html",kotae=kotae)
#	return jsonify(res)

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	line_bot_api.reply_message(
        event.reply_token,
#        TextSendMessage(text=u"「" + event.message.text + u"」って何？AAAA")
#       TextSendMessage(text=zd.henji(event.message.text))
        henji(event.message.text),qRepBtn()
	)
#	print(event)
#	print(event.source)
#	print(type(event))
#	print(type(event.source))
#	print(event.source.user_id)

def henji(msg):
	JsMsg=[]
#	f = open("temp.json", "r")
#	f = open("quickrep.json", "r")

#	JsonMsg = json.load(f)
	"""
	if u"ポチ" in msg :
		henjiMsg = u"わんわん"
	elif u"タマ" in msg :
		henjiMsg = u"ニャーニャー"
	else:
		henjiMsg = u"分かりません"
	"""
	#print(ev, file=sys.stderr)
	#henjiMsg=jsonify(ev)
	#henjiMsg=ev
	#new_from_json_dictメソッドはJSONデータをFlexMessage等各種オブジェクトに変換してくれるメソッドです
	#FlexSendMessage.new_from_json_dict(対象のJSONデータ）とすることで、
	#FlexSendMessage型に変換されます
	#container_obj = FlexSendMessage.new_from_json_dict(JsonMsg)

#	JsMsg = TemplateSendMessage(testjson.jsonMsg)

	#最後に、push_messageメソッドを使ってPUSH送信する
	#line_bot_api.push_message(event.source.userId, messages=container_obj)
	#print(userId)
	#	line_bot_api.push_message(event.source.userId, messages=TemplateSendMessage(container_obj))

	"""	
	moji = TemplateSendMessage(
	alt_text='Buttons template',
	template=ButtonsTemplate(
		thumbnail_image_url='https://example.com/image.jpg',
			title='Menu',
			text='Please select',
			actions=[
				PostbackAction(
					label='postback',
					display_text='postback text',
					data='action=buy&itemid=1'
				),
				MessageAction(
					label='message',
					text='message text'
				),
				URIAction(
					label='uri',
					uri='http://example.com/'
				)
			]
		)
	)
	"""
	
	"""
	jsonmoji = {
	  "type": "template",
	  "altText": "ボタン型テンプレートの練習",
	  "template": {
	    "type": "buttons",
	    "actions": [
	      {
	        "type": "uri",
	        "label": "参考になった",
	        "uri": "https://tsugabot.herokuapp.com/"
	      },
	      {
	        "type": "uri",
	        "label": "知っていることだった",
	        "uri": "https://liff.line.me/1654153400-yv5lR1Da"
	      },
	      {
	        "type": "uri",
	        "label": "質問内容と違う回答",
	        "uri": "https://liff.line.me/1654153400-yv5lR1Da"
	      }
	    ],
#	    "thumbnailImageUrl": "https://tsugabot.herokuapp.com/static/images/b-ken.png",
	    "title": "回答の評価",
	    "text": "回答について以下の評価ボタンをタップしてください。。"
	  }
	}
	"""



#	container_obj = TemplateSendMessage.new_from_json_dict(jsonmoji)
#	henjiMsg = henjiMsg  + "\n" + msg + "\n" + "\n１．アットホームな大学で、教職員と学生が仲良しです。\n２．先輩とも仲良くなれるのが楽しいです。\n３．海外プロジェクトに参加すると海外の友達もできます"
#	henjiMsg = aians.answer(msg)



	hmsg = TextSendMessage(text=henjiMsg)


#	return (hmsg,container_obj)
	return hmsg
#	return JsMsg
#	return henjiMsg

# ---------------------------------------
# QuickReplyButton テスト関数
# ---------------------------------------

def qRepBtn():
	
    language_list = ["Ruby", "Python", "PHP", "Java", "C"]

    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}が好き")) for language in language_list]

    msg = TextSendMessage(text="どの言語が好きですか？",quick_reply=QuickReply(items=items))

    return msg

# ----------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port,debug=True)
