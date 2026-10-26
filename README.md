# Road Lane Detection

A small lane detector built with OpenCV and NumPy.
It finds the white and yellow painted lines on a photo of a road and draws them in red on the original picture.
An image is a NumPy array of pixels. Color photos are stored as [B, G, R] (OpenCV uses BGR, not RGB), and grayscale images have one value per pixel from 0 (black) to 255 (white).

## Functions

### load_image(path)
Reads the photo from disk with OpenCV.
Output: the image as a NumPy array. If the file cannot be found, it prints a message and stops the program.

### blur_image(img)
Smooths the image with a 5x5 Gaussian blur so tiny noise dots disappear.
Output: an image of the same size where sharp specks are softened.

### color_mask(img)
Converts the image to HSV and keeps only white and yellow pixels. White is any pixel with low saturation (0-40) and high brightness (200-255). Yellow is a hue of 20-32 with saturation and brightness of at least 100.
Output: a black and white mask. White and yellow pixels become 255, everything else becomes 0.

### detect_edges(img)
Turns the image into grayscale, then runs Canny edge detection with thresholds 50 and 150.
Output: a black image with white outlines wherever the brightness changes sharply, such as around a painted line.

### region_of_interest(img, corners)
Keeps only the road-shaped polygon and blacks out the rest, so the sky and background are ignored. The corners are (x, y) fractions of the width and height.
Output: with ROI_2 on a 1280x853 photo, the corner (0.40, 0.64) becomes the pixel (512, 545). Everything outside the polygon becomes 0.

### draw_lanes(img, lane_edges)
Thickens the edges a little with a 3x3 dilation so they are easy to see, then paints them red on a copy of the photo.
Output: the original photo with red lane outlines. The original image is not changed.

### process(name, corners)
Runs the whole pipeline on one photo and saves the results.
Output: the final image with red lanes, plus four saved files per photo (see Output files).

## Pipeline order
1. load_image
2. color_mask: keep only white and yellow pixels
3. blur_image: smooth the masked photo
4. detect_edges: find the outlines of the paint
5. region_of_interest: crop to the road area
6. draw_lanes: paint the result red on the original

The ROI is applied after edge detection, so the sky is processed too but removed before drawing.

## Region of interest (ROI)
Each photo has its own polygon, because the road sits in a different place in every picture.

ROI_1 = [(0, 1), (0, 0.76), (0.55, 0.50), (0.60, 0.50), (1, 1)]
ROI_2 = [(0, 1), (0, 0.95), (0.40, 0.64), (0.56, 0.64), (1, 0.92), (1, 1)]

(0, 1) is the bottom-left corner and (1, 1) is the bottom-right. A new photo needs a new ROI: place the corners just outside the lane lines, from the bottom of the picture up to the horizon.

## Output files
For each photo (shown for Original.jpg), the outputs folder gets:
- OriginalMask.jpg: the white and yellow color mask
- OriginalDetect_Edges.jpg: the Canny edges
- OriginalDraw_Lanes.jpg: the edges left after the ROI crop
- OriginalLanes.jpg: the final photo with red lanes

## Requirements and running
Needs Python 3, OpenCV and NumPy: pip install opencv-python numpy
Put the photos in an images folder next to the script, run the script, and press any key to close the result windows.

## Tuning
Color ranges in color_mask: loosen them if lines are missed, tighten them if grass or road gets picked up.
Canny thresholds (50, 150): lower values find more edges, higher values find fewer.

## Known limitations
Faint lines far in the distance can be missed or look broken, especially in Photo 1.
Yellow-looking grass inside the ROI can leave small stray marks.
The result is the outline of the paint, not one clean line per lane.
The ROI and color ranges are set by hand for these two photos.

## Note
Every function returns a new image and does not change the original.