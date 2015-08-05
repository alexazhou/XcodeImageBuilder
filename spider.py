#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-08-04 23:44:38
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : 
# @Disc    : 

import os
import os.path
import resize

input_base_dir = "ImageBuilderResources"
output_base_dir = "XcodeImageOutputs"

def process_dir(input_path, output_path):
	
    for parent,dirnames,filenames in os.walk(input_path):

        output_parent = output_base_dir + parent[len(input_base_dir):]

        if os.path.exists(output_parent) == False:
            os.mkdir(output_parent)

        for f in filenames:
            if f.startswith("."):
                continue

            resize.resize_img( parent+os.sep+f, output_parent+os.sep+f )


def main():
    process_dir( input_base_dir, output_base_dir )

if __name__ == '__main__':
    main()
else:
    print ('spider.py had been imported as a module')
