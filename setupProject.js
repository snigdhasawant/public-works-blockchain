
import { JsonRpcProvider, Contract } from "ethers";
import { readFileSync } from "fs";

async function main() {
    const provider = new JsonRpcProvider("http://127.0.0.1:8545");

    const accounts = await provider.send("eth_accounts", []);

    const admin = await provider.getSigner(accounts[0]);

    const abi = JSON.parse(
        readFileSync("./artifacts/contracts_PublicWorks_sol_PublicWorks.abi", "utf8")
    );

    const contractAddress = "0x229fde4D8081Cb25101f6fD13068444f25382e53";
    const works = new Contract(contractAddress, abi, admin);

    const contractor = accounts[1];
    const officer = accounts[2];

    // Register Officer
    console.log("Registering Officer...");
    const officerTx = await works.setOfficer(officer, true);
    await officerTx.wait();

    // Create Project
    console.log("Creating Village Road Project...");

    const names = [
        "Land Preparation",
        "Foundation Work",
        "Road Construction",
        "Final Inspection"
    ];

    const amounts = [200000, 100000, 400000, 300000];

    const projectTx = await works.createProject(
        1,
        contractor,
        1000000,
        names,
        amounts
    );

    await projectTx.wait();

    console.log("Officer registered successfully!");

    const summary = await works.getProjectSummary(1);

    console.log("Project created successfully!");
    console.log("Contractor:", summary[0]);
    console.log("Total Budget:", summary[1].toString());
    console.log("Released Amount:", summary[2].toString());
    console.log("Remaining Budget:", summary[3].toString());
    console.log("Milestone Count:", summary[4].toString());
}

main().catch(console.error);
