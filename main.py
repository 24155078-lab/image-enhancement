"""Image enhancement using histogram equalization and contrast adjustment."""
import argparse
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np


def read_image(path):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def histogram_equalization(image):
    """Equalize luminance for color images to better preserve color."""
    if image.ndim == 2:
        return cv2.equalizeHist(image)
    ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)


def contrast_adjustment(image, alpha=1.5, beta=20):
    """Apply output = alpha * input + beta, clipping values to [0, 255]."""
    result = alpha * image.astype(np.float32) + beta
    return np.clip(result, 0, 255).astype(np.uint8)


def save_image(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(path), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if not ok:
        raise OSError(f"Could not save {path}")


def save_comparison(original, equalized, contrast, path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, title, img in zip(
        axes,
        ["Original Image", "Histogram Equalization", "Contrast Adjustment"],
        [original, equalized, contrast],
    ):
        ax.imshow(img)
        ax.set_title(title)
        ax.axis("off")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def save_histograms(original, equalized, contrast, path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, title, img in zip(
        axes,
        ["Original Image", "Histogram Equalization", "Contrast Adjustment"],
        [original, equalized, contrast],
    ):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ax.hist(gray.ravel(), bins=256, range=(0, 256), color="gray")
        ax.set(title=title, xlabel="Pixel intensity", ylabel="Pixel count")
        ax.set_xlim(0, 255)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description="Enhance an image using histogram equalization and contrast adjustment."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input image path")
    parser.add_argument("--alpha", type=float, default=1.5, help="Contrast multiplier")
    parser.add_argument("--beta", type=int, default=20, help="Brightness offset")
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()

    if args.alpha < 0:
        parser.error("--alpha must be zero or greater")

    original = read_image(args.input)
    equalized = histogram_equalization(original)
    contrast = contrast_adjustment(original, args.alpha, args.beta)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    save_image(args.output_dir / "original.png", original)
    save_image(args.output_dir / "histogram_equalized.png", equalized)
    save_image(args.output_dir / "contrast_adjusted.png", contrast)
    save_comparison(original, equalized, contrast, args.output_dir / "comparison.png")
    save_histograms(original, equalized, contrast, args.output_dir / "histograms.png")

    print("Image enhancement completed successfully.")
    print(f"Results saved in: {args.output_dir.resolve()}")
    for name in [
        "original.png", "histogram_equalized.png", "contrast_adjusted.png",
        "comparison.png", "histograms.png",
    ]:
        print(f"- {name}")


if __name__ == "__main__":
    main()
