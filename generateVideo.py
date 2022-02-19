#!/usr/bin/env python

import cv2
import numpy as np
import time
import argparse
import os
import json

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

def rgbArrayToBgrArray(rgb_input):

    rgb_color = np.uint8([[rgb_input]])
    bgr_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2BGR)[0][0]

    return bgr_color

def writeLogoOnImage(imageLogo, image):

    logo = cv2.imread(imageLogo)

    ## logo = cv2.resize(logo, (80,80)) 

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

    imageTopLayer = cv2.imread(logo_image_file)

    #imageGreenCv = cv2.blur(imageGreenCv,(15,15))


    lower_hsv_bound, upper_hsv_bound = generate_hsv_range_from_rgb_color(rbg_chroma_key_color)

    print(lower_hsv_bound)
    print(upper_hsv_bound)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(imageGreenCv, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_hsv_bound , upper_hsv_bound)

    mask2 = cv2.bitwise_not(mask)

    # #kernels for morphology operations
    #kernel_noise = np.ones((3,3),np.uint8) #to delete small noises
    #kernel_dilate = np.ones((30,30),np.uint8)  #bigger kernel to fill holes after ropes
    kernel_erode = np.ones((3,3),np.uint8)  #bigger kernel to delete pixels on edge that was add after dilate function

    #imgErode = cv.erode(frame_threshold, kernel_noise, 1)
    

    imgErode = cv2.erode(mask2, kernel_erode, 1)

    #imgDilate = cv2.dilate(imgErode , kernel_dilate, 1)
    

    # kernel = np.ones((7,7),np.uint8)
    # mask = cv2.dilate(mask,kernel,iterations = 1)

    background_part = cv2.bitwise_and(imageGreenCv,imageGreenCv, mask=imgErode)


    maskTest = cv2.bitwise_not(imgErode)

    #background_part = cv2.bitwise_and(imageGreenCv,imageGreenCv, mask=mask)

    background_part2 = cv2.bitwise_and(imageGreenCv,imageGreenCv, mask=mask2)

    # cv2.imshow('background_part',background_part)

    # cv2.imshow('background_part2',background_part2)

    


    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # fourcc = cap.get(cv2.CAP_PROP_FOURCC)

    

    fourcc = cv2.VideoWriter_fourcc(*'X264')

    outputVideoWriter = cv2.VideoWriter(outputVideoFile, fourcc, fps, (outputVideoWidth,outputVideoHeight))

    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
        exit()

    # if (capBackground.isOpened()== False): 
    #     print("Cap Background - Error opening video stream or file")
    #     exit()

    # Read until video is completed
    # count = 0

    #bottomRectText = generateRectWithText(rectangle_1_text, rectangle_2_text , rectangle_3_text, bottom_rect_rgb_color, moving_rectangles_rgb_color, text_box_rgb_color)

    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, backgroundframe = cap.read()

        if ret == True:

            backgroundframe = cv2.resize(backgroundframe, (outputVideoWidth,outputVideoHeight))

            width = int(backgroundframe.shape[1])
            height = int(backgroundframe.shape[0])
            dim = (width, height)
            # resize image


            backgroundTest = cv2.bitwise_and(backgroundframe,backgroundframe, mask=maskTest)


            imageTopLayerGrey = cv2.cvtColor(imageTopLayer, cv2.COLOR_BGR2GRAY)

            imageTopLayerBin = cv2.threshold(imageTopLayerGrey, 0, 255, cv2.THRESH_BINARY_INV)[1]



            imageOut = backgroundTest + background_part



            image1 = cv2.bitwise_and(imageOut,imageOut, mask=imageTopLayerBin)




            imageTopLayerBinInv = cv2.bitwise_not(imageTopLayerBin)


            image2 = cv2.bitwise_and(imageTopLayer,imageTopLayer, mask=imageTopLayerBinInv)


            imageOut = image1 + image2




            #imageOut = image1 + imageOut

            

#            cv2.imshow('imageGreenCv',imageGreenCv)

            # #mask2 = cv2.bitwise_not(mask)

            # #foreground_part = cv2.bitwise_and(frame,frame, mask=mask2)

            # background_plus_foreground = background_part + foreground_part

            # # background_plus_foreground = writeTopRec(background_plus_foreground, top_rect_rgb_color)

            # writeLogoOnImage(logo_image_file, background_plus_foreground)

            # # background_plus_foreground = writeBottomRec(background_plus_foreground, bottom_rect_rgb_color)

            #cv2.imshow('imageOut',imageOut)

            # cv2.imshow('imageTopLayer', imageTopLayerBin)

            # cv2.imshow('image1', image1)

            # cv2.imshow('image2', image2)

            # # get movedrect
            # bottomRectText = moveRect(bottomRectText, 20)

            # # write moved rect in bottom
            # # background_plus_foreground[880:outputVideoHeight, 16:outputVideoWidth-16] = bottomRectText[:, 0:outputVideoWidth-16-16]

            # testeRed = writeTitle(background_plus_foreground, title, title_rgb_color)

            outputVideoWriter.write(imageOut)

            # # Display the resulting frame

            # if (show_output_while_processing):
            #     cv2.imshow('background_plus_foreground',background_plus_foreground)

            # # Display the resulting frame resized for tests


            # if (show_smaller_output_while_processing):
            #     background_plus_foreground_smaller = cv2.resize(background_plus_foreground, (int(outputVideoWidth/4),int(outputVideoHeight/4)))
            #     cv2.imshow('background_plus_foreground_smaller',background_plus_foreground_smaller)

            # # count = count + 1

            # # if (count > 200):
            # #     break

            # Press Q on keyboard to  exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

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

        # if not outputVideoFile.endswith('.mp4'):
        #     print("Output file name: ", outputVideoFile)
        #     print("Invalid output format: needs to be .mp4")
        #     exit()

        # print("Output file name: ", outputVideoFile)

        rbg_chroma_key_color = [94, 185, 129]

        #background_video = "/home/luizmagnago/Luiz/Upwork/php/how-to-upload-a-file-in-php-with-example/Chroma/backgroundvideo.mp4"
        image_green = "/home/luizmagnago/Luiz/Upwork/php/how-to-upload-a-file-in-php-with-example/Chroma/greenscreenlayer.png"
        #top_layer = "/home/luizmagnago/Luiz/Upwork/php/how-to-upload-a-file-in-php-with-example/Chroma/toplayer.png"

        background_video = "aux_files/backgroundvideo.mp4"
        #image_green = "/home/luizmagnago/Luiz/Upwork/php/how-to-upload-a-file-in-php-with-example/Chroma/greenscreenlayer.png"
        top_layer = "aux_files/toplayer.png"


        filename = os.path.basename(inputFile)

        filenameNoExtension = os.path.splitext(os.path.basename(filename))[0]


        outputVideoFile  = "videoOut/" + filenameNoExtension + ".mp4"
        #print("outputVideoFile: ", outputVideoFile)
        show_output_while_processing = False
        show_smaller_output_while_processing = False    

        generateVideo(inputFile, background_video, top_layer, rbg_chroma_key_color, int(1080), int(1080), outputVideoFile, show_output_while_processing, show_smaller_output_while_processing)

        print(outputVideoFile)

    except Exception as e:
        print("ERROR - Something went wrong", e)
    else:
        print("OK")
        

    
