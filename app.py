
import streamlit as st
from blockchain import Blockchain
import config
from datetime import datetime

st.set_page_config(
    page_title="Public Works Monitoring",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Public Works Monitoring System")
st.caption(
    "Blockchain-Based Government Public Works Monitoring & Fund Tracking"
)

@st.cache_resource
def connect_blockchain():
    return Blockchain()


STATUS_NAMES = {
    0: "Not Started",
    1: "Submitted",
    2: "Approved",
    3: "Rejected"
}

try:
    blockchain = connect_blockchain()
    accounts = blockchain.get_accounts()

    st.success("Blockchain Connected Successfully")

    # SIDEBAR
    st.sidebar.title("Navigation")

    role = st.sidebar.selectbox(
        "Select User Role",
        ["Admin", "Contractor", "Officer", "Citizen"]
    )

    # PROJECT DATA
    summary = blockchain.get_project_summary(
        config.PROJECT_ID
    )

    total_budget = summary[1]
    released_amount = summary[2]
    remaining_budget = summary[3]
    total_milestones = summary[4]

    milestones = []

    for i in range(total_milestones):
        data = blockchain.get_milestone(
            config.PROJECT_ID, i
        )

        milestones.append({
            "index": i,
            "name": data[0],
            "amount": data[1],
            "status": data[2],
            "proof_hash": data[3]
        })

    # COMMON PROJECT OVERVIEW
    st.subheader("Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Budget", f"₹{total_budget:,}")
    col2.metric("Released Amount", f"₹{released_amount:,}")
    col3.metric("Remaining Budget", f"₹{remaining_budget:,}")

    st.divider()

    # ADMIN DASHBOARD
    if role == "Admin":

        st.header("👨‍💼 Admin Dashboard")

        st.write("Complete project monitoring and fund overview.")

        approved = sum(1 for m in milestones if m["status"] == 2)
        submitted = sum(1 for m in milestones if m["status"] == 1)
        rejected = sum(1 for m in milestones if m["status"] == 3)
        pending = sum(1 for m in milestones if m["status"] == 0)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Milestones", total_milestones)
        c2.metric("Approved", approved)
        c3.metric("Submitted", submitted)
        c4.metric("Pending", pending)

        st.subheader("All Milestone Records")

        for m in milestones:
            with st.expander(m["name"]):
                st.write(f"**Amount:** ₹{m['amount']:,}")
                st.write(f"**Status:** {STATUS_NAMES[m['status']]}")

                if m["status"] != 0:
                    st.code("0x" + m["proof_hash"].hex())

        st.subheader("Project Information")

        st.write("Project ID:", config.PROJECT_ID)
        st.write("Contract Address:", config.CONTRACT_ADDRESS)

        # TRANSACTION HISTORY
        st.divider()
        st.subheader("⛓️ Blockchain Transaction History")

        transactions = blockchain.get_transaction_history(
            config.PROJECT_ID
        )

        if not transactions:
            st.info("No transactions found.")

        else:
            history = []

            for tx in transactions:
                milestone_index = tx["milestone_index"]

                if milestone_index < len(milestones):
                    milestone_name = milestones[milestone_index]["name"]
                else:
                    milestone_name = f"Milestone {milestone_index}"

                timestamp = datetime.fromtimestamp(
                    tx["timestamp"]
                ).strftime("%d-%m-%Y %H:%M:%S")

                history.append({
                    "Milestone": milestone_name,
                    "Action": tx["action"],
                    "Block Number": tx["block_number"],
                    "Date & Time": timestamp,
                    "Transaction Hash": tx["transaction_hash"]
                })

            st.dataframe(
    history,
    width="stretch",
    hide_index=True
)

            st.caption(
                "All records are retrieved from blockchain event logs."
            )


            # TRANSACTION VERIFICATION
            st.divider()
            st.subheader("🔍 Verify Blockchain Transaction")

            tx_hash_input = st.text_input(
                "Enter Transaction Hash"
            )

            if st.button("Verify Transaction"):

                if not tx_hash_input.strip():
                    st.warning("Please enter a transaction hash.")

                else:
                    try:
                        result = blockchain.verify_transaction(
                            tx_hash_input.strip()
                        )

                        if result["status"] == 1:
                            st.success("Transaction Verified Successfully!")
                        else:
                            st.error("Transaction Failed.")

                        st.write("Block Number:", result["block_number"])
                        st.write("From Address:", result["from_address"])
                        st.write("To Address:", result["to_address"])
                        st.write("Gas Used:", result["gas_used"])

                        st.write("Transaction Hash:")
                        st.code(result["transaction_hash"])

                    except Exception:
                        st.error(
                            "Transaction not found. Please check the hash."
                        )

    # CONTRACTOR DASHBOARD
    elif role == "Contractor":

        st.header("👷 Contractor Dashboard")
        st.write("Submit completion details for project milestones.")

        for m in milestones:

            with st.expander(m["name"]):

                st.write(f"**Amount:** ₹{m['amount']:,}")
                st.write(f"**Status:** {STATUS_NAMES[m['status']]}")

                if m["status"] != 0:
                    st.code("0x" + m["proof_hash"].hex())

                if m["status"] in [0, 3]:

                    proof_details = st.text_area(
                        "Enter completion proof details",
                        key=f"proof_{m['index']}"
                    )

                    if st.button(
                        "Submit Completion",
                        key=f"submit_{m['index']}"
                    ):

                        if not proof_details.strip():
                            st.warning("Please enter proof details.")

                        else:
                            try:
                                proof_hash = blockchain.w3.keccak(
                                    text=proof_details
                                )

                                receipt = blockchain.submit_completion(
                                    accounts[config.CONTRACTOR_ACCOUNT_INDEX],
                                    config.PROJECT_ID,
                                    m["index"],
                                    proof_hash
                                )

                                st.success("Completion submitted successfully!")
                                st.code(receipt.transactionHash.hex())
                                st.rerun()

                            except Exception as e:
                                st.error(f"Submission failed: {e}")

    # OFFICER DASHBOARD
    elif role == "Officer":

        st.header("🧑‍💼 Officer Dashboard")
        st.write("Review contractor completion submissions.")

        submitted_milestones = [
            m for m in milestones if m["status"] == 1
        ]

        if not submitted_milestones:
            st.info("No milestones are waiting for approval.")

        for m in submitted_milestones:

            with st.expander(m["name"]):

                st.write(f"**Amount:** ₹{m['amount']:,}")
                st.write("**Status:** Submitted")
                st.write("**Proof Hash:**")
                st.code("0x" + m["proof_hash"].hex())

                col_a, col_b = st.columns(2)

                with col_a:

                    if st.button("Approve", key=f"approve_{m['index']}"):

                        try:
                            receipt = blockchain.review_milestone(
                                accounts[config.OFFICER_ACCOUNT_INDEX],
                                config.PROJECT_ID,
                                m["index"],
                                True
                            )

                            st.success("Milestone approved successfully!")
                            st.code(receipt.transactionHash.hex())
                            st.rerun()

                        except Exception as e:
                            st.error(f"Approval failed: {e}")

                with col_b:

                    if st.button("Reject", key=f"reject_{m['index']}"):

                        try:
                            receipt = blockchain.review_milestone(
                                accounts[config.OFFICER_ACCOUNT_INDEX],
                                config.PROJECT_ID,
                                m["index"],
                                False
                            )

                            st.warning("Milestone rejected.")
                            st.code(receipt.transactionHash.hex())
                            st.rerun()

                        except Exception as e:
                            st.error(f"Rejection failed: {e}")

    # CITIZEN DASHBOARD
    elif role == "Citizen":

        st.header("👥 Citizen Dashboard")

        st.write(
            "Public project progress and fund transparency."
        )

        approved = sum(1 for m in milestones if m["status"] == 2)
        submitted = sum(1 for m in milestones if m["status"] == 1)
        pending = sum(1 for m in milestones if m["status"] == 0)

        c1, c2, c3 = st.columns(3)

        c1.metric("Approved", approved)
        c2.metric("Submitted", submitted)
        c3.metric("Pending", pending)

        progress = (
            approved / total_milestones
            if total_milestones > 0 else 0
        )

        st.subheader("Overall Project Progress")
        st.progress(progress)

        st.write(
            f"{approved} out of {total_milestones} milestones approved"
        )

        st.subheader("Milestone Status")

        for m in milestones:
            with st.expander(m["name"]):
                st.write(f"**Amount:** ₹{m['amount']:,}")
                st.write(f"**Status:** {STATUS_NAMES[m['status']]}")

        st.subheader("Fund Transparency")

        st.write("Total Budget:", f"₹{total_budget:,}")
        st.write("Released Funds:", f"₹{released_amount:,}")
        st.write("Remaining Funds:", f"₹{remaining_budget:,}")

    # FOOTER
    st.divider()

    st.caption(
        "Public Works Monitoring System | Blockchain Powered"
    )

except Exception as e:
    st.error(f"Application Error: {e}")



# ---------------- CUSTOM UI DESIGN ----------------
