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

from pynq import MMIO
from .constants import *

__author__ = "Naveen Purushotham, KV Thanjavur Bhaaskar"
__copyright__ = "Copyright 2018, Xilinx"
__email__ = "npurusho@xilinx.com, kvt@xilinx.com"


class Motor_Controller(object):  # TODO comments
    """Class for the motor control. 

    This class is used to control the motor as well as read the status motor
    parameters. Motor control modes include: Speed mode and Current mode.
    In speed mode, the speed and direction of the motor are controlled using
    the RPM_Sp register. In current mode, the Torque_Sp register controls the
    current Iq to the motor. Relationship between current and torque is:
    Current = Torque*(0.00039)

    Attributes
    ----------
    mmio_blocks : dict
        A dict of IP blocks used by the motor controller.
    motor_modes : list
        A list of available modes of the motor controller.
    """

    def __init__(self):
        self.mmio_control = MMIO(CONTROL_BLOCK_OFFSET, ADDRESS_RANGE)
        self.mmio_capture = MMIO(CAPTURE_BLOCK_OFFSET, ADDRESS_RANGE)
        self.mmio_blocks = {'control_axi_block': hex(CONTROL_BLOCK_OFFSET),
                            'capture_axi_block': hex(CAPTURE_BLOCK_OFFSET)}
        self.motor_modes = ('reset_mode', 'torque_mode', 'rpm_mode')
        self.motor_capture_modes = ('ia_ib_angle_rpm', 'id_iq', 'vd_vq')

    def set_mode(self, mode='reset_mode'):
        reg_list = [CONTROL, FLUX_SP, FLUX_KP, FLUX_KI, TORQUE_SP, TORQUE_KP,
                    TORQUE_KI, RPM_SP, RPM_KP, RPM_KI, SHIFT, VD, VQ, FA, FB,
                    CONTROL_REG2]
        for reg in reg_list:
            if mode == 'torque_mode':
                self.mmio_control.write(reg.offset, reg.torque_mode)
            elif mode == 'rpm_mode':
                self.mmio_control.write(reg.offset, reg.rpm_mode)
            else:
                self.mmio_control.write(reg.offset, reg.reset_mode)

    def capture_mode(self, mode='ia_ib_angle_rpm'):
        reg = CONTROL_REG2
        if mode == 'ia_ib_angle_rpm':
            self.mmio_control.write(reg.offset, CAPTURE_IA_IB_ANGLE_RPM)
        elif mode == 'id_iq':
            self.mmio_control.write(reg.offset, CAPTURE_ID_IQ)
        elif mode == 'vd_vq':
            self.mmio_control.write(reg.offset, CAPTURE_VD_VQ)
        else:
            self.mmio_control.write(reg.offset, CAPTURE_IA_IB_ANGLE_RPM)

    def set_rpm(self, value):
        self.mmio_control.write(RPM_SP.offset, value)

    def set_torque(self, value):
        self.mmio_control.write(TORQUE_SP.offset, value)

    def stop(self):
        self.mmio_control.write(CONTROL.offset, CONTROL.reset_mode)

    def _read_controlreg(self, value):
        result = self.mmio_control.read(value)
        return result

    def _write_controlreg(self, offset, value):
        self.mmio_control.write(offset, value)

    def write_capturereg(self, offset, value):
        self.mmio_capture.write(offset, value)

    def read_capturereg(self, offset):
        result = self.mmio_capture.read(offset)
        return result

    def stream_capture(self, capture_address):  # TODO constants
        # Offset 0 - Control reg
        self.write_capturereg(0, 2)
        # Offset 4 - Transfer size
        self.write_capturereg(4, 256)
        # Offset 12 - Start address
        self.write_capturereg(12, capture_address)
        # Offset 16 - End address
        self.write_capturereg(16, capture_address + 256)
        # Offset 0 - Control reg
        self.write_capturereg(0, 3)
        # Offset 8 - Transfer count
        # print(f'Transfer count: {motor.read_capturereg(8)}')


def bytesplit(integer):
    return divmod(integer, 0x10000)
