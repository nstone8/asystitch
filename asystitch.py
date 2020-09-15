import cv2

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
    print('x edges')
    print((x0,x1))
    print('y edges')
    print((y0,y1))
    cropped_im=im[y0:y1,x0:x1]
    return cropped_im

imfile=r'C:\Users\stone\Downloads\RPEminus_20033_OD0000AmR.tif'
im=cv2.imread(imfile,cv2.IMREAD_GRAYSCALE)
im_cropped=crop(im)
cv2.imshow('Original',im)
cv2.imshow('Cropped',im_cropped)
cv2.waitKey(0)
