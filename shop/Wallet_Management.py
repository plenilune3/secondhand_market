import web3

from web3 import Web3


class WalletManagement:

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

    def createAccount(self, secret_key):
        new_account = self.w3.personal.newAccount(secret_key)
        return new_account

    def getBalance(self, account):
        balance = self.w3.eth.getBalance(account)
        return self.w3.toWei(balance, 'ether')


#from Wallet_Management import WalletManagement
#test = WalletManagement()
#파라미터로 비밀키 전달하셈
#test.createAccount("pass6")
#test.getBalance