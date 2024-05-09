import execjs
import requests

def productListVip():
    r =requests.post("https://vipapi.qimingpian.cn/DataList/productListVip")
    r.raise_for_status()
    encrypt_data = r.json().get("encrypt_data")

    with open('decode.js', 'r', encoding='utf-8') as f:
        js = f.read()

    ctx = execjs.compile(js)
    result = ctx.call('my_decode', encrypt_data)
    return result

if __name__ == '__main__':
    data = productListVip()
    print(data)

