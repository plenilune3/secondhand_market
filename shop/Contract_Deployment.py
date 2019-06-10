import json
import web3

from web3 import Web3
from web3.contract import ConciseContract


class ContractDeployment:
    def __init__(self):
        #아이피 주소 바꾸세용 제껄로~~~
        self.w3 = Web3(Web3.HTTPProvider('http://172.19.3.135:8545'))
        self.secondhand = None
        self.contractAbi = [{'constant': True,
                             'inputs': [],
                             'name': 'seller',
                             'outputs': [{'name': '', 'type': 'address'}],
                             'payable': False,
                             'stateMutability': 'view',
                             'type': 'function'},
                            {'constant': True,
                             'inputs': [],
                             'name': 'getBalance',
                             'outputs': [{'name': '', 'type': 'uint256'}],
                             'payable': False,
                             'stateMutability': 'view',
                             'type': 'function'},
                            {'constant': False,
                             'inputs': [],
                             'name': 'refund',
                             'outputs': [],
                             'payable': False,
                             'stateMutability': 'nonpayable',
                             'type': 'function'},
                            {'constant': True,
                             'inputs': [],
                             'name': 'buyer',
                             'outputs': [{'name': '', 'type': 'address'}],
                             'payable': False,
                             'stateMutability': 'view',
                             'type': 'function'},
                            {'constant': False,
                             'inputs': [],
                             'name': 'buy',
                             'outputs': [],
                             'payable': False,
                             'stateMutability': 'nonpayable',
                             'type': 'function'},
                            {'inputs': [{'name': '_new', 'type': 'address'}],
                             'payable': False,
                             'stateMutability': 'nonpayable',
                             'type': 'constructor'},
                            {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}]
        self.contractBytecode = '608060405234801561001057600080fd5b506040516020806104e88339810180604052602081101561003057600080fd5b810190808051906020019092919050505033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050610416806100d26000396000f3fe608060405260043610610067576000357c01000000000000000000000000000000000000000000000000000000009004806308551a531461006957806312065fe0146100c0578063590e1ae3146100eb5780637150d8ae14610102578063a6f2ae3a14610159575b005b34801561007557600080fd5b5061007e610170565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156100cc57600080fd5b506100d5610195565b6040518082815260200191505060405180910390f35b3480156100f757600080fd5b506101006101b9565b005b34801561010e57600080fd5b506101176102bf565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561016557600080fd5b5061016e6102e5565b005b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000803090508073ffffffffffffffffffffffffffffffffffffffff163191505090565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561021457600080fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc610258610195565b9081150290604051600060405180830381858888f19350505050158015610283573d6000803e3d6000fd5b50600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561034157600080fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc610384610195565b9081150290604051600060405180830381858888f193505050501580156103af573d6000803e3d6000fd5b506000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16fffea165627a7a72305820869ec4100813c51a9a4406a533d04caaab1416bcda3bfc939f1d9f99c1aeac7c0029'

    def unlockAccount(self, address, password):
        unlock = self.w3.personal.unlockAccount(address, password, 60)
        return unlock

    def deploy(self, buyer, seller, value):
        self.w3.eth.defaultAccount = buyer
        SecondHand = self.w3.eth.contract(abi=self.contractAbi, bytecode=self.contractBytecode)
        tx_hash = SecondHand.constructor(seller).transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        self.secondhand = self.w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=self.contractAbi,
        )

        print("Contract Address : {}".format(tx_receipt.contractAddress))

        tx_hash2 = self.w3.eth.sendTransaction({'from': buyer, 'to': tx_receipt.contractAddress,
                                                'value': self.w3.toWei(value, "ether")})
        tx_receipt2 = self.w3.eth.waitForTransactionReceipt(tx_hash2)

        print("Balance : {}".format(
            self.secondhand.functions.getBalance().call()
            ))

        return tx_receipt.contractAddress

    def buy(self, contractAddress, buyer):
        self.w3.eth.defaultAccount = buyer;
        self.secondhand = self.w3.eth.contract(
            address=contractAddress,
            abi=self.contractAbi,
        )

        tx_hash3 = self.secondhand.functions.buy().transact()
        tx_receipt3 = self.w3.eth.waitForTransactionReceipt(tx_hash3)


    def refund(self, contractAddress, seller):
        self.w3.eth.defaultAccount = seller;
        self.secondhand = self.w3.eth.contract(
            address=contractAddress,
            abi=self.contractAbi,
        )

        tx_hash3 = self.secondhand.functions.refund().transact()
        tx_receipt3 = self.w3.eth.waitForTransactionReceipt(tx_hash3)


#from Contract_Deployment import ContractDeployment
#test = ContractDeployment()
#test.unlockAccount('게좌주소', '비밀번호')
#test.deploy('구매자주소', '판매자주소', '가격')
#test.buy('컨트랙트 주소', '구매자주소')
#test.refund('컨트랙트 주소', '판매자주소')