from django.shortcuts import render
from .send_paxos_dollar import prepare_paxos_dollar_tx
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import decimal
import binascii

import web3 as w3
import os
import requests
import json
Infura_API_Key = '0fa94c53080547759661a8b3bdc1f63f'
os.environ['INFURA_API_KEY'] = Infura_API_Key
from web3.auto.infura import w3

# Create your views here.
class PaxosUSDRequest(APIView):

    def post(self, request, format=None):
        address_to_send_to = w3.toChecksumAddress(self.request.data['address_to_send_to'])
        amount_of_paxos_usd_to_send = decimal.Decimal(self.request.data['amount_of_paxos_usd_to_send'])
        #decode master wallet, make transactions
        decoding_string = 'teamkalsh'
        filename = 'paxos_payout/teamkalsh'
        key_data = json.loads(open(filename,'r').read())
        private_key = w3.eth.account.decrypt(key_data,decoding_string)
        signed_transaction = prepare_paxos_dollar_tx(address_to_send_to,
                                                           private_key, amount_of_paxos_usd_to_send)
        print(signed_transaction)
        tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        # tx_hash = signed_transaction['hash']
        print(tx_hash)
        # gasPurchaseObejct = handleGasPurchaseObject(tx_hash, self.request.user,
        #                                             amount_of_gas_in_nftg_units,
        #                                             amount_of_usd_spent)
        #delegates resolving gas purchase object to celery so server can run
        # resolveGasPurchaseObjectTask.delay(gasPurchaseObejct.id)
        # print(gasPurchaseObejct.id)
        tx_hash_string = ('0x' + binascii.hexlify(tx_hash).decode('utf-8'))
        print(tx_hash_string)
        return Response(tx_hash_string, status=status.HTTP_200_OK)
