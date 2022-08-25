# Youves indexer

Tool used to indexed youves important contracts and not only. It comes with a GraphQL API used by the youves frontend. Furthermore it reads the data and plots it in grafana. 

## Usage
We recommend running the indexer in a docker container in vscode using the provided **.devcontainer**. This will ease the installation of all dependencies.

To run the indexer:
- ```./starter.sh mainnet``` to run the mainnet indexer.
- ```./starter.sh testnet``` to run the testnet indexer