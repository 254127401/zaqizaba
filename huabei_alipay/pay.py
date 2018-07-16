from alipay import AliPay
import time,datetime,json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app_private_key_string = open("rsa_private_key.pem").read()
alipay_public_key_string = open("rsa_public_key.pem").read()
def buy_get(num):
    alipay = AliPay(
        appid="2017041*****31115",
        # appid='2018070560500495', # 企业
        app_notify_url='http://119.17.17.238:8080/',  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2", # RSA 或者 RSA2
        debug=False  # 默认False
    )
    result = alipay.api_alipay_trade_precreate(
        out_trade_no=datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        total_amount=num,
        subject="购物",
    )
    print(result)
    if result.get('msg')=='Success' and result.get('code')=='10000':
        data={
            'out_trade_no':result.get('out_trade_no'),
            'qr_code':result.get('qr_code')
        }
        print(json.dumps(data))
        return json.dumps(data)
