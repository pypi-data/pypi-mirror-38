edge-CNN-training
===============================

version number: 0.0.1
author: 余翰乔, 董元睿

Overview
--------
**ToE for training on edge!**

An edge-cloud collaborative training system for CNN and other DNNs.

Installation / Usage
--------------------

To install use pip:

    $ pip install ToE


Or clone the repo:

    $ git clone https://github.com/yhqjohn/ToE.git
    $ python setup.py install
    
Contributing
------------

TBD

Example
-------

TBD

Delete in master branch!
------
不可运行放入自定义branch；可运行的版本放入dev分支。

commit到master分支前，删除readme中这一章节。

项目名暂时写作ToE。

将工具性质的代码作为包添加到test/中,目前test文件夹还未finalize，可以随便写。

导入PyCharm之后PyCharm会自动安装requirements.txt中的包，注意PyTorch需要用pip手动安装。确定需要的包直接写在requirements.txt中，点击自动安装，测试中用到的包用pip安装，确定需要之后用pip freeze命令写入requirements.txt中。

修改以修改ToE/，test/，requirements.txt为主，其他部分暂时由余翰乔维护，文档直接放入项目根目录下。
