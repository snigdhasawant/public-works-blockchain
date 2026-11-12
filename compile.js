
import solc from "solc";
import { readFileSync, writeFileSync, mkdirSync } from "fs";

const source = readFileSync("./contracts/PublicWorks.sol", "utf8");

const input = {
    language: "Solidity",
    sources: {
        "PublicWorks.sol": {
            content: source
        }
    },
    settings: {
        evmVersion: "paris",
        outputSelection: {
            "*": {
                "*": ["abi", "evm.bytecode.object"]
            }
        }
    }
};

const output = JSON.parse(solc.compile(JSON.stringify(input)));

if (output.errors) {
    for (const error of output.errors) {
        console.log(error.formattedMessage);
    }

    if (output.errors.some(e => e.severity === "error")) {
        process.exit(1);
    }
}

const contract = output.contracts["PublicWorks.sol"]["PublicWorks"];

mkdirSync("./artifacts", { recursive: true });

writeFileSync(
    "./artifacts/contracts_PublicWorks_sol_PublicWorks.abi",
    JSON.stringify(contract.abi, null, 2)
);

writeFileSync(
    "./artifacts/contracts_PublicWorks_sol_PublicWorks.bin",
    contract.evm.bytecode.object
);

console.log("Contract compiled successfully!");
console.log("EVM Version: Paris");

