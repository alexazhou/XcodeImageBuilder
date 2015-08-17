#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-04 23:44:38
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : 
# @Disc    : 

import os
import os.path
import resize
import sys
import getopt
from mod_pbxproj import XcodeProject


input_base_dir = "ImageBuilderResources"
output_base_dir = "XcodeImageOutput"

project_file = ""
xcode_group = ""

def resize_img_in_path(input_path, output_path):
    
    for parent,dirnames,filenames in os.walk(input_path):

        output_parent = output_base_dir + parent[len(input_base_dir):]

        if os.path.exists(output_parent) == False:
            os.mkdir(output_parent)

        for f in filenames:
            if f.startswith("."):
                continue

            if "@3x" not in f and "@6x" not in f:
                continue

            resize.resize_img( parent+os.sep+f, (output_parent+os.sep+f).replace("@6x","").replace("@3x","") )


def xcode_get_or_create_group_by_path( project_obj, xcode_path):
    
    group_names = xcode_path.split("/")
    group = None
    for name in group_names:
        name = name.decode("utf-8")

        group = project_obj.get_or_create_group( name, parent= group)

    return group


def xcode_project_sync(file_path, xcode_group):

    if xcode_group == "":
        print("INFO: not specify xcode group, so ignore sync imgs to Xcode project")
        return False

    ret = os.system("xcproj -h")
    print("ret",ret)

    if ret != 0:
        print("please make sure xcproj tool installed. xcproj can make .pbxproj file look pretty")
        return False

    project_obj = XcodeProject.Load(project_file)
    modifyed = False
    
    for parent,dirnames,filenames in os.walk(file_path):

        xcode_path = xcode_group + parent[len(file_path):]
        group = xcode_get_or_create_group_by_path( project_obj, xcode_path )

        for f in filenames:
            if f.startswith("."):
                continue

            name = (parent+os.sep+f).decode("utf-8")

            if len(project_obj.get_files_by_name(f.decode("utf-8"), parent = group)) == 0:
                modifyed = True
                print("sync file to Xcode Group:%s"%name.encode("utf-8"))
                project_obj.add_file( name , parent = group )

    if modifyed:
        print("now save project file")
        project_obj.save()
        print("success!\nAnd now use xcproj to retouch project, make it what it was")

        retouch_ret = os.system('xcproj -p "%s" touch'%project_file)
        if retouch_ret == 0:
            print("success!")
        else:
            print("some thing was error, call xproj failed.")

        return True
    else:
        return False


def main():
    global input_base_dir, output_base_dir, project_file, xcode_group

    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:g:p:', ["help"]) 

    for option, value in opts: 
        #print("option:%s --> value:%s"%(option, value))

        if option == "-i":
            input_base_dir = value
        elif option == "-o":
            output_base_dir = value
        elif option == "-g":
            xcode_group = value
        elif option == "-p":
            project_file = value
        elif option == "-h" or option == "--help":
            print("use: spider.py -i [image input path] -o [image output path] -g [Xcode group] -p [Xcode .pbxproj file path]")
            sys.exit(1)

    resize_img_in_path( input_base_dir, output_base_dir )
    project_modifyed = xcode_project_sync(output_base_dir, xcode_group)

    if project_modifyed:
        print("images synced to xcode group, please build again")
        sys.exit(1)


if __name__ == '__main__':
    main()
else:
    print ('spider.py had been imported as a module')

