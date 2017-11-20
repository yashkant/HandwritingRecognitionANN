#!/usr/bin/env python

import sys
import requests
import pytesseract
from PIL import Image
from StringIO import StringIO
import os


def get_image(url):
    return Image.open(StringIO(requests.get(url).content))


if __name__ == '__main__':
    """Tool to test the raw output of pytesseract with a given input URL"""
    # sys.stdout.write("A simple OCR utility<!!>")
    # url = "file:///media/manikantanallagatla/D666D33D66D31D55/ManikantaBackup3/study/semVIII/Others/androidApp/results2.png"
    # print "Here"
    # url ="https://realpython.com/images/blog_images/ocr/results2.png"
    url = sys.argv[1]
    # url = "http://localhost/htdocs/AndroidApp/123.png"
    # url ="file:/home/manikantanallagatla/Downloads/results2.png"
    # url = raw_input("What is the url of the image you would like to analyze?\n")
    # print "Here"
    image = get_image(url)
    # print image
    # sys.stdout.write("-----------------BEGIN-----------------<!!>")
    output = pytesseract.image_to_string(image)
    arr = str(output).split('\n')
    # print arr
    for ele in arr:
        if(ele != ''):
            sys.stdout.write(ele+'\n')
    # print '\n' in output
    # sys.stdout.write(str(output))
    # sys.stdout.write("------------------END------------------<!!>")