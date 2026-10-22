"""Trim the white margin around a rendered sheet picture, keeping a small border. Usage: python3 trim.py picture.png"""
import sys
from PIL import Image, ImageChops
im = Image.open(sys.argv[1]).convert('RGB')
box = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255))).point(lambda v: 255 if v > 20 else 0).getbbox()
if box:
    p = 30
    im.crop((max(0, box[0] - p), max(0, box[1] - p), min(im.width, box[2] + p), min(im.height, box[3] + p))).save(sys.argv[1])
