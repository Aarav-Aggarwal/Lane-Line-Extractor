import os
import cv2
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
# ROI corners for each photo, as (x, y) fractions of the width and height
ROI_2 = [(0, 1), (0, 0.95), (0.40, 0.64), (0.56, 0.64), (1, 0.92), (1, 1)]
ROI_1 = [(0, 1), (0, 0.76), (0.55, 0.50), (0.60, 0.50), (1, 1)]


def load_image(path):
    img = cv2.imread(path)
    if img is None:
        print("Image not found, check the path:", path)
        exit()
    return img


def blur_image(img):
    # smooth the photo so tiny noise dots disappear
    return cv2.GaussianBlur(img, (5, 5), 0)


def color_mask(img):
    # keep only white and yellow pixels (255 = keep, 0 = throw away)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([179, 40, 255]))
    yellow = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([32, 255, 255]))
    return cv2.bitwise_or(white, yellow)


def detect_edges(img):
    # Canny needs a grayscale image (one number per pixel)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 50, 150)


def region_of_interest(img, corners):
    # keep only the road-shaped area, black out the rest
    h, w = img.shape[:2]
    points = []
    for x, y in corners:
        points.append((int(x * w), int(y * h)))
    polygon = np.array([points], dtype=np.int32)
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(img, mask)

def draw_lanes(img, lane_edges):
    # paint the lane edges red on a copy of the original photo
    thick = cv2.dilate(lane_edges, np.ones((3, 3), np.uint8))   # a bit thicker so it is visible
    result = img.copy()
    result[thick > 0] = (0, 0, 255)
    return result


def process(name, corners):
    img = load_image(os.path.join(BASE, "images", name))

    mask = color_mask(img)
    lane_pixels = cv2.bitwise_and(img, img, mask=mask)
    blurred = blur_image(lane_pixels)
    edges = detect_edges(blurred)
    lane_edges = region_of_interest(edges, corners)
    result = draw_lanes(img, lane_edges)

    out_dir = os.path.join(BASE, "outputs")
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(name)[0]
    cv2.imwrite(os.path.join(out_dir, base + "Mask.jpg"), mask)
    cv2.imwrite(os.path.join(out_dir, base + "Detect_Edges.jpg"), edges)
    cv2.imwrite(os.path.join(out_dir, base + "Draw_Lanes.jpg"), lane_edges)
    cv2.imwrite(os.path.join(out_dir, base + "Lanes.jpg"), result)
    print("Saved results for", name)
    return result

result1 = process("Original.jpg", ROI_1)
result2 = process("Original2.jpg", ROI_2)

cv2.imshow("Photo 1", result1)
cv2.imshow("Photo 2", result2)
cv2.waitKey(0)
cv2.destroyAllWindows()