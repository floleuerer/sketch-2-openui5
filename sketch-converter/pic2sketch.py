import os
import cv2
import random
import numpy as np
from matplotlib import pyplot as plt

screenshot_dir = '_screenshots/'
sketches_dir = '_sketches/'
elements_org_dir = '_elements/org/'
elements_drw_dir = '_elements/drw/'

def get_filelist(folder):
    filelist = os.listdir(folder)
    filelist.sort()
    return filelist

def load_images(folder):
    filelist = get_filelist(folder)
    images = []
    for f in filelist:
        if f.split('.')[1].lower() == 'png':
            img = cv2.imread(folder + f)
            images.append(img)
    return images

def load_image(image):
    img = cv2.imread(image)
    return img

def conv_gray(images):
    images_gray = []
    for img in images:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        images_gray.append(img_gray)
    return images_gray

screenshots_files = get_filelist(screenshot_dir)
screenshots = conv_gray(load_images(screenshot_dir))
elements_org = conv_gray(load_images(elements_org_dir))
#elements_drw = load_images(elements_drw_dir)

elements_list = get_filelist(elements_org_dir)
elements_drw_list = get_filelist(elements_drw_dir)
elements_drw = {}
for element in elements_list:
    element_name = element.split('.')[0]
    elements_drw[element_name] = []
    for element_drw in elements_drw_list:
        if element_drw.split('_')[0] == element_name:
            elements_drw[element_name].append(load_image(elements_drw_dir + element_drw))
    



for i, s in enumerate(screenshots):
    print(s.shape)
    s_h, s_w= s.shape

    # create sketch
    blank_image = np.zeros((s_h,s_w,3), np.uint8)
    blank_image[::] = (255,255,255)

    for j, e in enumerate(elements_org):
        # find element
        element_name = elements_list[j].split('.')[0]
        res = cv2.matchTemplate(s,e,cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)

        # insert sketch at element location
        for pt in zip(*loc[::-1]):
            rand_element = random.randint(0,len(elements_drw[element_name])-1)
            print(element_name + ' ' + str(rand_element))
            blank_image[pt[1]:pt[1]+e.shape[0], pt[0]:pt[0]+e.shape[1]] = elements_drw[element_name][rand_element]

        cv2.imwrite(sketches_dir + screenshots_files[i], blank_image)



        

