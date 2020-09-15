import cv2
import sys
import os
import numpy as np

def find_edges(im,axis):
    #Search for the last row or column of pixels on each side which are only white or black
    y_start=0
    y_end=im.shape[axis]
    for i in range(im.shape[axis]):
        if axis==0:
            this_row_vals=set(im[i,:])
        elif axis==1:
            this_row_vals=set(im[:,i])
        if this_row_vals==set([255,0]):
            #possible edge row
            if i<im.shape[axis]/2:
                #top edge
                y_start=i
            else:
                #bottom edge
                y_end=i
                break
    return y_start,y_end

def crop(im):
    #Remove axes labels from image
    y0,y1=find_edges(im,0)
    x0,x1=find_edges(im,1)
    cropped_im=im[y0:y1,x0:x1]
    return cropped_im

def stitch(ims):
    stitcher=cv2.Stitcher.create(cv2.Stitcher_SCANS)
    retval,stitched=stitcher.stitch(ims)
    print(retval)
    return stitched
'''
def stitch(ims):
    stitcher=cv2.Stitcher.create(1)
    stitched=ims.pop(0)
    count=0
    while ims:
        print(f'count={count}, len(ims)={len(ims)}')
        count+=1
        try:
            toadd=ims.pop(0)
            retval,stitched=stitcher.stitch([stitched,toadd])
        except(cv2.error):
            ims.append(toadd)
    return stitched
'''
imdir=sys.argv[-1]
im_paths=[a for a in os.listdir(imdir) if '.tif' in a]
ims=[cv2.cvtColor(crop(cv2.imread(os.path.join(imdir,b),cv2.IMREAD_GRAYSCALE)),cv2.COLOR_GRAY2BGR) for b in im_paths]
stitched=stitch(ims)
cv2.imwrite(os.path.join(imdir,'stitched.tif'),stitched)
