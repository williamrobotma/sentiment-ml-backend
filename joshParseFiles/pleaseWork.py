import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data() #load_data() is Keras shortcut for iterating and assigning data to arrays
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images/255.0 #divide by 255 so the scale is from 0-1 instead of 0-255
test_images = test_images/255.0

print(train_images)
plt.imshow(train_images[7], cmap=plt.cm.binary)
plt.show()



