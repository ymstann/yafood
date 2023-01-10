import pya3rt

API_KEY = 'DZZcRRhULAOOTi7Z9sAMxPygDbiZtIyj'  # 自分のAPI KEY

TEXTS = ['システムの企画から開発・運用まで幅広く関われます。',  # ITエンジニア
       'キッチン・ホールをやっていただきます。',  # 飲食
       'キリングループの未来に繋がる医と食をつなぐ事業領域において、競争優位性を担保する探索的研究および健康機能性などに関する基礎から応用までの研究に携わる',
       '商学部の出身でできる仕事',
       '人と関わることが好きな方大歓迎！']  # 介護

def answer(text):
	client = pya3rt.TextClassificationClient(API_KEY)
	result = client.classify(text)
	#print(text+'\n'+str(result['classes'])+'\n')
	msg = "該当する職種は、\n"
	i=1
	for ans in result['classes']:
		msg = msg + str(i)+". "+ans['label']+"  確率("+'{:.1f}'.format(ans['probability'])+")\n"
		i+=1
		if i > 3 :
			break
	
	print(msg)
	return msg
	