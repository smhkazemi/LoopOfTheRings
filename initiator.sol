// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;
import "./trader.sol";
import "./broadcast_sim.sol";

interface broadcast_interface{
    function switch_to_lor() external;
    function add_new_user_by_address(address adr, uint256 id) external;
}

contract initiator{
    mapping (uint256 => address) private traders;
    uint private randNonce = 0;
    bool private swtiched_to_lor;
    int private num_of_traders_signed_up;
    address private broadcast_addr;

    constructor(){
        swtiched_to_lor = false;
        num_of_traders_signed_up = 0;
        broadcast_addr = address(new broadcast_sim());
    }

    function rand_id() private returns(uint256)
    {
        // increase nonce
        randNonce++;
        return uint256(sha256(abi.encodePacked(block.timestamp,msg.sender,randNonce)));
    }

    // The admin desires to signup a new trader
    function sign_up(int ara) external returns(address){
        if(swtiched_to_lor == true){
            return address(0x0);
        }
        uint256 trader_id = rand_id();
        Trader trader = new Trader(trader_id, ara, broadcast_addr);
        num_of_traders_signed_up++;
        if(num_of_traders_signed_up >= 1000000){
            swtiched_to_lor = true;
            broadcast_interface(broadcast_addr).switch_to_lor();
        }
        broadcast_interface(broadcast_addr).add_new_user_by_address(address(trader), trader_id);
        traders[trader_id] = address(trader);
        return traders[trader_id];
    }

    function get_brroadcast_address() view external returns (address){
        return broadcast_addr;
    }
}


