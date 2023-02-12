from PIL import Image
import numpy as np


# per x & y
def get_intensities(image:Image.Image, numChunksX, numChunksY):
    intensities = np.ndarray((numChunksX, numChunksY))
    # print(im.size)
    px = image.load()
    # print(px[0, 0])
    px_per_chnk_x = int(image.size[0] / numChunksX)
    px_per_chnk_y = int(image.size[1] / numChunksY)
    px_per_chunk = px_per_chnk_x * px_per_chnk_y
    for yi in range(numChunksY):
        for xi in range(numChunksX):
            xs, xe = xi*px_per_chnk_x, (xi+1)*(px_per_chnk_x)
            ys, ye = yi*px_per_chnk_y, (yi+1)*(px_per_chnk_y)
            
            total = 0
            for x in range(xs, xe):
                for y in range(ys, ye):
                    total += sum(px[x, y])
            intensities[xi, yi] = total / px_per_chunk
    return intensities

class ImgConverter:
    def __init__(self, numChunks=100, fontAspectRatio=2.3):
        self.NUM_CHUNKS_X = numChunks
        self.NUM_CHUNKS_Y = self.NUM_CHUNKS_X // fontAspectRatio

        self.intensity_map = [" ", ".", ",", "^", "*", "1", "&", "%", "#", "@", "$"]
        # intensity_map = [' ', '.', '\'', '-', '"', '|', '/', '*', '!', '(', '{', '[', '&', '%', '#', '@', '$']
    
    def convert(self, inputName, outputName):
        intensities = self.get_intensities(inputName)
        self.generate_output(intensities, outputName)

    def convert_image(self, image, outputName):
        intensities = self.get_intensities_image(image)
        self.generate_output(intensities, outputName)

    def get_intensities(self, imageName):
        im = Image.open(imageName)
        return self.__get_intensities(im)

    def get_intensities_image(self, image):
        return self.__get_intensities(image)

    def __get_intensities(self, image):
        # we have to preserve the aspect ratio
        aspect_ratio = image.size[1] / image.size[0]
        numChunksX = self.NUM_CHUNKS_X
        numChunksY = int(aspect_ratio*self.NUM_CHUNKS_Y)

        return get_intensities(image, numChunksX, numChunksY)
        
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
                    charid = round(map_to(v, min_in, max_in, 0, num_in))
                    f.write(self.intensity_map[charid])
                f.write("\n")


if __name__ == "__main__":
    conv = ImgConverter()
    intensities = conv.get_intensities("img.png")
    conv.generate_output(intensities, "img.txt")
