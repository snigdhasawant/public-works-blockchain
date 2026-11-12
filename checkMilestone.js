
import { JsonRpcProvider, Contract } from "ethers";
import { readFileSync } from "fs";

async function main() {
    const provider = new JsonRpcProvider("http://127.0.0.1:8545");

    const abi = JSON.parse(
        readFileSync(
            "./artifacts/contracts_PublicWorks_sol_PublicWorks.abi",
            "utf8"
        )
    );

    const contractAddress =
        "0x229fde4D8081Cb25101f6fD13068444f25382e53";

    const works = new Contract(contractAddress, abi, provider);

    const milestone = await works.getMilestone(1, 1);

    console.log("Milestone:", milestone[0]);
    console.log("Amount:", milestone[1].toString());
    console.log("Status:", milestone[2].toString());
    console.log("Proof Hash:", milestone[3]);
}

main().catch(console.error);

