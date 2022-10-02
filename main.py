# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import hashlib
import random
import time

from web3 import Web3


class pseudoTCBRelatedItems:
    epsilon = 0.001
    users = {}
    id_to_list_of_invested_coins = {}
    fractal_ring_dict = {}
    ids_in_system = {}


class SWSE:  # Simulated Workstation Environment
    co_operation_table_dict = {}
    coin_dict_invest = {}
    coin_dict_storage_invest = {}
    coin_dict_cpu_invest = {}
    coin_dict_gpu_invest = {}
    coin_dict_typing_invest = {}
    coin_list_storage = []
    coin_list_cpu = []
    coin_list_gpu = []
    coin_list_typing = []


def get_random_id():
    random.seed(int(round(time.time() * 1000)))
    num = int(random.random() * 1000000000)
    while num in pseudoTCBRelatedItems.ids_in_system.keys():
        num = int(random.random() * 1000000000)
    return num


class Trader:
    def __init__(self, ara):
        self.id = get_random_id()
        self.ara_amount = ara

    def check_fractal_ring(self, owner_id, rand_num_of_co_rings):
        if len(SWSE.co_operation_table_dict[owner_id]) < rand_num_of_co_rings:
            return False
        sum_of_weights = 0
        there_is_a_coin_spent_more_than_once = False
        for table in SWSE.co_operation_table_dict[owner_id]:
            sum_of_weights = sum_of_weights + table.weight
            for coin_table in table.owner.binded_on:
                if coin_table.status is not 'run':
                    there_is_a_coin_spent_more_than_once = True
        if there_is_a_coin_spent_more_than_once:
            return False
        if pseudoTCBRelatedItems.users[owner_id].ara_amount < sum_of_weights:
            return False
        return True

    def submit_the_fractal_ring(self, verification_team, id):
        pseudoTCBRelatedItems.fractal_ring_dict[id].append(verification_team)
        for co_ring in pseudoTCBRelatedItems.fractal_ring_dict[id][0]:
            co_ring.status = 'blocked'

    def check_submission_of_fractal_ring(self, id):
        if len(pseudoTCBRelatedItems.fractal_ring_dict[id]) != 3:
            return True
        if len(pseudoTCBRelatedItems.fractal_ring_dict[id][-1]) < 503:
            return False
        return True


def register_a_user(ara):
    user = Trader(ara)
    pseudoTCBRelatedItems.users[user.id] = user
    return user.id


def calc_sha256(str):
    return hashlib.sha256(str.encode())


def get_corresponding_dict_for_invest(invest_type):
    if 'S' in invest_type:
        return SWSE.coin_dict_storage_invest
    elif 'C' in invest_type:
        return SWSE.coin_dict_cpu_invest
    elif 'G' in invest_type:
        return SWSE.coin_dict_gpu_invest
    elif 'T' in invest_type:
        return SWSE.coin_dict_typing_invest
    else:
        return None


def get_corresponding_list_for_work(work_type):
    if 'S' in work_type:
        return SWSE.coin_list_storage
    elif 'C' in work_type:
        return SWSE.coin_list_cpu
    elif 'G' in work_type:
        return SWSE.coin_list_gpu
    elif 'T' in work_type:
        return SWSE.coin_list_typing
    else:
        return None


def insert_invest_coin(coin_table):
    dict_invest = get_corresponding_dict_for_invest(coin_table.type)
    dict_invest[coin_table.coin_id] = coin_table


def register_a_coin(owner, abou, coin_type, nrr):
    coin_table = CoinTable(get_random_id(), abou, 'run', coin_type, None, None, None, owner)
    if 'I' in coin_type:
        insert_invest_coin(coin_table)
        if (create_co_op_ring(coin_table)) is not None:
            co_op_ring_table_instance = create_co_op_ring_table(abou, coin_table, nrr, abou)
            SWSE.co_operation_table_dict[co_op_ring_table_instance.group_id] = co_op_ring_table_instance
    work_list = get_corresponding_list_for_work(coin_type)
    if work_list is not None:
        work_list.append(coin_table)
    else:
        print("Invalid type of coin - type: : " + coin_table.type + " owner: " + str(owner.id))


def create_co_op_ring_table(ngm, owner, nrr, w):
    return CoOperationTable(get_random_id(), ngm, w, None, None, None, owner, nrr)

def get_random_index_sha256(size):
    return int(hashlib.sha256(str(int(round(time.time() * 1000))).encode()).hexdigest(), 32) % size


def get_random_form_list(l):
    result = l[get_random_index_sha256(len(l))]
    if result.binded_on is not None:
        for index in range(0, len(l)):
            if l[index].binded_on is None:
                return l[index]
    return result


def create_co_op_ring(coin_table_instance):
    coin_table_instance.binded_on = []
    rand_selected_coin = None
    list_to_use = None
    amount_based_on_one_unit = coin_table_instance.amount_based_on_one_unit
    if 'I' in coin_table_instance.type:
        list_to_use = get_corresponding_list_for_work(coin_table_instance.type)
    else:
        list_to_use = get_corresponding_dict_for_invest(coin_table_instance.type)
        list_to_use = list_to_use.values()
    while amount_based_on_one_unit > 0:
        rand_selected_coin = get_random_form_list(list_to_use)
        rand_selected_coin.binded_on = coin_table_instance
        coin_table_instance.binded_on.append(rand_selected_coin)
        amount_based_on_one_unit = amount_based_on_one_unit - rand_selected_coin.amount_based_on_one_unit
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
    frac_ring_and_id = generate_fractal_ring(average_number_of_fractal_rings, owner, rand_num_of_co_rings)
    if frac_ring_and_id is None:
        print("Failed to generate the fractal ring for the owner: " + str(owner.id))
        return None
    verification_team = select_members_of_the_verification_team_for(frac_ring_and_id[1])
    threshold_counter = 0
    for member in verification_team:
        if member.check_fractal_ring(frac_ring_and_id[0], SWSE.co_operation_table_dict) is True:
            threshold_counter = threshold_counter + 1
    if threshold_counter < (len(verification_team) / 2):
        print("The majority of the verification_team members did not endors creating the fractal ring for: " + owner.id)
        return None
    random_member = get_random_index_sha256(len(verification_team))
    random_member.submit_the_fractal_ring(verification_team, id)
    threshold_counter = 0
    for member in verification_team:
        if member is not random_member:
            if member.check_submission_of_fractal_ring(frac_ring_and_id[1]):
                threshold_counter = threshold_counter + 1
    if threshold_counter < ((len(verification_team) - 1) / 2):
        return None
    return frac_ring_and_id[1]


def select_members_of_the_verification_team_for(id):
    vt = (int(hashlib.sha256(str(int(round(time.time() * 1000))).encode()).hexdigest(), 32) % len(
        pseudoTCBRelatedItems.fractal_ring_dict[id][0])) + 503
    result = []
    list_of_users = list(pseudoTCBRelatedItems.users.values())
    for i in range(0, vt):
        result.append(list_of_users[get_random_index_sha256(len(list_of_users))])
    return result


def generate_fractal_ring(average_number_of_fractal_rings, owner, rand_num_of_co_rings):
    index = get_random_index_sha256(len(SWSE.co_operation_table_dict[owner.id]))
    first_item_in_result = SWSE.co_operation_table_dict[owner.id][index]
    while (index % average_number_of_fractal_rings) == 0:
        first_item_in_result = SWSE.co_operation_table_dict[owner.id][index]
        index = get_random_index_sha256(len(SWSE.co_operation_table_dict[owner.id]))
    indexes = {index: True}
    result = []
    result.append(first_item_in_result)
    for i in range(1, rand_num_of_co_rings):
        index = get_random_index_sha256(len(SWSE.co_operation_table_dict[owner.id]))
        while index in indexes.keys():
            index = get_random_index_sha256(len(SWSE.co_operation_table_dict[owner.id]))
        indexes[index] = True
        result.append(SWSE.co_operation_table_dict[owner.id][index])
    for i in range(1, rand_num_of_co_rings):
        result[i - 1].next_in_fractal_ring = result[i]
        if i > 1:
            result[i - 1].previous_in_fractal_ring = result[i - 2]
        else:
            result[i - 1].previous_in_fractal_ring = None
    return [result, get_random_id()]


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


def double_spending_attack_scenario():
    print("Creating 1,500,000 users...")
    rand_num_co_rings = randomized_number_of_cooperation_ring()
    for i in range(1, 1500000):
        register_a_user(rand_num_co_rings)
    random_investor_user_index = get_random_index_sha256(len(pseudoTCBRelatedItems.users.values()))
    random_storage_user_index = get_random_index_sha256(len(pseudoTCBRelatedItems.users.values()))
    list_of_values = list(pseudoTCBRelatedItems.users.values())
    print("investor user with id: " + str(
        list_of_values[random_investor_user_index].id) + " is picked randomly using sha256")
    print("storage user with id: " + str(
        list_of_values[random_storage_user_index].id) + " is picked randomly using sha256")
    for i in range(0, rand_num_co_rings):
        register_a_coin(list_of_values[random_storage_user_index], 1, 'S', 1)
    for i in range(0, rand_num_co_rings):
        register_a_coin(list_of_values[random_investor_user_index], 1, 'IS', 1)
    print("submitting a fractal ring...")
    submit_a_fractal_ring(list_of_values[random_investor_user_index], rand_num_co_rings, rand_num_co_rings)
    print("done")
    pseudoTCBRelatedItems.users.clear()

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
    double_spending_attack_scenario()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
