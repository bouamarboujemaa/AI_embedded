 """
 * @file        PASCAL_VOC2LABELME.py
 * @version     1.0
 * @author      BOUAMOR BOUJEMAA
 * @date        2022.05.22
 """

import glob
import os
import cv2
import base64
import json
import argparse


def getImgbyTxtFN(txtFN, imagePath):
    """
    this function to find the image path and get the image associated with the file
     which contains the pascal voc annotation
    :param txtFN:
        name of image
    :param imagePath:
        path of image and  source file to convert(pascal_voc_path)
    :return:
    img : matrix
        image
    img_full_fn : str
        name of image
    fn_only : str
       reference of image
    """
    path = os.path.abspath(txtFN)

    fn = path.split('\\')[-1]

    fn = name_finish_by_copy(fn)

    fn_only = fn.replace(".csv", "")
    # get absolut path
    img_full_fn = os.path.join(imagePath, fn_only + '.png')
    # read image
    img = cv2.imread(img_full_fn)

    return img, img_full_fn, fn_only


def name_finish_by_copy(fn):
    if fn[-11:] == " - Copy.csv":
        fn = fn.replace(" - Copy.csv", ".csv")
    elif fn[-15:] == " - Copy (2).csv":
        fn = fn.replace(" - Copy (2).csv", ".csv")
    return fn


def make_labelme_json(txt_full_fn, args):
    """

    :param txt_full_fn: str
        name of file to convert
    :param args: str
        -path to source file to convert(pascal_voc_path)
    :return:
    wdict : str
        json file content
    fn_only: str
        reference of image and file
    img : matrix
        image
    """
    file = open(txt_full_fn, 'r')
    img, img_full_fn, fn_only = getImgbyTxtFN(txt_full_fn, args.pascal_voc_path)

    if isinstance(img, type(None)):
        print("Error Name : This file can't be transformed - " + str(fn_only))
        return None, None, None

    else:
        h, w, _ = img.shape
        shape_dict = []
        lines = file.readlines()

        for v in lines:
            item = v.split(',')  # split
            X1, Y1, X2, Y2 = item[0], item[1], item[2], item[3]
            x1 = (float(X1))
            y1 = (float(Y1))
            x2 = (float(X2))
            y2 = (float(Y2))

            adict = {"label": "0", "points": [[x1, y1], [x2, y2]], "group_id": None, "shape_type": "rectangle",
                     "flags": {}}
            shape_dict.append(adict)

        image_string = cv2.imencode('.png', img)[1]
        image_string = base64.b64encode(image_string).decode()
        # make string image dict
        wdict = {"version": "4.5.6", "flags": {}, "shapes": shape_dict, "imagePath": img_full_fn,
                 "imageData": image_string}

        return wdict, fn_only, img


def pascal_voc2labelme(args):
    """
    This function  for convert  annotation pascal_voc to  lableme
    :param args: str
        -path to source file to convert(pascal_voc_path)
        -path to destination (labelme_path)
    """
    output_path_creation(args)

    input_path = os.path.abspath(args.pascal_voc_path)
    if not os.path.exists(input_path):
        raise "The input path does not exist"

    label_list = find_csv_filenames(args.pascal_voc_path)
    print("Wait a moment please...")

    for v in label_list:
        # call function fot make labelme json
        wdict, fn_only, img = make_labelme_json(v, args)

        if not isinstance(img, type(None)):
            # save json
            str_type = json.dumps(wdict)  # dic to json
            prefix_fn = "{}{}".format(args.labelme_path + '/', fn_only)
            f = open("{}.json".format(prefix_fn), "w+")
            f.write(str_type)
            f.close()
            # save image
            cv2.imwrite("{}.png".format(prefix_fn), img)


def find_csv_filenames(path_to_dir, suffix=".csv"):
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-LP', '--pascal_voc_path', type=str, default="data_in", help="Path to source folder")
    parser.add_argument('-YL', '--labelme_path', type=str, default="data_out", help="path to destination image path")
    args = parser.parse_args()
    pascal_voc2labelme(args)
