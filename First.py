import time
import hmac
import hashlib

def generate_totp(email):
    secret = (email + "HENNGECHALLENGE004").encode()

    counter = int(time.time()) // 30
    counter_bytes = counter.to_bytes(8, "big")

    digest = hmac.new(secret, counter_bytes, hashlib.sha512).digest()

    offset = digest[-1] & 0x0F
    binary = (
        ((digest[offset] & 0x7F) << 24)
        | (digest[offset + 1] << 16)
        | (digest[offset + 2] << 8)
        | digest[offset + 3]
    )

    otp = binary % (10 ** 10)
    return str(otp).zfill(10)

print(generate_totp("sajjatulsunny@gmail.com"))