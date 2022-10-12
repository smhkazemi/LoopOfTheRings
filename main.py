import hashlib
import random
import threading
import time

from numba import jit


class pseudoTCBRelatedItems:
    epsilon = 0.001
    users = {}
    fractal_ring_dict = {}  # A simulation for RCB
    ids_in_system = {}
    user_storage = {}  ## user id to a shared dict i.e. the simulation of the shared memory with the verification team
    id_to_vote = {}

class SWSE:  # Simulated Workstation Environment
    co_operation_table_dict = {}  ## id of coopRing to coopRing
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
    num = int(random.random() * 1000000000)  # calc_sha256(str(int(random.random() * 1000000000)))
    while num in pseudoTCBRelatedItems.ids_in_system.keys():
        num = int(random.random() * 1000000000)  #calc_sha256(str(int(random.random() * 1000000000)))
    return num


def check_if_co_ring_should_terminate(co_ring, to_remove):
    flag = False
    for coin in co_ring.trader_coin.binded_on:
        if type(coin) is list:
            to_remove.append(co_ring)
            flag = True
            break
    return flag

class Trader:
    def __init__(self, ara):
        self.id = get_random_id()
        self.ara_amount = ara
        pseudoTCBRelatedItems.user_storage[self.id] = {}

    def report_co_ring_status(self):
        random.seed(int(round(time.time() * 1000)))
        num = int(random.random() * 1000000000)
        if num > 9500000000:
            return False
        return True

    def check_payment(self, user_id, simulated_tcb_history_on_user_ara, simulated_tcb_history_on_payment_amount, coin):
        if user_id not in pseudoTCBRelatedItems.id_to_vote.keys():
            pseudoTCBRelatedItems.id_to_vote[user_id] = 0
        if pseudoTCBRelatedItems.users[
            user_id].ara_amount == simulated_tcb_history_on_user_ara + simulated_tcb_history_on_payment_amount and coin.status == 'paid':
            pseudoTCBRelatedItems.id_to_vote[user_id] = pseudoTCBRelatedItems.id_to_vote[user_id] + 1

    def factorial_calc_cpu_job(self):
        num = 100
        factorial = 1
        for i in range(num):
            factorial = factorial * (i + 1)
        return factorial

    def pay_user(self, user_id, ara, coin):
        pseudoTCBRelatedItems.users[user_id].ara_amount = pseudoTCBRelatedItems.users[user_id].ara_amount + ara
        coin.status = 'paid'

    def ask_co_ring_members(self, co_ring):
        if co_ring.group_id not in pseudoTCBRelatedItems.id_to_vote.keys():
            pseudoTCBRelatedItems.id_to_vote[co_ring.group_id] = 0
        for member in co_ring.trader_coin.binded_on:
            if not pseudoTCBRelatedItems.users[member[2].owner_id].report_co_ring_status():
                return
        if not pseudoTCBRelatedItems.users[co_ring.trader_coin.owner_id].report_co_ring_status():
            return
        pseudoTCBRelatedItems.id_to_vote[co_ring.group_id] = pseudoTCBRelatedItems.id_to_vote[co_ring.group_id] + 1

    def check_fractal_ring(self, frac_ring_and_id, trader_id):
        if 'threshold' not in pseudoTCBRelatedItems.user_storage[trader_id].keys():
            pseudoTCBRelatedItems.user_storage[trader_id]['threshold'] = 0
        sum_of_weights = 0
        there_is_a_coin_spent_more_than_once = False
        for table in frac_ring_and_id[0]:
            if table.trader_coin.owner_id == trader_id:
                sum_of_weights = sum_of_weights + table.weight
            for coin_table in table.trader_coin.binded_on:
                if coin_table.status != 'ready':
                    there_is_a_coin_spent_more_than_once = True
        if there_is_a_coin_spent_more_than_once:
            return False
        if pseudoTCBRelatedItems.users[trader_id].ara_amount < sum_of_weights:
            return False
        pseudoTCBRelatedItems.user_storage[trader_id]['threshold'] = \
            pseudoTCBRelatedItems.user_storage[trader_id]['threshold'] + 1
        return True

    def submit_the_fractal_ring(self, frac_ring_and_id, verification_team_ids, trader_id):
        if pseudoTCBRelatedItems.user_storage[trader_id]['threshold'] < len(verification_team_ids) / 2:
            return False
        pseudoTCBRelatedItems.user_storage[trader_id]['threshold'] = 0
        if trader_id not in pseudoTCBRelatedItems.fractal_ring_dict.keys():
            pseudoTCBRelatedItems.fractal_ring_dict[trader_id] = []
        pseudoTCBRelatedItems.fractal_ring_dict[frac_ring_and_id[1]] = []
        pseudoTCBRelatedItems.fractal_ring_dict[frac_ring_and_id[1]].append(frac_ring_and_id[0])
        pseudoTCBRelatedItems.fractal_ring_dict[frac_ring_and_id[1]].append(verification_team_ids)
        to_remove = []
        for co_ring in pseudoTCBRelatedItems.fractal_ring_dict[frac_ring_and_id[1]][0]:
            binding = []
            if check_if_co_ring_should_terminate(co_ring, to_remove): continue
            for coin in co_ring.trader_coin.binded_on:
                coin.status = 'blocked'
                coin.binded_on = [co_ring.trader_coin]
                binding.append([coin_to_string(coin), calc_sha256(coin_to_string(coin)), coin])
            co_ring.trader_coin.status = 'blocked'
            co_ring.trader_coin.binded_on = binding
            if co_ring.group_id in pseudoTCBRelatedItems.user_storage[co_ring.trader_coin.owner_id].keys():
                pseudoTCBRelatedItems.user_storage[co_ring.trader_coin.owner_id].pop(co_ring.group_id)
            co_ring.trader_coin_sha256 = coin_to_sha256(co_ring.trader_coin)
        for ring in to_remove:
            pseudoTCBRelatedItems.fractal_ring_dict[frac_ring_and_id[1]][0].remove(ring)
        return True

    def check_submission_of_fractal_ring(self, f_id, trader_id):
        valid_submission = True
        if len(pseudoTCBRelatedItems.fractal_ring_dict[f_id]) != 2:
            valid_submission = False
        if len(pseudoTCBRelatedItems.fractal_ring_dict[f_id][1]) < 1000:
            valid_submission = False
        if valid_submission is False:
            return valid_submission
        for co_ring in pseudoTCBRelatedItems.fractal_ring_dict[f_id][0]:
            if co_ring.trader_coin.status != 'blocked':
                print("blocked")
                valid_submission = False
            elif len(co_ring.trader_coin.binded_on) == 0:
                valid_submission = False
                print("len(co_ring.trader_coin.binded_on) == 0")
            elif valid_submission:
                for coin_pair in co_ring.trader_coin.binded_on:
                    if len(coin_pair) != 3:
                        valid_submission = False
                        print("len(coin_pair) != 3")
                    elif calc_sha256(coin_pair[0]).hexdigest() != coin_pair[1].hexdigest():
                        valid_submission = False
                        print(str(calc_sha256(coin_pair[0]).hexdigest()) + " " + str(coin_pair[1].hexdigest()))
                    elif 'blocked' not in coin_pair[0]:
                        valid_submission = False
                        print("coin_pair[0].status != 'blocked'")
                if calc_sha256(
                        coin_to_string(co_ring.trader_coin)).hexdigest() != co_ring.trader_coin_sha256.hexdigest():
                    valid_submission = False
                    print("coin_to_sha256(co_ring.trader_coin[0]).hexdigest() != co_ring.trader_coin[1].hexdigest()")
        if valid_submission:
            pseudoTCBRelatedItems.user_storage[trader_id]['threshold'] = \
                pseudoTCBRelatedItems.user_storage[trader_id]['threshold'] + 1
        return valid_submission


@jit(target_backend='cuda')
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


def broadcast_a_coin(trader, abou, coin_type, nrr):
    coin_table = CoinTable(get_random_id(), abou, 'ready', coin_type, None, None, None, trader.id)
    if 'I' in coin_type:
        insert_invest_coin(coin_table)  # broadcasting the coin into the system environment
        create_co_op_ring(coin_table)
        pseudoTCBRelatedItems.user_storage[trader.id][broadcast_co_op_ring(abou, coin_table, nrr)] = True
        # The trader stores the IDs of the above co_op ring
    else:
        work_list = get_corresponding_list_for_work(coin_type)
        if work_list is not None:
            work_list.append(coin_table)
        else:
            print("Invalid type of coin - type: : " + coin_table.type + " owner: " + str(trader.id))


def broadcast_co_op_ring(abou, coin_table, nrr):
    co_op_ring_table_instance = create_co_op_ring_table(abou, coin_table, nrr, abou)
    SWSE.co_operation_table_dict[co_op_ring_table_instance.group_id] = co_op_ring_table_instance
    return co_op_ring_table_instance.group_id


def create_co_op_ring_table(ngm, owner, nrr, w):
    return CoOperationTable(get_random_id(), ngm, w, None, None, owner, nrr)


def get_random_index_sha256(size):
    return int(hashlib.sha256(str(int(round(time.time() * 1000))).encode()).hexdigest(), 32) % size


def get_random_form_list(l):
    return l[get_random_index_sha256(len(l))]


def create_co_op_ring(coin_table_instance):  # nothing is being submitted here!
    coin_table_instance.binded_on = []
    list_to_use = None
    amount_based_on_one_unit = coin_table_instance.amount_based_on_one_unit
    if 'I' in coin_table_instance.type:
        list_to_use = get_corresponding_list_for_work(coin_table_instance.type)
    else:
        list_to_use = get_corresponding_dict_for_invest(coin_table_instance.type)
        list_to_use = list(list_to_use.values())
    while amount_based_on_one_unit > 0:
        rand_selected_coin = get_random_form_list(list_to_use)
        coin_table_instance.binded_on.append(rand_selected_coin)
        # the coin wants to bind the coins on itself but the final decision is on the verification team
        amount_based_on_one_unit = amount_based_on_one_unit - rand_selected_coin.amount_based_on_one_unit
    return coin_table_instance


def randomized_number_of_cooperation_ring():
    cf = 1000
    random.seed(int(round(time.time() * 1000)))
    h = int(random.random() * 1500) + cf
    for cf in range(500, h):
        for i in range(500, cf):
            h = (int(hashlib.sha256(str(h).encode()).hexdigest(), 32) % 500) + 1500
    return cf


@jit(target_backend='cuda')
def round_check_state(frac_id, round_num):
    for co_ring in pseudoTCBRelatedItems.fractal_ring_dict[frac_id][0]:
        if "F" in co_ring.co_status:
            continue
        length = len(pseudoTCBRelatedItems.fractal_ring_dict[frac_id][1])
        t1 = threading.Thread(target=ask_members, args=(co_ring, frac_id, 0, int(length / 4),))
        t1.start()
        # ask_members(co_ring, frac_id, 0, length / 2)
        t2 = threading.Thread(target=ask_members, args=(co_ring, frac_id, int(length / 4), int(length / 2),))
        t2.start()
        # ask_members(co_ring, frac_id, length / 2, length)
        t3 = threading.Thread(target=ask_members, args=(co_ring, frac_id, int(length / 2), 3 * int(length / 4),))
        t3.start()
        t4 = threading.Thread(target=ask_members, args=(co_ring, frac_id, 3 * int(length / 4), length,))
        t4.start()

        t1.join()
        t2.join()
        t3.join()

        if pseudoTCBRelatedItems.id_to_vote[co_ring.group_id] < len(
                pseudoTCBRelatedItems.fractal_ring_dict[frac_id][1]) / 2:
            co_ring.co_status = "F " + str(round_num)


def ask_members(co_ring, frac_id, start, length):
    for idx in range(start, length):
        pseudoTCBRelatedItems.users[pseudoTCBRelatedItems.fractal_ring_dict[frac_id][1][idx]].ask_co_ring_members(
            co_ring)


@jit(target_backend='cuda')
def apply_payment_polices(f_id, exec_round):
    for co_ring in pseudoTCBRelatedItems.fractal_ring_dict[f_id][0]:
        if "A" not in co_ring.co_status and "T" in co_ring.co_status:
            if "F" in co_ring.co_status:
                round_ended = int(co_ring.co_status.split()[1]) + 1
            else:
                round_ended = exec_round + 1
            # In reality, if a randomly selected member of the verification team fails to pay, we keep selecting a random member
            # This perhaps requires a while-loop
            for coin in co_ring.trader_coin.binded_on:
                random_member = pseudoTCBRelatedItems.users[pseudoTCBRelatedItems.fractal_ring_dict[f_id][1][
                    get_random_index_sha256(len(pseudoTCBRelatedItems.fractal_ring_dict[f_id][1]))]]
                simulated_tcb_history_on_user_ara = pseudoTCBRelatedItems.users[coin[2].owner_id].ara_amount
                simulated_tcb_history_on_payment_amount = ((float(round_ended) / float(
                    co_ring.number_of_required_rounds)) * float(coin[2].amount_based_on_one_unit)) + (
                                                                      -1. / float(round_ended) - (1. / (
                                                                          float(co_ring.weight) * float(
                                                                      1 + len(co_ring.trader_coin.binded_on)))))
                random_member.pay_user(coin[2].owner_id, simulated_tcb_history_on_payment_amount, coin[2])
                for user_id in pseudoTCBRelatedItems.fractal_ring_dict[f_id][1]:
                    if user_id is not random_member.id:
                        pseudoTCBRelatedItems.users[user_id].check_payment(coin[2].owner_id,
                                                                           simulated_tcb_history_on_user_ara,
                                                                           simulated_tcb_history_on_payment_amount,
                                                                           coin[2])
            co_ring.co_status = co_ring.co_status + " A"
        elif "T" not in co_ring.co_status:
            co_ring.co_status = co_ring.co_status + " T"


def check(verification_team_ids, start, end, rand_member_id, f_id, i_id):
    for idx in range(start, end):
        if verification_team_ids[idx] is not rand_member_id:
            pseudoTCBRelatedItems.users[verification_team_ids[idx]].check_submission_of_fractal_ring(f_id, i_id)


@jit(target_backend='cuda')
def submit_a_fractal_ring(investor, average_number_of_fractal_rings, rand_num_of_co_rings):
    frac_ring_and_id = generate_fractal_ring(average_number_of_fractal_rings, investor, rand_num_of_co_rings)
    if frac_ring_and_id is None:
        return None
    verification_team_ids = select_members_of_the_verification_team_for(frac_ring_and_id)
    for user_id in verification_team_ids:
        pseudoTCBRelatedItems.users[user_id].check_fractal_ring(frac_ring_and_id, investor.id)
    random_member = pseudoTCBRelatedItems.users[
        verification_team_ids[get_random_index_sha256(len(verification_team_ids))]]
    if random_member.submit_the_fractal_ring(frac_ring_and_id, verification_team_ids, investor.id) is False:
        return None
    length = len(verification_team_ids)
    t1 = threading.Thread(target=check, args=(
    verification_team_ids, 0, int(length / 3), random_member.id, frac_ring_and_id[1], investor.id,))
    t2 = threading.Thread(target=check, args=(
    verification_team_ids, int(length / 3), 2 * int(length / 3), random_member.id, frac_ring_and_id[1], investor.id,))
    t3 = threading.Thread(target=check, args=(
    verification_team_ids, 2 * int(length / 3), length, random_member.id, frac_ring_and_id[1], investor.id,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    # for user_id in verification_team_ids:
    #     if user_id is not random_member.id:
    #         pseudoTCBRelatedItems.users[user_id].check_submission_of_fractal_ring(frac_ring_and_id[1], investor.id)
    if pseudoTCBRelatedItems.user_storage[investor.id]['threshold'] < len(
            verification_team_ids) / 2:  # read only access
        return None
    return frac_ring_and_id[1]  # id of the fractal ring


@jit(target_backend='cuda')
def select_members_of_the_verification_team_for(fractal_ring_and_id):
    vt = (int(hashlib.sha256(str(int(round(time.time() * 1000))).encode()).hexdigest(), 32) % len(
        fractal_ring_and_id[0])) + 1000
    result = []
    list_of_users = list(pseudoTCBRelatedItems.users.values())
    for i in range(vt):
        result.append(list_of_users[get_random_index_sha256(len(list_of_users))].id)
    return result


def generate_fractal_ring(average_number_of_fractal_rings, trader, rand_num_of_co_rings):
    # The trader keeps its keys
    list_of_trader_co_op_rings_ids = list(pseudoTCBRelatedItems.user_storage[trader.id].keys())
    result = prioritizing_the_trader_co_op_rings(average_number_of_fractal_rings, list_of_trader_co_op_rings_ids)
    if len(result) is not average_number_of_fractal_rings:
        co_op_rings_list = list(SWSE.co_operation_table_dict.values())
        index = get_random_index_sha256(len(co_op_rings_list))
        while index in pseudoTCBRelatedItems.user_storage[trader.id].keys():
            index = get_random_index_sha256(len(co_op_rings_list))
        first_item_in_result = co_op_rings_list[index]
        while (index % average_number_of_fractal_rings) == 0:
            first_item_in_result = co_op_rings_list[index]
            index = get_random_index_sha256(len(co_op_rings_list))
        indexes = {index: True}
        result.append(first_item_in_result)
        length_of_result = len(result)
        for i in range(rand_num_of_co_rings - length_of_result):
            index = get_random_index_sha256(len(co_op_rings_list))
            if index in indexes.keys():
                for counter in range(len(co_op_rings_list)):
                    if counter not in indexes.keys():
                        index = counter
                        break
            indexes[index] = True
            result.append(co_op_rings_list[index])
    set_links_in_fractal_ring(rand_num_of_co_rings, result)
    return [result, get_random_id()]


def prioritizing_the_trader_co_op_rings(average_number_of_fractal_rings, list_of_trader_co_op_rings_ids):
    result = []
    if len(list_of_trader_co_op_rings_ids) != 0:
        for ring_id in list_of_trader_co_op_rings_ids:
            if len(result) < average_number_of_fractal_rings:
                result.append(SWSE.co_operation_table_dict[ring_id])
    return result


def set_links_in_fractal_ring(rand_num_of_co_rings, result):
    for i in range(1, rand_num_of_co_rings):
        result[i - 1].next_in_fractal_ring = result[i]
        if i > 1:
            result[i - 1].previous_in_fractal_ring = result[i - 2]
        else:
            result[i - 1].previous_in_fractal_ring = None


def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def coin_to_string(coin):
    return str(coin.coin_id) + str(coin.amount_based_on_one_unit) + str(coin.type) + str(coin.owner_id) + str(
        coin.binded_on) + str(coin.status)


def coin_to_sha256(coin):
    return calc_sha256(coin_to_string(coin))


class CoinTable:
    def __init__(self, id, abou, stat, type, n_in_co_ring, p_in_co_ring, b_on, owner_id):
        self.coin_id = id
        self.amount_based_on_one_unit = abou
        self.status = stat  # ready - blocked - expired/paid
        self.type = type
        self.next_in_cooporation_ring = n_in_co_ring
        self.previous_in_cooperation_link = p_in_co_ring
        self.binded_on = b_on  # we use a dict form user_id to a pair of coin + sha256(coin) here to simulate the cases of having more than one trader trying
        # to submit a fractal ring using the same coin, or even the cases that such traders exist in a single co_op ring
        self.owner_id = owner_id

class CoOperationTable:
    def __init__(self, id, ngm, w, nifr, pifr, owner, nrr):
        self.group_id = id
        self.number_of_group_members = ngm
        self.weight = w
        self.next_in_fractal_ring = nifr
        self.previous_in_fractal_ring = pifr
        self.trader_coin = owner
        self.trader_coin_sha256 = None
        self.number_of_required_rounds = nrr
        self.co_status = ""


def performance_evaluation_sort_and_factorial_scenario():
    check_point_duration = 3  # in reality, this one is the mean value of the runtime of the co_op rings
    percent_of_investors = 30. / 100.
    print("Creating 1,500,000 users...")
    for i in range(1500000):
        register_a_user(10)
    print("1,500,000 users are now registered!")
    size = int(len(pseudoTCBRelatedItems.users.values()) * percent_of_investors)
    randomly_selected_investors = {}
    randomly_selected_workers = {}
    print("Randomly selecting the investors...")
    index = 0
    user_ids = list(pseudoTCBRelatedItems.users.keys())
    for i in range(size):
        randomly_selected_investors[index] = True
        index = index + 1
    print("Randomly selecting the workers...")
    for i in range(size):
        randomly_selected_workers[index] = True
        index = index + 1
    print("Broadcasting the worker coins...")
    keys1 = list(randomly_selected_workers.keys())
    for worker_index in keys1:
        broadcast_a_coin(list(pseudoTCBRelatedItems.users.values())[worker_index], 1, 'C', check_point_duration)
    print("Broadcasting the investor coins...")
    keys2 = list(randomly_selected_investors.keys())
    for investor_index in keys2:
        broadcast_a_coin(list(pseudoTCBRelatedItems.users.values())[investor_index], 1, 'IC', check_point_duration)
    rand_num_of_co_rings = randomized_number_of_cooperation_ring()
    print("submitting a fractal_ring...")
    workers_ids = list(randomly_selected_workers.keys())
    f_id = submit_a_fractal_ring(
        pseudoTCBRelatedItems.users[user_ids[workers_ids[get_random_index_sha256(len(workers_ids))]]],
        50, rand_num_of_co_rings)
    if f_id is None:
        print("Failed")
        return
    # everybody starts if the fractal ring is generated successfully
    print("Preforming the jobs...")
    CheckPointCCounter = 0
    for exec_round in range(check_point_duration + 2):
        for co_ring in pseudoTCBRelatedItems.fractal_ring_dict[f_id][0]:
            for coin_pair in co_ring.trader_coin.binded_on:
                pseudoTCBRelatedItems.users[coin_pair[2].owner_id].factorial_calc_cpu_job()
        round_check_state(f_id, exec_round)
        CheckPointCCounter = CheckPointCCounter + 1
        if CheckPointCCounter >= check_point_duration:
            apply_payment_polices(f_id, exec_round)
        else:
            print("round " + str(exec_round) + " completed")
    print("Done!")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    performance_evaluation_sort_and_factorial_scenario()
    # freelancer simulation
    # performance vs CoopEdge
    # Recent attacks (security mesuerment)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
