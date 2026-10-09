# 🖼️ Image Processor

A desktop GUI application for applying classical image processing techniques — built with Python, OpenCV, and Tkinter.

---

## ✨ Features

The app supports two categories of operations, applied side-by-side on the original image:

### 🔧 Enhancement Techniques
| Technique | Description |
|---|---|
| **Thresholding** | Otsu's method to binarize an image automatically |
| **Power Transform** | Gamma correction with a user-supplied power value (γ > 0) |
| **Bit Plane Slicing** | Decomposes the image into 8 bit-planes and displays them combined |

### ✂️ Segmentation Techniques
| Technique | Description |
|---|---|
| **Adaptive Thresholding** | Local mean-based thresholding for uneven illumination |
| **Log Transform** | Logarithmic intensity mapping to enhance low-intensity details |
| **Watershed Segmentation** | Morphology + distance transform based region segmentation |

### 🛠️ Utility Controls
- **Load Image** — open any common image format
- **Export** — save the processed result as PNG or JPEG
- **Reset** — clear the canvases and start fresh
- **Close** — exit the application

---

## 📸 Demo

> See `demo/Project_Demonstration.rar` for a recorded walkthrough of the application.

---

## 🗂️ Project Structure

```
Image_Processing/
├── main.py                          # Main application (GUI + all algorithms)
├── requirements.txt                 # Python dependencies
├── notebooks/
│   └── watershed_segmentation_algorithm.ipynb   # Algorithm deep-dive notebook
├── demo/
│   └── Project_Demonstration.rar    # Recorded demo video
└── archive/
    ├── legacy_single_canvas_app.py  # Earlier single-canvas version
    └── early_experiments/           # Historical experimental scripts
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/Image_Processing.git
   cd Image_Processing
   ```

2. **Create and activate a virtual environment** *(recommended)*
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Run the App

```bash
python main.py
```

---

## 🧪 How to Use

1. Click **Load Image** to open an image file.
2. Choose an **Enhancement** or **Segmentation** button from the toolbar.
   - For **Power Transform**, a dialog will prompt you to enter a gamma value (e.g. `0.5` to brighten, `2.0` to darken).
3. The processed image appears on the right canvas alongside the original.
4. Click **Export** to save the result, or **Reset** to start over.

---

## 🔬 Algorithms

| Algorithm | Key Implementation |
|---|---|
| Otsu Thresholding | `cv2.threshold(..., THRESH_OTSU)` |
| Power Transform | `np.power(img / 255, γ) * 255` |
| Bit Plane Slice | `cv2.bitwise_and(gray, 1 << i)` for i in 0–7 |
| Adaptive Thresholding | `cv2.adaptiveThreshold(..., ADAPTIVE_THRESH_MEAN_C)` |
| Log Transform | `np.log(gray + ε)` normalized to [0, 255] |
| Watershed | Morphological opening → distance transform → `cv2.watershed` |

For an in-depth explanation of the Watershed algorithm, see the notebook in [`notebooks/`](./notebooks/watershed_segmentation_algorithm.ipynb).

---

## 📦 Dependencies

| Library | Version | Purpose |
|---|---|---|
| `numpy` | 2.5.3 | Array operations & pixel math |
| `opencv-python` | 5.0.0.93 | Core image processing algorithms |
| `Pillow` | 12.3.0 | Image I/O & Tkinter integration |
| `tkinter` | stdlib | GUI framework |

---

## 📄 License

This project is open-source. Feel free to use and modify it for educational purposes.

---

## Author

Tasneem Ibrahim - Rana Hossam - Alaa Ibrahim - Ahmed Sweed
