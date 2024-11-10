import cv2
import pandas as pd
import argparse

# global variables
clicked = False
r = g = b = x_pos = y_pos = 0

# reading the csv file with pandas
# source: https://github.com/codebrainz/color-names/blob/master/output/colors.csv
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# template for the app-open command
command = argparse.ArgumentParser()
command.add_argument("-i", "--image", required=True, help="Image Path")
args = vars(command.parse_args())


# reading the picture given as argument
image_path = args["image"]
img = cv2.imread(image_path)


def getColorName(red, green, blue):
    """
    Finds the closest matching color of the given color (given as rgb values), from our dataset.

    :param red: integer ([0, 255])
    :param green: integer ([0, 255])
    :param blue: integer ([0, 255])
    :return: string
    """
    minimum_error = 100000
    color_name = None

    for i in range(len(csv)):
        error_score = abs(red - int(csv.loc[i, "R"])) + abs(green - int(csv.loc[i, "G"])) + abs(
            blue - int(csv.loc[i, "B"]))

        if error_score <= minimum_error:
            minimum_error = error_score
            color_name = csv.loc[i, "color_name"]

    if color_name is None:
        return "invalid color"

    return color_name


def draw_function(event, x, y, flags, param):
    """
    Get x,y coordinates of mouse double click;
    Callback function for mouse-click events.

    :param event: mouse-click event
    :param x: integer
    :param y: integer
    """
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked

        clicked = True
        x_pos = x
        y_pos = y

        b, g, r = img[y, x]

        r = int(r)
        g = int(g)
        b = int(b)


cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_function)

while True:

    cv2.imshow("image", img)
    cv2.putText(img, "Press esc to exit", (10, 20), 2, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
    if clicked:

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)
        cv2.rectangle(img, (20, 780), (900, 720), (b, g, r), -1)

        # text string for display (color name and RGB values)
        text = getColorName(r, g, b) + " red: " + str(r) + " green: " + str(g) + " blue: " + str(b)

        cv2.putText(img, text, (30, 760), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if r + g + b >= 500:
            cv2.putText(img, text, (30, 760), 2, 1, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

# close app's window
cv2.destroyAllWindows()
