# RCV-Synthesis

Complimentary models for the article 'Formal Synthesis of Safe Stop Tactical Planners for an Automated Vehicle' by [Jonas Krook](https://www.chalmers.se/en/staff/Pages/krookj.aspx), [Roozbeh Kianfar](https://scholar.google.se/citations?user=OJH6u0MAAAAJ&hl=en), and [Martin Fabian](https://www.chalmers.se/en/staff/Pages/martin-fabian.aspx).

This repository contains [Supremica](https://supremica.org/) and [TuLiP](https://github.com/tulip-control/tulip-control) models for synthesiszing a controller for an automated vehicle.

This work is a continuation of an earlier research [project](https://github.com/krooken/wasp-des-rcv) named ['Design and Formal Verification of a Safe Stop Supervisor for an Automated Vehicle'](https://ieeexplore.ieee.org/document/8793636).

## Mission

The scenario considered is a transport mission where an automated vehicle is initially parked in a parking spot in parking lot A, and receives a mission goal where it needs to drive to and park in a goal parking spot in parking lot B. To do this, it first has to plan a path connecting the two parking lots via the road network. The start and end point of this path is called transition point 1 and 2 (Tp1 and Tp2), respectively. Then the vehicle needs to generate a path from a point in A to Tp1. When it arrives at parking lot B it needs to construct a path from Tp2 on the road to the goal parking spot in B.

The task of the synthesized planners is to complete the transport mission safely. Therefore the vehicle needs a safe backup solution if a system degradation occurs. One such backup solution is a *minimal risk maneuver*. When a safety critical system becomes degraded, the task of a minimal risk maneuver is to swiftly bring the automated vehicle to a *minimal risk condition*, which is supposed to be a safe state where the risk of harm or damage is minimal.

Available to the tactical planners to complete the transport mission safely are several subsystems. The different subsystems provide the following services:
- The localization subsystem uses a GPS sensor to position the \RCV in a global map. It is also responsible for sending the goal position to the tactical planner. If the GPS sensor experiences a failure the localization subsystem cannot perform these tasks anymore and indicates this to the tactical planner.
- The Trajectory Planner (TP) receives a path from the tactical planner and generates *trajectories* of speeds and yaw angles by considering the vehicle dynamics and physical limits of the vehicle. The trajectory planner also plans a stop at the end of the current path.
- The Structured Area Path Planner (SPP) and Unstructured Area Path Planner (UPP) plan the paths from the starting spot to the goal spot.
- The Safe Stop Trajectory Planner (SSTP) plans minimal risk maneuvers and keeps them up to date.
- The Controller receives commands from three sources: TP, SSTP, and the tactical planner. The nominal operation is to execute the trajectories from TP, but depending on the mode sent by the tactical planner the controller either executes the minimal risk maneuver, or applies the brakes as hard as possible, referred to as *Automatic Emergency Braking* (AEB).

## Models

The synthesis is performed for a simplified scenario where Tp1 and Tp2 are not considered. The name UPP2, which would be both the path connecting Tp2 with the goal and the software component responsible for the generation of that path, is here used as it would be the path from the initial spot in A to the goal spot in B.

The [supremica](supremica/) folder and the [tulip](tulip/) folder contain Supremica and TuLiP models. The files named supervisor_synthesis produce tactical planners where the localization, UPP2, SSTP, and AEB work according to the above description.

The models with the prefix simple_ implement simplified requirements and environments compared to the supervisor_synthesis models. These simplified models produce tactical planners that are easier to inspect.
- simple_upp2 only captures the successful interaction between the tactical planner and the UPP2. A correct tactical planner must only guarantee that the goal is reached.
- simple_sstp adds the localization subsystem and the SSTP. Hence, the sensor can fail, and in that case the tactical planner must activate SSTP.
- simple_aeb adds the possibility to activate AEB, and also that SSTP can be unavailable. If the sensor fails and SSTP is unavailable, the tactical planner must activate AEB.

The files in the supremica folder are opened through the Supremica IDE, which provides access to synthesis algorithms.

The files in the tulip folder are python 3 files. They require an installation of python and tulip to be run.

## Acknowledgement

This work was partially supported by the Wallenberg AI, Autonomous Systems and Software Program ([WASP](http://wasp-sweden.org/)) funded by the Knut and Alice Wallenberg Foundation.
