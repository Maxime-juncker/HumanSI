import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import time

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=10)


def FunctTime(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time() - t1
        print(f"a pris {t2} seconds")

    return wrapper


xpix, ypix = 1080, 1920
pic = []  # pic est la liste de ligne avec toutes les valueurs des pixel


@FunctTime
def GenerateMap():
    for i in range(xpix):
        row = []
        print("Generation : " + str(round(i/xpix*100, 1)) + "%")

        for j in range(ypix):
            noise_val = noise1([i / xpix, j / ypix])  # basic noise

            # on ajoute different type de noise pour ajouter un peu de varieter
            noise_val += 0.5 * noise2([i / xpix, j / ypix])

            row.append(noise_val)

        pic.append(row)

    plt.imshow(pic, cmap='turbo')
    plt.show()


GenerateMap()
