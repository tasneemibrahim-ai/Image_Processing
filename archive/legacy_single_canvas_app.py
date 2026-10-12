import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import cv2
import numpy as np


class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processor")

        self.original_image = None
        self.enhanced_image = None
        self.segmented_image = None
        self.enhancement_technique = None
        self.segmentation_technique = None

        self.canvas_width = 800
        self.canvas_height = 400

        self.create_widgets()

    def create_widgets(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.load_image, font=("Arial", 12), bg="lightblue", fg="black")
        self.load_button.pack(side=tk.LEFT, padx=3)

        self.enhance_button1 = tk.Button(self.button_frame, text="Enhance (Thresholding)", command=lambda: self.enhance_image("Thresholding"), font=("Arial", 12), bg="lightgreen", fg="black")
        self.enhance_button1.pack(side=tk.LEFT, padx=3)

        self.enhance_button2 = tk.Button(self.button_frame, text="Enhance (Power Transform)", command=lambda: self.enhance_image("Power Transform"), font=("Arial", 12), bg="lightgreen", fg="black")
        self.enhance_button2.pack(side=tk.LEFT, padx=5)

        self.enhance_button3 = tk.Button(self.button_frame, text="Enhance (Bit Plane Slice)", command=lambda: self.enhance_image("Bit Plane Slice"), font=("Arial", 12), bg="lightgreen", fg="black")
        self.enhance_button3.pack(side=tk.LEFT, padx=4)

        self.log_transform_button = tk.Button(self.button_frame, text="Segment(LogTransform)", command=lambda:self.segment_image("Log Transform"), font=("Arial", 12), bg="lightcoral", fg="black")
        self.log_transform_button.pack(side=tk.LEFT, padx=5)

        self.segment_button1 = tk.Button(self.button_frame, text="Segment (Adaptive Thresholding)", command=lambda: self.segment_image("Adaptive Thresholding"), font=("Arial", 12), bg="lightcoral", fg="black")
        self.segment_button1.pack(side=tk.LEFT, padx=5)

        self.segment_button2 = tk.Button(self.button_frame, text="Segment (Watershed)", command=self.segment_watershed, font=("Arial", 12), bg="lightcoral", fg="black")
        self.segment_button2.pack(side=tk.LEFT, padx=5)

        self.display_button = tk.Button(self.button_frame, text="Display", command=self.display_results, font=("Arial", 12), bg="lightyellow", fg="black")
        self.display_button.pack(side=tk.LEFT, padx=3)

        self.export_button = tk.Button(self.button_frame, text="Export", command=self.export_image, font=("Arial", 12), bg="lightpink", fg="black")
        self.export_button.pack(side=tk.LEFT, padx=3)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset, font=("Arial", 12), bg="lightgray", fg="black")
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10)

        self.enhancement_technique_label = tk.Label(self.master, text="Enhancement Technique: None", font=("Arial", 12))
        self.segmentation_technique_label = tk.Label(self.master, text="Segmentation Technique: None", font=("Arial", 12))

        self.close_frame = tk.Frame(self.master)
        self.close_frame.pack(expand=True, fill=tk.BOTH)

        self.close_button = tk.Button(self.close_frame, text="Close The Program", command=self.master.destroy, font=("Arial", 12), bg="red", fg="white")
        self.close_button.pack(side=tk.LEFT, padx=5)

    def load_image(self):
        loading_text = tk.Label(self.master, text="Loading...", font=("Arial", 12))
        loading_text.pack()
        
        self.master.update()

        self.master.after(2000)

        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.resize_image(self.original_image)
            self.display_image(self.original_image)

        loading_text.pack_forget()

    def enhance_image(self, technique):
        enhancing_text = tk.Label(self.master, text="Enhancing Image...", font=("Arial", 12))
        enhancing_text.pack()
        self.master.update()

        self.master.after(2000)

        if self.original_image is not None:
            if technique == "Thresholding":
                self.enhanced_image = self.thresholding(self.original_image)
                self.enhancement_technique = "Thresholding"
            elif technique == "Power Transform":
                self.enhanced_image = self.power_transform(self.original_image, 1.5)
                self.enhancement_technique = "Power Transform"
            elif technique == "Bit Plane Slice":
                self.enhanced_image = self.bit_plane_slice(self.original_image)
                self.enhancement_technique = "Bit Plane Slice"

        enhancing_text.pack_forget()

    def apply_log_transform(self,img):
        if self.original_image is not None:
            self.segmented_image = self.log_transform(self.original_image)
            self.segmentation_technique = "Log Transform"
            self.display_results()

    def segment_image(self, technique):
        segmenting_text = tk.Label(self.master, text="Segmenting Image...", font=("Arial", 12))
        segmenting_text.pack()
        self.master.update()

        self.master.after(2000)

        if self.original_image is not None:
            if technique == "Adaptive Thresholding":
                self.segmented_image = self.adaptive_thresholding(self.original_image)
                self.segmentation_technique = "Adaptive Thresholding"
            elif technique == "Log Transform":
                self.segmented_image = self.log_transform(self.original_image)
                self.segmentation_technique = "Log Transform"
                

        segmenting_text.pack_forget()

    def segment_watershed(self):
        segmenting_text = tk.Label(self.master, text="Segmenting Image (Watershed)...", font=("Arial", 12))
        segmenting_text.pack()
        self.master.update()

        self.master.after(2000)

        if self.original_image is not None:
            self.segmented_image = self.watershed_segmentation(self.original_image)
            self.segmentation_technique = "Watershed"

        segmenting_text.pack_forget()

    def display_results(self):
        displaying_text = tk.Label(self.master, text="Displaying Results...", font=("Arial", 12))
        displaying_text.pack()
        self.master.update()

        self.master.after(2000)

        self.canvas.delete("all")

        if self.original_image is not None:
            self.display_image(self.original_image)

        if self.enhanced_image is not None:
            self.display_image(self.enhanced_image)
            self.display_technique_label(self.enhancement_technique)

        if self.segmented_image is not None:
            self.display_image(self.segmented_image)
            self.display_technique_label(self.segmentation_technique)

        displaying_text.pack_forget()

    def display_image(self, img):
        img = self.resize_image(img)
        img = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, anchor=tk.CENTER, image=img)
        self.canvas.image = img

    def resize_image(self, img):
        img_width, img_height = img.size
        max_width = self.canvas_width - 20
        max_height = self.canvas_height - 20
        if img_width > max_width or img_height > max_height:
            ratio = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            img = img.resize((new_width, new_height))
        return img

    def display_technique_label(self, technique):
        if technique == "Thresholding":
            label_text = "Enhancement Technique: Thresholding"
        elif technique == "Power Transform":
            label_text = "Enhancement Technique: Power Transform"
        elif technique == "Bit Plane Slice":
            label_text = "Enhancement Technique: Bit Plane Slice"
        elif technique == "Log Transform":
            label_text = "Segmentation Technique: Log Transform"
        elif technique == "Adaptive Thresholding":
            label_text = "Segmentation Technique: Adaptive Thresholding"
        elif technique == "Watershed":
            label_text = "Segmentation Technique: Watershed"
        
        technique_label = tk.Label(self.master, text=label_text, font=("Arial", 12))
        technique_label.pack()

    def thresholding(self, img):
        gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        threshold = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh_I = np.zeros_like(gray_img)
        thresh_I[gray_img > threshold[0]] = 255
        return Image.fromarray(thresh_I)

    def power_transform(self, img, power):
        img_converted = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img_normalized = img_converted / 255
        power_transformed_img = np.power(img_normalized, power)
        power_transformed_img *= 255
        power_transformed_img = power_transformed_img.astype(np.uint8)
        power_transformed_img = cv2.cvtColor(power_transformed_img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(power_transformed_img)

    def bit_plane_slice(self, img):
        gray_image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        # Initialize an empty list to store the bit-plane images
        bit_planes = []
 
        for i in range(8):
         
            mask = 1 << i  # Use bitwise shift to create the mask
           
            bit_plane = cv2.bitwise_and(gray_image, mask)
            # Convert the bit-plane image to PIL format
            bit_plane_pil = Image.fromarray(bit_plane.astype('uint8'))
     
            if bit_plane_pil.mode != 'L':
                bit_plane_pil = bit_plane_pil.convert('L')
            bit_planes.append(bit_plane_pil)
   
        combined_image = Image.new('RGB', (8 * bit_planes[0].width, bit_planes[0].height))
        x_offset = 0
        for plane in bit_planes:
            combined_image.paste(plane, (x_offset, 0))
            x_offset += plane.width
        return combined_image

    def log_transform(self, image, c=1):
        # Convert image to grayscale
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        gray_image = gray_image + 1e-10   
        
        # Apply log transformation
        transformed_image = c * np.log(gray_image)
        
        
        transformed_image = np.uint8(transformed_image * 255 / np.max(transformed_image))
        
        # Convert the transformed image to PIL format
        transformed_image_pil = Image.fromarray(transformed_image)
        
        return transformed_image_pil

    def adaptive_thresholding(self, img):
        gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        adaptive_threshold = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        return Image.fromarray(adaptive_threshold)

    def watershed_segmentation(self, img):
        image = np.array(img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(image, markers)
        image[markers == -1] = [0, 0, 255]
        segmented_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        segmented_image_pil = Image.fromarray(segmented_image_rgb)
        return segmented_image_pil

    def export_image(self):
        if self.canvas.find_all():
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                displayed_image = self.get_displayed_image()
                displayed_image.save(file_path)

    def get_displayed_image(self):
        x = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab().crop((x, y, x1, y1))
        return image

    def reset(self):
        self.original_image = None
        self.enhanced_image = None
        self.segmented_image = None
        self.enhancement_technique = None
        self.segmentation_technique = None
        self.canvas.delete("all")

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
