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
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False ,若开启则使用沙盒环境的支付宝公钥
    )
    return alipay
if __name__ == '__main__':
    # result = init_alipay_cfg().api_alipay_trade_precreate(
    #     subject='数据测试',
    #     out_trade_no="20161112",
    #     total_amount=0.01)
    # print('返回值：',result)


    #demo01:
    subject = '测试订单'
    order_string = init_alipay_cfg().api_alipay_trade_page_pay(
        out_trade_no="20161112",
        total_amount=0.01,
        subject=subject,
        return_url="https://example.com",
        notify_url="https://example.com/notify"  # this is optional
    )
    print(order_string)


