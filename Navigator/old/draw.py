from PIL import Image, ImageDraw


def redraw_picture(pic_path,point_mas):

    stop=len(point_mas)
    stop=stop-1
    lines = []
    for i in range(0,stop):
        line=[]
        line.append(point_mas[i].x)
        line.append(point_mas[i].y)
        line.append(point_mas[i+1].x)
        line.append(point_mas[i + 1].y)
        lines.append(line)


    im = Image.open(pic_path)
    #im.show()
    draw = ImageDraw.Draw(im)

    #draw.line((0, 0) + im.size, fill=128)
    for line in lines:
        draw.line((line[0], line[1], line[2], line[3]), fill=(255,0,0,255),width=10)

    #draw.line((0, im.size[1], im.size[0], 0), fill=128)
    #del draw
    im.save(pic_path)


#redraw_picture('',[])