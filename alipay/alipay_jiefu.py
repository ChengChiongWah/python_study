# coding: utf-8
#__author__ = 'william.ru'
#__create__ = '17-1-20'

import datetime
import re
import json
import base64
from httplib import HTTPSConnection, HTTPResponse
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import urllib


class AliPayClient(object):

    ALIPAY_HOST = u"openapi.alipay.com"
    ALIPAY_GATEWAY = u"/gateway.do"

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
        digest = SHA256.new()
        digest.update(data.encode())
        return self._verifier.verify(digest, base64.b64decode(sign))

    def verify_async_signature(self, **kwargs):
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

    def unify_order(self, subject, out_trade_no, total_amount, notify_url,
                    product_code=u"QUICK_MSECURITY_PAY", goods_type=u"0",
                    seller_id=None, body=None,
                    passback_params=None, timeout_express=None, promo_params=None,
                    enable_pay_channels=None, disable_pay_channels=None, store_id=None,
                    sys_service_provider_id=None, need_buyer_real_named=None, trans_memo=None):
        u"""
        生成调用支付宝下单接口的参数
        :param subject: 商品的标题/交易标题/订单标题/订单关键字等。
        :param out_trade_no: 商户网站唯一订单号
        :param int total_amount: 订单总金额，单位为分，整数
        :param seller_id: 收款支付宝用户ID。 如果该值为空，则默认为商户签约账号对应的支付宝用户ID
        :param body: 对一笔交易的具体描述信息。如果是多种商品，请将商品描述字符串累加传给body。
        :param product_code: 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
        :param goods_type: 商品主类型：0—虚拟类商品，1—实物类商品
        :param passback_params: 公用回传参数，如果请求时传递了该参数，则返回给商户时会回传该参数。
                                支付宝会在异步通知时将该参数原样返回。本参数必须进行UrlEncode之后才可以发送给支付宝
        :param timeout_express: 设置未付款支付宝交易的超时时间，一旦超时，该笔交易就会自动被关闭。
                                当用户进入支付宝收银台页面（不包括登录页面），会触发即刻创建支付宝交易，此时开始计时。
                                取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（1c-当天的情况下，无论交易何时创建，都在0点关闭）。
                                该参数数值不接受小数点， 如 1.5h，可转换为 90m。
        :param promo_params: 优惠参数
        :param enable_pay_channels: 可用渠道，用户只能在指定渠道范围内支付 当有多个渠道时用“,”分隔
        :param disable_pay_channels: 禁用渠道，用户不可用指定渠道支付 当有多个渠道时用“,”分隔
        :param store_id: 商户门店编号
        :param sys_service_provider_id: 系统商编号，该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的PID
        :param need_buyer_real_named: 是否发起实名校验 T：发起 F：不发起
        :param trans_memo: 账务备注 该字段显示在离线账单的账务备注中
        :return:
        """
        biz_content = {
            u"subject": subject,
            u"out_trade_no": out_trade_no,
            u"total_amount": u"%.2f" % (total_amount * 0.01),
            u"product_code": product_code,
            u"goods_type": goods_type
        }
        if seller_id:
            biz_content[u"seller_id"] = seller_id
        if body:
            biz_content[u"body"] = body
        if passback_params:
            biz_content[u"passback_params"] = passback_params
        if timeout_express:
            biz_content[u"timeout_express"] = timeout_express
        if promo_params:
            biz_content[u"promo_params"] = promo_params
        if enable_pay_channels:
            biz_content[u"enable_pay_channels"] = enable_pay_channels
        if disable_pay_channels:
            biz_content[u"disable_pay_channels"] = disable_pay_channels
        if store_id:
            biz_content[u"store_id"] = store_id

        extend_params = dict()
        if sys_service_provider_id:
            extend_params[u"sys_service_provider_id"] = sys_service_provider_id
        if need_buyer_real_named:
            extend_params[u"needBuyerRealnamed"] = need_buyer_real_named
        if trans_memo:
            extend_params[u"TRANS_MEMO"] = trans_memo
        if extend_params:
            biz_content[u"extend_params"] = extend_params

        request_arguments = self.__wrap_request_argumets(method=u"alipay.trade.app.pay",
                                            biz_content=biz_content,
                                            notify_url=notify_url)
        return urllib.urlencode(request_arguments)

    def __handle_response(self, response_raw, response_data_key):
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
        url = self.ALIPAY_GATEWAY+u"?" + urllib.urlencode(arguments)

        try:
            http_client.request(method="GET",
                                url=url)
            response = http_client.getresponse()    # type: HTTPResponse
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

    def trade_close(self, callback, out_trade_no=None, trade_no=None, operator_id=None, notify_url=None, app_auth_token=None):
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
