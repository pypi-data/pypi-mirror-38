from distutils.core import setup
setup(
        name        =   'HS_recursion_List',
        version     =   '1.0.0',
        py_modules  =   ['HS_recursion_List'],
        author      =   'zhs0331',
        author_email=   '13811827020@139.com',
        url         =   'http://www.headfirstlabs.com',
        description =   "A simple printer of ecursion list",

      )

"""
构建发布 
 ########################## 执行内容 #############################
 cd E:\Automation\Python\Python Study_HeadFirst
 # py37 setup.py sdist
 ##########################   结果    #############################
running sdist
running check
warning: sdist: manifest template 'MANIFEST.in' does not exist (using default file list)

warning: sdist: standard file not found: should have one of README, README.txt, README.rst

writing manifest file 'MANIFEST'
creating nester-1.0.0
making hard links in nester-1.0.0...
hard linking nester.py -> nester-1.0.0
hard linking setup.py -> nester-1.0.0
creating dist
Creating tar archive
removing 'nester-1.0.0' (and everything under it)

 ##########################   将构建安装到python本地副本中    #############################
sudo py37 setup.py install
--------------Windows 执行-------------
# py37 setup.py install
--------------Windows 结果-------------
running install
running build
running build_py
creating build
creating build\lib
copying nester.py -> build\lib
running install_lib
copying build\lib\nester.py -> E:\Automation\Python\venv2\Lib\site-packages
byte-compiling E:\Automation\Python\venv2\Lib\site-packages\nester.py to nester.cpython-37.pyc
running install_egg_info
Writing E:\Automation\Python\venv2\Lib\site-packages\nester-1.0.0-py3.7.egg-info
 """