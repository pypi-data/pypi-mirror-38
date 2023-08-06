import numpy as np
from skimage.morphology import closing, square,disk,opening,binary_opening
import cv2
from skimage.filters import threshold_otsu
def rotatedRets(z):
    if not binary_opening(z > 0.5, np.expand_dims(disk(2), -1)).sum():
        return (z>0.9).astype(np.float32)
    r=np.zeros(z.shape,np.uint8)
    thresh = threshold_otsu(z)
    z = opening(z[:,:,0] > thresh, disk(1))
    _,cs,_=cv2.findContours(z.astype(np.uint8),1,1)
    for x in cs:
        rect = cv2.minAreaRect(x)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(r,[box],0,1,-1)
    return r.astype(np.float32)