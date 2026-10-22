"""Make images/qr-home.svg, the QR code on the home page. Needs: pip install qrcode==7.4.2
Run from the repo root: python3 tools/make_qr.py"""
import re, qrcode, qrcode.image.svg
URL = 'https://cbct-2026.github.io/ABG/'
p = 'images/qr-home.svg'
qrcode.make(URL, image_factory=qrcode.image.svg.SvgPathImage, border=2).save(p)
s = re.sub(r'<svg width="[^"]*" height="[^"]*"', '<svg', open(p).read())
open(p, 'w').write(s.replace('<path ', '<rect width="100%" height="100%" fill="#fff"/><path ', 1))
