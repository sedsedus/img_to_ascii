#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import pprint
import string 
to_check = string.punctuation

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
set_vals = set()
def test(v):
    if(v[1] in set_vals):
        return False
    else:
        set_vals.add(v[1])
        return True
    
res = filter(test, res)
sorted_v = sorted(res, key=lambda x: x[1])
print("The sorted intensity scaling is:")
pprint.pprint(sorted_v)

definition = ','.join([f'"{ch}"' for ch, v in sorted_v])
print(f"intensity_map=[{definition}]")