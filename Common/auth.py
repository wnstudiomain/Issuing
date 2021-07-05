class Auth:
    @staticmethod
    def encode(value):
        val = value.encode('cp037')
        return binascii.hexlify(val).decode('utf-8')


def encode_ebcdic(text):
    return text.decode('utf-8').encode('cp037')


def str_to_bcd(text):
    return bytes(str).decode('hex')


def str_to_binary(str):
    return int(str, 16)


def str_to_bcd(str):
    return bytes(str, encoding='utf8').decode('utf-8').encode('cp037')


import binascii


def bin2hex(str1):
    bytes_str = bytes(str1, 'utf-8')
    return binascii.hexlify(bytes_str)


a = "\xf4\xf7\xf8\xf5\xf6\xf7\xf3\xf3\xf2\xf8\xf1\xf5"
c = bin2hex(a)

print(c)
print(str_to_bcd('478567332815'))

print(Auth.encode('478567332815'))
