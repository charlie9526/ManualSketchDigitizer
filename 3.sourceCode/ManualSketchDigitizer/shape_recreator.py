import cv2
import numpy as np
from sd1 import detct_shapes

# this function is for the convertion of lines to gradient and intercept format


def m_and_c(cordinates):
    m_c = []
    x1 = cordinates[0][0]
    x2 = cordinates[1][0]
    y1 = cordinates[0][1]
    y2 = cordinates[1][1]

    if (x1 == x2):
        m_c.append(x1)
    else:
        m = ((y2-y1)*1.0)/(x2-x1)
        m_c.append(m)
        c = y1 - ((m*1.0)*x1)
        m_c.append(c)
    return m_c

# this function can find interscetion points of two lines

def intersection(lines):
    final_list = []
    for line1 in lines:
        for line2 in lines:
            inters = []
            if ((line1 == line2) or (len(line1) == 1 and len(line2) == 1)):
                continue
            elif(((line1[0]-line2[0]) <= 0.1 and (line1[0]-line2[0]) >= 0) or ((line1[0]-line2[0]) >= -0.1 and (line1[0]-line2[0]) <= 0)):
                continue
            elif(len(line1) == 1):
                x = line1[0]
                inters.append(x)
                y = (line1[0]*line2[0])+line2[1]
                inters.append(y)

                if (inters not in final_list):
                    final_list.append(inters)
            elif(len(line2) == 1):
                x = line2[0]
                inters.append(x)
                y = (line2[0]*line1[0])+line1[1]
                inters.append(y)

                if (inters not in final_list):
                    final_list.append(inters)
            else:
                x = -(line2[1]-line1[1])/(line2[0]-line1[0])
                inters.append(x)
                y = ((line2[0]*line1[1])-(line1[0]*line2[1])) / \
                    (line2[0]-line1[0])
                inters.append(y)

                if (inters not in final_list):
                    final_list.append(inters)
    return final_list

# here pair of points according to edges are chosen from suitable intersection points


def choice_points(lines, points):
    pairs = []
    instance_lines = lines
    for x in points:
        for y in points:
            if (x == y):
                continue
            else:
                if (x[0] == y[0]):
                    for l in instance_lines:
                        if (len(l) == 1):
                            if ((x[0]-l[0])**2 < 1):
                                # instance_lines.remove(l)
                                pairs.append([x, y])
                else:
                    m1 = ((y[1]-x[1])*1.0)/(y[0]-x[0])
                    c1 = y[1] - ((m1*1.0)*y[0])
                    for l in instance_lines:
                        if (len(l) == 1):
                            continue
                        else:

                            if(((m1-l[0])**2 < 1) and ((c1-l[1])**2 < 1)):
                                # instance_lines.remove(l)
                                pairs.append([x, y])
    return pairs


def shape_recreator(shape_list):
    ii = 0
    final_detail = []

    for img in shape_list:
        location = img[0]
        img = img[1]

        #img = cv2.imread(image)
        # convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #ii = ii+1
        # Apply edge detection method on the image
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # This returns an array of r and theta values
        lines = cv2.HoughLines(edges, 1, np.pi/180,100)  
        #print (lines)
        if lines is None:
            circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)          
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                sub_detail = []
                centere = [i[0],i[1]]
                radius = i[2]
                sub_detail = [location,centere,radius,"c"]
                final_detail.append(sub_detail)
                break

        # height and width of the image
        height, width, channels = img.shape

        # according to the shape this array should be changed. But considering the restrictions of this algorithm, we choose 10 for all
        strong_lines = np.zeros([10, 1, 2])

        final_lines_row_theta = []
        n2 = 0

        if lines is not None:
            sub_detail = []
            # here main lines are selected
            for n1 in range(0, len(lines)):
                for rho, theta in lines[n1]:
                    if n1 == 0:
                        strong_lines[n2] = lines[n1]
                        n2 = n2 + 1
                    else:
                        #if rho < 0:
                        #    rho *= -1
                        #   theta -= np.pi
                        closeness_rho = np.isclose(
                            rho, strong_lines[0:n2, 0, 0], atol=10)
                        closeness_theta = np.isclose(
                            theta, strong_lines[0:n2, 0, 1], atol=np.pi/36)
                        closeness = np.all(
                            [closeness_rho, closeness_theta], axis=0)
                        # here also the number with n2 should be changed accoding to the shape.
                        if not any(closeness) and n2 < 10:
                            strong_lines[n2] = lines[n1]
                            n2 = n2 + 1

            # here row theta values of strong lines are put in to a list
            for x in strong_lines:
                final_lines_row_theta.append(x[0])
            nulity = 0
            for y in final_lines_row_theta:
                if (y[0]==0 and y[1]==0):
                    break
                else:
                    nulity = nulity + 1
            final_lines_row_theta = final_lines_row_theta[:nulity]
      
            
            # xylines list consits of lists of line representation with two x,y cordinates from each line
            xylines = []
            for x in final_lines_row_theta:
                cordinate1 = []
                cordinate2 = []
                r = x[0]
                theta = x[1]

                # Stores the value of cos(theta) in a
                a = np.cos(theta)

                # Stores the value of sin(theta) in b
                b = np.sin(theta)

                # x0 stores the value rcos(theta)
                x0 = a*r

                # y0 stores the value rsin(theta)
                y0 = b*r

                # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
                x1 = int(x0 + 1000*(-b))

                # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
                y1 = int(y0 + 1000*(a))

                cordinate1.append(x1)
                cordinate1.append(y1)

                # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
                x2 = int(x0 - 1000*(-b))

                # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
                y2 = int(y0 - 1000*(a))

                cordinate2.append(x2)
                cordinate2.append(y2)


                xylines.append([cordinate1, cordinate2])

            lines_with_mc = []
            # lines with m_c consists line representaiion with m and c values(y = mx+c)
            for x in xylines:
                lines_with_mc.append(m_and_c(x))

            intersect = intersection(lines_with_mc)
            new_int = []
            # here unwanted interssections are removed
            for x in intersect:
                if (x[0] < 0 or x[1] < 0 or x[0] > width or x[1] > height):
                    continue
                else:
                    new_int.append(x)

            pairs = choice_points(lines_with_mc, new_int)

            sub_detail.append(location)

            final_pairs = []
            for c in pairs:
                invertion = []
                invertion.append(c[1])
                invertion.append(c[0])
                if (invertion in final_pairs):
                    continue
                else:
                    final_pairs.append(c)

            sub_detail.append(final_pairs)

            final_detail.append(sub_detail)
            #print pairs
            
            ii = ii + 1

    print (final_detail)
    return final_detail


