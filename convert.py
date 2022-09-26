from PIL import Image
import numpy as np

# per x & y
class ImgConverter:
    def __init__(self, numChunks=100):
        pass
        self.NUM_CHUNKS_X = numChunks
        self.NUM_CHUNKS_Y = self.NUM_CHUNKS_X // 2 

        self.intensity_map = [" ", ".",",", "^", "*", "1","&","%","#","@", "$"]
        # intensity_map = [' ', '.', '\'', '-', '"', '|', '/', '*', '!', '(', '{', '[', '&', '%', '#', '@', '$']
        
    def get_intensities(self, imageName):
        intensities = np.ndarray((self.NUM_CHUNKS_X, self.NUM_CHUNKS_Y))
        im = Image.open(imageName)
        # print(im.size)
        px = im.load()
        # print(px[0, 0])

        # we have to preserve the aspect ratio
        aspect_ratio = im.size[1] / im.size[0]
        self.NUM_CHUNKS_Y = int(aspect_ratio*self.NUM_CHUNKS_Y)

        px_per_chnk_x = int(im.size[0] / self.NUM_CHUNKS_X)
        px_per_chnk_y = int(im.size[1] / self.NUM_CHUNKS_Y)

        for yi in range(self.NUM_CHUNKS_Y):
            for xi in range(self.NUM_CHUNKS_X):
                total = 0
                for x in range(xi*px_per_chnk_x, (xi+1)*(px_per_chnk_x)):
                    for y in range(yi*px_per_chnk_y, (yi+1)*(px_per_chnk_y)):
                        total += sum(px[x,y])
                total = total / (px_per_chnk_x * px_per_chnk_y)
                intensities[xi, yi] = total
        return intensities

    def generate_output(self, intensities, outputName):
        def map_to(v, vmin, vmax, tomin, tomax):
            return (v - vmin) * (tomax - tomin) / (vmax - vmin) + tomin

        max_in = intensities.max()
        min_in =  intensities.min()
        num_in = len(self.intensity_map) - 1

        with open(outputName, "w") as f:
            for y in range(intensities.shape[1]):
                for x in range(intensities.shape[0]):
                    v = intensities[x,y]
                    charid = int(map_to(v, min_in, max_in, 0, num_in))
                    f.write(self.intensity_map[charid])
                f.write("\n")


if __name__ == "__main__":
    conv = ImgConverter()
    intensities = conv.get_intensities("img.jpeg")
    conv.generate_output(intensities, "img.txt")