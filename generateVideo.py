#!/usr/bin/env python

import cv2
import numpy as np
import time
import argparse
import os
import json
import timeit



def generate_hsv_range_from_rgb_color(rgb_color):

    rgb = rgb_color

    rgb_color = np.uint8([[rgb]])
    hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)[0][0]

    H = hsv_color[0]
    S = hsv_color[1]
    V = hsv_color[2]

    print("teste: ", H, S, V)

    Hmax = H + 15
    Hmin = H - 15

    Smax = S + 210
    Smin = S - 210

    Vmax = V + 210
    Vmin = V - 210




    if (Hmax >= 179):
        Hmax = 179

    if (Hmax <= 0):
        Hmax = 0

    if (Hmin >= 179):
        Hmin = 179

    if (Hmin <= 0):
        Hmin = 0

    # S
    if (Smax >= 220):
        Smax = 220

    if (Smax <= 0):
        Smax = 0

    if (Smin >= 220):
        Smin = 220

    if (Smin <= 0):
        Smin = 0

    # V
    if (Vmax >= 255):
        Vmax = 255

    if (Vmax <= 0):
        Vmax = 0

    if (Vmin >= 255):
        Vmin = 255

    if (Vmin <= 0):
        Vmin = 0

    Smax = 255
    Smin = 0
    Vmax = 255
    Vmin = 70

    lower_hsv_bound = (int(Hmin),int(Smin),int(Vmin))
    upper_hsv_bound = (int(Hmax),int(Smax),int(Vmax))

    return lower_hsv_bound, upper_hsv_bound

# works but its really slow
def transparentOverlay2(src , overlay , pos=(0,0),scale = 1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay,(0,0),fx=scale,fy=scale)
    h,w,_ = overlay.shape  # Size of foreground
    rows,cols,_ = src.shape  # Size of background Image
    y,x = pos[0],pos[1]    # Position of foreground/overlay image
    
    #loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x+i >= rows or y+j >= cols:
                continue
            alpha = float(overlay[i][j][3]/255.0) # read the alpha channel 
            src[x+i][y+j] = alpha*overlay[i][j][:3]+(1-alpha)*src[x+i][y+j]
    return src

def transparentOverlay(background, overlay, x=0, y=0):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background


def rgbArrayToBgrArray(rgb_input):

    rgb_color = np.uint8([[rgb_input]])
    bgr_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2BGR)[0][0]

    return bgr_color

def writeLogoOnImage(imageLogo, image):

    logo = cv2.imread(imageLogo)

    img_height = int(logo.shape[0])
    img_width = int(logo.shape[1])

    y = 10
    x = 10

    image[ y:y+img_height , x:x+img_width ] = logo

    imageCopy = image.copy()

    return imageCopy

def generateVideo(image_green, background_video, logo_image_file, rbg_chroma_key_color, outputVideoWidth, outputVideoHeight, outputVideoFile, show_output_while_processing, show_smaller_output_while_processing):

    print("Generating output video: ", outputVideoFile)

    generate_hsv_range_from_rgb_color(rbg_chroma_key_color)

    cap = cv2.VideoCapture(background_video)

    # capBackground = cv2.VideoCapture(background_video)

    imageGreenCv = cv2.imread(image_green)

    #imageGreenCv = cv2.resize(imageGreenCv, (outputVideoWidth,outputVideoHeight))

    

    height, width, channels = imageGreenCv.shape

    # Create a black image
    removeSide = 0
    removeVertical = 0
    new_h = height
    new_w = width
    if (height < width):
        removeSide = 1
        new_h = height
        new_w = new_h
    elif (height > width):
        removeVertical = 1
        new_h = width
        new_w = new_h

    if (removeSide):
        side = int((width - new_w)/2)
        imageGreenCv = imageGreenCv[0:new_h,side:width-side]

    if (removeVertical):
        top = int((height - new_h)/2)
        imageGreenCv = imageGreenCv[top:height-top,0:new_w]


    imageGreenCv = cv2.resize(imageGreenCv, (outputVideoWidth,outputVideoHeight))

    imageTopLayer = cv2.imread(logo_image_file, cv2.IMREAD_UNCHANGED)


    #imageGreenCv = cv2.blur(imageGreenCv,(15,15))


    lower_hsv_bound, upper_hsv_bound = generate_hsv_range_from_rgb_color(rbg_chroma_key_color)

    # print(lower_hsv_bound)
    # print(upper_hsv_bound)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(imageGreenCv, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_hsv_bound , upper_hsv_bound)

    mask2 = cv2.bitwise_not(mask)

    
    kernel_erode = np.ones((3,3),np.uint8)  #bigger kernel to delete pixels on edge that was add after dilate function

    imgErode = cv2.erode(mask2, kernel_erode, 1)

    background_part = cv2.bitwise_and(imageGreenCv,imageGreenCv, mask=imgErode)


    maskTest = cv2.bitwise_not(imgErode)

    background_part2 = cv2.bitwise_and(imageGreenCv,imageGreenCv, mask=mask2)


    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # fourcc = cap.get(cv2.CAP_PROP_FOURCC)

    

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    outputVideoWriter = cv2.VideoWriter(outputVideoFile, fourcc, fps, (outputVideoWidth,outputVideoHeight))

    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
        exit()


    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, backgroundframe = cap.read()

        if ret == True:

            backgroundframe = cv2.resize(backgroundframe, (outputVideoWidth,outputVideoHeight))

            backgroundTest = cv2.bitwise_and(backgroundframe,backgroundframe, mask=maskTest)


            imageOut = backgroundTest + background_part


            imageOut = transparentOverlay(imageOut, imageTopLayer)


            outputVideoWriter.write(imageOut)

            # Press Q on keyboard to  exit
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        else:
            break

    outputVideoWriter.release()

if __name__ == "__main__":

    try:

        parser = argparse.ArgumentParser(description='Background replace program')
        parser.add_argument('-i','--input', help='Input Png File', required=True)
        # parser.add_argument('-o','--output', help='Output Video File', required=True)
        args = vars(parser.parse_args())

        inputFile = args['input']
        
        if (os.path.isfile(inputFile)):
            print("Input File: ", inputFile)
        else:
            print("Invalid input file", inputFile)
            exit()

        rbg_chroma_key_color = [94, 185, 129]

        background_video = "aux_files/backgroundvideo.mp4"
        top_layer = "aux_files/toplayer.png"


        filename = os.path.basename(inputFile)

        filenameNoExtension = os.path.splitext(os.path.basename(filename))[0]

        outputVideoFile  = "videoOut/" + filenameNoExtension + ".mp4"
        show_output_while_processing = False
        show_smaller_output_while_processing = False    

        generateVideo(inputFile, background_video, top_layer, rbg_chroma_key_color, int(1080), int(1080), outputVideoFile, show_output_while_processing, show_smaller_output_while_processing)

        print(outputVideoFile)

    except Exception as e:
        print("ERROR - Something went wrong", e)
    else:
        print("OK")
        

    
