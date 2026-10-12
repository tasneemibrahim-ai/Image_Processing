import tkinter as tk
from tkinter import filedialog

#from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageDraw, ImageStat, ImageEnhance
#from skimage import filters, morphology, segmentation
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import cv2

class ImageProcessorApp(tk.Tk):
    def __init__(img):
        
        img.title("Image Processor")
        img.geometry("800x600")

        img.original_image = None
        img.enhanced_images = []
        img.segmented_images = []

        img.create_widgets()

    def create_widgets(img):
       # Menu bar
       
       menubar = tk.Menu(img)
       file_menu = tk.Menu(menubar, tearoff=0)
       file_menu.add_command(label="UPload", command=img.Upload_image)
       file_menu.add_command(label="Save", command=img.save_image)
       file_menu.add_command(label="Exit", command=img.quit)
       menubar.add_cascade(label="File", menu=file_menu)
       img.config(menu=menubar)

       # Tabs for Enhancement and Segmentation
       tab_control = tk.Notebook(img)
       enhancement_tab = tk.Frame(tab_control)
       segmentation_tab = tk.Frame(tab_control)
       tab_control.add(enhancement_tab, text="Enhancement")
       tab_control.add(segmentation_tab, text="Segmentation")

       # Original Image display
       img.original_label = tk.Label(enhancement_tab)
       img.original_label.pack()

       # Enhanced Image display
       img.enhanced_label = tk.Label(enhancement_tab)
       img.enhanced_label.pack()

       # Segmented Image display
       img.segmented_label = tk.Label(segmentation_tab)
       img.segmented_label.pack()

       # Final Screen
       final_label = tk.Label(img, text="Final Screen")
       final_label.pack()
       
       def Upload_image(img):
           file_path = filedialog.askopenfilename()
           if file_path:
               img.original_image = Image.open(file_path)
               img.display_image(img.original_label, img.original_image)

       def save_image(img):
           if img.segmented_images:
               save_path = filedialog.asksaveasfilename(defaultextension=".png")
               if save_path:
                   img.segmented_images[0].save(save_path)

       def enhance_image(img, technique):
           if img.original_image:
               enhanced_image = None
               if technique == "Enhancement Technique 1":
                   enhanced_image = img.original_image.filter(ImageFilter.SHARPEN)
               elif technique == "Enhancement Technique 2":
                     enhanced_image = ImageOps.autocontrast(img.original_image)
               img.enhanced_images.append(enhanced_image)
               img.display_image(img.enhanced_label, enhanced_image)


       def watershed_segmentation(path):
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


       def display_image(img, label, image):
           img_tk = ImageTk.PhotoImage(image)
           label.config(image=img_tk)
           label.image = img_tk
           
       #final Screen   
       def Final_Screen(img):
           if img.original_image is not None:
               img.original_image()
               img.enhance_image()
               img.segment_image()
                  
if __name__ == "__main__":
        app = ImageProcessorApp()
        app.mainloop()