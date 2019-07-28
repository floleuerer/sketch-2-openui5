import os
import cv2
import random
import numpy as np

blank = True
folder_org = 'elements/org/'
folder_drw = 'elements/drw/'
elements_org_files = os.listdir(folder_org)


for element_file in elements_org_files:
    if element_file.split('.')[1] == 'png':
        img = cv2.imread(folder_org + element_file)
        img = np.zeros(img.shape, np.uint8)

        if blank:
            img[::] = (255,255,255)
        else:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            img[::] = (r,g,b)

        element_drw_path = folder_drw + element_file
        if not (os.path.exists(element_drw_path) and os.path.isfile(element_drw_path)):
            print('writing file ' + element_drw_path)
            cv2.imwrite(element_drw_path ,img)
        else: 
            print('file exists ' + element_drw_path)


