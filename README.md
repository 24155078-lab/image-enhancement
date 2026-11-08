# Image Enhancement Using Histogram Equalization and Contrast Adjustment

A Python image-processing project that improves image visibility using two classical techniques: **Histogram Equalization** and **Contrast Adjustment**. It also saves comparison images and grayscale intensity histograms.

## Features
- Supports common color image formats readable by OpenCV (JPG, PNG, BMP, TIFF).
- Performs histogram equalization on the luminance channel (Y) in YCrCb color space.
- Adjusts contrast and brightness using `output = alpha * input + beta`.
- Saves enhanced images, a side-by-side comparison, and histograms.

## Project structure

├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements
- Python 3.14 or newer
- pip

## Installation

```

Create and activate a virtual environment (recommended).

**Windows**
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install libraries:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```



Optional parameters:
```bash
python main.py --input images/input/sample.jpg --alpha 1.8 --beta 15
```
- `--alpha`: contrast multiplier; values above 1 generally increase contrast. Default: `1.5`.
- `--beta`: brightness offset; positive values brighten and negative values darken. Default: `20`.
- `--output-dir`: output folder. Default: `results`.

## Generated output
The `results/` folder will contain:

| File | Description |
|---|---|
| `original.png` | Copy of the input image |
| `histogram_equalized.png` | Result after histogram equalization |
| `contrast_adjusted.png` | Result after contrast/brightness adjustment |
| `comparison.png` | Three-image visual comparison |
| `histograms.png` | Grayscale intensity histograms |

The generated results are excluded from Git by `.gitignore`. If you want the GitHub page to display your own results, selectively add the output images after running the program.

## Algorithms

### Histogram Equalization
1. Convert the RGB image to YCrCb color space.
2. Extract the Y (luminance) channel.
3. Apply histogram equalization to the Y channel.
4. Convert the image back to RGB.

For a grayscale image, equalization is applied directly.

### Contrast Adjustment
Each pixel is transformed by:
```text
new_pixel = alpha * old_pixel + beta
```
The output is clipped to the valid 0–255 range.


## Limitations
- Global histogram equalization may amplify noise or over-enhance some regions.
- One contrast setting may not suit every image.
- This is a classical image-processing project, not a deep-learning model.
- Histograms are plotted using grayscale intensity, including for color images.

## Future improvements
- Add CLAHE for local contrast enhancement.
- Add batch processing and a graphical interface.
- Compare results using entropy, PSNR, or SSIM where a suitable reference image exists.

