#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import numpy as np
from PIL import Image


def main():
    img_file = sys.argv[1]
    img = Image.open(img_file)
    w, h = img.size
    # 是否已经裁剪
    if float(h)/w > 1.3:
        img_ = Image.new("RGB", (330, 330))
        for y in range(610, 940):
            for x in range(195, 525):
                    img_.putpixel((x-195, y-610), img.getpixel((x, y)))
        img = img_

    w, h = img.size
    img_ = Image.new("RGB", (w, h))

    grid= []
    for y in range(h):
        line = []
        for x in range(w):
            # gray value
            pix = img.getpixel((x, y))
            pix = (pix[0]*299+pix[1]*587+pix[2]*114)/1000
            line.append(pix)

        lmean = np.mean(line)
        lvar =np.var(line)
        if 40 < lmean and lmean < 70 and lvar < 500:
            grid.append(1)
        else:
            grid.append(0)
            copy_row(img, img_, y)

    ggrid, gain, flag = [], 0, grid[0]
    for i in grid:
        if i != flag:
            ggrid.append((flag, gain))
            gain, flag = 0, i
        gain += 1

    print ggrid
    x = 0

    # 图片顶部位置是否有效
    if len(ggrid)>0 and ggrid[0][0] == 1:
        _, x = ggrid.pop(0)
        print "pop first black line:", x

    for i in range(len(ggrid)):
        h = ggrid[i][1]
        if ggrid[i][0] == 1:
            fix_row(img, img_, x-1, x-h-1)
            for j in range(x, x+h-1):
                fix_row(img, img_, j, j-h-1)
            fix_row(img, img_, x+h-1, x+h+2)
            fix_row(img, img_, x+h, x+h+2)

        x += h

    img_.save("out_" + img_file)


def copy_row(img, img_, y):
    print "copy line:", y
    w, _ = img.size
    for x in range(w):
        point = (x, y)
        img_.putpixel(point, img.getpixel(point))
        #img_.putpixel(point, (255, 255, 255))


def fix_row(img, img_, drt, src):
    print "fix line: %s with %s" % (drt, src)
    w, _ = img.size
    for x in range(w):
        try:
            img_.putpixel((x, drt), img.getpixel((x, src)))
            #img_.putpixel((x, drt), (255, 255, 255))
        except:
            pass


if __name__ == "__main__":
    main()
