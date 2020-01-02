import numpy as np

#Blue filter effect
def blue_filter(image):
    image2 = np.copy(image)
    image2[:,:,:2].fill(0) #Puts to zero red and green values -> only keeps blue values
    return image2
