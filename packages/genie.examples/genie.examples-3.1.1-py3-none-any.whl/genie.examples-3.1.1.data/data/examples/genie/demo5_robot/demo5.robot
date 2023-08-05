# Demo Script to verify sanity of network

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        ats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot


*** Variables ***
# Defining variables that can be used elsewhere in the test data. 
# Can also be driven as dash argument at runtime

# Define the pyATS testbed file to use for this run
${testbed}     virl.yaml 

*** Test Cases ***
# Creating test cases from available keywords.

Initialize
    # Initializes the pyATS/Genie Testbed
    # pyATS Testbed can be used within pyATS/Genie
    use genie testbed "${testbed}"

    # Connect to both device
    connect to device "uut"
    connect to device "helper"

Verify Ping from uut to helper
    run testcase     examples.genie.demo5_robot.pyats_loopback_reachability.NxosPingTestcase    device=uut
Verify Ping from helper to uut
    run testcase     examples.genie.demo5_robot.pyats_loopback_reachability.PingTestcase    device=helper

# Verify Bgp Neighbors
Verify the counts of Bgp 'established' neighbors for uut&helper
    verify count "1" "bgp neighbors" on device "uut"
    verify count "1" "bgp neighbors" on device "helper"

# Verify Bgp Routes
# Tags can be used to control the behavior of the tests, noncritical tests which
# fail, will not cause the entire job to fail

Verify the counts of Bgp routes for uut&helper
    [Tags]    noncritical
    verify count "2" "bgp routes" on device "uut"
    verify count "2" "bgp routes" on device "helper"

# Verify OSPF neighbor counts
Verify the counts of Ospf 'full' neighbors for uut&helper
    verify count "2" "ospf neighbors" on device "uut"
    verify count "2" "ospf neighbors" on device "helper"

# Verify Interfaces
Verify the counts of 'up' Interace for uut&helper
    verify count "5" "interface up" on device "uut"
    verify count "5" "interface up" on device "helper"

Profile bgp & ospf on uut
    Profile the system for "bgp;ospf" on devices "uut" as "snap1"

verify Bgp Nexthop Database before trigger sleep
    run verification "Verify_BgpAllNexthopDatabase" on device "uut"

Trigger sleep
    run trigger "TriggerSleep" on device "uut" using alias "cli"

verify Bgp Nexthop Database after trigger sleep
    run verification "Verify_BgpAllNexthopDatabase" on device "uut"

Profile bgp & ospf on uut, Compare it with previous snapshot
    Profile the system for "bgp;ospf" on devices "uut" as "snap2"
    Compare profile "snap2" with "snap1" on devices "uut"

