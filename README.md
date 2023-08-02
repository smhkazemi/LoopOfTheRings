# Loop of the Rings (LoR) - Vanilla Version
The Vanilla Version allows the readers to execute their desiered choice of scenario on the LoR's simulation. Note that it has zero users registered. As we provide a simulation of the LoR using smart contracts, the readers need to deploy them using [Avalanche](https://docs.avax.network/). It requirs creating an account on the Avalanche to obtain an address, also a private key. 

Note that the folder "Videos" contains short videos of running the simulation. But, the readers can feel free to try running the simulation by themselves. Before running the simulation, make sure you have the Python 3.10.12, also Solc library and Web3 (both on python) installed. The following would help you to install all the requirments:

pip install web3

sudo add-apt-repository ppa:ethereum/ethereum

sudo apt-get update

sudo apt-get install solc

sudo apt-get upgrade solc

solc-select install 0.8.21

solc-select use 0.8.21

solc --evm-version shanghai initiator.sol

python3 main.py # NB: This will run the simulation
