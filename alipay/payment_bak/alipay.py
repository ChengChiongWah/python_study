# coding: utf-8

import datetime
import re
import json
import base64
# from httplib import HTTPSConnection, HTTPResponse
from http.client import HTTPSConnection, HTTPResponse
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from config import Settings
import urllib


class AliPayClient(object):
    ALIPAY_HOST = u"openapi.alipay.com"
    ALIPAY_GATEWAY = u"/gateway.do"
    _GATEWAY = u'https://openapi.alipay.com/gateway.do'

    def __init__(self, appid,
                 sign_key=None, sign_key_file_path=None,
                 verify_key=None, verify_key_file_path=None):
        self.appid = appid
        # 商户私钥
        assert sign_key or sign_key_file_path
        if sign_key:
            sign_key = RSA.importKey(sign_key)
        else:
            with open(sign_key_file_path) as f:
                sign_key = RSA.importKey(f.read())
        self._signer = Signature_pkcs1_v1_5.new(sign_key)
        # 支付宝公钥
        assert verify_key or verify_key_file_path
        if verify_key:
            verify_key = RSA.importKey(verify_key)
        else:
            with open(verify_key_file_path) as f:
                verify_key = RSA.importKey(f.read())
        self._verifier = Signature_pkcs1_v1_5.new(verify_key)

    def __wrap_request_argumets(self, method, biz_content, notify_url=None, app_auth_token=None):
        """添加公共请求参数并生成签名"""
        date = datetime.datetime.now()
        if not isinstance(biz_content, str):
            biz_content = json.dumps(biz_content)
        args = {
            u"app_id": self.appid,
            u"method": method,
            u"charset": u"utf-8",
            u"sign_type": u"RSA2",
            u"sign": None,
            u"timestamp": unicode(date.strftime(u"%Y-%m-%d %H:%M:%S")),
            u"version": u"1.0",
            u"biz_content": biz_content,
        }
        if notify_url:
            args[u"notify_url"] = notify_url
        if app_auth_token:
            args[u"app_auth_token"] = app_auth_token
        args[u"sign"] = self.get_ras2_signature(**args)
        return args

    def get_ras2_signature(self, **kwargs):
        arguments = [(key, val) for (key, val) in kwargs.items() if val and key != u"sign"]
        arguments.sort(key=lambda p: p[0])
        data = u""
        for (key, val) in arguments:
            data += key + u"=" + val + u"&"
        data = data[:-1]
        digest = SHA256.new()
        digest.update(data.encode())
        sign = self._signer.sign(digest)
        signature = base64.b64encode(sign)
        return signature.decode()

    def __verify_ras2_signature(self, data, sign):
        '''认证RAS签名'''
        digest = SHA256.new()
        digest.update(data.encode())
        return self._verifier.verify(digest, base64.b64decode(sign))

    def verify_async_signature(self, **kwargs):
        '''异步签名认证'''
        sign = kwargs[u"sign"]
        if isinstance(sign, str):
            sign = sign.encode()
        arguments = [(key, val) for (key, val) in kwargs.items() if val and key != u"sign" and key != u"sign_type"]
        arguments.sort(key=lambda p: p[0])
        data = u""
        for (key, val) in arguments:
            data += key + u"=" + val + u"&"
        data = data[:-1]
        return self.__verify_ras2_signature(data, sign)

    def create_direct_pay_by_user(tn, subject, body, total_fee):
        params = {}
        params['service'] = 'jie_fu_capital_payment'  # 接口名称
        params['payment_type'] = '1'  # 支付类型。默认值为：1（商品购买）。

        # 获取配置文件
        params['seller_id'] = Settings.ALIPAY_SELLER_ID  # 卖家支付宝账号 卖家支付宝账号（邮箱或手机号码格式）或其对应的支付宝唯一用户号（以2088开头的纯16位数字）。
        params['partner'] = Settings.ALIPAY_PARTNER  # 合作者身份ID,签约的支付宝账号对应的支付宝唯一用户号。以2088开头的16位纯数字组成。
        params['notify_url'] = Settings.ALIPAY_NOTIFY_URL  # 服务器异步通知页面路径, 支付宝服务器主动通知商户网站里指定的页面http路径。
        params['_input_charset'] = Settings.ALIPAY_INPUT_CHARSET  # 参数编码字符集,  商户网站使用的编码格式，固定为UTF-8。

        # 从订单数据中动态获取到的必填参数
        params['out_trade_no'] = tn  # 商户网站唯一订单号 支付宝合作商户网站唯一订单号。
        params['subject'] = subject  # 商品名称 商品的标题/交易标题/订单标题/订单关键字等。该参数最长为128个汉字。
        params['body'] = body  # 商品详情 对一笔交易的具体描述信息。如果是多种商品，请将商品描述字符串累加传给body。
        params['total_fee'] = total_fee  # 总金额 该笔订单的资金总额，单位为RMB-Yuan。取值范围为[0.01，100000000.00]，精确到小数点后两位。

        # params, prestr = params_filter(params)

        #       params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE) # 签名
        params['sign'] = self.get_ras2_signature(params)  # 签名
        params['sign_type'] = Settings.ALIPAY_SIGN_TYPE  # 签名方式 签名类型，目前仅支持RSA。

        return _GATEWAY + urlencode(params)

    def __handle_response(self, response_raw, response_data_key):
        '''处理响应'''
        patter = u"\"%s\"\\s*[:]\\s*([{].*[}])[,]\"sign\"\\s*[:]\\s*\"(.*)\"" % response_data_key
        matchobject = re.search(patter, response_raw)
        data = matchobject.group(1)
        sign = matchobject.group(2)
        if not self.__verify_ras2_signature(data, sign):
            return None, u"verifySignatureError"
        response = json.loads(data)
        if response[u"code"] != u"10000":
            return None, response[u"sub_code"]
        else:
            return response, None

    def __send_request(self, arguments, callback, response_data_key):
        http_client = HTTPSConnection(host=self.ALIPAY_HOST)
        url = self.ALIPAY_GATEWAY + u"?" + urllib.urlencode(arguments)

        try:
            http_client.request(method="GET",
                                url=url)
            response = http_client.getresponse()  # type: HTTPResponse
            if int(response.status) / 100 != 2:
                callback(None, error=response.status)
            else:
                response_raw = response.read().decode()
                response_body, error = self.__handle_response(response_raw, response_data_key)
                callback(response_body, error)
        except:
            callback(None, error="connectionError")
        finally:
            http_client.close()
        pass



    def trade_query(self, callback, out_trade_no=None, trade_no=None, app_auth_token=None):
        '''交易查询'''
        assert out_trade_no or trade_no
        biz_content = dict()
        if out_trade_no:
            biz_content[u"out_trade_no"] = out_trade_no
        if trade_no:
            biz_content[u"trade_no"] = trade_no
        arguments = self.__wrap_request_argumets(method=u"alipay.trade.query",
                                                 biz_content=biz_content,
                                                 app_auth_token=app_auth_token)
        self.__send_request(arguments=arguments,
                            callback=callback,
                            response_data_key=u"alipay_trade_query_response")

    def trade_close(self, callback, out_trade_no=None, trade_no=None, operator_id=None, notify_url=None,
                    app_auth_token=None):
        '''交易关闭'''
        assert out_trade_no or trade_no
        biz_content = dict()
        if out_trade_no:
            biz_content[u"out_trade_no"] = out_trade_no
        if trade_no:
            biz_content[u"trade_no"] = trade_no
        if operator_id:
            biz_content[u"operator_id"] = operator_id
        arguments = self.__wrap_request_argumets(method=u"alipay.trade.close",
                                                 biz_content=biz_content,
                                                 app_auth_token=app_auth_token,
                                                 notify_url=notify_url)
        self.__send_request(arguments=arguments,
                            callback=callback,
                            response_data_key=u"alipay_trade_close_response")

    def trade_refund(self, callback, refund_amount,
                     out_trade_no=None, trade_no=None,
                     refund_reason=None, out_request_no=None,
                     operator_id=None, store_id=None,
                     terminal_id=None, app_auth_token=None):
        '''交易退款'''
        assert out_trade_no or trade_no
        biz_content = {
            u"refund_amount": u"%.2f" % (refund_amount * 0.01)
        }
        if out_trade_no:
            biz_content[u"out_trade_no"] = out_trade_no
        if trade_no:
            biz_content[u"trade_no"] = trade_no
        if refund_reason:
            biz_content[u"refund_reason"] = refund_reason
        if out_request_no:
            biz_content[u"out_request_no"] = out_request_no
        if operator_id:
            biz_content[u"operator_id"] = operator_id
        if store_id:
            biz_content[u"store_id"] = store_id
        if terminal_id:
            biz_content[u"terminal_id"] = terminal_id
        arguments = self.__wrap_request_argumets(method=u"alipay.trade.refund",
                                                 biz_content=biz_content,
                                                 app_auth_token=app_auth_token)
        self.__send_request(arguments=arguments,
                            callback=callback,
                            response_data_key=u"alipay_trade_refund_response")

    def trade_refund_query(self, callback, out_request_no, out_trade_no=None, trade_no=None, app_auth_token=None):
        '''交易退款查询'''
        assert out_trade_no or trade_no
        biz_content = {
            u"out_request_no": out_request_no
        }
        if out_trade_no:
            biz_content[u"out_trade_no"] = out_trade_no
        if trade_no:
            biz_content[u"trade_no"] = trade_no
        arguments = self.__wrap_request_argumets(method=u"alipay.trade.fastpay.refund.query",
                                                 biz_content=biz_content,
                                                 app_auth_token=app_auth_token)
        self.__send_request(arguments=arguments,
                            callback=callback,
                            response_data_key=u"alipay_trade_fastpay_refund_query_response")

    def bill_downloadurl_query(self, callback, bill_type, bill_date, app_auth_token=None):
        biz_content = {
            u"bill_type": bill_type,
            u"bill_date": bill_date
        }
        arguments = self.__wrap_request_argumets(method=u"alipay.data.dataservice.bill.downloadurl.query",
                                                 biz_content=biz_content,
                                                 app_auth_token=app_auth_token)
        self.__send_request(arguments=arguments,
                            callback=callback,
                            response_data_key=u"alipay_data_dataservice_bill_downloadurl_query_response")

# if __name__ == "__main__":
#     client = AliPayClient(appid=ALIPAY_APPID, key_file_path=ALIPAY_KEYFILE)
#     # print(client.test())
#     # client.test()
