# LoopOfTheRings
Please refer to the techincal report pdf file in the repository for more details.
Before running the simulation, make sure you have the Python 3.10.12, also Solc library and Web3 (both on python) installed. 
The following would help you to install all the requirments:

pip install web3

sudo add-apt-repository ppa:ethereum/ethereum

sudo apt-get update

sudo apt-get install solc

sudo apt-get upgrade solc

solc-select install 0.8.21

solc-select use 0.8.21

solc --evm-version shanghai initiator.sol

python3 main.py # NB: This will run the simulation
