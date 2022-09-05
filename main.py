# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import hashlib

from web3 import Web3


def calc_sha256(str):
    return hashlib.sha256(str.encode())


class CoinTable:
    def __init__(self, id, abou, stat, type, n_in_co_ring, p_in_co_ring, b_on, owner):
        self.coin_id = id
        self.amount_based_on_one_unit = abou
        self.status = stat  # run - blocked - expired/paid
        self.type = type
        self.next_in_cooporation_ring = n_in_co_ring
        self.previous_in_cooperation_link = p_in_co_ring
        self.binded_on = b_on
        self.owner = owner


class CoOperationTable:
    def __init__(self, id, ngm, w, nifr, pifr, p_in_co_ring, owner, nrr):
        self.group_id = id
        self.number_of_group_members = ngm
        self.weight = w  # run - blocked - expired/paid
        self.next_in_fractal_ring = nifr
        self.previous_in_fractal_ring = pifr
        self.owner = owner
        self.number_of_required_rounds = nrr


def ether_connection_unit_test():
    infura_url = 'https://mainnet.infura.io/v3/81d6d934a6584310978f5d82c58bc1c6'
    print(infura_url)
    # HTTPProvider:
    w3 = Web3(Web3.HTTPProvider(infura_url))
    res = w3.isConnected()
    print(res)
    print(w3.eth.blockNumber)


def coin_table_unit_test():
    coin = CoinTable(1, 1, 'ready', 'x', None, None, None, 'someone')
    print(coin.owner)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(calc_sha256("GeeksforGeeks").hexdigest())
    coin_table_unit_test()
    ether_connection_unit_test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
