# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import hashlib
from web3 import Web3
import time
import random

epsilon = 0.001

users = {}

id_to_sha_table = {}
id_to_list_of_invested_coins = {}
co_operation_table_dict = {}

coin_dict_invest = {}
###
coin_list_storage = []
coin_list_cpu = []
coin_list_gpu = []
coin_list_typing = []

fractal_ring_dict = {}

ids_in_system = {}

def get_random_id():
    random.seed(int(round(time.time() * 1000)))
    num = int(random.random() * 1000000000)
    while num in ids_in_system.keys():
        num = int(random.random() * 1000000000)
    return num


class Trader:
    def __init__(self, ara):
        self.id = get_random_id()
        self.ara_amount = ara


def register_a_user(ara):
    user = Trader(ara)
    users[user.id] = user
    return user.id


def calc_sha256(str):
    return hashlib.sha256(str.encode())


def register_a_coin(owner, abou, type, nrr):
    if owner.ara_amount < abou:
        raise ("Not enough Ara for trader: " + owner.id)
    coin_table = CoinTable(get_random_id(), abou, 'run', type, None, None, None, owner)
    if 'I' in type:
        if owner.id not in coin_dict_invest:
            coin_dict_invest[owner.id] = []
        coin_dict_invest[owner.id].append(coin_table)
        if (create_co_op_ring(coin_table, 10)) is not None:
            if owner.id not in id_to_list_of_invested_coins.keys():
                id_to_list_of_invested_coins[owner.id] = []
            id_to_list_of_invested_coins[owner.id].append(coin_dict_invest[-1])
            coin_dict_invest[owner.id].pop(-1)
            if owner.id not in co_operation_table_dict.keys():
                co_operation_table_dict[owner.id] = []
            co_operation_table_dict[owner.id].append(create_co_op_ring_table(ngm, owner, nrr))
    elif type == 'S':
        coin_list_storage.append(coin_table)
    elif type == 'C':
        coin_list_cpu.append(coin_table)
    elif type == 'G':
        coin_list_gpu.append(coin_table)
    elif type == 'T':
        coin_list_typing.append(coin_table)
    else:
        raise ("Invalid type of coin - type: : " + coin_table.type + " owner: " + str(owner))


def create_co_op_ring_table(ngm, owner, nrr):
    return CoOperationTable(get_random_id(), ngm, 1, None, None, owner, nrr)


def get_random_index_sha256(size):
    return int(hashlib.sha256(str(h).encode()).hexdigest(), 32) % size


def create_co_op_ring(coin_table_instance, nrr):
    coin_table_instance.binded_on = []
    for round_reqiered in range(0, nrr):
        randomly_selected_coin = None
        if 'S' in coin_table_instance.type:
            randomly_selected_coin = coin_list_storage[get_random_index_sha256(len(coin_list_storage))]
        elif 'C' in coin_table_instance.type:
            randomly_selected_coin = coin_list_cpu[get_random_index_sha256(len(coin_list_cpu))]
        elif 'G' in coin_table_instance.type:
            randomly_selected_coin = coin_list_gpu[get_random_index_sha256(len(coin_list_gpu))]
        elif 'T' in coin_table_instance.type:
            randomly_selected_coin = coin_list_typing[get_random_index_sha256(len(coin_list_typing))]
        else:
            return None
        randomly_selected_coin.binded_on = coin_table_instance
        coin_table_instance.binded_on.append(randomly_selected_coin)
    return coin_table_instance


def randomized_number_of_cooperation_ring():
    cf = 500
    random.seed(int(round(time.time() * 1000)))
    h = int(random.random() * 1500) + cf
    for cf in range(500, h):
        for i in range(500, cf):
            h = (int(hashlib.sha256(str(h).encode()).hexdigest(), 32) % 500) + 1500
    return cf


def submit_a_fractal_ring(owner, average_number_of_fractal_rings, rand_num_of_co_rings):
    id = generate_fractal_ring(average_number_of_fractal_rings, owner, rand_num_of_co_rings)
    if id is None:
        print("Failed to generate the fractal ring for the owner: " + owner.id)
        return None
    fractal_ring_dict[id].append(select_members_of_the_verification_team_for(id))
    return id


def select_members_of_the_verification_team_for(id):
    vt = (int(hashlib.sha256(str(h).encode()).hexdigest(), 32) % len(fractal_ring_dict[id][0])) + 503
    result = []
    list_of_users = users.values()
    for i in range(0, vt):
        result.append(list_of_users[get_random_index_sha256(len(list_of_users))])
    return result


def generate_fractal_ring(average_number_of_fractal_rings, owner, rand_num_of_co_rings):
    if owner.id not in co_operation_table_dict.keys():
        return None
    if len(co_operation_table_dict[owner.id]) < rand_num_of_co_rings:
        return None
    first_item_in_result = None
    index = get_random_index_sha256(len(co_operation_table_dict[owner.id]))
    while (index % average_number_of_fractal_rings) == 0:
        first_item_in_result = co_operation_table_dict[owner.id][index]
    indexes = {index: True}
    result = []
    result.append(first_item_in_result)
    for i in range(1, rand_num_of_co_rings):
        index = get_random_index_sha256(len(co_operation_table_dict[owner.id]))
        if index not in indexes.keys():
            result.append(co_operation_table_dict[owner.id][index])
    for i in range(1, rand_num_of_co_rings):
        result[i - 1].next_in_fractal_ring = result[i]
        if i > 1:
            result[i - 1].previous_in_fractal_ring = result[i - 2]
        else:
            result[i - 1].previous_in_fractal_ring = None
    fractal_ring_dict[owner.id] = [result, get_random_id()]
    return owner.id


def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


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
        self.weight = w
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
    print(randomized_number_of_cooperation_ring())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
