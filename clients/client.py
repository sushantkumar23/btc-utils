# client.py

import json
import decimal

import requests
from requests.auth import HTTPBasicAuth


class BitcoinClient:

    def __init__(self, username, password, url='http://localhost:8332'):
        self.username = username
        self.password = password
        self.url = url
        self.jsonrpc_version = '2.0'

    def _call(self, service_name, *args):
        """
        Method for making JSON RPC calls by service name and params
        """
        headers = { 'content-type': 'application/json' }
        auth = HTTPBasicAuth(self.username, self.password)
        payload = json.dumps({
            'jsonrpc': self.jsonrpc_version,
            'id': 'curltest',
            'method': service_name,
            'params': args
        })
        response = requests.post(self.url, headers=headers, auth=auth, data=payload)
        return response.json(parse_float=decimal.Decimal)['result']

    def getblockchaininfo(self):
        """
        Method which gets basic information about the blockchain
        """
        return self._call('getblockchaininfo')

    def getrawtransaction(self, txid):
        """
        Method which gets the raw JSON data for a transaction
        """
        return self._call('getrawtransaction', txid, True)

    def getblockhash(self, block_number):
        """
        Method which gets the hash for the given block number
        """
        return self._call('getblockhash', block_number)

    def getblock(self, block_hash):
        """
        Method which gets all information about block given its hash
        """
        return self._call('getblock', block_hash)
    
    def createwallet(self, wallet_name):
        """
        Method to create a new wallet
        """
        return self._call('createwallet', wallet_name)

    def getwalletinfo(self):
        """
        Method to info about the wallet
        """
        return self._call('getwalletinfo')

    def getnewaddres(self):
        """
        Method to create a new wallet address
        """
        return self._call('getnewaddress')
    
    def dumpprivkey(self, wallet_address):
        """
        Method to get the private key of existing wallet address
        """
        return self._call('dumpprivkey', wallet_address)
