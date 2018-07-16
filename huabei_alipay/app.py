from alipay import AliPay
import time,datetime

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app_private_key_string = open("rsa_private_key.pem").read()
alipay_public_key_string = open("rsa_public_key.pem").read()
def getAlipay(payee_account,amount):
    alipay = AliPay(
        appid="2018*******495",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2", # RSA 或者 RSA2
        debug=False  # 默认False
    )
    result = alipay.api_alipay_fund_trans_toaccount_transfer(
        out_biz_no=datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        payee_type="ALIPAY_USERID",
        payee_account=payee_account,
        amount=amount
    )
    print(result)
