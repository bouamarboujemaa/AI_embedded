 """
 * @file        LABELME2YOLO.py
 * @version     1.0
 * @author      BOUAMOR BOUJEMAA
 * @date        2022.05.22
 """


import cv2
import base64
import json
import argparse
import numpy as np
import glob
import os

def conv_annotation(json_fn):
    """
    This function  for calculate yolo annotations from labelme annotation
    :param json_fn:str
        data store in json file
    :return:
    img: matrix
        image
    str_lines:  array
        array  contains yolo coordinates with their class
    """
    # read file
    with open(json_fn, 'r') as myfile:
        data = myfile.read()
    # parse file
    obj = json.loads(data)
    # image string to mat
    jpg_original = base64.b64decode(obj['imageData'])
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    # return img
    H, W, _ = img.shape
    str_lines = []
    for idx, item in enumerate(obj['shapes']):
        class_number = item['label']
        x1, y1 = item['points'][0]
        x2, y2 = item['points'][1]
        # mestart calcul
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        rw = (x2 - x1)
        rh = (y2 - y1)
        ncx = cx / W
        ncy = cy / H
        nrw = rw / W
        nrh = rh / H
        str_lines.append("{} {} {} {} {}".format(class_number, ncx, ncy, nrw, nrh))

    return img, str_lines


def writeYolocsv(fn_only, str_lines, args):
    """
    this function for save the yolo coordinates in csv file
    :param fn_only: str
        name of file
    :param str_lines: array
        array  contains yolo coordinates with their class
    :param args: path
        the path to save the file
    """

    file = open('{}{}.csv'.format(args.yolo_labels+ '/', fn_only), 'w')

    for v in str_lines:
        file.write(v)
        file.write('\n')
    file.close()


def labelme2yolo_main(args):
    """
     this function its main unction for convert annotation labelme to yolo
    :param args:  str
        -path to source file to convert(labelme_path)
        -path to destination  after convertion (yolo_labels)
    """
    # get all label txt
    #labels_list = glob.glob(args.labelme_path +"/"+ '*.json')
    output_path_creation(args)
    input_path = os.path.abspath(args.labelme_path)
    print(input_path)
    if not os.path.exists(input_path):
        raise "The input path does not exist"

    labels_list = find_csv_filenames(args.labelme_path)
    print("Wait a moment please...")

    #for idx, v in enumerate(labels_list):
    for v in labels_list:
        # get yolo txt strings, image
        img, str_lines = conv_annotation(v)
        path = os.path.abspath(v)
        #fn_only = v.split('/')[-1][9:-5]
        fn_only = path.split('\\')[-1][:-5]
        # save image
        cv2.imwrite('{}{}.png'.format(args.yolo_labels + '/', fn_only), img)
        # save txt
        writeYolocsv(fn_only, str_lines, args)

def find_csv_filenames(path_to_dir, suffix=".json"):
    """

    :param path_to_dir: str
     path to source file to convert(labelme_path)
    :param suffix: str
      file extensions
    :return: str
     file name

    """
    filenames = os.listdir(path_to_dir)
    return [os.path.join(path_to_dir, filename) for filename in filenames if filename.endswith(suffix)]


def output_path_creation(args):
    path = args.labelme_path
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    """
    main function
    """
    paser = argparse.ArgumentParser()
    paser.add_argument('-LP', '--labelme_path', type=str, default="data_out", help="Path to source folder")
    paser.add_argument('-YL', '--yolo_labels', type=str, default="data_yolo_out", help="path to destination image path")
    args = paser.parse_args()
    labelme2yolo_main(args)
    ##### set params #####
    # input : labelme  path
    # args.labelme_path = './data_out/'
    # output : yolo image, label path
    # args.yolo_labels = './data_yolo_out/'




