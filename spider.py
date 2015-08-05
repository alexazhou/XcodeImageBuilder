#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-08-04 23:44:38
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : 
# @Disc    : 

import os
import os.path
import resize
import sys
from mod_pbxproj import XcodeProject


input_base_dir = "ImageBuilderResources"
output_base_dir = "XcodeImageOutputs"

project_file = "lcf-newproject.xcodeproj/project.pbxproj"
xcode_group = "lcf-newproject/Supporting Files/AutoBuildImages"

def resize_img_in_path(input_path, output_path):
    
    for parent,dirnames,filenames in os.walk(input_path):

        output_parent = output_base_dir + parent[len(input_base_dir):]

        if os.path.exists(output_parent) == False:
            os.mkdir(output_parent)

        for f in filenames:
            if f.startswith("."):
                continue

            resize.resize_img( parent+os.sep+f, (output_parent+os.sep+f).replace("@6x","") )


def xcode_get_or_create_group_by_path( project_obj, xcode_path):
    
    group_names = xcode_path.split("/")
    group = None
    for name in group_names:
        name = name.decode("utf-8")

        group = project_obj.get_or_create_group( name, parent= group)

    return group


def xcode_project_sync(file_path, xcode_group):

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
        project_obj.save()
        return True
    else:
        return False


def main():
    
    resize_img_in_path( input_base_dir, output_base_dir )
    project_modifyed = xcode_project_sync(output_base_dir, xcode_group)

    if project_modifyed:
        print("images synced to xcode group, please build again")
        sys.exit(1)


if __name__ == '__main__':
    main()
else:
    print ('spider.py had been imported as a module')

