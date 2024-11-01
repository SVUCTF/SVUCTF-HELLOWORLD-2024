import base64


def rc4_init(key):
    S = list(range(256))
    j = 0
    key_length = len(key)

    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def rc4_decrypt(data, key):
    S = rc4_init(key)
    i = j = 0
    output = bytearray()

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        K = S[(S[i] + S[j]) % 256]
        output.append(byte ^ K)

    return bytes(output)


if __name__ == "__main__":
    key = b"svuctf"
    encrypted_data_b64 = "cShiGz8rdlXyFRggqjmEyOm4S5dblDTev+C5AM3FlRc="

    encrypted_data = base64.b64decode(encrypted_data_b64)

    decrypted_data = rc4_decrypt(encrypted_data, key)

    print("解密后的数据：", decrypted_data.decode("latin-1"))
