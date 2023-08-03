# Loop of the Rings (LoR) - Vanilla Version

The Vanilla Version allows the readers to execute their desired choice of scenario on the LoR's simulation. Note that it has zero users registered. Also, the <u>service<u>, as discussed in the LoR paper, is considered here as a dummy action. This is particularly to remove extra gas consumption and keep the focus on the details of the system. As we provide a simulation of the LoR using smart contracts, the readers need to deploy them using [Avalanche](https://docs.avax.network/). It requires having an address, also a private key. To do so, you must create a [MetaMask](https://metamask.io/) account. Then, you can connect MetaMask to Avalanche, as appeared [here](https://support.avax.network/en/articles/4626956-how-to-connect-metamask-to-avalanche). Note that you will need the chainId and the private key later. To deploy the smart contract, you may use the [RPC Gatway to Avalanche](https://avalanche-c-chain.publicnode.com/). You can either pick the Mainnet or the Testnet. In order to get a faucet for AVAX (i.e. the Avalanche cryptocurrency), please visit [here](https://support.avax.network/en/articles/6110239-is-there-an-avax-faucet) for more details. Further, to learn about the implementation details of the smart contracts we developed for LoR's simulation, please refer to the technical report (pdf file) in this repository.

Note that the folder "Videos" contains short videos of running the simulation. But, the readers can feel free to try running the simulation for themselves. Before running the simulation, make sure you have Python 3.10.12, also Solc library, and Web3 (both on Python) installed. The following would help you to install all the requirements:

pip install web3

sudo add-apt-repository ppa:ethereum/ethereum

sudo apt-get update

sudo apt-get install solc

sudo apt-get upgrade solc

solc-select install 0.8.21

solc-select use 0.8.21

solc --evm-version shanghai initiator.sol

python3 main.py # NB: This will run the simulation
