// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

interface broadcast{

    function get_coin_owner_address_by_id(uint256 id) view external returns(address);
    // Function adding values to service_coin_table_map
    function adding_service_coin(uint256 coin_id, address corresponding_trader) external;
    function get_service_coin_table_by_id(uint256 id) view external returns (address);
    function get_service_coin_table_by_id_uar() view external returns (uint256);
    // Function adding values to invest_coin_table_map
    function adding_invest_coin(uint256 coin_id, address corresponding_trader) external;
    function get_invest_coin_table_by_id(uint256 id) view external returns (address);
    function get_invest_coin_table_by_id_uar() view external returns (uint256);
    function insert_co_ring_table(uint256 trader_id, uint256 g_id, address corresponding_trader) external;
    function num_of_co_op_rings() view external returns (uint256);
    function get_co_ring_id_by_index(uint256 index) view external returns (uint256);
    function get_co_rings_for_trader_id(uint256 t_id) view external returns (uint256[] memory);
    function get_co_ring_table(uint256 g_id) view external returns (address);
    function add_new_user(uint256 id) external;
    function add_new_user_by_address(address adr, uint256 id) external;
    function get_addresses_of(uint256[] memory v_team_ids) view external returns (address[] memory);
    function get_num_of_users() view external returns (uint256);
    function get_user_id_by_index(uint256 idx) view external returns (uint256);
    function get_user(uint256 id) view external returns (address);
    function is_switched_to_lor() view external returns (bool);
}

interface verification_team_member{
    function get_vote_from_address(uint256[] memory co_ring_ids, address[] memory f_ids, uint256 f_id) external returns (uint256);
    function submit_fractal_ring(uint256[] memory result, uint256 len_of_ver_tream, uint256 votes, uint256 f_id) external;
    function end_of_round_check(uint256 f_id) external returns (uint256);
    function payment_check(uint256 f_id) external returns (uint256);
}

interface co_op_ring_owner{
    function get_co_op_ring(uint256 g_id) view external returns(CoOperationTable memory);
}

interface coin_owner{
    function get_ara_amount() view external returns (int);
    function get_coin(uint256 cid, string memory coin_type) view external returns(CoinTable memory);
    function get_amount_b_o_invest_coin_by_id(uint256 cid) view external returns (int);
    function get_amount_b_o_service_coin_by_id(uint256 cid) view external returns (int);
    function set_bindings_invest_coin(uint256 coin_instance_id, uint256[] memory coin_ids_randomly_picked) external;
    function set_bindings_service_coin(uint256 coin_instance_id, uint256[] memory coin_ids_randomly_picked) external;
    function coin_ids_binded_on(uint256 cid) view external returns(uint256[] memory);
    function status_of(uint256 cid) view external returns (string memory);
    function service_received_or_not(uint256) view external returns (bool);
    function service_provided_or_not(uint256) view external returns (bool);
    function receive_service(uint256 result, uint256 c_id) external;
    function provide_service(uint256 c_id) external returns(uint256);
    function payment_received_or_not(uint256) view external returns (bool);
    function payment_provided_or_not(uint256) view external returns (bool);
    function pay(uint256 c_id) external;
    function receive_payment(uint256 c_id) external returns (bool);
}

struct CoinTable{
    uint256 coin_id;
    int amount_based_on_one_unit;
    string status;  // ready - blocked - expired/paid
    string type_of_coin;
    uint256 next_id_in_cooporation_ring;
    uint256 previous_id_in_cooperation_link;
    uint256 user_id_binded_on;
    uint256[] coin_ids_binded_on;
    uint256[] sha256_binded_on;
    // to submit a fractal ring using the same coin, or even the cases that such traders exist in a single co_op ring
    uint256 owner_id;
} 

struct CoOperationTable{
    uint256 group_id;
    int number_of_group_members;
    int weight;
    uint256 next_id_in_fractal_ring;
    uint256 previous_id_in_fractal_ring;
    uint256 trader_coin_id;
    bytes32 trader_coin_sha256;
    int number_of_required_rounds;
    string co_status;   
}

struct fractalRing{
    uint256 id;
    uint256[] coopRing_ids;
    uint256[] verification_team_ids;
}

contract Trader {
    uint256 private id;
    int private ara_amount;
    uint private randNonce = 0;
    uint private randNonceFrac = 0;
    address private broadcast_addr;
    mapping (uint256 => bool) private payment_received;
    mapping (uint256 => bool) private service_provided;
    mapping (uint256 => CoinTable) private service_coin_table_map;
    uint256[] private service_coin_table_ids;
    mapping (uint256 => bool) private payment_provided;
    mapping (uint256 => bool) private service_received;
    mapping (uint256 => CoinTable) private invest_coin_table_map;
    uint256[] private invest_coin_table_ids;
    mapping (uint256 => CoOperationTable) private co_op_rings_map;
    uint256[] private co_op_rings_ids;

    constructor(uint256 id_, int ara, address b_addr) public {
      id = id_;  
      ara_amount = ara;
      broadcast_addr = b_addr;
    }

    function payment_received_or_not(uint256 c_id) view external returns (bool){
        if(payment_received[c_id]){
            return true;
        }
        return false;
    }
    function payment_provided_or_not(uint256 c_id) view external returns (bool){
        if(payment_provided[c_id]){
            return true;
        }
        return false;
    }
    function pay(uint256 c_id) external{
        payment_provided[c_id] = true;
    }
    function receive_payment(uint256 c_id) external returns (bool){
        payment_received[c_id] = true;
        return true;
    }

    function service_provided_or_not(uint256 c_id) view external returns (bool){
        if(service_provided[c_id]){
            return true;
        }
        return false;
    }
    function service_received_or_not(uint256 c_id) view external returns (bool){
        if(service_received[c_id]){
            return false;
        }
        return true;
    }
    function receive_service(uint256 result, uint256 c_id) external{
        service_received[c_id] = true;
    }
    function provide_service(uint256 c_id) external returns(uint256){
        service_provided[c_id] = true;
        return 1;
    }

    function get_co_op_ring(uint256 g_id) view external returns(CoOperationTable memory){
        return co_op_rings_map[g_id];
    }
 
    // Defining a function to generate a random number
    function rand_id() public returns(uint256){
        // increase nonce
        randNonce++;
        return uint256(sha256(abi.encodePacked(block.timestamp,msg.sender,randNonce)));
    }

    function rand_index(uint256 len) public returns(uint256){
        randNonce++;
        return uint256(sha256(abi.encodePacked(block.timestamp,msg.sender,randNonce))) % len;
    }

    function rand_num_of_co_rings_in_fractal_ring() public returns (uint){
        randNonceFrac++;
        uint result = uint(sha256(abi.encodePacked(block.timestamp,msg.sender,randNonceFrac))) % 2000;
        if(result < 500){
            result += 500;
        }
        return result;
    }

    function generate_service_coin(int amount_based_on_one_unit ) public{
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return;
        }
        uint256 coin_id = rand_id();
        uint256[] memory bindings;
        uint256 x = 0;
        service_coin_table_map[coin_id] = CoinTable(coin_id, amount_based_on_one_unit, "ready", "service", 0, 0, x, bindings, bindings, id);
        service_coin_table_ids.push(coin_id);
        broadcast(broadcast_addr).adding_service_coin(coin_id, address(this));
    }

    function generate_invest_coin(int amount_based_on_one_unit) public{
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return;
        }
        uint256 coin_id = rand_id();
        uint256[] memory bindings;
        invest_coin_table_map[coin_id] = CoinTable(coin_id, amount_based_on_one_unit, "ready", "invest", 0, 0, 0, bindings, bindings, id);
        invest_coin_table_ids.push(coin_id);
        broadcast(broadcast_addr).adding_invest_coin(coin_id, address(this));
    }

    function compare(string memory str1, string memory str2) public pure returns (bool) {
        return keccak256(abi.encodePacked(str1)) == keccak256(abi.encodePacked(str2));
    }

    uint256[] private coin_ids_randomly_picked; 

    function generate_co_op_ring(uint256 coin_instance_id, string memory coin_type) public {
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return;
        }
        bool is_invest = (compare("invest", coin_type)) ? true : false;
        CoinTable memory coin_table = is_invest ? invest_coin_table_map[coin_instance_id] : service_coin_table_map[coin_instance_id];
        int num_of_group_members = 0;
        int amount_based_on_one_unit = coin_table.amount_based_on_one_unit;
        while(amount_based_on_one_unit > 0){
            num_of_group_members++;
            uint256 cid = is_invest ? broadcast(broadcast_addr).get_invest_coin_table_by_id_uar() : broadcast(broadcast_addr).get_service_coin_table_by_id_uar();
            coin_ids_randomly_picked.push(cid);
            amount_based_on_one_unit -=  (is_invest ? coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(cid)).get_amount_b_o_invest_coin_by_id(cid)
                :  coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(cid)).get_amount_b_o_service_coin_by_id(cid));
        }
        // the coin wants to bind the coins on itself but the final decision is on the verification team
        if(is_invest)
            coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(coin_instance_id)).set_bindings_invest_coin(coin_instance_id, coin_ids_randomly_picked);
        else
            coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(coin_instance_id)).set_bindings_service_coin(coin_instance_id, coin_ids_randomly_picked);
        uint256 g_id = rand_id();
        broadcast(broadcast_addr).insert_co_ring_table(id, g_id, address(this));
        co_op_rings_map[g_id] = CoOperationTable(g_id, num_of_group_members, coin_table.amount_based_on_one_unit, 0, 0, coin_table.coin_id,
         sha256(bytes(abi.encodePacked(coin_table.status,' ',coin_table.type_of_coin))), 1, "ready");
        delete coin_ids_randomly_picked;
    }

    mapping (uint256 => address[]) private ver_team_ids_trader_was_a_member_of;
    mapping (uint256 => uint256[]) private co_rings_of_frac_rings_received;
    mapping (uint256 => bool) private votes_to_f_ids;

    function get_vote_from_address(uint256[] memory co_ring_ids, address[] memory v_team_ids, uint256 f_id) external returns (uint256) {
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return 0;
        }
        votes_to_f_ids[f_id] = false;
        ver_team_ids_trader_was_a_member_of[f_id] = v_team_ids;
        for(uint256 i = 0; i < co_ring_ids.length; i++ /*table in frac_ring_and_id[0]*/){
            CoOperationTable memory co_op = co_op_ring_owner(broadcast(broadcast_addr).get_co_ring_table(co_ring_ids[i])).get_co_op_ring(co_ring_ids[i]);
            uint256[] memory cids_binded_on = coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(co_op.trader_coin_id)).coin_ids_binded_on(co_op.trader_coin_id);
            for(uint256 j = 0; j < cids_binded_on.length; j++){
                if(compare(coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(cids_binded_on[j])).status_of(cids_binded_on[j]), "ready")){
                    return 0;
                }
                if(coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(co_op.trader_coin_id)).get_ara_amount() < co_op.weight){
                    return 0;
                }
            }
        }
        votes_to_f_ids[f_id] = true;
        return 1;
    }

    function end_of_round_check(uint256 f_id) external returns (uint256){
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return 0;
        }
        for(uint256 i = 0; i < co_rings_of_frac_rings_received[f_id].length; i++){
            CoOperationTable memory co_op = co_op_ring_owner(broadcast(broadcast_addr).get_co_ring_table(
                co_rings_of_frac_rings_received[f_id][i])).get_co_op_ring(co_rings_of_frac_rings_received[f_id][i]);
            uint256[] memory cids_binded_on = coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(
                co_op.trader_coin_id)).coin_ids_binded_on(co_op.trader_coin_id);
            for(uint256 j = 0; j < cids_binded_on.length; j++){
                if(!(coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(cids_binded_on[j])).service_received_or_not(cids_binded_on[j]) ||
                 coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(cids_binded_on[j])).service_provided_or_not(cids_binded_on[j]))){
                     votes_to_f_ids[f_id] = false;
                     return 0;
                 }
            }
        }
        votes_to_f_ids[f_id] = true;
        return 1;
    }

    function payment_check(uint256 f_id) external returns (uint256){
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return 0;
        }
        for(uint256 i = 0; i < co_rings_of_frac_rings_received[f_id].length; i++){
            CoOperationTable memory co_op = co_op_ring_owner(broadcast(broadcast_addr).get_co_ring_table(
                co_rings_of_frac_rings_received[f_id][i])).get_co_op_ring(co_rings_of_frac_rings_received[f_id][i]);
            uint256[] memory cids_binded_on = coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(
                co_op.trader_coin_id)).coin_ids_binded_on(co_op.trader_coin_id);
            for(uint256 j = 0; j < cids_binded_on.length; j++){
                if(!(coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(cids_binded_on[j])).payment_received_or_not(cids_binded_on[j]) ||
                 coin_owner(broadcast(broadcast_addr).get_coin_owner_address_by_id(cids_binded_on[j])).payment_provided_or_not(cids_binded_on[j]))){
                     votes_to_f_ids[f_id] = false;
                     return 0;
                 }
            }
        }
        votes_to_f_ids[f_id] = true;
        return 1;
    }

    function submit_fractal_ring(uint256[] memory result, uint256 len_of_ver_tream, uint256 votes, uint256 f_id) external{
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return;
        }
        if(votes < len_of_ver_tream / 2){
            return;
        }
        co_rings_of_frac_rings_received[f_id] = result;
    }

    function generate_a_fractal_ring() public {
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return;
        }
        // uint256 average_number_of_fractal_rings = 510; 
        uint rand_num_of_co_rings = rand_num_of_co_rings_in_fractal_ring();
        uint256[] memory co_ring_ids_to_submit = broadcast(broadcast_addr).get_co_rings_for_trader_id(id);
        uint256[] memory result = new uint256[](rand_num_of_co_rings);
        if(co_ring_ids_to_submit.length != 0){
            for(uint256 i = 0; i < co_ring_ids_to_submit.length; i++){
                if(result.length < rand_num_of_co_rings){
                    result[i] = co_ring_ids_to_submit[i];
                }
            }
        }
        uint256 len = broadcast(broadcast_addr).num_of_co_op_rings();
        for(uint256 i = result.length; i < rand_num_of_co_rings; i++){
            result[i] = broadcast(broadcast_addr).get_co_ring_id_by_index(rand_index(len));
        }
        len = broadcast(broadcast_addr).get_num_of_users();
        uint256 vt = rand_index(rand_num_of_co_rings) + 1000;
        uint256[] memory verification_team_memebers_ids = new uint256[](vt);
        for(uint256 i = 0; i < vt; i++){
            verification_team_memebers_ids[i] = broadcast(broadcast_addr).get_user_id_by_index(len);
        }
        address[] memory verification_team_memebers_addresses = broadcast(broadcast_addr).get_addresses_of(verification_team_memebers_ids);
        uint256 votes = 0;
        uint256 f_id = rand_id();
        for(uint256 i = 0; i < verification_team_memebers_addresses.length; i++){
           votes += verification_team_member(verification_team_memebers_addresses[i]).get_vote_from_address(result, verification_team_memebers_addresses, f_id);
        }
        for(uint256 i = 0; i < verification_team_memebers_ids.length; i++){
            verification_team_member(verification_team_memebers_addresses[i]).submit_fractal_ring(result, verification_team_memebers_ids.length, votes, f_id);
        }
    }

    function get_ara_amount() view external returns (int){
        return ara_amount;
    }
    function get_coin(uint256 cid, string memory coin_type) view external returns(CoinTable memory){
        bool is_invest = (compare("invest", coin_type)) ? true : false;
        if(is_invest){
            return invest_coin_table_map[cid];
        }
        return service_coin_table_map[cid];
    }
    function get_amount_b_o_invest_coin_by_id(uint256 cid) view external returns (int){
        return invest_coin_table_map[cid].amount_based_on_one_unit;
    }
    function get_amount_b_o_service_coin_by_id(uint256 cid) view external returns (int){
        return service_coin_table_map[cid].amount_based_on_one_unit;
    }
    function set_bindings_invest_coin(uint256 cid, uint256[] memory cids) external{
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return;
        }
        invest_coin_table_map[cid].coin_ids_binded_on = cids;
    }
    function set_bindings_service_coin(uint256 cid, uint256[] memory cids) external{
        if(broadcast(broadcast_addr).is_switched_to_lor() == false){
            return;
        }
        service_coin_table_map[cid].coin_ids_binded_on = cids;
    }
    function coin_ids_binded_on(uint256 cid) view external returns(uint256[] memory) {
        if(invest_coin_table_map[cid].coin_id > 0){
            return invest_coin_table_map[cid].coin_ids_binded_on;
        }
        return service_coin_table_map[cid].coin_ids_binded_on;
    }
    function status_of(uint256 cid) view external returns (string memory){
        if(invest_coin_table_map[cid].coin_id > 0){
            return invest_coin_table_map[cid].status;
        }
        return service_coin_table_map[cid].status;
    }

}