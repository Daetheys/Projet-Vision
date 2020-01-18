import skvideo.io
import skvideo.datasets
from skimage import io,exposure,img_as_uint, img_as_float
from skimage.transform import resize
from skimage.viewer import ImageViewer
from skimage.filters import gaussian
import numpy as np

#------------------------------------
#
#   Argument parser
#
#------------------------------------

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("-rx",help="set the X resolution of output images")
parser.add_argument("-ry",help="set the X resolution of output images")
args = parser.parse_args()
name = args.name
image_resolution = (args.ry,args.rx)

#------------------------------------
#
#   Save images of the video
#
#------------------------------------

videoreader = skvideo.io.FFmpegReader(name)
(nb_frames,height,width,_) = videoreader.getShape()

length = int(np.ceil(np.log10(nb_frames)))
def get_name_from_index(index,folder):
    #Returns the name of the image depending on its index
    global length
    s = str(index)
    for i in range(len(s),length):
        s = "0"+s #0 padding
    return folder+"/"+s+".png"

videogen = videoreader.nextFrame()

for index,frame in enumerate(videogen):
    print(str(index/nb_frames*100)[:4]+"%",end="\r")
    if args.ry and args.rx:
        f = io.imsave(get_name_from_index(index,"video"),resize(frame,image_resolution,anti_aliasing=True))
    else:
        f = io.imsave(get_name_from_index(index,"video"),frame)
