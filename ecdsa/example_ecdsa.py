from ecdsa import curve, scalar_mult
import random

print(f'Basepoint: {curve.g}')

aliceSecretKey = random.randrange(1, curve.n)
alicePublicKey = scalar_mult(aliceSecretKey, curve.g)

bobSecretKey = random.randrange(1, curve.n)
bobPublicKey = scalar_mult(bobSecretKey, curve.g)

print('------')
print(f"Alice's Secret Key: {aliceSecretKey}")
print(f"Bob's Secret Key: {bobSecretKey}")

print('------')
print(f"Alice's Public Key: {alicePublicKey}")
print(f"Bob's Public Key: {bobPublicKey}")

sharedSecret1 = scalar_mult(aliceSecretKey, bobPublicKey)
sharedSecret2 = scalar_mult(bobSecretKey, alicePublicKey)

print('------')
print(f"Alice's Shared Key: {sharedSecret1}")
print(f"Bob's Shared Key: {sharedSecret2}")

print('------')
print(f"abG: {sharedSecret1[0]}")

resKey = (aliceSecretKey*bobSecretKey) % curve.n
result = scalar_mult(resKey, curve.g)

print(f"abG: {result[0]}")
