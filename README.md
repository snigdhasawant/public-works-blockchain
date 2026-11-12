# Public Works Monitoring & Fund Tracking Using Blockchain

## Project Overview

Public Works Monitoring & Fund Tracking is a blockchain-based application designed to improve transparency and accountability in government public works projects.

The system uses a Solidity smart contract to manage project budgets, track milestone completion, and control fund release after officer approval.

## Objectives

- Improve transparency in public works fund management.
- Track project progress through milestones.
- Ensure funds are released only after authorized officer approval.
- Maintain proof hashes and transaction records on the blockchain.
- Prevent unauthorized access to project operations.

## User Roles

1. **Admin:** Registers officers and creates projects.
2. **Contractor:** Submits milestone completion requests with proof hashes.
3. **Officer:** Reviews submitted milestones and approves or rejects them.
4. **Citizen:** Represents the public stakeholder role.

## Key Features

- Officer registration by Admin.
- Project creation with a predefined budget.
- Multiple milestone management.
- Contractor completion submission.
- Proof hash recording.
- Officer approval and rejection.
- Resubmission of rejected milestones.
- Automatic released and remaining budget calculation.
- Role-based access control.

## Technologies Used

- Solidity
- JavaScript
- Ethers.js
- Ganache
- Node.js
- Solidity Compiler (solc)
- Git and GitHub
- Visual Studio Code

## Project Structure

```text
public-works-blockchain/
│
├── contracts/
│   └── PublicWorks.sol
│
├── artifacts/
├── test/
├── python/
│
├── compile.js
├── connection.js
├── deploy.js
├── setupProject.js
├── submitCompletion.js
├── approveMilestone.js
├── rejectMilestone.js
├── checkMilestone.js
├── verifySecurity.js
│
├── package.json
├── hardhat.config.ts
├── tsconfig.json
└── README.md
```

## Project Workflow

1. Admin deploys the smart contract.
2. Admin registers an authorized officer.
3. Admin creates a project with a total budget and milestones.
4. Contractor submits completion details and a proof hash.
5. Officer reviews the submitted milestone.
6. Officer approves or rejects the milestone.
7. If approved, the milestone amount is added to the released amount.
8. If rejected, the contractor can submit it again.
9. The system tracks the remaining project budget.

## Installation and Setup

Install dependencies:

```bash
npm install
```

Start Ganache local blockchain:

```bash
npx.cmd ganache --server.port 8545 --wallet.totalAccounts 10 --chain.chainId 1337
```

Compile the smart contract:

```bash
node compile.js
```

Deploy the contract:

```bash
node deploy.js
```

Run the project setup:

```bash
node setupProject.js
```

Other scripts can be executed to submit, approve, reject, and verify milestone operations.

## Testing

The following operations have been manually tested using JavaScript scripts and the local Ganache blockchain:

- Smart contract deployment.
- Project creation and budget allocation.
- Milestone completion submission.
- Milestone approval and rejection.
- Rejected milestone resubmission.
- Budget tracking.
- Unauthorized review attempts by Citizen and Contractor.

## Disclaimer

This project is an academic prototype. It uses a local blockchain network and simulated project funds. It does not transfer actual government funds.

## Future Scope

- Web-based dashboard for all user roles.
- Citizen access to project progress.
- Upload and verification of completion documents.
- Integration with a public blockchain network.

## Repository

[GitHub Repository](https://github.com/snigdhasawant/public-works-blockchain)