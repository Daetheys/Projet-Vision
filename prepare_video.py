import skvideo.io
import skvideo.datasets
from skimage import io,exposure,img_as_uint, img_as_float
from skimage.viewer import ImageViewer
import numpy as np
from waiting import Waiting #Waiting animations
from effect import blue_filter #Effect function
from segmentation import get_mask

effect = blue_filter #Effect used

generate = (False,False,True)


videoreader = skvideo.io.FFmpegReader("video_very_short.mp4") #Loads the video
(nb_frames,height,width,_) = videoreader.getShape()
#videogen = videoreader.nextFrame()

#videogen in a generator of numpy array of shape (height,width,3)
#for frame in videogen:
#    print(frame.shape)

#We need to fill 3 folders : [keys] with keyframes, [video] with video images and [mask] with masks

#--------------------------
#  Fill [video] (easiest)
#--------------------------

#For each image in the video, it will create an .png image file with the frame in the [video] folder. It's name needs to be the number of the frame with 0 padding so that all names have the same length

#Get the size of the name of each name
length = int(np.ceil(np.log10(nb_frames)))

def get_name_from_index(index,folder):
    #Returns the name of the image depending on its index
    global length
    s = str(index)
    for i in range(len(s),length):
        s = "0"+s #0 padding
    return folder+"/"+s+".png"
if generate[0]:
    videoreader = skvideo.io.FFmpegReader("video_very_short.mp4") #Loads the video
    videogen = videoreader.nextFrame()
    wait = Waiting() #Only for wainting animation
    #Save each image with the right name
    print("Generating [video]")
    wait.start()
    for index,frame in enumerate(videogen):
        wait.update(index/nb_frames*100)
        f = io.imsave(get_name_from_index(index,"video"),frame)
    wait.stop()

#--------------------------
#  Fill [mask] 
#--------------------------
#We assume the user already gave a function for effects (filter, style transfert, ...). This function is effect : image -> image

mask = []

if generate[1]:
    wait = Waiting() #Only for wainting animation
    videoreader = skvideo.io.FFmpegReader("video_very_short.mp4") #Loads the video
    videogen = videoreader.nextFrame()
    #Save each image with the right name
    print("Generating [mask]")
    wait.start()
    for index,frame in enumerate(videogen):
        wait.update(index/nb_frames*100)
        mask_frame = get_mask(frame)
        mask.append(mask_frame)
        f = io.imsave(get_name_from_index(index,"mask"),mask_frame)
    wait.stop()

#--------------------------
#  Fill [keys] 
#--------------------------
#We assume the user already gave a function for effects (filter, style transfert, ...). This function is effect : image -> image

if generate[2]:
    wait = Waiting() #Only for wainting animation
    videoreader = skvideo.io.FFmpegReader("video_very_short.mp4") #Loads the video
    videogen = videoreader.nextFrame()
    #Save each image with the right name
    print("Generating [keys]")
    wait.start()
    for index,frame in enumerate(videogen):
        if index % 10 == 5:
            mask_name = get_name_from_index(index,"mask")
            print(mask_name)
            name = get_name_from_index(index,"keys")
            mask = io.imread(mask_name)
            wait.update(index/nb_frames*100)
            style = effect(mask*frame)
            reversed_mask = np.dot(mask,np.ones((3,1)))
            style += (reversed_mask==0)*frame
            f = io.imsave(name,style)
    wait.stop()
