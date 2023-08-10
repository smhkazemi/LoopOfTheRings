// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;
import "./trader.sol";

interface broadcast_interface{
    function switch_to_lor() external;
    function add_new_user_by_address(address adr, uint256 id, address v_address) external;
}

contract initiator{
    uint private randNonce = 0;
    uint256 private num_of_traders_signed_up;
    uint256 private threshold_of_switching_to_lor;
    address private broadcast_addr;

    constructor(address b_address, uint256 t) {
        num_of_traders_signed_up = 0;
        broadcast_addr = b_address;
        threshold_of_switching_to_lor = t;
    }

    function rand_id() private returns(uint256)
    {
        // increase nonce
        randNonce++;
        return uint256(sha256(abi.encodePacked(block.timestamp,msg.sender,randNonce)));
    }

    // The admin desires to signup a new trader
    function sign_up(int ara, address v_address) external returns(address){
        if(num_of_traders_signed_up >= threshold_of_switching_to_lor){
            return address(0x0);
        }
        uint256 trader_id = rand_id();
        Trader trader = new Trader(trader_id, ara, broadcast_addr, v_address);
        num_of_traders_signed_up++;
        if(num_of_traders_signed_up >= threshold_of_switching_to_lor){
            broadcast_interface(broadcast_addr).switch_to_lor();
        }
        broadcast_interface(broadcast_addr).add_new_user_by_address(address(trader), trader_id, v_address);
        return address(trader);
    }

    function get_broadcast_address() view external returns (address){
        return broadcast_addr;
    }
    
}


