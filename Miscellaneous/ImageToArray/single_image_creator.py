from PIL import Image
import numpy as np

bg = (123, 209, 224)
hr = (255, 171, 0)
sk = (241, 194, 125)
jk = (121, 86, 156)
ey = (135, 181, 44)
bd = (0, 0, 0)
mt = (0, 0, 0)
eb = (255, 255, 255)

pixels_list = [
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bd, bd, bd, bd, bd, bd, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bd, hr, hr, hr, hr, hr, hr, bd, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, hr, hr, hr, hr, hr, hr, hr, hr, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, hr, sk, hr, sk, hr, sk, hr, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, sk, sk, sk, sk, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, eb, eb, sk, eb, eb, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, ey, eb, sk, ey, eb, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, sk, sk, sk, sk, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, sk, sk, sk, sk, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, sk, sk, sk, mt, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, sk, mt, mt, mt, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, sk, sk, sk, sk, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bd, sk, sk, sk, sk, sk, sk, sk, bd, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bd, jk, sk, sk, jk, jk, bd, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bd, bd, bd, bd, bd, jk, sk, sk, jk, jk, bd, bd, bd, bd, bd, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bd, jk, jk, jk, jk, jk, sk, sk, jk, jk, jk, jk, jk, jk, bd, bd, bg, bg, bg, bg],
    [bg, bg, bg, bg, bd, bd, jk, jk, jk, jk, jk, sk, sk, jk, jk, jk, jk, jk, jk, jk, bd, bg, bg, bg, bg],
    [bg, bg, bg, bg, bd, jk, jk, jk, jk, jk, jk, sk, sk, jk, jk, jk, jk, jk, jk, jk, bd, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
    [bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg, bg],
]

avatar_array = np.array(pixels_list, dtype=np.uint8)
avatar_image = Image.fromarray(avatar_array)
avatar_image = avatar_image.resize((480, 480), resample=Image.NEAREST)
avatar_image.save("avatar.png")
