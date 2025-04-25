import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import VGG19
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

# Ensure 'data' directory exists
os.makedirs("data", exist_ok=True)

# Load FER2013 dataset
dataset_path = "C:\\Users\\ASUS\\Desktop\\fer2013\\fer2013.csv"  # Update this path if needed
df = pd.read_csv(dataset_path)

# Extract features and labels
X = []
y = []
for index, row in df.iterrows():
    pixels = np.array(row['pixels'].split(), dtype='float32').reshape(48, 48, 1)  # Grayscale
    X.append(pixels)
    y.append(row['emotion'])

X = np.array(X) / 255.0  # Normalize
y = np.array(y)

# Convert grayscale (1 channel) images to RGB (3 channels) for VGG-19
X = np.repeat(X, 3, axis=-1)

# Split dataset
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save preprocessed data
np.save("data/X_train.npy", X_train)
np.save("data/X_test.npy", X_test)
np.save("data/y_train.npy", y_train)
np.save("data/y_test.npy", y_test)

print("Data preprocessing completed!")   

# Load VGG-19 model
base_model = VGG19(weights="imagenet", include_top=False, input_shape=(48, 48, 3))

# Freeze base model layers
for layer in base_model.layers:
    layer.trainable = False

# Add custom layers
x = Flatten()(base_model.output)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(7, activation="softmax")(x)  # 7 emotions in FER2013 dataset

# Create model
model = Model(inputs=base_model.input, outputs=x)
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=32)

# Save model
model.save("C:\\MajorProject8thsem\\emotion_vgg19.h5")

print("Model training completed and saved!")
 
# Load trained model
model = tf.keras.models.load_model("emotion_vgg19.h5")

