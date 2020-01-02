import numpy as np
from scipy import signal

def pixel_distance(px1,px2):
    return np.sum(np.abs(px1-px2))

def get_mask(image):
    #print(image[543,442])
    def compute_mask_color(image,color):
        image = image[:,:,np.newaxis]
        mask = (image >= color[None,None,:,:])*(image-color[None,None,:])+(image < color[None,None,:,:])*(color[None,None,:]-image)
        mask = np.int64(np.sum(mask,axis=3) > epsilon)
        return np.int64(mask)
    step = 50
    back_colors = [image[y,x] for (x,y) in zip(range(0,len(image),step),range(0,len(image[0]),step)) if not(300<x<900) and not(50<y<600)]
    back_colors += np.array([30,20,15])
    back_colors = np.array(back_colors)
    epsilon = 100
    mask = np.ones(image.shape[:2])
    mask = compute_mask_color(image,back_colors)
    mask = np.prod(mask,axis=2)
    mask = np.dot(mask[:,:,None],np.ones((1,3)))
    mask = np.uint8(mask*255)
    return mask
