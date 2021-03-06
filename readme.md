#XcodeImageBuilder

XcodeImageBuilder是一个由@6x图片自动生成@3x @2x @1x图片的工具。

>只需要把大图放入文件夹，XcodeImageBuilder将自动为你生成@3x @2x @1x图片，并自动把这些图片添加到Xcode工程当中（可选）。

###特性
* 由@6x图片得到@3x @2x @1x图片
* 为resize得到的图片自动命名
* 保持图片文件夹结构
* 自动添加图片到Xcode工程
* 和Xcode无缝集成

###依赖
XcodeImageBuilder用到了python2，并使用了pillow来处理图片，mod_pbxproj来对Xcode工程进行读写，以及xcproj来保持Xcode工程文件格式。

请通过以下命令进行安装:  
**pip install pillow**  
**pip install mod_pbxproj**  
**brew install xcproj**
###使用方法

命令行方式调用：

**spider.py -i [image input path] -o [image output path] -g [Xcode group] -p [Xcode .pbxproj file path]**

* **-i**: 一个输入文件的路径
* **-o**: 存放输出文件的路径

这条命令将为输入文件夹中的每张图片生成三个尺寸的小图，并按照同样的名称，以同样的目录结构，存放在指定的输出文件夹中。  

####如果需要把缩小之后的图片自动添加到Xcode工程，需要指定以下两个参数，不需要添加到工程则留空

* **-g**: Xcode中存放图片的Group，如 AAA/Images
* **-p**: Xcode工程文件路径，如"abc-newproject.xcodeproj/project.pbxproj"

图片在Xcode Group中将会依旧保持同样的目录结构

####Xcode集成

为了更加方便，省去手动执行的步骤，推荐在Xcode工程的Build phases选项卡中添加一个run script项目，使每次编译时，自动运行XcodeImageBuilder工具。这样需要添加图片素材的时候，只需要把@6x的素材放入文件夹，其他就全自动了。。。


![image](http://7oxic4.com1.z0.glb.clouddn.com/XcodeImageBuilderWithXcode.png) 


####FAQ:

###@6x图片是什么?以及为什么需要@6x的图片？
按照Xcode中的命名规则，@6x图片就是6倍分辨率的图片。使用@6x图片作为输入是为了使resize得到的@2x和@3x图片都不失真。