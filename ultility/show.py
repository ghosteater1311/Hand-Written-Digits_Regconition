import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file (change path if needed)
file_path = '../digit_data1.csv'
data = pd.read_csv(file_path)

# Function to show a digit from the dataset
def show_digit(index):
    row = data.iloc[index]
    label = row['label']
    pixels = row[1:].values.reshape(28, 28)  # From flat to 2D
    plt.imshow(pixels, cmap='gray')
    plt.title(f"Label: {label}")
    plt.axis('off')
    plt.show()

# Show the first digit
for i in range(10):
    show_digit(i)
