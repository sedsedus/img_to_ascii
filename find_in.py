#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import pprint 
to_check = [" ", ".",",","^", "*", "1", "%", "$","&","#","@"]

def get_total(char):
    im = Image.new("RGB", (20, 20))
    dr = ImageDraw.Draw(im)
    
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    dr.text((0,0), char)
    
    px = im.load()

    total = 0
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            total += sum(px[i, j])
    return total
vals = map(get_total, to_check)
res = zip(to_check, vals)
pprint.pprint(sorted(res, key=lambda x: x[1]))
