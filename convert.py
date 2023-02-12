from PIL import Image
import numpy as np


# per x & y
def get_intensities(image, numChunksX, numChunksY):
    intensities = np.ndarray((numChunksX, numChunksY))
    # print(im.size)
    px = image.load()
    # print(px[0, 0])
    px_per_chnk_x = int(image.size[0] / numChunksX)
    px_per_chnk_y = int(image.size[1] / numChunksY)

    for yi in range(numChunksY):
        for xi in range(numChunksX):
            total = 0
            for x in range(xi*px_per_chnk_x, (xi+1)*(px_per_chnk_x)):
                for y in range(yi*px_per_chnk_y, (yi+1)*(px_per_chnk_y)):
                    total += sum(px[x, y])
            total = total / (px_per_chnk_x * px_per_chnk_y)
            intensities[xi, yi] = total
    return intensities

class ImgConverter:
    def __init__(self, numChunks=100, fontAspectRatio=2.3):
        self.NUM_CHUNKS_X = numChunks
        self.NUM_CHUNKS_Y = self.NUM_CHUNKS_X // fontAspectRatio

        self.intensity_map = [" ", ".", ",", "^", "*", "1", "&", "%", "#", "@", "$"]
        # intensity_map = [' ', '.', '\'', '-', '"', '|', '/', '*', '!', '(', '{', '[', '&', '%', '#', '@', '$']

    def get_intensities(self, imageName):
        # we have to preserve the aspect ratio
        im = Image.open(imageName)
        aspect_ratio = im.size[1] / im.size[0]
        numChunksX = self.NUM_CHUNKS_X
        numChunksY = int(aspect_ratio*self.NUM_CHUNKS_Y)

        return get_intensities(im, numChunksX, numChunksY)

    def generate_output(self, intensities, outputName):
        def map_to(v, vmin, vmax, tomin, tomax):
            return (v - vmin) * (tomax - tomin) / (vmax - vmin) + tomin

        max_in = intensities.max()
        min_in = intensities.min()
        num_in = len(self.intensity_map) - 1

        with open(outputName, "w") as f:
            for y in range(intensities.shape[1]):
                for x in range(intensities.shape[0]):
                    v = intensities[x, y]
                    charid = int(map_to(v, min_in, max_in, 0, num_in))
                    f.write(self.intensity_map[charid])
                f.write("\n")


if __name__ == "__main__":
    conv = ImgConverter()
    intensities = conv.get_intensities("img.jpeg")
    conv.generate_output(intensities, "img.txt")
