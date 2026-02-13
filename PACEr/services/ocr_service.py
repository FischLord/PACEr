"""
OCR-Service zur Erkennung von Strecke, Geschwindigkeit und Art aus Fotos.
Primär: Claude Vision API, Fallback: Tesseract OCR.
"""
import os
import re
import base64


class OcrResult:
    def __init__(self, laenge=None, kmh=None, art=None,
                 bz_min=None, bz_sec=None, ez_min=None, ez_sec=None,
                 hz_min=None, hz_sec=None, confidence=0, raw_text=''):
        self.laenge = laenge
        self.kmh = kmh
        self.art = art
        self.bz_min = bz_min
        self.bz_sec = bz_sec
        self.ez_min = ez_min
        self.ez_sec = ez_sec
        self.hz_min = hz_min
        self.hz_sec = hz_sec
        self.confidence = confidence
        self.raw_text = raw_text

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class ClaudeVisionOcr:
    """Uses Claude API for image analysis."""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')

    def available(self):
        return bool(self.api_key)

    def analyze(self, image_data, mime_type='image/jpeg'):
        try:
            import anthropic
        except ImportError:
            return None

        if not self.api_key:
            return None

        client = anthropic.Anthropic(api_key=self.api_key)

        image_b64 = base64.b64encode(image_data).decode('utf-8')

        prompt = """Analysiere dieses Bild eines Fahrsport-Marathon-Formulars.
Extrahiere folgende Informationen falls vorhanden:
- Streckenlänge in Metern (laenge)
- Geschwindigkeit in km/h (kmh)
- Streckenart: "wegstrecke", "hindernisstrecke" oder "schrittstrecke" (art)
- Bestzeit in Minuten und Sekunden (bz_min, bz_sec)
- Erlaubte Zeit in Minuten und Sekunden (ez_min, ez_sec)
- Höchstzeit in Minuten und Sekunden (hz_min, hz_sec)

Antworte NUR im folgenden JSON-Format (ohne Markdown):
{"laenge": 4900, "kmh": 14, "art": "wegstrecke", "bz_min": 16, "bz_sec": 37, "ez_min": 19, "ez_sec": 37, "hz_min": 45, "hz_sec": 14, "confidence": 85}

Setze confidence auf 0-100 je nachdem wie sicher du dir bist.
Lasse Felder weg die du nicht erkennen kannst."""

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": mime_type, "data": image_b64}},
                    {"type": "text", "text": prompt},
                ],
            }],
        )

        import json
        text = message.content[0].text.strip()
        # Remove possible markdown code fences
        if text.startswith('```'):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)

        data = json.loads(text)
        return OcrResult(**data)


class TesseractOcr:
    """Fallback OCR using Tesseract."""

    def available(self):
        try:
            import pytesseract
            return True
        except ImportError:
            return False

    def analyze(self, image_data, mime_type='image/jpeg'):
        try:
            import pytesseract
            from PIL import Image
            import io

            image = Image.open(io.BytesIO(image_data))
            text = pytesseract.image_to_string(image, lang='deu')

            return self._parse_text(text)
        except Exception:
            return None

    def _parse_text(self, text):
        result = OcrResult(raw_text=text, confidence=30)

        # Try to extract distance
        m = re.search(r'(\d{3,6})\s*m', text)
        if m:
            result.laenge = int(m.group(1))
            result.confidence += 10

        # Try to extract speed
        m = re.search(r'(\d{1,2})\s*km/?h', text, re.IGNORECASE)
        if m:
            result.kmh = int(m.group(1))
            result.confidence += 10

        # Try to detect art
        text_lower = text.lower()
        if 'hindernis' in text_lower:
            result.art = 'hindernisstrecke'
            result.confidence += 10
        elif 'schritt' in text_lower:
            result.art = 'schrittstrecke'
            result.confidence += 10
        elif 'weg' in text_lower:
            result.art = 'wegstrecke'
            result.confidence += 10

        # Try to extract times (MM:SS pattern)
        times = re.findall(r'(\d{1,3}):(\d{2})', text)
        labels = ['bz', 'ez', 'hz']
        for i, (minutes, seconds) in enumerate(times[:3]):
            if i < len(labels):
                setattr(result, f'{labels[i]}_min', int(minutes))
                setattr(result, f'{labels[i]}_sec', int(seconds))
                result.confidence += 5

        result.confidence = min(result.confidence, 100)
        return result


def get_ocr_service():
    """Returns the best available OCR service."""
    claude = ClaudeVisionOcr()
    if claude.available():
        return claude

    tesseract = TesseractOcr()
    if tesseract.available():
        return tesseract

    return None
