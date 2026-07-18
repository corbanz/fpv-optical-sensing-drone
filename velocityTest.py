from dronekit import connect, VehicleMode
from dronekit import LocationGlobalRelative, LocationGlobal
from dronekit import Command
import time
from pymavlink import mavutil

print("Connecting to vehicle...")
vehicle = connect('udp:127.0.0.1:14551', wait_ready=True)
print("Connected!")
print("GPS: %s" % vehicle.gps_0)
print("Battery: %s" % vehicle.battery)
print("Mode: %s" % vehicle.mode.name)
print("Armed: %s" % vehicle.armed)
print("Vehicle is armable:", vehicle.is_armable)

def arm_and_takeoff(aTargetAltitude ):
    print("Pre-arm Checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise")
        time.sleep(1)
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print("Waiting for arming")
        time.sleep(1)
    print("Taking off")
    vehicle.simple_takeoff(aTargetAltitude ) # It sends a takeoff command to Ardupilot via MAVLink.
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude  * 0.95:
            #vehicle.location — the drone's location object, which contains different coordinate frames
            #.global_relative_frame — specifically the frame that measures altitude relative to the ground (where it took off from), not sea level
            #.alt — the actual altitude number in meters
            print("Reached target altitude")
            break
        time.sleep(1)

import time
from pymavlink import mavutil

def send_velocity(vx, vy, vz, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111,
            0, 0, 0,
            vx, vy, vz,
            0, 0, 0,
            0, 0
        )
        vehicle.send_mavlink(msg)
        time.sleep(0.1)

arm_and_takeoff(10)
print("Takeoff complete")
send_velocity(2, 0, 0, 5) #Move forward at 2 m/s for 5 seconds
send_velocity(0, 0, 0, 2)
time.sleep(5)
vehicle.mode = VehicleMode("RTL")
print("Returning to Launch")