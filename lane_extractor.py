
import cv2 as cv
import numpy as np


def make_polygon(w, h, points):
    return np.array([[(int(x * w), int(y * h)) for (x, y) in points]])


def extract_lanes(img, roi_points, name):
    h, w = img.shape[:2]

    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    white_mask = cv.inRange(hsv, (0, 0, 215), (180, 25, 255))
    yellow_mask = cv.inRange(hsv, (18, 70, 90), (32, 255, 255))
    color_mask = cv.bitwise_or(white_mask, yellow_mask)
    filtered = cv.bitwise_and(img, img, mask=color_mask)

    blur = cv.GaussianBlur(filtered, (5, 5), 0)
  
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150)

    roi_mask = np.zeros((h, w), dtype="uint8")
    polygon = make_polygon(w, h, roi_points)
    cv.fillPoly(roi_mask, polygon, 255)
    result = cv.bitwise_and(edges, roi_mask)

    preview = img.copy()
    cv.polylines(preview, polygon, True, (0, 0, 255), 2)

    cv.imwrite(f"results/{name}_1_roi_preview.png", preview)
    cv.imwrite(f"results/{name}_2_color_mask.png", color_mask)
    cv.imwrite(f"results/{name}_3_edges.png", edges)
    cv.imwrite(f"results/{name}_4_result.png", result)
    return result


images = {
    "lane1": ("images/lane1.jpg",
              [(0, 1.0), (0, 0.66), (0.47, 0.36), (0.53, 0.36), (1.0, 0.66), (1.0, 1.0)]),
    "lane2": ("images/lane2.jpg",
              [(0.2, 1.0), (0.475, 0.40), (0.525, 0.40), (0.8, 1.0)]),
}

for name, (path, roi_points) in images.items():
    img = cv.imread(path)
    if img is None:
        print("Could not read", path)
        continue
    extract_lanes(img, roi_points, name)
    print("Done:", name)
