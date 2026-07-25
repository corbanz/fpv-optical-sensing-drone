#README 
[Updated 7/25/26]

# FPV Optical Sensing Drone

A custom-built First-Person-View cinewhoop quadrotor with an onboard 
Raspberry Pi companion computer implementing real-time optical flow 
positioning for GPS-denied indoor flight.

## Overview

This drone enables stable position holding and navigation when GPS 
signal is unavailable. Originally conceived for indoor filming of 
large live events. A downward-facing camera feeds into a Lucas-Kanade 
optical flow algorithm running on the Raspberry Pi, which computes 
drift corrections and sends velocity commands to the Ardupilot flight 
controller via MAVLink in real time.

## How It Works

1. A downward camera captures ground footage
2. OpenCV's Lucas-Kanade algorithm tracks feature points between frames
3. Frame-to-frame movement is converted to a velocity estimate
4. Velocity corrections are sent to Ardupilot via MAVLink
5. Ardupilot adjusts motor output to counteract drift
6. The result is stable hands-free hover with no GPS signal

## Scripts

| `drone_test.py` | Connect to vehicle and read telemetry state |
| `QuickLoop.py` | Arm, takeoff, hover, and RTL sequence |
| `flyToGPS.py` | Fly to user-defined GPS coordinate |
| `velocityTest.py` | Send raw MAVLink velocity commands |
| `optical_flow_sim.py` | Lucas-Kanade optical flow algorithm test |
| `opt_flow_feed.py` | Full optical flow correction loop integrated with drone with simulated data|
