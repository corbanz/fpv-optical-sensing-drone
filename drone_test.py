from dronekit import connect

print("Connecting to vehicle...")
vehicle = connect('udp:127.0.0.1:14551', wait_ready=True)
print("Connected!")
print("GPS: %s" % vehicle.gps_0)
print("Battery: %s" % vehicle.battery)
print("Mode: %s" % vehicle.mode.name)
print("Armed: %s" % vehicle.armed)

vehicle.close()
print("Done")