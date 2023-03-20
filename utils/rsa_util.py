import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

utf8 = 'utf-8'


def encrypt_rsa(base64_key, text):
    """
    ras 加密
    :param base64_key: base64 public key
    :param text: 加密文本
    :return:
    """
    pub_key = RSA.import_key(base64.b64decode(base64_key))
    cip_key = PKCS1_v1_5.new(pub_key)
    encrypt_text = base64.b64encode(cip_key.encrypt(text.encode(utf8)))
    return encrypt_text.decode()
