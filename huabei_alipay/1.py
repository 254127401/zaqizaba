from flask import Flask,request,render_template
import time
from alipay import AliPay
from app import getAlipay
from pay import buy_get
app = Flask(__name__)
app_private_key_string = open("rsa_private_key.pem").read()
alipay_public_key_string = open("rsa_public_key.pem").read()
alipay = AliPay(
    appid='201807*****500495', 
    app_notify_url='http://119.17.171.238:8080/',  # 默认回调url
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    sign_type="RSA2", # RSA 或者 RSA2
    debug=False  # 默认False
)
@app.route('/',methods=['POST'])
def hello_world():
	data = request.form.to_dict()
	print(data)
	with open(str(time.time())+".txt",'w+') as f:
		f.write(str(data))
	if request.form.get('status')=='buy':
		return buy_get(request.form.get('buy_num'))
	signature = data.pop("sign")
	success = alipay.verify(data, signature)
	print(success)
	if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
		if request.form.get('trade_status')=='TRADE_SUCCESS':
			buy_id=request.form.get('buyer_id')
			buy_num=request.form.get('receipt_amount')
			print('单号：%s'%buy_id)
			print('金额：%s'%buy_num)
			print(type(buy_num))
			getAlipay(buy_id,float(buy_num)*0.97)

		# getAlipay(request.form.get('buyer_id'),request.form.get('receipt_amount')*0.97)
	return 'success'
@app.route('/',methods=['GET'])
def index():
	return render_template('index.html')
# 	return '''
# 	<head>
# <meta http-equiv="Content-Language" content="zh-CN">
# <meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=gb2312">
# <meta http-equiv="refresh" content="0;url=https://www.baidu.com">
# </head>
#
# 	'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

