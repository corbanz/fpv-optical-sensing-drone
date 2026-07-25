import cv2
import numpy as np
from dronekit import connect, VehicleMode
from dronekit import LocationGlobalRelative, LocationGlobal
from dronekit import Command
import time
from pymavlink import mavutil

ground = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
ground = cv2.GaussianBlur(ground, (15, 15), 0)

print("Connecting to vehicle...")
vehicle = connect('udp:127.0.0.1:14551', wait_ready=True)
print("Connected!")
print("GPS: %s" % vehicle.gps_0)
print("Battery: %s" % vehicle.battery)
print("Mode: %s" % vehicle.mode.name)
print("Armed: %s" % vehicle.armed)
print("Vehicle is armable:", vehicle.is_armable)

prev_frame = ground.copy()
prev_points = cv2.goodFeaturesToTrack(prev_frame, maxCorners=200, qualityLevel=0.3, minDistance=7)

total_x = 0
total_y = 0

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
while True:
    # shift_x = 3 #np.random.randint
    # shift_y = 0 #np.random.randint(-5, 5)
    total_x = (total_x + 3) % 200
    total_y += 0
    M = np.float32([[1, 0, total_x], [0, 1, total_y]])
    shifted_ground = cv2.warpAffine(ground, M, (ground.shape[1], ground.shape[0]))
    curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_frame, shifted_ground, prev_points, None)
    #curr_points — the new positions of the points in prev_points in the current frame / where each tracked point ended up in the new frame
    #status — an array indicating whether each point was successfully tracked (1) or not (0)
    #err — an array of error values for each point, indicating how well the point was tracked (lower values are better)
    good_prev = prev_points[status == 1]
    good_curr = curr_points[status == 1]
    movement = good_curr - good_prev
    avg_movement = np.mean(movement, axis=0)
    scale = 0.01
    vx = float(avg_movement[0] * scale)
    vy = float(avg_movement[1] * scale)
    send_velocity(vx, vy, 0, 0.1)
    print("Flow X: %.2f, Flow Y: %.2f" % (avg_movement[0], avg_movement[1]))
    cv2.imshow("Shifted Ground Texture", shifted_ground)
    prev_frame = shifted_ground.copy()
    prev_points = cv2.goodFeaturesToTrack(prev_frame, maxCorners=200, qualityLevel=0.3, minDistance=7)
    if prev_points is None:
        prev_points = cv2.goodFeaturesToTrack(prev_frame, maxCorners=200, qualityLevel=0.3, minDistance=7)
        continue
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
time.sleep(5)
vehicle.mode = VehicleMode("RTL")
print("Returning to Launch")