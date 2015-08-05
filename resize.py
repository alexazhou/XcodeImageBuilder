#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-08-04 22:06:17
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : 
# @Disc    : 

from PIL import Image
import sys
import os.path


def resize_img(name, output_name):

    print("resize: %s"%name)

    output_name_tail = output_name[ output_name.rfind(".") : ]
    img_3x_name = output_name.replace(output_name_tail,"@3x" + output_name_tail)
    img_2x_name = output_name.replace(output_name_tail,"@2x" + output_name_tail)
    img_1x_name = output_name

    if os.path.exists( img_3x_name ) and os.path.exists( img_2x_name ) and os.path.exists( img_1x_name ):
        print("resized image already existed")
        return

    img_6x = Image.open( name )

    img_3x = img_6x.resize(( int(img_6x.size[0]/2),int(img_6x.size[1]/2) ), Image.BICUBIC)
    img_2x = img_6x.resize(( int(img_6x.size[0]/3),int(img_6x.size[1]/3) ), Image.BICUBIC)
    img_1x = img_6x.resize(( int(img_6x.size[0]/6),int(img_6x.size[1]/6) ), Image.BICUBIC)

    img_3x.save( img_3x_name )
    img_2x.save( img_2x_name )
    img_1x.save( img_1x_name )


def show_help():
    help_doc = '''commands:
    resize xxx@6x.png, output: xxx@3x.png xxx@2x.png xxx.png
    '''
    print(help_doc)



def main():
    
    if len(sys.argv) == 1:
        show_help()
        return

    cmd = sys.argv[1]

    if cmd != "resize":
        show_help()

    items = sys.argv[2:]
    for name in items:
        resize_img( name, name.replace("@6x",""))



if __name__ == '__main__':
    main()
else:
    print ('resize.py had been imported as a module')



