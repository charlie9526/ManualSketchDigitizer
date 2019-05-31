from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import cv2
from shape_recreator import shape_recreator
from sd1 import detct_shapes
from text_box import text_out
from reportlab.lib.units import inch
inch = int(inch)

def cordiante_to_point(cordinate, height):
    pix_x = cordinate[0]

    x = pix_x * 0.75
    pix_y = cordinate[1]
    y = (height - pix_y) * 0.75
    point_cordinate = [x, y]
    return point_cordinate


def generate_pdf(height_pixel, width_pixel, text_list, shape_list,path):

    height = height_pixel * 0.75
    width = width_pixel * 0.75

    myCanvas = canvas.Canvas(path, pagesize=(width, height))

    for inst_shape in shape_list:
        location_pixel = inst_shape[0]

        if (inst_shape[-1]=="c"):
            center_pixel_x = inst_shape[1][0] + location_pixel[0][0]
            center_pixel_y = inst_shape[1][1] + location_pixel[0][1]
            center_pixel = [center_pixel_x,center_pixel_y]
            center = cordiante_to_point(center_pixel,height_pixel)
            radius = inst_shape[2]*0.75
            myCanvas.circle(center[0] ,center[1], radius, stroke=1, fill=0)


        else:
            pairs_pixel = inst_shape[1]

            point_pairs = []

            for cordinate_pixel in pairs_pixel:

                old_pixel_x1 = cordinate_pixel[0][0]
                old_pixel_y1 = cordinate_pixel[0][1]

                old_pixel_x2 = cordinate_pixel[1][0]
                old_pixel_y2 = cordinate_pixel[1][1]

                new_pixel_x1 = old_pixel_x1 + location_pixel[0][0]
                new_pixel_y1 = old_pixel_y1 + location_pixel[0][1]

                new_pixel_x2 = old_pixel_x2 + location_pixel[0][0]
                new_pixel_y2 = old_pixel_y2 + location_pixel[0][1]

                new_cordinates1 = [new_pixel_x1, new_pixel_y1]
                new_cordinates2 = [new_pixel_x2, new_pixel_y2]

                point_pairs.append([cordiante_to_point(
                    new_cordinates1, height_pixel), cordiante_to_point(new_cordinates2, height_pixel)])

            for pair in point_pairs:
                myCanvas.line(pair[0][0], pair[0][1], pair[1][0], pair[1][1])

    for inst_text in text_list:
        location_pixel = inst_text[0][0]
        text_location = cordiante_to_point(location_pixel, height_pixel)
        myCanvas.drawString(text_location[0], text_location[1], inst_text[1])

    myCanvas.showPage()
    
    #memory_array = [text_list,shape_list]
    #string_M_array = " ".join(map(str,memory_array))
    #myCanvas.drawString(width,height, string_M_array )
    #myCanvas.showPage()

    
    myCanvas.save()
