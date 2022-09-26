from PIL import Image
import numpy as np
im = Image.open("me.jpeg")

print(im.size)

px = im.load()

print(px[0, 0])

# per x & y
NUM_CHUNKS_X = 200
NUM_CHUNKS_Y = NUM_CHUNKS_X // 2 
px_per_chnk_x = int(im.size[0] / NUM_CHUNKS_X)
px_per_chnk_y = int(im.size[1] / NUM_CHUNKS_Y)
size_x = im.size[0]
size_y = im.size[1]

intensity_map = [" ", ".",",", "^", "*", "1","&","%","#","@", "$"]
# intensity_map = [' ', '.', '\'', '-', '"', '|', '/', '*', '!', '(', '{', '[', '&', '%', '#', '@', '$']
intensities = np.ndarray((NUM_CHUNKS_X, NUM_CHUNKS_Y))

for yi in range(NUM_CHUNKS_Y):
    for xi in range(NUM_CHUNKS_X):
        total = 0
        num_pxs = 0
        for x in range(xi*px_per_chnk_x, (xi+1)*(px_per_chnk_x)):
            for y in range(yi*px_per_chnk_y, (yi+1)*(px_per_chnk_y)):
                total += sum(px[x,y])
                num_pxs += 1
        total = total / (px_per_chnk_x * px_per_chnk_y)
        intensities[xi, yi] = total

def map_to(v, vmin, vmax, tomin, tomax):
    return (v - vmin) * (tomax - tomin) / (vmax - vmin) + tomin

max_in = intensities.max()
min_in =  intensities.min()
num_in = len(intensity_map) - 1


with open("image.txt", "w") as f:
    for y in range(intensities.shape[1]):
        for x in range(intensities.shape[0]):
            v = intensities[x,y]
            # print(v)
            charid = int(map_to(v, min_in, max_in, 0, num_in))
            # charid = int(map_to(v, min_in, max_in,num_in, 0))
            # print(charid)
            f.write(intensity_map[charid])
        f.write("\n")