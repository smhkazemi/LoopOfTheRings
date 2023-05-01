// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

/**
 * @title broadcast_sim

 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract broadcast_sim {   

    mapping (uint256 => address) internal coins;

    function get_coin_owner_address_by_id(uint256 id) view external returns(address) {
        return coins[id];
    }

    mapping (uint256 => address) internal service_coin_table_map;
    uint256[] internal service_coin_table_ids;

    // Function adding values to service_coin_table_map
    function adding_service_coin(uint256 coin_id, address corresponding_trader) external {
        service_coin_table_map[coin_id] = corresponding_trader;
        service_coin_table_ids.push(coin_id);
        coins[coin_id] = corresponding_trader;
    }
     
    function get_service_coin_table_by_id(uint256 id) view external returns (address) {
        return service_coin_table_map[id];
    }

    function get_service_coin_table_by_id_uar() view external returns (uint256){
        return service_coin_table_ids[uint256(keccak256(abi.encodePacked(block.timestamp,msg.sender,randNonce))) % service_coin_table_ids.length];
    }
    
    mapping (uint256 => address) internal invest_coin_table_map;
    uint256[] internal invest_coin_table_ids;

    // Function adding values to invest_coin_table_map
    function adding_invest_coin(uint256 coin_id, address corresponding_trader) external {
        if(!switched_to_lor){
            return;
        }
        invest_coin_table_map[coin_id] = corresponding_trader;
        invest_coin_table_ids.push(coin_id);
        coins[coin_id] = corresponding_trader;
    }
     
    function get_invest_coin_table_by_id(uint256 id) view external returns (address) {
        return invest_coin_table_map[id];
    }

    uint private randNonce = 0;

    function get_invest_coin_table_by_id_uar() view external returns (uint256){
        return invest_coin_table_ids[uint256(keccak256(abi.encodePacked(block.timestamp,msg.sender,randNonce))) % invest_coin_table_ids.length];
    }

    mapping (uint256 => address) internal co_operation_table_map;
    mapping (uint256 => uint256[]) internal trader_id_to_co_op_ring_ids;
    uint256[] internal co_op_ring_ids;

    function insert_co_ring_table(uint256 trader_id, uint256 g_id, address corresponding_trader) external {
        if(!switched_to_lor){
            return;
        }
        co_operation_table_map[g_id] = corresponding_trader;  
        co_op_ring_ids.push(g_id);
        trader_id_to_co_op_ring_ids[trader_id].push(g_id);
    }

    function num_of_co_op_rings() view external returns (uint256){
        return co_op_ring_ids.length;
    }

    function get_co_ring_id_by_index(uint256 index) view external returns (uint256){
        return co_op_ring_ids[index];
    }

    function get_co_rings_for_trader_id(uint256 t_id) view external returns (uint256[] memory){
        return trader_id_to_co_op_ring_ids[t_id];
    }

    function get_co_ring_table(uint256 g_id) view external returns (address){
        return co_operation_table_map[g_id];
    }

    mapping(uint256 => address) internal users_addresses;
    uint256[] internal user_ids;

    function add_new_user_by_address(address adr, uint256 id) external {
        if(!switched_to_lor){
            return;
        }
        user_ids.push(id);
        users_addresses[id] = adr;
    }

    function get_addresses_of(uint256[] memory v_team_ids) view external returns (address[] memory){
        address[] memory result = new address[](v_team_ids.length);
        if(!switched_to_lor){
            return result;
        }
        for(uint256 i = 0; i < v_team_ids.length; i++){
            result[i] = users_addresses[v_team_ids[i]];
        }
        return result;
    }

    function get_num_of_users() view external returns (uint256){
        return user_ids.length;
    }

    function get_user_id_by_index(uint256 idx) view external returns (uint256){
        return user_ids[idx];
    }

    function get_user(uint256 id) view external returns (address){
        return users_addresses[id];
    }
     
    bool internal switched_to_lor = false;

    function switch_to_lor() external{
        switched_to_lor = true;
    }

    function is_switched_to_lor() view external returns (bool){
        return switched_to_lor;
    }
    
}


