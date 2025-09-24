import matplotlib.pyplot as plt
import tensorflow as tf

# Load MNIST dataset from TensorFlow
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Function to display a digit
def show_digit(index):
    image = x_train[index]
    label = y_train[index]

    plt.imshow(image, cmap='gray')
    plt.title(f"Label: {label}")
    plt.axis('off')
    plt.show()

# Example: Show the 0th digit
for i in range(100):
    show_digit(i)
