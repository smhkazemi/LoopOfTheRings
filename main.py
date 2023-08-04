import random

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
                },
                "optimizer": {
                    "enabled": True,
                    "runs": 2,
                },
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
    address = input("-->")  # "0xCE6dD32848276F9C05134A3B9aD887EaFcBBb5bB"
    # "Oxe72CfeDE68AF32d6354143DC35e61987BD384EEf"

    # 0xe72CfeDE68AF32d6354143DC35e61987BD384EEf

    # if w3.is_address(address) is False:
    #     print("Invalid address. Try again:")
    #     address = input("-->")
    #     if w3.is_address(address) is False:
    #         print("Invalid address. First, make sure of the correctness of the address and the url.")
    #         return
    check_sum = w3.to_checksum_address(address)
    if w3.eth.get_balance(check_sum) <= 0:
        print("Not enough balance!")
        return

    # "Oxe72CfeDE68AF32d6354143DC35e61987BD384EEf"
    # "OxCE6dD32848276F9C05134A3B9aD887EaFcBBb5bB"
    print("Please enter your 32-byte private key:")
    private_key = input("-->").encode()  # b'e6b2290a4b444f3d91945d02f9c7b267'
    # b'c3e16d258afdcbf16e4af44e5353ff788c5dd58d67e51b65049631c0a1a697af'
    # 'e6b2290846444 3091945d029c762671
    # initialize contract
    nonce = w3.eth.get_transaction_count(address)
    print("Deploying Contract with nonce: " + str(nonce))
    contract_with_user_info = w3.eth.contract(abi=abi, bytecode=bytecode)
    transaction_dict = {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce
    }
    transaction_receipt = perform_transaction(private_key, transaction_dict, w3, contract_with_user_info.constructor)
    initiator_contract = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
    return transaction_dict, initiator_contract, w3, private_key, address


def perform_transaction(private_key, transaction_dict, w3, to_invoke, argument=None, argument2=None):
    if argument is None:
        transaction = to_invoke().build_transaction(transaction_dict)
    elif argument2 is None:
        transaction = to_invoke(argument).build_transaction(transaction_dict)
    else:
        transaction = to_invoke(argument, argument2).build_transaction(transaction_dict)
    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    return transaction_receipt


def adding_users(transaction_dict, initiator_contract, w3, private_key, address, investors, workers):
    print("How many users would you like to add? (please enter an integer)")
    num_users_to_add = int(input("->>"))
    print("Which type would you like the users to be: investor (i) OR worker (w)")
    user_type = input("-->")
    while user_type != "i" and user_type != "w":
        print("wrong type. Please enter investor (i) OR worker (w).")
        user_type = input("-->")
    print("How many coins does each user have? (please enter an integer) \n "
          "NB: You may choose two positive integers as the range the number of coins are picked u.a.r by"
          " entering the number -1")
    num_coins = int(input())
    lower_bound_of_range = num_coins
    upper_bound_of_range = num_coins
    if num_coins == -1:
        print("Please enter the lower bound of the range:")
        lower_bound_of_range = int(input("-->"))
        print("Please enter the upper bound of the range:")
        upper_bound_of_range = int(input("-->"))
    for counter in range(num_users_to_add):
        num_coins = int(random.Random.randint(lower_bound_of_range, upper_bound_of_range))
        transaction_dict["nonce"] = w3.eth.get_transaction_count(address)

        # NB: We considered 1 coin = 1 Ara
        transaction_receipt = perform_transaction(private_key, transaction_dict, w3,
                                                  initiator_contract.functions.sign_up, num_coins)

        if user_type == "i":
            investors.append([num_coins, transaction_receipt])
        else:
            workers.append([num_coins, transaction_receipt])
    return num_users_to_add


def form_fractal_ring(number_of_users, threshold_of_starting_lor, investors, transaction_dict, address, private_key,
                      w3):
    if number_of_users < threshold_of_starting_lor:
        print("Not enough users! There are " + str(number_of_users) +
              " users registered, but you need at least " + str(threshold_of_starting_lor))
        return
    if len(investors) == 0 or len(workers) == 0:
        print("You have " + str(len(investors)) + " investors, but " + str(len(workers)) + " workers")
        return
    investor_index = random.randint(0, len(investors) - 1)
    transaction_dict["nonce"] = w3.eth.get_transaction_count(address)

    # NB: We considered 1 coin = 1 Ara
    investor_user = w3.eth.contract(address=investors[investor_index][1].contractAddress,
                                    abi=transaction_dict["abi"])
    print(perform_transaction(private_key, transaction_dict, w3, investor_user.functions.generate_a_fractal_ring))


def form_co_operation_ring(investors, address, transaction_dict, private_key, w3):
    investor_index = random.randint(0, len(investors) - 1)
    transaction_dict["nonce"] = w3.eth.get_transaction_count(address)
    # NB: We considered 1 coin = 1 Ara
    investor_user = w3.eth.contract(address=investors[investor_index][1].contractAddress,
                                    abi=transaction_dict["abi"])
    broadcast_contract = w3.eth.contract(address=investor_user.functions.get_broadcast_address().call(),
                                         abi=transaction_dict["abi"])
    perform_transaction(private_key, transaction_dict, w3, investor_user.functions.generate_co_op_ring,
                        broadcast_contract.functions.get_invest_coin_table_by_id(investor_user.call().id()).call(),
                        "invest")


if __name__ == '__main__':
    print("----Deploying the initiator-----")
    transaction_dict, initiator_contract, w3, private_key, address = deploy("initiator.sol")
    print("-----Press any key to proceed-----")
    input("-->")
    number_of_users = 0
    investors = []
    workers = []
    threshold_of_starting_lor = 1000000
    while True:
        print("Please choose a number among one of the following:")
        print("1. add user(s). ")
        print("2. form a co-operation ring by picking users u.a.r (you should have at least one million users)")
        print("3. form a fractal ring by picking users u.a.r (you should have at least one million users)")
        print("4. exit")
        input_num = int(input("-->"))
        if input_num == 4:  # exit
            break
        elif input_num == 1:  # add user(s)
            number_of_users += adding_users(transaction_dict, initiator_contract, w3, private_key, address, investors,
                                            workers)
        elif input_num == 2:
            if number_of_users < threshold_of_starting_lor:
                print("Not enough users! There are " + str(number_of_users) +
                      " users registered, but you need at least " + str(threshold_of_starting_lor))
                continue
            if len(investors) == 0 or len(workers) == 0:
                print("You have " + str(len(investors)) + " investors, but " + str(len(workers)) + " workers")
                continue
            print("How many co-operation rings would you like to have?")
            co_op_count = int(input("-->"))
            for ctr in range(co_op_count):
                form_co_operation_ring(investors, address, transaction_dict, private_key, w3)
        elif input_num == 3:  # form a fractal ring
            form_fractal_ring(number_of_users, threshold_of_starting_lor, investors, transaction_dict, address,
                              private_key, w3)

    # with open(r'initiator_contract.txt', 'w') as fp:
    #     fp.write(str(contact))
