
from web3 import Web3
import json
import config


class Blockchain:

    def __init__(self):
        self.w3 = Web3(
            Web3.HTTPProvider(config.BLOCKCHAIN_URL)
        )

        if not self.w3.is_connected():
            raise Exception("Ganache connection failed!")

        with open(config.ABI_PATH, "r") as file:
            self.abi = json.load(file)

        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(
                config.CONTRACT_ADDRESS
            ),
            abi=self.abi
        )

    def get_accounts(self):
        return self.w3.eth.accounts

    def get_project_summary(self, project_id):
        return self.contract.functions.getProjectSummary(
            project_id
        ).call()

    def get_milestone(self, project_id, milestone_index):
        return self.contract.functions.getMilestone(
            project_id,
            milestone_index
        ).call()

    def submit_completion(self, account, project_id, milestone_index, proof_hash):
        account = Web3.to_checksum_address(account)

        tx = self.contract.functions.submitCompletion(
            project_id,
            milestone_index,
            proof_hash
        ).transact({
            "from": account
        })

        return self.w3.eth.wait_for_transaction_receipt(tx)

    def review_milestone(self, account, project_id, milestone_index, approved):
        account = Web3.to_checksum_address(account)

        tx = self.contract.functions.reviewMilestone(
            project_id,
            milestone_index,
            approved
        ).transact({
            "from": account
        })

        return self.w3.eth.wait_for_transaction_receipt(tx)

    def get_transaction_history(self, project_id):
        transactions = []

        submitted_events = self.contract.events.CompletionSubmitted.get_logs(
            from_block=0,
            to_block="latest"
        )

        for event in submitted_events:
            args = event["args"]

            if args["projectId"] == project_id:
                block = self.w3.eth.get_block(event["blockNumber"])

                transactions.append({
                    "action": "Completion Submitted",
                    "milestone_index": args["milestoneIndex"],
                    "proof_hash": args["proofHash"].hex(),
                    "approved": None,
                    "transaction_hash": event["transactionHash"].hex(),
                    "block_number": event["blockNumber"],
                    "timestamp": block["timestamp"]
                })

        reviewed_events = self.contract.events.MilestoneReviewed.get_logs(
            from_block=0,
            to_block="latest"
        )

        for event in reviewed_events:
            args = event["args"]

            if args["projectId"] == project_id:
                block = self.w3.eth.get_block(event["blockNumber"])

                transactions.append({
                    "action": "Milestone Approved" if args["approved"] else "Milestone Rejected",
                    "milestone_index": args["milestoneIndex"],
                    "proof_hash": None,
                    "approved": args["approved"],
                    "transaction_hash": event["transactionHash"].hex(),
                    "block_number": event["blockNumber"],
                    "timestamp": block["timestamp"]
                })

        transactions.sort(
            key=lambda x: (x["block_number"], x["transaction_hash"])
        )

        return transactions

    def verify_transaction(self, transaction_hash):

        transaction_hash = transaction_hash.strip()

        if not transaction_hash.startswith("0x"):
            transaction_hash = "0x" + transaction_hash

        receipt = self.w3.eth.get_transaction_receipt(
            transaction_hash
        )

        transaction = self.w3.eth.get_transaction(
            transaction_hash
        )

        return {
            "status": receipt["status"],
            "block_number": receipt["blockNumber"],
            "from_address": transaction["from"],
            "to_address": transaction["to"],
            "gas_used": receipt["gasUsed"],
            "transaction_hash": transaction["hash"].hex()
        }
