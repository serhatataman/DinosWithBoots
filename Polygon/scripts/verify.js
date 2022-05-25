const { ethers } = require("hardhat");
require("dotenv").config({ path: ".env" });
require("@nomiclabs/hardhat-etherscan");

async function main() {
// Verify the contract after deploying
await hre.run("verify:verify", {
address: "0x070f7638fa7932048f6aba082c58cd353a992693",
constructorArguments: ["dinoswithboots","NFT"],
});
}

// Call the main function and catch if there is any error
main()
.then(() => process.exit(0))
.catch((error) => {
console.error(error);
process.exit(1);
});