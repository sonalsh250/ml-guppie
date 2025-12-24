import colorgram                   # Library for extracting prominent colors from an image
import matplotlib.pyplot as plt    # Library for plotting/visualizing data in graphs and images
import os
import re

IMAGE_PATH = 'image5.jpg'  # The file name of your image (make sure this image is in your project folder)
NUM_COLORS = 6             # How many colors do you want in your palette? Change this for more/less colors

# --------- COLOR EXTRACTION PHASE ---------

# Extract 'NUM_COLORS' most common colors from the image using colorgram
# 'colors' will be a list of Color objects extracted from the image
colors = colorgram.extract(IMAGE_PATH, NUM_COLORS)

# --------- OPTIONAL SORTING ---------

# This line sorts the colors list by each color's hue (color family), for a rainbow-like effect.
# Remove/comment this if you want them to stay unsorted.
colors.sort(key=lambda c: c.hsl.h)

# --------- DATA PREPARATION FOR VISUALIZATION ---------

# Create a list of RGB tuples from the Color objects.
# Example: (250, 200, 10)
rgb_colors = [(c.rgb.r, c.rgb.g, c.rgb.b) for c in colors]

# Create a list of how much of the image each color covers (values sum to ~1)
proportions = [c.proportion for c in colors]

# Normalize proportions just in case they do not add to exactly 1
total = sum(proportions)
proportions = [p / total for p in proportions]

# --------- VISUALIZATION: DRAW THE PALETTE BAR ---------

# Set up a blank figure sized 8 units wide by 2 tall
fig, ax = plt.subplots(figsize=(8, 2))

start = 0  # This marks where each color block starts

# For each color and how much of the image it covers:
for rgb, prop in zip(rgb_colors, proportions):
    # Plots a rectangle of width equal to the color's proportion.
    # Colors must be in [0, 1] for matplotlib, so divide each RGB value by 255.
    rect = plt.Rectangle((start, 0), prop, 1, color=[v/255 for v in rgb])
    ax.add_patch(rect)          # Add the rectangle to the figure
    start += prop               # Move the start point to the right for the next color

# Hide axis lines and numbers for a cleaner look
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# --- Find the next available paletteX.png ---
pattern = re.compile(r"palette(\d+)\.png")
existing_files = [f for f in os.listdir('.') if pattern.match(f)]
indices = [int(pattern.match(f).group(1)) for f in existing_files if pattern.match(f)]
next_index = 1
if indices:
    next_index = max(indices) + 1

output_filename = f"palette{next_index}.png"

# --------- SAVE AND SHOW THE OUTPUT ---------

plt.savefig(output_filename)
# plt.savefig("palette.png") # Save the palette bar as an image file in your folder
plt.show()                # Open a window to show the palette bar visually