
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract PublicWorks {

    address public admin;

    mapping(address => bool) public officers;

    enum Status {
        NotStarted,
        Pending,
        Released,
        Rejected
    }

    struct Milestone {
        string name;
        uint256 amount;
        Status status;
        bytes32 proofHash;
        uint256 submittedAt;
        uint256 reviewedAt;
    }

    struct Project {
        bool exists;
        address contractor;
        uint256 totalBudget;
        uint256 releasedAmount;
        Milestone[] milestones;
    }

    mapping(uint256 => Project) private projects;

    event OfficerUpdated(address officer, bool status);

    event ProjectCreated(
        uint256 projectId,
        address contractor,
        uint256 totalBudget
    );

    event CompletionSubmitted(
        uint256 projectId,
        uint256 milestoneIndex,
        bytes32 proofHash
    );

    event MilestoneReviewed(
        uint256 projectId,
        uint256 milestoneIndex,
        bool approved
    );

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin allowed");
        _;
    }

    modifier onlyOfficer() {
        require(officers[msg.sender], "Only officer allowed");
        _;
    }

    function setOfficer(
        address officer,
        bool status
    ) external onlyAdmin {
        require(officer != address(0), "Invalid address");

        officers[officer] = status;

        emit OfficerUpdated(officer, status);
    }

    function createProject(
        uint256 projectId,
        address contractor,
        uint256 totalBudget,
        string[] calldata names,
        uint256[] calldata amounts
    ) external onlyAdmin {

        require(!projects[projectId].exists, "Project already exists");
        require(contractor != address(0), "Invalid contractor");
        require(totalBudget > 0, "Invalid budget");
        require(names.length > 0, "Add milestones");
        require(names.length == amounts.length, "Length mismatch");

        uint256 sum = 0;

        for (uint256 i = 0; i < amounts.length; i++) {
            require(amounts[i] > 0, "Invalid amount");
            sum += amounts[i];
        }

        require(sum == totalBudget, "Budget mismatch");

        Project storage p = projects[projectId];

        p.exists = true;
        p.contractor = contractor;
        p.totalBudget = totalBudget;

        for (uint256 i = 0; i < names.length; i++) {
            p.milestones.push(
                Milestone({
                    name: names[i],
                    amount: amounts[i],
                    status: Status.NotStarted,
                    proofHash: bytes32(0),
                    submittedAt: 0,
                    reviewedAt: 0
                })
            );
        }

        emit ProjectCreated(projectId, contractor, totalBudget);
    }

    function submitCompletion(
        uint256 projectId,
        uint256 milestoneIndex,
        bytes32 proofHash
    ) external {

        Project storage p = projects[projectId];

        require(p.exists, "Project not found");
        require(msg.sender == p.contractor, "Only contractor allowed");
        require(milestoneIndex < p.milestones.length, "Invalid milestone");

        Milestone storage m = p.milestones[milestoneIndex];

        require(
            m.status == Status.NotStarted ||
            m.status == Status.Rejected,
            "Invalid milestone status"
        );

        require(proofHash != bytes32(0), "Proof hash required");

        m.status = Status.Pending;
        m.proofHash = proofHash;
        m.submittedAt = block.timestamp;

        emit CompletionSubmitted(projectId, milestoneIndex, proofHash);
    }

    function reviewMilestone(
        uint256 projectId,
        uint256 milestoneIndex,
        bool approved
    ) external onlyOfficer {

        Project storage p = projects[projectId];

        require(p.exists, "Project not found");
        require(milestoneIndex < p.milestones.length, "Invalid milestone");

        Milestone storage m = p.milestones[milestoneIndex];

        require(m.status == Status.Pending, "Not awaiting review");

        m.reviewedAt = block.timestamp;

        if (approved) {
            require(
                p.releasedAmount + m.amount <= p.totalBudget,
                "Budget exceeded"
            );

            m.status = Status.Released;
            p.releasedAmount += m.amount;
        } else {
            m.status = Status.Rejected;
        }

        emit MilestoneReviewed(projectId, milestoneIndex, approved);
    }

    function getProjectSummary(
        uint256 projectId
    ) external view returns (
        address contractor,
        uint256 totalBudget,
        uint256 releasedAmount,
        uint256 remainingBudget,
        uint256 milestoneCount
    ) {

        Project storage p = projects[projectId];

        require(p.exists, "Project not found");

        return (
            p.contractor,
            p.totalBudget,
            p.releasedAmount,
            p.totalBudget - p.releasedAmount,
            p.milestones.length
        );
    }

    function getMilestone(
        uint256 projectId,
        uint256 index
    ) external view returns (
        string memory name,
        uint256 amount,
        Status status,
        bytes32 proofHash,
        uint256 submittedAt,
        uint256 reviewedAt
    ) {

        Project storage p = projects[projectId];

        require(p.exists, "Project not found");
        require(index < p.milestones.length, "Invalid milestone");

        Milestone storage m = p.milestones[index];

        return (
            m.name,
            m.amount,
            m.status,
            m.proofHash,
            m.submittedAt,
            m.reviewedAt
        );
    }
}
