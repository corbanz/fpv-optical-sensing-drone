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

def ReturnToLaunch():
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

ReturnToLaunch()
vehicle.close()