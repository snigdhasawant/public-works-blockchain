
import { JsonRpcProvider, Contract } from "ethers";
import { readFileSync } from "fs";

async function main() {
    const provider = new JsonRpcProvider("http://127.0.0.1:8545");

    const accounts = await provider.send("eth_accounts", []);
    const officer = await provider.getSigner(accounts[2]);

    const abi = JSON.parse(
        readFileSync(
            "./artifacts/contracts_PublicWorks_sol_PublicWorks.abi",
            "utf8"
        )
    );

    const contractAddress =
        "0x229fde4D8081Cb25101f6fD13068444f25382e53";

    const works = new Contract(contractAddress, abi, officer);

    console.log("Officer approving Land Preparation...");

    const tx = await works.reviewMilestone(1, 1, true);
    await tx.wait();

    console.log("Milestone approved!");

    const summary = await works.getProjectSummary(1);
    const milestone = await works.getMilestone(1, 0);

    console.log("Milestone:", milestone[0]);
    console.log("Status:", milestone[2].toString());
    console.log("Released Amount:", summary[2].toString());
    console.log("Remaining Budget:", summary[3].toString());
}

main().catch(console.error);

