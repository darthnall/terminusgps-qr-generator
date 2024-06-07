from PIL import Image, ImageDraw, ImageFont
from qrcode import QRCode, constants


class QrGenerator:
    def create_qr(self, imei: str) -> QRCode:
        qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("https://register.terminusgps.com?imei={imei}")
        qr.make(fit=True)
        return qr

    def save_qr(self, qr: QRCode, *, name: str, text: str) -> None:
        def _draw_text(img: Image, text: str) -> Image:
            img = img.convert("RGB")
            overlay = ImageDraw.Draw(img)

            font = ImageFont.truetype("/usr/share/fonts/TFF/OpenSans-Regular.ttf", 28)
            padding = 10

            text_bbox = overlay.textbbox((0, 0), text, font=font)
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]

            img_w, img_h = img.size
            x_pos = (img_w - text_w) / 2
            y_pos = img_h - text_h - padding - 10

            overlay.text((x_pos, y_pos), text, font=font, fill="black")

            return img

        img = qr.make_image(fill_color="black", back_color="white")
        img = _draw_text(img, text)
        img.save(f"media/{name}.png")


if __name__ == "__main__":
    generator = QrGenerator()
    imei = "12345567891234"
    qr = generator.create_qr(imei=imei)
    generator.save_qr(qr, name=imei, text=f"IMEI #: {imei}")
