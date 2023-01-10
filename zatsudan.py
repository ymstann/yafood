# -----------------------------------
# Chaplus APIを用いた雑談応答クラス
# -----------------------------------
import requests # web request
#import pprint
import json
import random

class Zatsudan:
	APIKEY = "5f9267a9e29f8"
	url = f'https://www.chaplus.jp/v1/chat?apikey={APIKEY}'
	headers = {"Content-Type": "application/json"}
	data = {
	    "utterance": "",
	    "username":"",
	    "agentState":{"agentName":"エージェント","tone":"normal", "age":"20歳"},
	#    "addition":{"options":["疲れた","肩凝った"],"utterancePairs":[{"utterance":"肩凝った","response":"適度に運動しないとね"}]}
	    }

	def __init__( self,userName,agentName,age) :
		random.seed()
		self.data["username"] = userName
		self.data["agentState"]["agentName"] = agentName
		self.data["agentState"]["age"] = age

	def henji(self,msg):
		self.data["utterance"] = msg	# チャットユーザーからのメッセージ
		res = requests.post(self.url, headers=self.headers, json=self.data)	# Chaplus APIに応答メッセージを求める
		values = res.text					# APIの応答メッセージを抽出する
		dict_values = json.loads(values)	# APIの応答メッセージ(json形式）をpythonのdictionary形式に変換する
		resp_dict = dict_values['responses']	# 複数の応答メッセージの配列を抽出する
		resp_len = len(resp_dict)				# 応答メッセージの候補の数を得る（配列の数）
#print ("配列の長さ＝",resp_len)
		resp_index = random.randrange(resp_len) # 複数の応答メッセージの中からランダムにメッセージを１つ選ぶ
		respMsg = resp_dict[resp_index]['utterance']
		return respMsg


