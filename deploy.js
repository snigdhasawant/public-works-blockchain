
import { JsonRpcProvider, ContractFactory } from "ethers";
import { readFileSync } from "fs";

async function main() {
    // Connect to Ganache
    const provider = new JsonRpcProvider("http://127.0.0.1:8545");

    // Get Admin account
    const accounts = await provider.send("eth_accounts", []);
    const admin = await provider.getSigner(accounts[0]);

    // Read ABI and Bytecode
    const abi = JSON.parse(
        readFileSync("./artifacts/contracts_PublicWorks_sol_PublicWorks.abi", "utf8")
    );

    const bytecode =
        "0x" +
        readFileSync("./artifacts/contracts_PublicWorks_sol_PublicWorks.bin", "utf8").trim();

    // Deploy Smart Contract
    const factory = new ContractFactory(abi, bytecode, admin);

    console.log("Deploying PublicWorks contract...");

    const contract = await factory.deploy();
    await contract.waitForDeployment();

    const address = await contract.getAddress();

    console.log("Contract deployed successfully!");
    console.log("Contract Address:", address);
    console.log("Admin Address:", accounts[0]);
}

main().catch(console.error);
