import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import cv2
import numpy as np
import time


class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Enhancement & Segmentation Studio")

        self.original_image = None
        self.filtered_image = None
        self.enhancement_technique = None
        self.segmentation_technique = None
        self.segmented_image = None
        self.power_value = None  # Store power value entered by user

        self.canvas_width = 800
        self.canvas_height = 400

        self.create_widgets()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(pady=10)

        self.original_canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width // 2, height=self.canvas_height, bg="white")
        self.original_canvas.pack(side=tk.LEFT, padx=(0, 5))

        self.processed_canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width // 2, height=self.canvas_height, bg="white")
        self.processed_canvas.pack(side=tk.LEFT, padx=(5, 0))

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.load_image, font=("Arial", 12), bg="lightblue", fg="black")
        self.load_button.pack(side=tk.LEFT, padx=3)

        self.enhance_button1 = tk.Button(self.button_frame, text="Enhance (Thresholding)", command=lambda: self.enhance_image("Thresholding"), font=("Arial", 12), bg="lightgreen", fg="black")
        self.enhance_button1.pack(side=tk.LEFT, padx=3)

        self.enhance_button2 = tk.Button(self.button_frame, text="Enhance (Power Transform)", command=self.ask_power_transform, font=("Arial", 12), bg="lightgreen", fg="black")
        self.enhance_button2.pack(side=tk.LEFT, padx=5)

        self.enhance_button3 = tk.Button(self.button_frame, text="Enhance (Bit Plane Slice)", command=lambda: self.enhance_image("Bit Plane Slice"), font=("Arial", 12), bg="lightgreen", fg="black")
        self.enhance_button3.pack(side=tk.LEFT, padx=4)

        self.segment_button1 = tk.Button(self.button_frame, text="Segment (Adaptive Thresholding)", command=lambda: self.segment_image("Adaptive Thresholding"), font=("Arial", 12), bg="lightcoral", fg="black")
        self.segment_button1.pack(side=tk.LEFT, padx=5)

        self.segment_button2 = tk.Button(self.button_frame, text="Segment (Log Transform)", command=lambda: self.segment_image("Log Transform"), font=("Arial", 12), bg="lightcoral", fg="black")
        self.segment_button2.pack(side=tk.LEFT, padx=5)

        self.segment_button3 = tk.Button(self.button_frame, text="Segment (Watershed)", command=self.segment_watershed, font=("Arial", 12), bg="lightcoral", fg="black")
        self.segment_button3.pack(side=tk.LEFT, padx=5)

        self.display_button = tk.Button(self.button_frame, text="Close", command=self.close_program, font=("Arial", 12), bg="red", fg="white")
        self.display_button.pack(side=tk.LEFT, padx=3)

        self.export_button = tk.Button(self.button_frame, text="Export", command=self.export_canvas, font=("Arial", 12), bg="lightblue", fg="black")
        self.export_button.pack(side=tk.LEFT, padx=3)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_canvas, font=("Arial", 12), bg="lightgray", fg="black")
        self.reset_button.pack(side=tk.LEFT, padx=3)

       

        self.filter_text = tk.Label(self.master, text="", font=("Arial", 12), wraplength=400)
        self.filter_text.pack()

    def load_image(self):
        loading_text = tk.Label(self.master, text="Loading...", font=("Arial", 12))
        loading_text.pack()
        self.master.update()
        self.master.after(2000)

        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.resize_image(self.original_image)
            self.display_image(self.original_image, canvas=self.original_canvas)
        loading_text.pack_forget()
        
    def ask_power_transform(self):
        self.ask_for_power()

    def ask_for_power(self):
        power_dialog = tk.Toplevel(self.master)
        power_dialog.title("Enter Power Value")
        power_dialog.geometry("200x100")
        power_dialog.resizable(False, False)

        power_label = tk.Label(power_dialog, text="Enter Power Value:", font=("Arial", 12))
        power_label.pack(pady=5)

        power_entry = tk.Entry(power_dialog, font=("Arial", 12))
        power_entry.pack(pady=5)

        def apply_power():
            try:
                power_value = float(power_entry.get())
                if power_value <= 0:
                    messagebox.showerror("Error", "Power value must be > 0")
                else:
                    power_dialog.destroy()
                    self.enhance_image("Power Transform", power_value)  
            except ValueError:
                messagebox.showerror("Error", "Invalid . Please enter a number.")

        apply_button = tk.Button(power_dialog, text="Apply", command=apply_power, font=("Arial", 12))
        apply_button.pack(pady=5)

    def enhance_image(self, technique, power=None):
        
        enhancing_text = tk.Label(self.master, text="Enhancing Image...", font=("Arial", 12))
        enhancing_text.pack()
        self.master.update()

        self.master.after(2000)

        if technique == "Thresholding":
            self.filtered_image = self.thresholding(self.original_image)
            self.enhancement_technique = "Thresholding"
        elif technique == "Power Transform":
            if power is None:
                messagebox.showerror("Error", "Power value is required for Power Transform.")
                return
            self.filtered_image = self.power_transform(self.original_image, power)  
            self.enhancement_technique = "Power Transform"
        elif technique == "Bit Plane Slice":
            self.filtered_image = self.bit_plane_slice(self.original_image)
            self.enhancement_technique = "Bit Plane Slice"
        self.display_results()
        enhancing_text.pack_forget()
        
        
        
    def segment_image(self, technique):
        enhancing_text = tk.Label(self.master, text="Segmenting Image...", font=("Arial", 12))
        enhancing_text.pack()
        self.master.update()

        self.master.after(2000)

        if technique == "Adaptive Thresholding":
            self.segmented_image = self.adaptive_thresholding(self.original_image)
            self.segmentation_technique = "Adaptive Thresholding"
        elif technique == "Log Transform":
            self.segmented_image = self.log_transform(self.original_image)
            self.segmentation_technique = "Log Transform"
        self.display_results()
        
        enhancing_text.pack_forget()

    def segment_watershed(self):
        enhancing_text = tk.Label(self.master, text="Segmenting Image...", font=("Arial", 12))
        enhancing_text.pack()
        self.master.update()

        self.master.after(2000)

        if self.original_image is not None:
            self.segmented_image = self.watershed_segmentation(self.original_image)
            self.segmentation_technique = "Watershed"
            self.display_results()
        enhancing_text.pack_forget()    

    def display_results(self):
        self.processed_canvas.delete("all")
        if self.filtered_image is not None:
            if self.enhancement_technique == "Bit Plane Slice":
            # Display the Bit Plane Slice result in a larger size
               self.display_image(self.filtered_image, canvas=self.processed_canvas, x_offset=10, y_offset=150)
            else:
                self.display_image(self.filtered_image, canvas=self.processed_canvas)
            self.filter_text.config(text=f"Enhancement Technique: {self.enhancement_technique}")
        elif self.segmented_image is not None:
            self.display_image(self.segmented_image, canvas=self.processed_canvas)
            self.filter_text.config(text=f"Segmentation Technique: {self.segmentation_technique}") 

    def export_canvas(self):
        if self.filtered_image or self.segmented_image:
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if filename:
                if self.filtered_image:
                    self.filtered_image.save(filename)
                elif self.segmented_image:
                    self.segmented_image.save(filename)

    def display_image(self, img, x_offset=0, y_offset=0, canvas=None):
        img = self.resize_image(img)
        img = ImageTk.PhotoImage(image=img)
        if canvas:
            canvas.create_image(x_offset + img.width() // 2, y_offset + img.height() // 2, anchor=tk.CENTER, image=img)
            canvas.image = img

    def resize_image(self, img):
        img_width, img_height = img.size
        max_width = self.canvas_width // 2 - 20
        max_height = self.canvas_height - 20
        if img_width > max_width or img_height > max_height:
            ratio = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            img = img.resize((new_width, new_height))
        return img

    def thresholding(self, img):
        gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        threshold = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
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
        bit_planes = []
        fixed_width = 40   
        fixed_height = 100   

        for i in range(8):
            mask = 1 << i
            bit_plane = cv2.bitwise_and(gray_image, mask)
            bit_plane_pil = Image.fromarray(bit_plane.astype('uint8'))
            if bit_plane_pil.mode != 'L':
                bit_plane_pil = bit_plane_pil.convert('L')
            bit_plane_pil = bit_plane_pil.resize((fixed_width, fixed_height))
            bit_planes.append(bit_plane_pil)

        combined_image = Image.new('RGB', (8 * fixed_width, fixed_height))
        x_offset = 0
        for plane in bit_planes:
            combined_image.paste(plane, (x_offset, 0))
            x_offset += fixed_width
        return combined_image

    def adaptive_thresholding(self, img):
        gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        adaptive_threshold = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        return Image.fromarray(adaptive_threshold)

    def log_transform(self, image):
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        gray_image = gray_image + 1e-10
        transformed_image = np.log(gray_image)
        transformed_image = np.uint8(transformed_image * 255 / np.max(transformed_image))
        transformed_image_pil = Image.fromarray(transformed_image)
        return transformed_image_pil

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

    def reset_canvas(self):
        self.original_image = None
        self.filtered_image = None
        self.enhancement_technique = None
        self.segmentation_technique = None
        self.segmented_image = None
        self.original_canvas.delete("all")
        self.processed_canvas.delete("all")
        self.filter_text.config(text="")

    def close_program(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
