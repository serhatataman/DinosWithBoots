const { ethers } = require("ethers");
const { web3 } = require("@nomiclabs/hardhat-web3");
const { getContractAt } = require("@nomiclabs/hardhat-ethers/internal/helpers");

// Helper method for fetching environment variables from .env
function getEnvVariable(key, defaultValue) {
    if (process.env[key]) {
        return process.env[key];
    }
    if (!defaultValue) {
        throw `${key} is not defined and no default value was provided`;
    }
    return defaultValue;
}

// Helper method for fetching a connection provider to the Ethereum network
function getProvider() {
    let url = "https://polygon-rpc.com/";
    const dic_net = {
        name: 'polygon',
        chainId: 137,
        _defaultProvider: (providers) => new providers.JsonRpcProvider(url)
    };
    
    //ethers.providers.AlchemyProvider()

    //const provider = ethers.getDefaultProvider(dic_net);
    return ethers.getDefaultProvider(dic_net, {
        alchemy: getEnvVariable("ALCHEMY_KEY"),
    });
}

// Helper method for fetching a wallet account using an environment variable for the PK
function getAccount() {
    return new ethers.Wallet(getEnvVariable("ACCOUNT_PRIVATE_KEY"), getProvider());
}

// Helper method for fetching a contract instance at a given address
function getContract(contractName, hre) {
    const account = getAccount();
    return getContractAt(hre, contractName, getEnvVariable("NFT_CONTRACT_ADDRESS"), account);
}

async function getCode(contractAddress, hre) {
    var smth = await web3.eth.getCode(contractAddress);

    return smth;
}

async function getGasPrice() {
    let provider = getProvider()
    let feeData = await provider.getFeeData()
    return feeData.gasPrice
}

async function getChain() {
    let provider = getProvider()
    let chainId = await provider.getNetwork()
    return chainId.chainId
}

async function getNonce() {
    let signer = getAccount()
    return await signer.getTransactionCount()
}

module.exports = {
    getEnvVariable,
    getProvider,
    getAccount,
    getContract,
    getCode,
    getGasPrice,
    getChain,
    getNonce
}