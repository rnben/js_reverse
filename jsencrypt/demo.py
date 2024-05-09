import rsa
import base64
import execjs
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

with open("demo.js", "r", encoding="utf-8") as f:
    js = f.read()

ctx = execjs.compile(js)

public_key = ctx.call("get_public_key")
private_key = ctx.call("get_private_key")

# ValueError: RSA key format is not supported
# public_key = """migfma0gcsqgsib3dqebaquaa4gnadcbiqkbgqdloju6tyygqxfwt7eltgdwajtn
# fob9i5xrb6khyfd1yt3yicgqwmnw649887vgjigr/l5i2osbl8c9+wjteucf+s76
# xfxdu6je0nq+z+zedhutoonray5nziu5pgdb0ed/zkbuslkl7eibmxztmludhjm4
# gwqco1krmdsmxsmkdwidaqab"""


def rsa_encrypt(message):
    """校验RSA加密 使用公钥进行加密"""
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(public_key))
    cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
    return cipher_text


def rsa_decrypt(text):
    """校验RSA加密 使用私钥进行解密"""
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(private_key))
    retval = cipher.decrypt(base64.b64decode(text), "ERROR").decode("utf-8")
    return retval


# TODO
def encrypt_rsa(text):
    key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key.encode("utf-8"))
    encMessage = rsa.encrypt(message.encode("utf-8"), key)
    return encMessage


# TODO
def decrypt_rsa(encMessage):
    key = rsa.key.PrivateKey.load_pkcs1(private_key.encode("utf-8"))
    blocksize = rsa.common.byte_size(key.n)
    print(blocksize < len(private_key.encode("utf-8")))  # ???
    decMessage = rsa.decrypt(encMessage.encode("utf-8"), key)
    return decMessage.decode("utf-8")


if __name__ == "__main__":
    message = "hello geeks"

    # js
    encrypted = ctx.call("encrypt", message)
    unencrypted = ctx.call("decrypt", encrypted)
    if unencrypted != message:
        raise Exception("decrypt failed")
    else:
        print("js")

    # python
    if rsa_decrypt(rsa_encrypt(message)) != message:
        raise Exception("decrypt failed")
    else:
        print("python")

    # js == python
    if ctx.call("decrypt", rsa_encrypt(message)) != message:
        raise Exception("decrypt failed")
    else:
        print("js decrypted python")

    # python == js
    if rsa_decrypt(encrypted) != message:
        raise Exception("decrypt failed")
    else:
        print("python decrypted js")

    # TODO
    a = decrypt_rsa(rsa_encrypt(message))
    if a != message:
        raise Exception("decrypt failed")
    else:
        print(decrypt_rsa(rsa_encrypt(message)))
