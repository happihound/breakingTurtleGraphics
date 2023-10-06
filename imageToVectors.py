import numpy as np
import cv2
from tqdm import tqdm
from skimage.measure import approximate_polygon


def main(pictureName, quality=3):
    SIZE_FACTOR = 50
    img = cv2.imread(pictureName, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img, -1)
    if img is None:
        print("Could not read input image")
        return
    scale_percent = 100
    # Resize if the image is too small
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

    # Resize and preprocess
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    img = cv2.resize(img, (img.shape[1] * SIZE_FACTOR//100, img.shape[0]
                     * SIZE_FACTOR//100), interpolation=cv2.INTER_AREA)
    img = cv2.flip(img, -1)
    img = cv2.flip(img, 1)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray_img1 = cv2.GaussianBlur(gray_img, (quality, quality), 0)
    gray_img = cv2.medianBlur(gray_img, quality)
    gray_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
    gray_img = cv2.bitwise_not(gray_img)
    display_image = cv2.flip(gray_img, 1)
    display_image = cv2.flip(display_image, -1)
    display_image = cv2.rotate(display_image, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("display_image", display_image)
    cv2.waitKey(0)
    # Find contours using OpenCV
    contours, _ = cv2.findContours(gray_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

    line_segments = []
    for con in tqdm(contours):

        # Ensure the contour has multiple points before simplifying
        if len(con) > 1:
            simplified_contour = con[:, 0, :]
            if len(simplified_contour) < 2:
                continue
            current_color = findColor(img, con)
            color = current_color

            for index in range(len(simplified_contour) - 1):
                y1, x1 = simplified_contour[index]
                y2, x2 = simplified_contour[index + 1]

                if x1 == x2 and y1 == y2:
                    continue
                line_segments.append(((x1, y1), (x2, y2), color))

    lineResult = np.zeros((img.shape[1], img.shape[0], img.shape[2]), np.uint8)
    for segment in line_segments:
        r, g, b = segment[2]
        color = (b, g, r)
        cv2.line(lineResult, segment[0], segment[1], color)
    cv2.imshow("lineResult", lineResult)
    cv2.waitKey(0)

    save(line_segments)


def save(saved_points):
    np.save('polygonStorage/polygonalPoints.npy', np.array(saved_points, dtype=object))


def findColor(image, contour):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours(mask, contour, -1, 255, -1)
    return tuple(int(x) for x in cv2.mean(image, mask=mask)[:3])


if __name__ == "__main__":
    main("base_image/abbey_road.jpg")
