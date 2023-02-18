import glob
import imageToVectors
import drawVectors
def main():
    #collect image from base_image folder
    # to be fed to the imageToVectors.py

    for image in glob.glob('base_image/*.jpg'):
        print("Processing: ", image)
        imageToVectors.main(image)
        print("Done Processing: ", image)
        print("--------------------------------------------------------------")
        print("Drawing: ", image)
        drawVectors.startDrawing()


if __name__ == "__main__":
    main()

