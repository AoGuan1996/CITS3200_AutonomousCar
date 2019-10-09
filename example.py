import cv2
import numpy as np
import math
img = cv2.imread('3.jpg');
# create the small border around the image, just bottom
img=cv2.copyMakeBorder(img, top=0, bottom=1, left=0, right=0, borderType= cv2.BORDER_CONSTANT, value=[255,255,255] )

# create the params and deactivate the 3 filters
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000
params.maxArea = 30000
params.filterByInertia = False
params.filterByConvexity = False

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# detect the blobs
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(gray)
positions = []
for keypoint in keypoints:
    pos = int(keypoint.pt[0]), int(keypoint.pt[1])
    positions.append(pos)

#########################################################################
newWaypoints = []
conePairs = []
while positions:
    currentCone = positions.pop(0)
    minDist = 99999                # Arbitrarily large number
    pairedIndex = 1
    for posPair in positions:
        currentDist = math.sqrt((currentCone[0] - posPair[0])**2 + (currentCone[1] - posPair[1])**2)
        if minDist > currentDist:
            minDist = currentDist
            pairedIndex = positions.index(posPair)
    conePairs.append((currentCone, positions[pairedIndex]))
    newWaypoints.append((round((currentCone[0] + positions[pairedIndex][0])/2), round((currentCone[1] + positions[pairedIndex][1])/2)))
    positions.pop(pairedIndex)
newWaypoints.sort(key=lambda y: y[0])
print (newWaypoints)
file = open("/Users/leitguan/Desktop/testbed/maps/map_blank/map_blank.txt","w")
'''for position in positions:
    file.write(' '.join(map(str, position))+'\n')'''
for newWaypoint in newWaypoints:
    file.write(' '.join(map(str, newWaypoint))+'\n')
file.close()
#########################################################################
# display them
for newWaypoint in newWaypoints:
    image_with_waypoints = cv2.circle(gray,tuple(newWaypoint),5,(0,0,255))
img_with_keypoints = cv2.drawKeypoints(image_with_waypoints, keypoints, outImage=np.array([]), color=(0, 0, 255),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Frame", img_with_keypoints)

#cv2.imshow("Frame", img_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
