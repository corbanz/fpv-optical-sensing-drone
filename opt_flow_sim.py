import cv2
import numpy as np

ground = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
ground = cv2.GaussianBlur(ground, (15, 15), 0)
# cv2.imshow("Ground Texture", ground)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
prev_frame = ground.copy()
prev_points = cv2.goodFeaturesToTrack(prev_frame, maxCorners=200, qualityLevel=0.3, minDistance=7)
#prev_frame — the image to find features in
#maxCorners=200 — find at most 200 feature points
#qualityLevel=0.3 — only keep points with at least 30% of the best point's quality score
#minDistance=7 — only keep points that are at least 7 pixels apart from each other
total_x = 0
total_y = 0
while True:
    # shift_x = 3 #np.random.randint
    # shift_y = 0 #np.random.randint(-5, 5)
    total_x += 3
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
    print("Flow X: %.2f, Flow Y: %.2f" % (avg_movement[0], avg_movement[1]))
    cv2.imshow("Shifted Ground Texture", shifted_ground)
    prev_frame = shifted_ground.copy()
    if prev_points is None:
        prev_points = cv2.goodFeaturesToTrack(prev_frame, maxCorners=200, qualityLevel=0.3, minDistance=7)
        continue
    prev_points = cv2.goodFeaturesToTrack(prev_frame, maxCorners=200, qualityLevel=0.3, minDistance=7)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break