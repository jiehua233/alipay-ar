#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PIL import Image


def main():
    img_file = "g.jpeg"
    img = Image.open(img_file)
    w, h = img.size
    img_ = Image.new("RGB", (w, h))
    print w, h

    grid= []
    threshold = w*0.6
    print threshold
    for y in range(h):
        black = 0
        tmp = []
        for x in range(w):
            pix = img.getpixel((x, y))[0]
            tmp.append(pix)
            if pix < 100:
                black += 1
        #print tmp
        print black, threshold
        if black < threshold:
            copy_row(img, img_, y)
            grid.append(0)
        else:
            grid.append(1)

    ggrid, gain, flag = [], 0, grid[0]
    for i in grid:
        if i != flag:
            ggrid.append((flag, gain))
            gain, flag = 0, i
        gain += 1

    print ggrid
    x = 0
    if len(ggrid)>0 and ggrid[0][0] == 1:
        _, x = ggrid.pop(0)
        print "pop first black line:", x

    for i in range(len(ggrid)):
        if ggrid[i][0] == 1:
            up = ggrid[i][1] / 2
            down = ggrid[i][1] - up
            for j in range(x-1, x+up):
                fix_row(img, img_, j-up-1, j)
            for j in range(x+up, x+ggrid[i][1]+1):
                fix_row(img, img_, j+down+1, j)

        x += ggrid[i][1]

    img_.save("out_" + img_file)


def copy_row(img, img_, y):
    print "copy line:", y
    w, _ = img.size
    for x in range(w):
        point = (x, y)
        img_.putpixel(point, img.getpixel(point))
        #img_.putpixel(point, (255, 255, 255))


def fix_row(img, img_, src, drt):
    print "fix line: %s with %s" % (drt, src)
    w, _ = img.size
    for x in range(w):
        try:
            img_.putpixel((x, drt), img.getpixel((x, src)))
            #img_.putpixel((x, drt), (255, 255, 255))
        except Exception as e:
            print e


if __name__ == "__main__":
    main()
