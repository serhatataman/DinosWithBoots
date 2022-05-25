import PIL
from skimage.io import imread
import numpy as np


# https://stackoverflow.com/questions/27026866/convert-an-image-to-2d-array-in-python
im = imread("snowboarder.jpg")
indices = np.dstack(np.indices(im.shape[:2]))
data = np.concatenate((im, indices), axis=-1)
new_data = data[:, :, :]
print(new_data)

# np.savetxt("somefile.txt", new_data.reshape((4,5,10)), newline="\n")



