
import { JsonRpcProvider, Contract, keccak256, toUtf8Bytes } from "ethers";
import { readFileSync } from "fs";

async function main() {
    const provider = new JsonRpcProvider("http://127.0.0.1:8545");

    const accounts = await provider.send("eth_accounts", []);
    const contractor = await provider.getSigner(accounts[1]);

    const abi = JSON.parse(
        readFileSync("./artifacts/contracts_PublicWorks_sol_PublicWorks.abi", "utf8")
    );

    const contractAddress = "0x229fde4D8081Cb25101f6fD13068444f25382e53";
    const works = new Contract(contractAddress, abi, contractor);

    // Generate sample proof hash
    const proofHash = keccak256(toUtf8Bytes("Land Preparation Completed"));

    console.log("Contractor submitting completion request...");

    const tx = await works.submitCompletion(1, 1, proofHash);
    await tx.wait();

    console.log("Completion request submitted!");

    const milestone = await works.getMilestone(1, 1);

    console.log("Milestone:", milestone[0]);
    console.log("Amount:", milestone[1].toString());
    console.log("Status:", milestone[2].toString());
    console.log("Proof Hash:", milestone[3]);
}

main().catch(console.error);
