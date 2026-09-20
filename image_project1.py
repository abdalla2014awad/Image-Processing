import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageProcessingApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Image Processing Project")
        self.root.geometry("1550x900")
        self.root.configure(bg="#eaeaea")

        # ___VARIABLES__

        self.original_image = None
        self.current_image = None
        self.history = []

        # ___TOP FRAME___

        top_frame = tk.Frame(root, bg="#d0d0d0", pady=10)
        top_frame.pack(fill="x")

        tk.Button(
            top_frame,
            text="Browse Image",
            command=self.load_image,
            width=18,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        tk.Button(
            top_frame,
            text="Reset",
            command=self.reset_image,
            width=15,
            bg="#f39c12",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        tk.Button(
            top_frame,
            text="Undo",
            command=self.undo,
            width=15,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        tk.Button(
            top_frame,
            text="Save",
            command=self.save_image,
            width=15,
            bg="#2980b9",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        self.status_label = tk.Label(
            top_frame,
            text="No Image Loaded",
            bg="#d0d0d0",
            fg="black",
            font=("Arial", 12, "bold")
        )

        self.status_label.pack(side="right", padx=20)

        # ___IMAGE FRAME___

        image_frame = tk.Frame(root, bg="#eaeaea")
        image_frame.pack(pady=10)

        self.original_label = tk.Label(
            image_frame,
            text="Original Image",
            bg="white",
            width=350,
            height=240,
            bd=3,
            relief="solid",
            font=("Arial", 12, "bold")
        )

        self.original_label.pack(side="left", padx=20)

        self.processed_label = tk.Label(
            image_frame,
            text="Processed Image",
            bg="white",
            width=350,
            height=240,
            bd=3,
            relief="solid",
            font=("Arial", 12, "bold")
        )

        self.processed_label.pack(side="right", padx=20)

        # ___FILTER FRAME___

        filter_frame = tk.Frame(root, bg="#eaeaea")
        filter_frame.pack()

        # ROW 1

        row1 = tk.Frame(filter_frame, bg="#eaeaea")
        row1.pack()

        self.create_histogram_operations(row1)
        self.create_lowpass_filters(row1)
        self.create_highpass_filters(row1)
        self.create_noise_filters(row1)

        # ROW 2

        row2 = tk.Frame(filter_frame, bg="#eaeaea")
        row2.pack()

        self.create_color_operations(row2)
        self.create_point_operations(row2)
        self.create_nonlinear_filters(row2)
        self.create_morphology_filters(row2)

    # ___IMAGE FUNCTIONS___

    def load_image(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg *.png *.jpeg *.bmp")
            ]
        )

        if path:
            image = cv2.imread(path)

            self.original_image = image.copy()
            self.current_image = image.copy()

            self.history.clear()

            self.display_images()

            self.status_label.config(text="Image Loaded")

    def display_images(self):

        if self.original_image is None:
            return

        DISPLAY_WIDTH = 350
        DISPLAY_HEIGHT = 240

        # ___ORIGINAL IMAGE___

        original_rgb = cv2.cvtColor(
            self.original_image,
            cv2.COLOR_BGR2RGB
        )

        original_pil = Image.fromarray(original_rgb)

        original_pil.thumbnail(
            (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        )

        original_tk = ImageTk.PhotoImage(original_pil)

        self.original_label.config(
            image=original_tk,
            width=DISPLAY_WIDTH,
            height=DISPLAY_HEIGHT
        )

        self.original_label.image = original_tk

        # ___PROCESSED IMAGE___

        processed = self.current_image.copy()

        if len(processed.shape) == 2:

            processed_pil = Image.fromarray(processed)

        else:

            processed_rgb = cv2.cvtColor(
                processed,
                cv2.COLOR_BGR2RGB
            )

            processed_pil = Image.fromarray(processed_rgb)

        processed_pil.thumbnail(
            (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        )

        processed_tk = ImageTk.PhotoImage(processed_pil)

        self.processed_label.config(
            image=processed_tk,
            width=DISPLAY_WIDTH,
            height=DISPLAY_HEIGHT
        )

        self.processed_label.image = processed_tk

    def update_image(self, new_image, filter_name):

        if self.current_image is not None:
            self.history.append(self.current_image.copy())

        self.current_image = new_image

        self.display_images()

        self.status_label.config(
            text=f"Current Filter: {filter_name}"
        )

    def reset_image(self):

        if self.original_image is not None:
            self.current_image = self.original_image.copy()

            self.display_images()

            self.status_label.config(text="Image Reset")

    def undo(self):

        if len(self.history) > 0:
            self.current_image = self.history.pop()

            self.display_images()

            self.status_label.config(text="Undo Applied")

    def save_image(self):

        if self.current_image is None:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".jpg"
        )

        if path:
            cv2.imwrite(path, self.current_image)

            messagebox.showinfo(
                "Saved",
                "Image Saved Successfully"
            )

    # ___GROUP CREATOR___

    def create_group(self, parent, title):

        frame = tk.LabelFrame(
            parent,
            text=title,
            padx=10,
            pady=10,
            bg="white",
            font=("Arial", 11, "bold")
        )

        frame.pack(side="left", padx=10, pady=10)

        return frame

    # ___POINT OPERATIONS___

    def create_point_operations(self, parent):

        frame = self.create_group(parent, "Point Operations")

        tk.Button(frame, text="Addition",
                  width=18,
                  command=self.addition).pack(pady=3)

        tk.Button(frame, text="Subtraction",
                  width=18,
                  command=self.subtraction).pack(pady=3)

        tk.Button(frame, text="Division",
                  width=18,
                  command=self.division).pack(pady=3)

        tk.Button(frame, text="Complement",
                  width=18,
                  command=self.complement).pack(pady=3)

    def addition(self):

        image = cv2.convertScaleAbs(
            self.current_image,
            alpha=1,
            beta=50
        )

        self.update_image(image, "Addition")

    def subtraction(self):

        image = cv2.convertScaleAbs(
            self.current_image,
            alpha=1,
            beta=-50
        )

        self.update_image(image, "Subtraction")

    def division(self):

        image = self.current_image / 2

        image = np.uint8(image)

        self.update_image(image, "Division")

    def complement(self):

        image = 255 - self.current_image

        self.update_image(image, "Complement")

    # ___COLOR OPERATIONS___

    def create_color_operations(self, parent):

        frame = self.create_group(parent, "Color Operations")

        tk.Button(frame, text="Increase Red",
                  width=18,
                  command=self.change_red).pack(pady=3)

        tk.Button(frame, text="Swap R-G",
                  width=18,
                  command=self.swap_rg).pack(pady=3)

        tk.Button(frame, text="Remove Red",
                  width=18,
                  command=self.remove_red).pack(pady=3)

    def change_red(self):

        image = self.current_image.copy()

        image[:, :, 2] = cv2.add(
            image[:, :, 2],
            50
        )

        self.update_image(image, "Increase Red")

    def swap_rg(self):

        image = self.current_image.copy()

        image[:, :, [1, 2]] = image[:, :, [2, 1]]

        self.update_image(image, "Swap R-G")

    def remove_red(self):

        image = self.current_image.copy()

        image[:, :, 2] = 0

        self.update_image(image, "Remove Red")

    # HISTOGRAM

    def create_histogram_operations(self, parent):

        frame = self.create_group(parent, "Histogram")

        tk.Button(frame,
                  text="Histogram Stretch",
                  width=18,
                  command=self.hist_stretch).pack(pady=3)

        tk.Button(frame,
                  text="Histogram Equalization",
                  width=18,
                  command=self.hist_equalization).pack(pady=3)

    def hist_stretch(self):

        gray = cv2.cvtColor(
            self.current_image,
            cv2.COLOR_BGR2GRAY
        )

        image = cv2.normalize(
            gray,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        self.update_image(image, "Histogram Stretch")

    def hist_equalization(self):

        gray = cv2.cvtColor(
            self.current_image,
            cv2.COLOR_BGR2GRAY
        )

        image = cv2.equalizeHist(gray)

        self.update_image(image,
                          "Histogram Equalization")

    # LOW PASS FILTERS

    def create_lowpass_filters(self, parent):

        frame = self.create_group(parent,
                                  "Low Pass Filters")

        tk.Button(frame,
                  text="Mean Filter",
                  width=18,
                  command=self.mean_filter).pack(pady=3)

        tk.Button(frame,
                  text="Median Filter",
                  width=18,
                  command=self.median_filter).pack(pady=3)

    def mean_filter(self):

        image = cv2.blur(
            self.current_image,
            (5, 5)
        )

        self.update_image(image, "Mean Filter")

    def median_filter(self):

        image = cv2.medianBlur(
            self.current_image,
            5
        )

        self.update_image(image, "Median Filter")

    # HIGH PASS FILTERS

    def create_highpass_filters(self, parent):

        frame = self.create_group(parent,
                                  "High Pass Filters")

        tk.Button(frame,
                  text="Laplacian",
                  width=18,
                  command=self.laplacian_filter).pack(pady=3)

        tk.Button(frame,
                  text="Sobel",
                  width=18,
                  command=self.sobel_filter).pack(pady=3)

    def laplacian_filter(self):

        gray = cv2.cvtColor(
            self.current_image,
            cv2.COLOR_BGR2GRAY
        )

        image = cv2.Laplacian(
            gray,
            cv2.CV_64F
        )

        image = np.uint8(np.absolute(image))

        self.update_image(image, "Laplacian")

    def sobel_filter(self):

        gray = cv2.cvtColor(
            self.current_image,
            cv2.COLOR_BGR2GRAY
        )

        sobelx = cv2.Sobel(
            gray,
            cv2.CV_64F,
            1,
            0
        )

        sobely = cv2.Sobel(
            gray,
            cv2.CV_64F,
            0,
            1
        )

        image = cv2.magnitude(sobelx, sobely)

        image = np.uint8(image)

        self.update_image(image, "Sobel")

    # NOISE RESTORATION

    def create_noise_filters(self, parent):

        frame = self.create_group(parent,
                                  "Noise Restoration")

        tk.Button(frame,
                  text="Salt & Pepper Removal",
                  width=22,
                  command=self.median_filter).pack(pady=3)

        tk.Button(frame,
                  text="Outlier Method",
                  width=22,
                  command=self.outlier_filter).pack(pady=3)

    def outlier_filter(self):

        image = cv2.medianBlur(
            self.current_image,
            3
        )

        self.update_image(image,
                          "Outlier Filter")

    # ___MORPHOLOGY___

    def create_morphology_filters(self, parent):

        frame = self.create_group(parent,
                                  "Morphology")

        tk.Button(frame,
                  text="Dilation",
                  width=22,
                  command=self.dilation).pack(pady=3)

        tk.Button(frame,
                  text="Erosion",
                  width=22,
                  command=self.erosion).pack(pady=3)

        tk.Button(frame,
                  text="Opening",
                  width=22,
                  command=self.opening).pack(pady=3)

        tk.Button(frame,
                  text="Internal Boundary",
                  width=22,
                  command=self.internal_boundary).pack(pady=3)

        tk.Button(frame,
                  text="External Boundary",
                  width=22,
                  command=self.external_boundary).pack(pady=3)

        tk.Button(frame,
                  text="Morph Gradient",
                  width=22,
                  command=self.morph_gradient).pack(pady=3)

    def get_binary(self):

        gray = cv2.cvtColor(
            self.current_image,
            cv2.COLOR_BGR2GRAY
        )

        _, binary = cv2.threshold(
            gray,
            127,
            255,
            cv2.THRESH_BINARY
        )

        return binary

    def dilation(self):

        kernel = np.ones((5, 5), np.uint8)

        binary = self.get_binary()

        image = cv2.dilate(
            binary,
            kernel,
            iterations=1
        )

        self.update_image(image, "Dilation")

    def erosion(self):

        kernel = np.ones((5, 5), np.uint8)

        binary = self.get_binary()

        image = cv2.erode(
            binary,
            kernel,
            iterations=1
        )

        self.update_image(image, "Erosion")

    def opening(self):

        kernel = np.ones((5, 5), np.uint8)

        binary = self.get_binary()

        image = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            kernel
        )

        self.update_image(image, "Opening")

    def internal_boundary(self):

        kernel = np.ones((3, 3), np.uint8)

        binary = self.get_binary()

        eroded = cv2.erode(binary, kernel)

        image = binary - eroded

        self.update_image(image,
                          "Internal Boundary")

    def external_boundary(self):

        kernel = np.ones((3, 3), np.uint8)

        binary = self.get_binary()

        dilated = cv2.dilate(binary, kernel)

        image = dilated - binary

        self.update_image(image,
                          "External Boundary")

    def morph_gradient(self):

        kernel = np.ones((3, 3), np.uint8)

        binary = self.get_binary()

        image = cv2.morphologyEx(
            binary,
            cv2.MORPH_GRADIENT,
            kernel
        )

        self.update_image(image,
                          "Morph Gradient")

    # ___NON LINEAR FILTERS___

    def create_nonlinear_filters(self, parent):

        frame = self.create_group(parent, "Non Linear Filters")

        tk.Button(frame,
                  text="Maximum Filter",
                  width=20,
                  command=self.max_filter).pack(pady=3)

        tk.Button(frame,
                  text="Minimum Filter",
                  width=20,
                  command=self.min_filter).pack(pady=3)

        tk.Button(frame,
                  text="Median Filter",
                  width=20,
                  command=self.median_filter).pack(pady=3)

        tk.Button(frame,
                  text="Mode Filter",
                  width=20,
                  command=self.mode_filter).pack(pady=3)

    def max_filter(self):

        kernel = np.ones((5, 5), np.uint8)

        image = cv2.dilate(self.current_image, kernel, iterations=1)

        self.update_image(image, "Maximum Filter")

    def min_filter(self):

        kernel = np.ones((5, 5), np.uint8)

        image = cv2.erode(self.current_image, kernel, iterations=1)

        self.update_image(image, "Minimum Filter")

    def mode_filter(self):

        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)

        padded = np.pad(gray, 2, mode='constant', constant_values=0)

        output = np.zeros_like(gray)

        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                window = padded[i:i + 5, j:j + 5].flatten()

                values, counts = np.unique(window, return_counts=True)

                output[i, j] = values[np.argmax(counts)]

        self.update_image(output, "Mode Filter")




root = tk.Tk()

app = ImageProcessingApp(root)

root.mainloop()