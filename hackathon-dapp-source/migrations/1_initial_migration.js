const Migrations = artifacts.require("Testament");

module.exports = function(deployer) {
  deployer.deploy(Migrations);
};
