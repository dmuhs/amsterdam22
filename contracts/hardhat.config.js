require("@nomiclabs/hardhat-waffle");
require('dotenv').config();

const infuraSecret = process.env.INFURA_SECRET;
if (!infuraSecret) {
  throw new Error("Please set your Infura secret in a .env file");
}

const deployerPrivateKey = process.env.DEPLOYER_PRIVATE_KEY;
if (!deployerPrivateKey) {
  throw new Error("Private key not set in .env file")
}

// You need to export an object to set up your config
// Go to https://hardhat.org/config/ to learn more

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: "0.8.4",
  defaultNetwork: "mumbai",
  networks: {
    mumbai: {
      url: `https://polygon-mumbai.infura.io/v3/${infuraSecret}`,
      accounts: [deployerPrivateKey]
    }
  }
};
