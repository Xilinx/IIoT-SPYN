#   Copyright (c) 2018, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from setuptools import setup, find_packages
import shutil
import subprocess
import sys
import os
from datetime import datetime

__author__ = "KV Thanjavur Bhaaskar, Naveen Purushotham"
__copyright__ = "Copyright 2018, Xilinx"
__email__ = "kvt@xilinx.com, npurusho@xilinx.com"

GIT_DIR = os.path.dirname(os.path.realpath(__file__))

from setuptools import setup, Extension, find_packages
import shutil
import subprocess
import sys
import os
import site
import warnings
from datetime import datetime
dst_base_dir ='/opt/python3.6/lib/python3.6/site-packages/spyn'
# Board specific package delivery setup
def exclude_from_files(exclude, path):
    return [file for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
            and file != exclude]


def exclude_from_dirs(exclude, path):
    return [folder for folder in os.listdir(path)
            if os.path.isdir(os.path.join(path, folder))
            and folder != exclude]


# Install packages
def install_packages():
    subprocess.check_call(['apt-get', '--yes', '--force-yes', 'install'])
    subprocess.check_call(['pip3.6', 'install',
                           'dash', 'dash-renderer',
                           'dash-html-components', 'dash-core-components',
                           'plotly'])
    print("Installing packages done ...")

	
if 'BOARD' not in os.environ:
    print("Please set the BOARD environment variable "
          "to get any BOARD specific overlays (e.g. Pynq-Z1).")
    board = None
    board_folder = None
else:
    board = os.environ['BOARD']
    board_folder = 'boards/{}'.format(board)

# Notebook delivery
def fill_notebooks():
    src_nb = os.path.join(GIT_DIR,board_folder,'notebooks')
    dst_nb_dir = '/home/xilinx/jupyter_notebooks/spyn'
    if os.path.exists(dst_nb_dir):
        shutil.rmtree(dst_nb_dir)
    shutil.copytree(src_nb, dst_nb_dir)

    print("Filling notebooks done ...")


# Images delivery
def fill_images():
    src_nb = os.path.join(GIT_DIR, board_folder, 'images')
    dst_nb_dir = '/home/xilinx/jupyter_notebooks/spyn/images'
    if os.path.exists(dst_nb_dir):
        shutil.rmtree(dst_nb_dir)
    shutil.copytree(src_nb, dst_nb_dir)

    print("Filling notebooks done ...")


# Overlays delivery
def fill_overlays():
    src_nb = os.path.join(GIT_DIR, board_folder,'overlays')
    dst_nb_dir = os.path.join(dst_base_dir, 'overlays')
    if os.path.exists(dst_nb_dir):
        shutil.rmtree(dst_nb_dir)
    shutil.copytree(src_nb, dst_nb_dir)

    print("Filling overlays done ...")


# Overlays delivery
def fill_lib():
    src_nb = os.path.join(GIT_DIR, board_folder,'lib')
    dst_nb_dir = os.path.join(dst_base_dir, 'lib')
    if os.path.exists(dst_nb_dir):
        shutil.rmtree(dst_nb_dir)
    shutil.copytree(src_nb, dst_nb_dir)

    print("Filling overlays done ...")


if len(sys.argv) > 1 and sys.argv[1] == 'install':
	install_packages()
	fill_notebooks()
	fill_images()
	fill_overlays()
	fill_lib()


def package_files(directory):
    paths = []
    for (path, directories, file_names) in os.walk(directory):
        for file_name in file_names:
            paths.append(os.path.join('..', path, file_name))
    return paths


extra_files = package_files('spyn')

setup(name='spyn',
      version='1.0',
      description='Motor Control using PYNQ package',
      author='Xilinx ISM + PYNQ',
      author_email='kvt@xilinx.com & npurusho@xilinx.com',
      url='https://github.com/Xilinx/SPYN-Starter',
      packages=find_packages(),
      download_url='https://github.com/Xilinx/SPYN-Starter',
      package_data={
          '': extra_files,
      }
      )
	  

