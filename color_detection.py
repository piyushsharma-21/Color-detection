import cv2
import numpy as np
import pandas as pd
# Specify the path to the image file
img_path = 'C:/Users/piyus/OneDrive/Desktop/projects/color detection/colorpic.jpg'

# Reading the image with OpenCV
img = cv2.imread(img_path)

# Declaring global variables 
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
# Ensure that 'colors.csv' is in the same directory as your script,
# or provide the correct path to it.
csv_path = 'C:/Users/piyus/OneDrive/Desktop/projects/color detection/colors.csv'
try:
    csv = pd.read_csv(csv_path, names=index, header=None)
except FileNotFoundError:
    print(f"Error: File '{csv_path}' not found.")
    exit()

# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

# Function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow("image", img)
    
    if clicked:
        # Draw rectangle to show selected color region
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Create text string to display (Color name and RGB values)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        
        # Display color name and RGB values
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            
        clicked = False

    # Exit the program when the user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
