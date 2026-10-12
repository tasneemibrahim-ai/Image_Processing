#import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")

        self.original_image_label = tk.Label(root)
        self.original_image_label.pack()

        self.enhanced_image_labels = [tk.Label(root), tk.Label(root)]
        for label in self.enhanced_image_labels:
            label.pack()

        self.segmented_image_labels = [tk.Label(root), tk.Label(root)]
        for label in self.segmented_image_labels:
            label.pack()

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.enhance_button = tk.Button(root, text="Enhance Image", command=self.enhance_image)
        self.enhance_button.pack()

        self.segment_button = tk.Button(root, text="Segment Image", command=self.segment_image)
        self.segment_button.pack()

        self.final_screen_button = tk.Button(root, text="Final Process", command=self.final_screen)
        self.final_screen_button.pack()

        self.original_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.original_image_label)

    def enhance_image(self):
        if self.original_image is not None:
           self.Thresholding(self.original_image)
           self.power_trnsform()
           self.display_image(self.original_image, self.original_image_label)
            
           
    def segment_image(self):
        if self.original_image is not None:
            self.watershed_segmentation(self.original_image)
            self.display_image(self.original_image, self.original_image_label)
            
    def display_image(self, image, label):
        image.thumbnail((300, 300))
        photo_image = ImageTk.PhotoImage(image)
        label.configure(image=photo_image)
        label.image = photo_image

    def final_screen(self):
        self.display_image(self.original_image, self.original_image_label)
        self.enhance_image()
        self.segment_image()

    def watershed_segmentation(self, path):

          image = cv2.imread(path)
        
        # Convert BGR image to RGB for displaying with matplotlib
          image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Display the original image
          plt.imshow(image_rgb)
          plt.title('Original Image')
          plt.axis('off')
          plt.show()
        
        # Convert the image to grayscale
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Display the grayscale image
          plt.imshow(gray, cmap='gray')
          plt.title('Grayscale Image')
          plt.axis('off')
          plt.show()
        
        # Apply thresholding
          ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Noise removal
          kernel = np.ones((3, 3), np.uint8)
          opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Display the enhanced image
          plt.imshow(opening, cmap='gray')
          plt.title('Enhanced Image')
          plt.axis('off')
          plt.show()
        
        # Sure background area
          sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # Finding sure foreground area
          dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
          ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        
        # Finding unknown region
          sure_fg = np.uint8(sure_fg)
          unknown = cv2.subtract(sure_bg, sure_fg)
        
        # Marker labelling
          ret, markers = cv2.connectedComponents(sure_fg)
        
        # Add one to all labels so that sure background is not 0, but 1
          markers = markers + 1
        
        # Mark the unknown region with 0
          markers[unknown == 255] = 0
        
        # Apply watershed algorithm
          markers = cv2.watershed(image, markers)
        
        # Mark watershed boundaries
          image[markers == -1] = [0, 0, 255]
        
        # Convert BGR image to RGB for displaying with matplotlib
          segmented_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Display the segmented image
          plt.imshow(segmented_image_rgb)
          plt.title('Segmented Image')
          plt.axis('off')
          plt.show()
          
    def power_trnsform ( self , power ):
    
       img_converted=cv2.cvtColor(self,cv2.COLOR_BGR2RGB)           # convert to show the origenal photos 
            
       imge_normalize = img_converted / 255      # normalize photos 
        
       power_trnsform =  np.power(imge_normalize, power )  #conve normalize photo brightness
         
       plt.figure(figsize=[15,5])
       plt.subplot(121); plt.imshow(self,cmap='gray') ; plt.title("orignal ")
       plt.subplot(122); plt.imshow(power_trnsform,cmap='gray') ; plt.title("transform ")
    
       return power_trnsform
    
    
    def Thresholding(self, path):
        
        gray_img=cv2.cvtColor(Image,cv2.COLOR_BGR2GRAY) # Convert the image to grayscale
        
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(Image)
        plt.title('Original Image') 
        
    
        threshold = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) #calculates the optimal threshold value
        
        thresh_I = np.zeros_like(Image)
        thresh_I[Image > threshold[0]] = 255
        
        plt.subplot(1, 2, 2)
        Threshold_Image=plt.imshow(thresh_I, cmap='gray')
        plt.title('Threshold Image')
    
        return Threshold_Image

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
