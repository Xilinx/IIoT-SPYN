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
import sys
import os
import site


__author__ = "KV Thanjavur Bhaaskar, Naveen Purushotham"
__copyright__ = "Copyright 2018, Xilinx"
__email__ = "kvt@xilinx.com, npurusho@xilinx.com"


GIT_DIR = os.path.dirname(os.path.realpath(__file__))


# Board specific package delivery setup
def exclude_from_files(exclude, path):
    return [file for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
            and file not in exclude]


def exclude_from_dirs(exclude, path):
    return [folder for folder in os.listdir(path)
            if os.path.isdir(os.path.join(path, folder))
            and folder not in exclude]


def collect_data_files():
    return [(os.path.join(
        '{}/spyn/overlays'.format(os.path.dirname(site.__file__) +
                                  "/site-packages"), ol),
             [os.path.join(board_folder, ol, f)
              for f in exclude_from_files(
                 ['makefile'], os.path.join(board_folder, ol))])
            for ol in exclude_from_dirs(['notebooks', 'vivado'],
                                        board_folder)]


if 'BOARD' not in os.environ:
    print("Please set the BOARD environment variable "
          "to get any BOARD specific overlays (e.g. Pynq-Z1).")
    board = None
    board_folder = None
    data_files = None
else:
    board = os.environ['BOARD']
    board_folder = 'boards/{}'.format(board)
    data_files = collect_data_files()


# Notebook delivery
def fill_notebooks():
    src_nb = os.path.join(GIT_DIR, 'notebooks')
    dst_nb_dir = '/home/xilinx/jupyter_notebooks/spyn'
    if os.path.exists(dst_nb_dir):
        shutil.rmtree(dst_nb_dir)
    shutil.copytree(src_nb, dst_nb_dir)

    print("Filling notebooks done ...")


if len(sys.argv) > 1 and sys.argv[1] == 'install':
    fill_notebooks()


setup(name='spyn',
      version='1.0',
      description='Motor Control using PYNQ package',
      author='Xilinx ISM + PYNQ',
      author_email='kvt@xilinx.com',
      url='https://github.com/Xilinx/IIoT-SPYN',
      packages=find_packages(),
      download_url='https://github.com/Xilinx/IIoT-SPYN',
      package_data={
          '': ['*.bin', '*.so'],
      },
      data_files=data_files
      )
