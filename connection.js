
import { JsonRpcProvider } from "ethers";

async function main() {
    const provider = new JsonRpcProvider("http://127.0.0.1:8545");

    const network = await provider.getNetwork();
    const accounts = await provider.send("eth_accounts", []);

    console.log("Connected to Ganache!");
    console.log("Chain ID:", network.chainId.toString());
    console.log("Accounts:", accounts.slice(0, 4));
}

main().catch(console.error);
