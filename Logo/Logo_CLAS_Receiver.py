from PIL import Image, ImageOps, ImageFont, ImageDraw
import os

name = "CLAS Receiver"
detail = "Designed by"
detail2 = "takuhoTech"


def scale_to_height(img, height):
    width = round(img.width * height / img.height)
    return img.resize((width, height)), width


def paste(img, x, y, height, list):
    w = [x]
    for im in list:
        im, width = scale_to_height(im, height)
        img.paste(im, (w[-1], y))
        w.append(w[-1] + width+10)


def alpha_binarization(img):
    width = img.size[0]
    height = img.size[1]
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if (pixel[3] < 255):
                img.putpixel((x, y), (0, 0, 0, 0))


dir = os.path.dirname(__file__) + '/'

# img_main
img_main = Image.open(dir + "QZSS.jpg")
img_main = ImageOps.invert(img_main)
img_main = img_main.point(lambda x: 0 if x < 150 else x)
img_main, _ = scale_to_height(img_main, 150)

# kicad
kicad = Image.open(dir + "kicad.png")

# canfd
canfd = Image.open(dir + "canfd.jpg")
canfd = ImageOps.invert(canfd)

# rmf-nhk
rmf = Image.open(dir + "rmf-nhk.png")

# ublox
ublox = Image.open(dir + "ublox.png")

img = Image.new("1", (570, 160))
img.paste(img_main, (0, 0))
paste(img, 370, 68, 90, [ublox])
draw = ImageDraw.Draw(img)
font1 = ImageFont.truetype(dir + "impact.ttf",  72)#75
font2 = ImageFont.truetype(dir + "impact.ttf",  40)
draw.text((152, -5), name, fill="white", font=font1)
draw.text((156, 69), detail, fill="white", font=font2)
draw.text((166, 106), detail2, fill="white", font=font2)

#img.show()
img.save(dir + "Logo_CLAS_Receiver.jpg")
