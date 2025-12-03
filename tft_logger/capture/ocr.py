from dataclasses import dataclass

import pytesseract
from PIL import Image, ImageFilter, ImageOps

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@dataclass
class OcrEngine:
    whitelist_digits: str = "0123456789"

    def _preprocess(self, image: Image.Image) -> Image.Image:
        scale = 4
        w, h = image.size
        img = image.resize((w * scale, h * scale), Image.BICUBIC)

        gray = img.convert("L")
        gray = ImageOps.autocontrast(gray)
        gray = gray.filter(ImageFilter.SHARPEN)

        return gray

    def read_number(self, image: Image.Image) -> int | None:
        processed = self._preprocess(image)

        custom_config = rf"--psm 7 -c tessedit_char_whitelist={self.whitelist_digits}"

        raw_text = pytesseract.image_to_string(processed, config=custom_config)

        digits_only = "".join(ch for ch in raw_text if ch.isdigit())

        if not digits_only:
            return None

        try:
            return int(digits_only)
        except ValueError:
            return None
