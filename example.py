import os
from client import BitcoinClient


RPC_USERNAME = os.getenv('RPC_USERNAME')
RPC_PASSWORD = os.getenv('RPC_PASSWORD')


client = BitcoinClient(RPC_USERNAME, RPC_PASSWORD)
data = client.getblockchaininfo()
print(f"Number of blocks: {data['blocks']}")


print('-----')
txid = '0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2'
data = client.getrawtransaction(txid)

for output in data['vout']:
    print(f"{output['scriptPubKey']['addresses'][0]}: {output['value']}")


print('-----')
block_number = 277316
block_hash = client.getblockhash(block_number)
block = client.getblock(block_hash)

total_value = 0
for transaction in block['tx']:
    tx_data = client.getrawtransaction(transaction)
    for output in tx_data['vout']:
        total_value += output['value']

print(f'Total value in block: {total_value}')
