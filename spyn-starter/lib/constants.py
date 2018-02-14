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

import collections

__author__ = "Naveen Purushotham, KV Thanjavur Bhaaskar"
__copyright__ = "Copyright 2018, Xilinx"
__email__ = "npurusho@xilinx.com, kvt@xilinx.com"

# Offsets and mode constants for AXI 32 control registers - axi_reg32_0
AXI_CONTROL = collections.namedtuple('AXI_CONTROL',
                                     'offset reset_mode rpm_mode torque_mode')

# reset_mode, rpm_mode and torque_mode are the available motor controller modes
# They contain the respective initializations
# WR0_OFFSET
CONTROL = AXI_CONTROL(offset=64, reset_mode=0x0, rpm_mode=0x141,
                      torque_mode=0x145)
# WR1_OFFSET
FLUX_SP = AXI_CONTROL(offset=68, reset_mode=0x0, rpm_mode=0x0,
                      torque_mode=0x0)
# WR2_OFFSET
FLUX_KP = AXI_CONTROL(offset=72, reset_mode=0xFFFFF000, rpm_mode=0xFFFFF000,
                      torque_mode=0xFFFFF000)
# WR3_OFFSET
FLUX_KI = AXI_CONTROL(offset=76, reset_mode=0x0, rpm_mode=0x0,
                      torque_mode=0x0)
# WR4_OFFSET
TORQUE_SP = AXI_CONTROL(offset=80, reset_mode=0x0, rpm_mode=0x0,
                        torque_mode=0x0)
# WR5_OFFSET
TORQUE_KP = AXI_CONTROL(offset=84, reset_mode=0x1388, rpm_mode=0x1388,
                        torque_mode=0xFFFFB1E0)
# WR6_OFFSET
TORQUE_KI = AXI_CONTROL(offset=88, reset_mode=0x0, rpm_mode=0x0,
                        torque_mode=0xFFFFEC78)
# WR7_OFFSET
RPM_SP = AXI_CONTROL(offset=92, reset_mode=0x0, rpm_mode=0x0,
                     torque_mode=0x64)
# WR8_OFFSET
RPM_KP = AXI_CONTROL(offset=96, reset_mode=0xFFFFFF38, rpm_mode=0xFFFFFF38,
                     torque_mode=0xFFFFFF38)
# WR9_OFFSET
RPM_KI = AXI_CONTROL(offset=100, reset_mode=0xFFFFFFFB, rpm_mode=0xFFFFFFFB,
                     torque_mode=0xFFFFFFFB)
# WR10_OFFSET
SHIFT = AXI_CONTROL(offset=104, reset_mode=0x357, rpm_mode=0x357,
                    torque_mode=0x164)
# WR11_OFFSET
VD = AXI_CONTROL(offset=108, reset_mode=0xFFFFE300, rpm_mode=0xFFFFE300,
                 torque_mode=0xFFFFE300)
# WR12_OFFSET
VQ = AXI_CONTROL(offset=112, reset_mode=0xFFFFC100, rpm_mode=0xFFFFC100,
                 torque_mode=0xFFFFC100)
# WR13_OFFSET
FA = AXI_CONTROL(offset=116, reset_mode=0, rpm_mode=0,
                 torque_mode=18120)
# WR14_OFFSET
FB = AXI_CONTROL(offset=120, reset_mode=0, rpm_mode=0,
                 torque_mode=14647)
# WR15_OFFSET
CONTROL_REG2 = AXI_CONTROL(offset=124, reset_mode=0x0, rpm_mode=0x2,
                           torque_mode=0x100000)

# Offsets and mode constants for AXI 32 Status registers - axi_reg32_0
AXI_STATUS = collections.namedtuple('AXI_status', 'offset')
# SR0_OFFSET
ANGLE = AXI_STATUS(offset=128)
# SR1_OFFSET
SPEED = AXI_STATUS(offset=132)
# SR2_OFFSET
ID = AXI_STATUS(offset=136)
# SR3_OFFSET
IQ = AXI_STATUS(offset=140)

# Memory mapped blocks physical offset addresses
CONTROL_BLOCK_OFFSET = 0x43C00000
CAPTURE_BLOCK_OFFSET = 0x43C10000

# Address range for AXI control and capture blocks
ADDRESS_RANGE = 65536  # 64K

# Capture modes for stream capture
CAPTURE_IA_IB_ANGLE_RPM = 0x0
CAPTURE_ID_IQ = 0x2
CAPTURE_VD_VQ = 0x6
