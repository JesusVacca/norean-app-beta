import base64
import qrcode
from io import BytesIO
from django.conf import settings


class QRCode:
    def _generate_qr_code(self, reverse):
        url = settings.SITE_URL + reverse
        qr = qrcode.make(url)
        buffer = BytesIO()
        qr.save(buffer, format='png')
        img_bytes = buffer.getvalue()
        base64_img = base64.b64encode(img_bytes).decode('utf-8')
        return f'data:image/png;base64,{base64_img}'

    @property
    def qr_code(self):
        pass