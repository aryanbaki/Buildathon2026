"""
Charan — ocr_processor.py
Wraps pytesseract for image-based document OCR.
"""
def ocr_image(image_path: str) -> str:
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        # Upscale small images for better OCR accuracy
        if img.width < 1000:
            scale = 1000 / img.width
            img = img.resize((int(img.width * scale), int(img.height * scale)))
        text = pytesseract.image_to_string(img, config="--psm 6")
        return text.strip()
    except ImportError:
        raise RuntimeError("pytesseract or Pillow not installed.")
    except Exception as e:
        return f"[OCR failed: {e}]"
