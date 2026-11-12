
import { JsonRpcProvider, Contract } from "ethers";
import { readFileSync } from "fs";

async function main() {
    const provider = new JsonRpcProvider("http://127.0.0.1:8545");

    const accounts = await provider.send("eth_accounts", []);

    const abi = JSON.parse(
        readFileSync(
            "./artifacts/contracts_PublicWorks_sol_PublicWorks.abi",
            "utf8"
        )
    );

    const contractAddress =
        "0x229fde4D8081Cb25101f6fD13068444f25382e53";

    const roles = [
        { name: "Citizen", index: 3 },
        { name: "Contractor", index: 1 }
    ];

    for (const role of roles) {
        const signer = await provider.getSigner(accounts[role.index]);
        const works = new Contract(contractAddress, abi, signer);

        console.log(`Testing ${role.name} permissions...`);

        try {
            await works.reviewMilestone.staticCall(1, 0, true);
            console.log("FAILED: Unauthorized approval allowed!");
        } catch (error) {
            console.log("PASSED: Access denied to", role.name);
        }
    }
}

main().catch(console.error);
