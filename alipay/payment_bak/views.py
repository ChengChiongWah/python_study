# coding: utf-8

from . import payment
from .alipay import AliPayClient
from .config import Settings
import os
from flask import render_template, redirect, request


@payment.route('/payment_submit', methods=['GET'])
def payment_submit():
    return render_template('payment_submit.html')


@payment.route('/payment_require_handle', methods=['GET', 'POST'])
def payment_require_handle():
    payment_appid = Settings.PAYMENT_APPID
    payment_sign_key_file_path = Settings.PAYMENT_SIGN_KEY_FILE_PATH  # 私钥路径
    payment_verify_key_file_path = Settings.PAYMENT_VERIFY_KEY_FILE_PATH  # 淘宝公钥
    payment_alipay_order = AliPayClient(appid=payment_appid, sign_key_file_path=payment_sign_key_file_path,
                                        verify_key_file_path=payment_verify_key_file_path)
    tn = '001'
    subject = 'test'
    body = 'test pay'
    total_fee = 0.01
    payment_require_url = payment_alipay_order.create_direct_pay_by_user(tn, subject, body, total_fee)
    return redirect(payment_require__url)


@payment.route('/payment_notify_url')
def payment_notify_url_handler(request):
    """
    Handler for notify_url for asynchronous updating billing information.
    Logging the information.
    """
    payment_appid = Settings.PAYMENT_APPID
    payment_sign_key_file_path = Settings.PAYMENT_SIGN_KEY_FILE_PATH
    payment_verify_key_file_path = Settings.PAYMENT_VERIFY_KEY_FILE_PATH
    payment_alipay_notify = AliPayClient(appid=payment_appid, sign_key_file_path=payment_sign_key_file_path,
                                      verify_key_file_path=payment_verify_key_file_path)
    if request.method == 'POST':
        if payment_alipay_notify.verify_async_signature(request.POST):
            # logger1.info('pass verification...')
            tn = request.POST.get('out_trade_no')
            # logger1.info('Change the status of bill %s' % tn)
            bill = Bill.objects.get(pk=tn)
            trade_status = request.POST.get('trade_status')
            # logger1.info('the status of bill %s changed to %s' % (tn, trade_status))
            bill.trade_status = trade_status
            bill.save()
            trade_no = request.POST.get('trade_no')
            if trade_status == 'TRADE_SUCCESS':
                # logger1.info('It is WAIT_SELLER_SEND_GOODS, so upgrade bill')
                # upgrade_bill(bill, 6 * 30 + 7)
                # url = send_goods_confirm_by_platform(trade_no)
                # logger1.info('send goods confirmation. %s' % url)
                # req = urllib.urlopen(url)
                return "success"
    return "fail"


def return_url_handler(request):
  """
  Handler for synchronous updating billing information.
  """
  # logger1.info('>> return url handler start')
  payment_appid = Settings.PAYMENT_APPID
  payment_sign_key_file_path = Settings.PAYMENT_SIGN_KEY_FILE_PATH
  payment_verify_key_file_path = Settings.PAYMENT_VERIFY_KEY_FILE_PATH
  payment_alipay_return = AliPayClient(appid=payment_appid, sign_key_file_path=payment_sign_key_file_path,
                                       verify_key_file_path=payment_verify_key_file_path)
  if payment_alipay_notify.verify_async_signature(request.GET):
    tn = request.GET.get('out_trade_no')
    trade_no = request.GET.get('trade_no')
    # logger1.info('Change the status of bill %s'%tn)
    # bill = Bill.objects.get (pk=tn)
    trade_status = request.GET.get('trade_status')
    # logger1.info('the status changed to %s'%trade_status)
    bill.trade_status = trade_status
    # upgrade_bill (bill, 30*6+7)
    url=send_goods_confirm_by_platform (trade_no)
    req=urllib.urlopen (url)
    # logger1.info('send goods confirmation. %s'%url)
    return 'payment_success'
  return 'payment_error'

