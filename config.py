
import os

# Blockchain connection
BLOCKCHAIN_URL = "http://127.0.0.1:8545"

# Smart Contract Address
CONTRACT_ADDRESS = "0x408E6EA829cc2B55405e32EfED38aB334d369CEA"

# ABI File Path
ABI_PATH = os.path.join(
    os.path.dirname(__file__),
    "artifacts",
    "contracts_PublicWorks_sol_PublicWorks.abi"
)

# Project Configuration
PROJECT_ID = 1

# Ganache Account Roles
ADMIN_ACCOUNT_INDEX = 0
CONTRACTOR_ACCOUNT_INDEX = 1
OFFICER_ACCOUNT_INDEX = 2
