
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES

key = b"1234567890123456" 
data = b"hogehoge" # 暗号化する文字

# 暗号化処理
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

print(ciphertext)
print(tag)
print(cipher.nonce)

# 復号処理
cipher_dec = AES.new(key, AES.MODE_EAX, cipher.nonce)
dec_data = cipher_dec.decrypt_and_verify(ciphertext, tag)

print(dec_data)