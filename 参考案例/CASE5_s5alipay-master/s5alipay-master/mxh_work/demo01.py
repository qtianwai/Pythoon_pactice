from alipay import AliPay
import time, qrcode

alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlSZ2oiSjigITaRW84blcA2uXxy+dSYtwqE+aoO4ng39SK+j/AKJ2qVt1vTAJNbqgIPq7rnFxMhgdUkY824RawrMmuVjAVij2jORFkMAP1mxc0xsMZRXmgb/uXcLJIp63OCJ7kkxD5MhWs2McfU2OebjSlRLlzIMXpCdJO7+cZ3ZCnmz/rDnr46t2G6SDy8osznmsRqY/3ap7oVEvjsM6vHwYvd9wm25B3dYclYrmmBFkjhPb6b8apogI2VIKV/WMLrcGgfPRgbJVj3wYja/CYU8Vn68ZXCRyKgOiHNQSz5YwCWfrmtWSFBvBgLqUXV9bQQVPBhHf3pLHQ8/q3gG0bQIDAQAB
-----END PUBLIC KEY-----'''

app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCH1egfWWeTfzVpty7RQSYtKIzQ9Z7pk42RvMlgqNgnw7BHu4HUjrfgRLSLqSQFip/Nr+oL9A+CBRm0EI2aAu0cWh6hulbyYaI3/8Ap/SXB2Arez96bzlVUnYb9q13kPkQHURRdbPDOEYC8+OYrUgdB1CrjwHADLtzvWmlIRzw5wFUxF/hIZUizo6FfPlIAf/ZWhS1ngq8HnCFN/hd8qWTMlnDebcwZd3Q44BGCFaMu5CRpBGkR7ZWywS9fFYJcdxznTBt3ukBh2Hu0Bmra5KNqUU769K1esI/enCoQC8jTU6f+mZCrTfivxLMCaJFQDMPEuzhmpFsPb3+JRoA/8LvPAgMBAAECggEABi7HVP31x/HnVXuABwhHG5EX777uT8VmkTadl+e3hv/SO0GepDUmy291JFI7kIEByxPxvD+MoSdoRxjlyRfPARZdBJF9uaSWBKSAc6jRGiSiQggGIuNeYO6WoV82c9gdspOPML1vrIGBcZiGqXwfVnC4zwsITizI46Ai4KZVaG92jv57rkg56+xhUlMxe+C2KFEPPJgxHDefNxNNjdGS5+LB5gLwNJxJYOD0JAxruAThoddyiGsbEOVJuOVjYYwD14YjUsxYyMZaTWHJG8I5G8WKf1crnojbhdO1yxToLiu1mYbXIy7xzfcuHcImsevQ6a6WhCpZVwciG316qOxp6QKBgQDVtLReFbdA9fVUhJMPA4dlQhX7v3bZrtMY7LprpfoMPJe9IfdmODCoBL/5zlRzhEeZGy5fE+YhrxCuSEsivTEK0aiivKGaZFb0kABAVwnLUfRv8nUDBekWUlnr3MsEhxVNv0s+7wsmlkxxFw3TDxTwVor+cgxNlQ9WIHIKzMIcHQKBgQCit/G/YMXe4MFUxl8R+qMWWvWgOMmFJ/oVn0R5taInQzcap11n5H7WvsgKOnF6zoS3WnHa+YL97Syh2zjirKCprnwt5s6JOvDqSQE7dexy1BSWhpikc1elmbZjuKR3e4ompkByAGUQU5IrAsKhwWVujLJ7zN77bG6nVtfg8og72wKBgFhdlzNMMXE4AtCG3TQZFnRFRkfJnMBYLMuin1cB04oZx/iZwe3PkDb5d9Q4f+0gJmbluV/xH3iQJgqatA7SQiQiG2PnMb9gfCA2JxRzqQYchkF/9OhiGkZzmOERdBUUMjfqwJduSqMTBNrCWKIMG3Fhp6mcyP+Pgj7vvZg/oIf1AoGAJLlNFzs5DTc+iuqGdGFTw2zd+L44RRQjrhOW+b0TjrbtzdcuDo+UTNUcAqr0B5pqe5MvFROxC6wmoZT/frElRYZ6wkVQIcqqqsW1QH050ySoTNytwJfDlT1e25zFia3ZHSXyb4hFRu0FlS13Tdh/EvcwJR60yJvNUXkZGczDEHcCgYB9ShRXBSXW9gLyTb6otvpgStjTJk/16xMt4/oMPE6AZozKqS4RxBvBKskrec99Fy0IReFTRzY9La5OrqVGXtpXj1ZxTBRvmOp29aRFQcmDMcNRZygi5UuF6NCIvB4h+TqgfjpBN9E9+1DW68xIQDXbLSmckVVwiAHxR1D10A2oOA==
-----END RSA PRIVATE KEY-----'''

# 注意：一个是支付宝公钥，一个是应用私钥

APP_ID = '2016100100635842'
NOTIFY_URL = "https://your_domain/alipay_callback"


def init_alipay_cfg():
    '''
    初始化alipay配置
    :return: alipay 对象
    '''
    alipay = AliPay(
        appid=APP_ID,
        app_notify_url=NOTIFY_URL,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False ,若开启则使用沙盒环境的支付宝公钥
    )
    return alipay


def get_qr_code(code_url):
    '''
    生成二维码
    :return None
    '''
    # print(code_url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data(code_url)  # 二维码所含信息
    img = qr.make_image()  # 生成二维码图片
    img.save(r'.\qr_test_ali.png')
    print('二维码保存成功！')


def preCreateOrder(subject: 'order_desc', out_trade_no: int, total_amount: (float, 'eg:0.01')):
    '''
    创建预付订单
    :return None：表示预付订单创建失败  [或]  code_url：二维码url
    '''
    result = init_alipay_cfg().api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount)
    print('返回值：', result)
    code_url = result.get('qr_code')
    if not code_url:
        print(result.get('预付订单创建失败：', 'msg'))
        return
    else:
        get_qr_code(code_url)
        # return code_url


def query_order(out_trade_no: int, cancel_time: int and 'secs'):
    '''
    :param out_trade_no: 商户订单号
    :return: None
    '''
    print('预付订单已创建,请在%s秒内扫码支付,过期订单将被取消！' % cancel_time)
    # check order status
    _time = 0
    for i in range(10):
        # check every 3s, and 10 times in all

        print("now sleep 2s")
        time.sleep(2)

        result = init_alipay_cfg().api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            print('订单已支付!')
            print('订单查询返回值：', result)
            break

        _time += 2
        if _time >= cancel_time:
            cancel_order(out_trade_no, cancel_time)
            return


def cancel_order(out_trade_no: int, cancel_time=None):
    '''
    撤销订单
    :param out_trade_no:
    :param cancel_time: 撤销前的等待时间(若未支付)，撤销后在商家中心-交易下的交易状态显示为"关闭"
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_cancel(out_trade_no=out_trade_no)
    # print('取消订单返回值：', result)
    resp_state = result.get('msg')
    action = result.get('action')
    if resp_state == 'Success':
        if action == 'close':
            if cancel_time:
                print("%s秒内未支付订单，订单已被取消！" % cancel_time)
        elif action == 'refund':
            print('该笔交易目前状态为：', action)

        return action

    else:
        print('请求失败：', resp_state)
        return


def need_refund(out_trade_no: str or int, refund_amount: int or float, out_request_no: str):
    '''
    退款操作
    :param out_trade_no: 商户订单号
    :param refund_amount: 退款金额，小于等于订单金额
    :param out_request_no: 商户自定义参数，用来标识该次退款请求的唯一性,可使用 out_trade_no_退款金额*100 的构造方式
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_refund(out_trade_no=out_trade_no,
                                                       refund_amount=refund_amount,
                                                       out_request_no=out_request_no)

    if result["code"] == "10000":
        return result  # 接口调用成功则返回result
    else:
        return result["msg"]  # 接口调用失败则返回原因


def refund_query(out_request_no: str, out_trade_no: str or int):
    '''
    退款查询：同一笔交易可能有多次退款操作（每次退一部分）
    :param out_request_no: 商户自定义的单次退款请求标识符
    :param out_trade_no: 商户订单号
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_fastpay_refund_query(out_request_no, out_trade_no=out_trade_no)

    if result["code"] == "10000":
        return result  # 接口调用成功则返回result
    else:
        return result["msg"]  # 接口调用失败则返回原因


if __name__ == '__main__':
    # cancel_order(1527212120)
    # subject = "话费余额充值"
    # out_trade_no = int(time.time())
    # total_amount = 0.01
    # preCreateOrder(subject, out_trade_no, total_amount)
    #
    # query_order(out_trade_no, 40)
    #
    # print('5s后订单自动退款')
    # time.sleep(5)
    # print(need_refund(out_trade_no, 0.01, 111))
    #
    # print('5s后查询退款')
    # time.sleep(5)
    # print(refund_query(out_request_no=111, out_trade_no=out_trade_no))
    # 操作完登录 https://authsu18.alipay.com/login/index.htm中的对账中心查看是否有一笔交易生成并退款
    preCreateOrder('maxiaohui',33333,0.1)