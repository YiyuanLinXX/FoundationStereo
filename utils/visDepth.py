#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: visDepth.py
Author: Yiyuan Lin
Email: yl3663@cornell.edu
Date: 2025-04-21
Description: visualize depth map from a .npy file
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Load depth map (.npy file)
depth = np.load("../outputs/Crittenden_1004_DS_00112/depth_meter.npy")  # Replace with your file path

# Create a mask for valid depth values (> 0)
valid_mask = depth > 0
valid_depth = depth[valid_mask]

# Print basic statistics
print(f"Number of valid pixels: {valid_depth.size}")
print(f"Minimum valid depth: {valid_depth.min():.2f} m")
print(f"Maximum valid depth: {valid_depth.max():.2f} m")
print(f"Median depth: {np.median(valid_depth):.2f} m")
print(f"99th percentile depth: {np.percentile(valid_depth, 99):.2f} m")

# Clip depth values to 99th percentile for visualization
max_clip_depth = np.percentile(valid_depth, 99)

# Step 1: Plot depth histogram
plt.figure(figsize=(6, 4))
plt.hist(valid_depth[valid_depth < max_clip_depth], bins=100, color='steelblue')
plt.title("Depth Value Histogram (Clipped to 99th Percentile)")
plt.xlabel("Depth (meters)")
plt.ylabel("Pixel Count")
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 2: Visualize depth map
plt.figure(figsize=(10, 6))

# Mask invalid values and clip to visual range
masked_depth = np.ma.masked_where(~valid_mask, np.clip(depth, 0, max_clip_depth))

# Set color map and style
cmap = plt.cm.viridis
cmap.set_bad(color='black')  # Show invalid pixels as black

img = plt.imshow(masked_depth, cmap=cmap)
plt.colorbar(img, label="Depth (meters)")
plt.title("Depth Map (Clipped and Masked)")
plt.axis("off")
plt.tight_layout()
plt.show()

# Step 3 (Optional): Save depth visualization as PNG
# from PIL import Image
# import cv2
# normed_depth = np.uint8(255 * (np.clip(depth, 0, max_clip_depth) / max_clip_depth))
# color_depth = cv2.applyColorMap(normed_depth, cv2.COLORMAP_VIRIDIS)
# cv2.imwrite("depth_visualization.png", color_depth)
