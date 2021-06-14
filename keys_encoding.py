import base58
from hashlib import sha256


def verify_checksum(payload, checksum):
    """
    Verifies the checksum of a payload
    """
    calc_checksum = sha256(sha256(bytes.fromhex(payload)).digest()).hexdigest()
    return checksum == calc_checksum[:8]


def wif_to_ec(wif):
    """
    Returns all the components of WIF (Wallet Import Format)
    """
    data = base58.b58decode(wif).hex()
    ver_payload, checksum = data[:-8], data[-8:]

    assert verify_checksum(ver_payload, checksum)
    version, payload = int(ver_payload[:2], 16), ver_payload[2:]
    return version, payload, checksum


def ec_to_wif(ec, version):
    """
    Returns the WIF from the key and the version
    """
    payload = f'{int(version):x}{ec}'
    checksum = sha256(sha256(bytes.fromhex(payload)).digest()).hexdigest()[:8]
    payload += checksum
    print(payload)
    wif = base58.b58encode(bytes.fromhex(payload))
    return wif

print("Decode WIF")
version, key, checksum = wif_to_ec('5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn')
print(f"version: {version}")
print(f"key: {key}")
print(f"checksum: {checksum}")

print("-"*10)
print("Decode Compressed WIF")
version, key, checksum = wif_to_ec('KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ')
print(f"version: {version}")
print(f"key: {key}")
print(f"checksum: {checksum}")


print('-'*10)
print('Encode hex to WIF')
wif = ec_to_wif('1e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd', version=128)
print(f'wif: {wif}')

print('Encode from hex (Compressed Key) to WIF')
wif = ec_to_wif('1e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd01', version=128)
print(f'wif: {wif}')

