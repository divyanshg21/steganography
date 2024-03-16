import cv2
import numpy as np
import math

# Function to generate Fibonacci series
def generate_fibonacci_series(n):
    fib_series = [0, 1]
    while len(fib_series) < n:
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series

# Function to convert decimal to binary
def decimal_to_binary(decimal):
    return bin(decimal)[2:].zfill(8)

# Length of the binary representation of the Fibonacci series
def get_fibonacci_binary_length(fibonacci_series):
    return len(''.join([decimal_to_binary(x) for x in fibonacci_series]))

# Calculate the number of pixels needed to embed the Fibonacci series using LSB steganography
def calculate_pixels_needed(fibonacci_series):
    fibonacci_binary_length = get_fibonacci_binary_length(fibonacci_series)
    bits_per_pixel = 3  # Assuming each pixel has 3 channels (BGR) and we use the LSB of each channel
    return math.ceil(fibonacci_binary_length / bits_per_pixel)

# Read the image using OpenCV
image = cv2.imread('input_image.png')

# Check if the image was read successfully
if image is None:
    print("Error: Unable to read the image.")
else:
    print("Image read successfully.")

    # Generate Fibonacci series
    fibonacci_series = generate_fibonacci_series(20)

    # Calculate the number of pixels needed
    pixels_needed = calculate_pixels_needed(fibonacci_series)

    print("Number of pixels needed to embed the Fibonacci series:", pixels_needed)
