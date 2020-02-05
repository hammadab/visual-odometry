import numpy as np
import cv2

orb = cv2.ORB_create()
cap = cv2.VideoCapture(0)
_, img0 = cap.read()
img0 = cv2.resize(img0, (990, 990))
train_keypoints0, train_descriptor0 = orb.detectAndCompute(img0, None)
while True:
    _, img1 = cap.read()
    if img1 is None:
        break
    #    cv2.imshow("frame", frame)
    img1 = cv2.resize(img1, (990, 990))
    train_keypoints1, train_descriptor1 = orb.detectAndCompute(img1, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(train_descriptor0, train_descriptor1)
    #    nMatches = len(matches)

    matches = sorted(matches, key=lambda x: x.distance)[:20]

    #    good_points = []
    #    for m in matches:
    #        if m.distance < 15:
    #            good_points.append(m)

    matching_result = cv2.drawMatches(img0, train_keypoints0, img1, train_keypoints1, matches, None)
    cv2.imshow("Matching result", matching_result)

    key = cv2.waitKey(50)
    if key == 27:
        break
#    img0 = img1
#    train_keypoints0 = train_keypoints1
#    train_descriptor0 = train_descriptor1

cap.release()
cv2.destroyAllWindows()

good = []
pts1 = []
pts2 = []
for m in matches:
    # if m.distance < 32:
    good.append(m)
    pts2.append(train_keypoints0[m.queryIdx].pt)
    pts1.append(train_keypoints1[m.trainIdx].pt)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)
E, EMmask = cv2.findEssentialMat(pts1, pts2)
retval, R, t, RPmask = cv2.recoverPose(E, pts1, pts2)