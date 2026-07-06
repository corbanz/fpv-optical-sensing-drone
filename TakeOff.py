from dronekit import connect, VehicleMode
import time

print("Connecting to vehicle...")
vehicle = connect('127.0.0.1:14551', wait_ready=True)
print("Connected")

def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(10)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= 9.5:
            print("Reached target altitude")
            break
        time.sleep(1)



arm_and_takeoff(10)
print("Takeoff complete")
vehicle.close()