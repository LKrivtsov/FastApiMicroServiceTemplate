import hashlib
import base64
import os
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives import hashes


# def verify_password(password, hashed_password):
#     salt = base64.b64decode(hashed_password.split('$')[2])
#     iterations = int(hashed_password.split('$')[1])
#     key = PBKDF2HMAC(
#         algorithm=hashes.SHA256,
#         length=32,
#         salt=salt,
#         iterations=iterations
#     ).derive(password.encode())
#     return base64.b64encode(key).decode() == hashed_password.split('$')[3]


# password = "F1rstB1t"
# hashed_password = "pbkdf2_sha256$12000$zaMBvEoXVx2g$C9juFdXxrMyDDIA8nqYEICOVMtQ03uGJbyA0eDBvrSY="

# if verify_password(password, hashed_password):
#     print("Password is correct")
# else:
#     print("Password is incorrect")

from passlib.hash import django_pbkdf2_sha256
print(django_pbkdf2_sha256.verify("F1rstB1t", "pbkdf2_sha256$12000$wer$ucNHdHiYJp2nsbdWLnERbONMuxiLH46tK8bBmrEDzEw="))
hash = django_pbkdf2_sha256.using(salt="wer", rounds=12000).hash("F1rstB1t")
print(hash)