const { task } = require("hardhat/config");
const { getContract } = require("./helpers");
const { getCode } = require("./helpers");
const { getNonce } = require("./helpers");
const { getGasPrice } = require("./helpers");

task("mint", "Mints from the NFT contract")
.addParam("address", "The address to receive a token")
.setAction(async function (taskArguments, hre) {
    const contract = await getContract("DinosWithBoots", hre);
    const nonce = await getNonce()
    const gasFee = await getGasPrice()

    const transactionResponse = await contract.mintTo(taskArguments.address, {
        gasPrice: gasFee, 
        nonce: nonce
    });

    console.log(`Transaction Hash: ${transactionResponse.hash}`);
});

task("code", "Gets code of the contract")
.addParam("contract", "The contract address")
.setAction(async function (taskArguments, hre) {    
    let codeOfContract = await getCode(taskArguments.contract, hre)
    console.log(`Code of contract: ${codeOfContract}`);
});

task("set-base-token-uri", "Sets the base token URI for the deployed smart contract")
.addParam("baseUrl", "The base of the tokenURI endpoint to set")
.setAction(async function (taskArguments, hre) {
    const contract = await getContract("DinosWithBoots", hre);
    const transactionResponse = await contract.setBaseTokenURI(taskArguments.baseUrl, {
        gasLimit: 500_000,
    });
    console.log(`Transaction Hash: ${transactionResponse.hash}`);
});

task("token-uri", "Fetches the token metadata for the given token ID")
.addParam("tokenId", "The tokenID to fetch metadata for")
.setAction(async function (taskArguments, hre) {
    const contract = await getContract("DinosWithBoots", hre);
    const response = await contract.tokenURI(taskArguments.tokenId, {
        gasLimit: 500_000,
    });
    
    const metadata_url = response;
    console.log(`Metadata URL: ${metadata_url}`);

    const metadata = await fetch(metadata_url).then(res => res.json());
    console.log(`Metadata fetch response: ${JSON.stringify(metadata, null, 2)}`);
});