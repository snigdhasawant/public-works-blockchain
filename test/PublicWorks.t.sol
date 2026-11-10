
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../contracts/PublicWorks.sol";

contract PublicWorksTest {

    PublicWorks public works;

    function setUp() public {
        works = new PublicWorks();

        works.setOfficer(address(this), true);

        string[] memory names = new string[](4);
        uint256[] memory amounts = new uint256[](4);

        names[0] = "Land Preparation";
        names[1] = "Foundation Work";
        names[2] = "Road Construction";
        names[3] = "Final Inspection";

        amounts[0] = 200000;
        amounts[1] = 100000;
        amounts[2] = 400000;
        amounts[3] = 300000;

        works.createProject(
            1,
            address(this),
            1000000,
            names,
            amounts
        );
    }

    function testProjectCreation() public view {
        (
            ,
            uint256 total,
            uint256 released,
            uint256 remaining,
            uint256 count
        ) = works.getProjectSummary(1);

        require(total == 1000000, "Wrong budget");
        require(released == 0, "Initial release must be zero");
        require(remaining == 1000000, "Wrong remaining budget");
        require(count == 4, "Wrong milestone count");
    }

    function testMilestoneApproval() public {
        bytes32 proof = keccak256("demo proof");

        works.submitCompletion(1, 0, proof);
        works.reviewMilestone(1, 0, true);

        (
            ,
            ,
            PublicWorks.Status status,
            ,
            ,

        ) = works.getMilestone(1, 0);

        require(
            status == PublicWorks.Status.Released,
            "Milestone not released"
        );

        (
            ,
            ,
            uint256 released,
            uint256 remaining,

        ) = works.getProjectSummary(1);

        require(released == 200000, "Wrong released amount");
        require(remaining == 800000, "Wrong remaining amount");
    }

    function testMilestoneRejection() public {
        bytes32 proof = keccak256("demo proof");

        works.submitCompletion(1, 0, proof);
        works.reviewMilestone(1, 0, false);

        (
            ,
            ,
            PublicWorks.Status status,
            ,
            ,

        ) = works.getMilestone(1, 0);

        require(
            status == PublicWorks.Status.Rejected,
            "Milestone not rejected"
        );

        (
            ,
            ,
            uint256 released,
            uint256 remaining,

        ) = works.getProjectSummary(1);

        require(released == 0, "Funds should not be released");
        require(remaining == 1000000, "Wrong remaining budget");
    }
}
