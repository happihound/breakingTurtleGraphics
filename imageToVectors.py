import numpy as np
from skimage.measure import approximate_polygon, find_contours
import cv2 as cv
import cv2
from tqdm import tqdm


def main(pictureName, quality=0):
    lineResult = 0
    img1 = cv2.imread(pictureName)
    img = cv2.imread(pictureName, 0)
    if img is None:
        print("Could not read input image")
        return
    scale_percent = 100  # percent of original size
    #fix the image if it is too small
    if img.shape[0] < 800:
        scale_percent = 200
    if img.shape[0] < 400:
        scale_percent = 400
    if img.shape[0] < 200:
        scale_percent = 800
    if img.shape[0] < 100:
        scale_percent = 1600
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    img1 = cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)
    img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv.THRESH_BINARY, 11, 0)
    img1 = cv2.flip(img1, -1)
    img1 = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.flip(img, 0)
    contours = find_contours(img, 4)
    lineResult = np.zeros(img.shape + (3,), np.uint8)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    color = []
    for con in tqdm(contours):
        cv_contour = []
        for point in con:
            intify = [int(point[0]), int(point[1])]
            cv_contour.append([intify])
        cv_contour = np.array(cv_contour)
        color.append(findColor(img1, [cv_contour.astype(int)]))
    iterationCount = 0
    points = []
    for contour in tqdm(contours):
        # change tolerance value to control quality
        simplifiedLine = approximate_polygon(contour, tolerance=quality)
        simplifiedLine = simplifiedLine.astype(np.int64).tolist()
        for index, coords in enumerate(simplifiedLine[:-1]):
            y1, x1, y2, x2 = coords + simplifiedLine[index + 1]
            if (x1 == x2 and y1 == y2):
                continue
            points.append(((y1 - 400), (x1 - 400), (y2 - 400), (x2 - 400), color[iterationCount]))
            lineResult = cv2.line(lineResult, (x1, y1),
                                  (x2, y2), color[iterationCount])
        iterationCount = iterationCount + 1
    save(points)
    #lineResult = cv2.flip(lineResult, 0)
    #lineResult = cv2.cvtColor(lineResult, cv2.COLOR_BGR2RGB)
    #uncomment to see preview of the image
    #cv2.imshow("title",  lineResult)
    #cv2.waitKey()


def save(saved_points):
    saved_points = np.array(saved_points, dtype=object)
    np.save('polygonStorage/polygonalPoints.npy',
            saved_points)


def findColor(image, c):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours(mask, c, -1, 255, -1)
    mean = cv2.mean(image, mask=mask)[:3]
    tupint = tuple(int(x) for x in mean)
    return tupint


if __name__ == "__main__":
    main("base_image/abbey_road.jpg")

