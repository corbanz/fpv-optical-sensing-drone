from dronekit import connect, VehicleMode
from dronekit import LocationGlobalRelative, LocationGlobal
from dronekit import Command
import time



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


latdelta = float(input("Latitude change (in Degrees): "))
longdelta = float(input("Longitude change (in Degrees): "))
altdelta = float(input("Altitude change (in Meters): "))

pos = vehicle.location.global_relative_frame
targetpos = LocationGlobalRelative(pos.lat + latdelta, pos.lon + longdelta, pos.alt + altdelta)

arm_and_takeoff(altdelta)
print("Takeoff complete")
vehicle.simple_goto(targetpos)
time.sleep(10)
vehicle.mode = VehicleMode("RTL")
print("Returning to Launch")