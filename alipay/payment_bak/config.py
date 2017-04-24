import os


class Settings(object):
    ALIPAY_SELLER_ID = u'dong@biaojiepay.com'
    ALIPAY_PARTNER = u'2088521336283795'
    ALIPAY_NOTIFY_URL = u'http://jiefucapital.com/payment_notify_url'
    ALIPAY_INPUT_CHARSET = u'UTF-8'
    ALIPAY_SIGN_TYPE = u'RSA2'
    PAYMENT_APPID = '2088521336283795'
    PAYMENT_SIGN_KEY_FILE_PATH = os.getcwd() + '/app/payment/secrect_key_2048.txt'  # 私钥路径
    PAYMENT_VERIFY_KEY_FILE_PATH = os.getcwd() + 'app/payment/alipay_public_key_sha256.txt'  # 淘宝公钥
