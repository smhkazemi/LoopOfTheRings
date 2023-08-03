from web3 import Web3
from solcx import compile_standard
import json

from web3.middleware import geth_poa_middleware


def deploy(filename):
    print("Processing the initiator solidity file...")
    with open(filename, "r") as file:
        simple_storage_file = file.read()
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {filename: {"content": simple_storage_file}},
            "settings": {
                "evmVersion": "paris",
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        }
    )
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)
    print("The code was compiled to json format successfully, and the result is stored in file compiled_code.json")
    # get bytecode
    bytecode = compiled_sol["contracts"][filename]["initiator"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_sol["contracts"][filename]["initiator"]["metadata"])["output"]["abi"]
    print("Please enter thee url of the http service provide (Web3.HTTPProvider):")
    url = input("-->")  # "https://avalanche-fuji-c-chain.publicnode.com"
    w3 = Web3(Web3.HTTPProvider(url))
    w3.middleware_onion.inject(geth_poa_middleware, '', 0)
    print("Please enter the chain ID:")
    chain_id = int(input("-->"))  # 43113
    print("Please enter the address of your account (you may find it in your MetaMask account)")
    my_address = input("-->")  # "0xCE6dD32848276F9C05134A3B9aD887EaFcBBb5bB"
    # "Oxe72CfeDE68AF32d6354143DC35e61987BD384EEf"

    if w3.is_address(my_address) is False:
        print("Invalid address. Try again:")
        my_address = input("-->")
        if w3.is_address(my_address) is False:
            print("Invalid address. First, make sure of the correctness of the address and the url.")
            return
    check_sum = w3.to_checksum_address(my_address)
    balance = w3.eth.get_balance(check_sum)
    print(balance)
    if balance <= 0:
        print("Not enough balance!")
        return

    # "Oxe72CfeDE68AF32d6354143DC35e61987BD384EEf"
    # "OxCE6dD32848276F9C05134A3B9aD887EaFcBBb5bB"
    print("Please enter your 32-byte private key:")
    private_key = input("-->").encode()  # b'e6b2290a4b444f3d91945d02f9c7b267'
    # b'c3e16d258afdcbf16e4af44e5353ff788c5dd58d67e51b65049631c0a1a697af'
    # 'e6b2290846444 3091945d029c762671
    # initialize contract
    nonce = w3.eth.get_transaction_count(my_address)
    print("Deploying Contract with nonce: " + str(nonce))
    ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
    transaction = ContactList.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce
        }
    )
    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key - private_key)
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
    return contact_list

if __name__ == '__main__':
    print(deploy("initiator.sol"))
