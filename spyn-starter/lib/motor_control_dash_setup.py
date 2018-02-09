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


__author__ = "Kiran Vishal Thanjavur Bhaaskar & Naveen Purushotham"
__copyright__ = "Copyright 2018, Xilinx"
__email__ = "kvt@xilinx.com & npurusho@xilinx.com"


from pynq import Overlay
from pynq import MMIO
import numpy as np
from motor_controller import *
from constants import *
from pynq import Xlnk
import pandas as pd
import time

overlay = Overlay("eddp.bit")
overlay.download()

motor = Motor_Controller()
motor.set_mode('rpm_mode')
motor.set_rpm(1500)
motor.capture_mode('ia_ib_angle_rpm')

time.sleep(4)

motor_status = [(motor._read_controlreg(i + ANGLE.offset)) for i in
                range(0, 16, 4)]
high_sp, low_sp = bytesplit(motor_status[1])
high_id, low_id = bytesplit(motor_status[2])
high_iq, low_iq = bytesplit(motor_status[3])
print(f'Angle in degrees : {motor_status[0] * 0.36}')
print(f'Angle in steps per thousand: {(motor_status[0])}')
print(f'Id : {np.int16(low_id) * 0.00039} Amp')
print(f'Iq : {np.int16(low_iq) * 0.00039} Amp')
print(f'Speed in RPM : {-(np.int16(low_sp))}')

xlnk = Xlnk()
input_buffer = xlnk.cma_array(shape=(256,), dtype=np.uint8)

capture_address = input_buffer.physical_address

# capture_count = int(input('Enter capture count: '))
capture_count = 2000

def continuous_capture(capture_count):    
    mmio_stream = MMIO(capture_address, 256)
    cap_list = [([]) for i in range(4)]
    for _ in range(capture_count):
        motor.stream_capture(capture_address)
        for i in range(4, 260, 4):
            stream = mmio_stream.read(i - 4, 4)
            highbits, lowbits = bytesplit(stream)
            if (i % 8 != 0):
                cap_list[0].extend([(np.int16(lowbits))])
                cap_list[1].extend([(np.int16(highbits))])
            else:
                cap_list[2].extend([(np.int16(lowbits))])
                cap_list[3].extend([(np.int16(highbits))])
    return cap_list

cap_list = continuous_capture(capture_count)
Ia, Ib, angle, rpm  = cap_list[0], cap_list[1], cap_list[3], cap_list[2]

current_Ia = np.array(Ia) * 0.00039
current_Ib = np.array(Ib) * 0.00039
data = {'Ia' : current_Ia,
        'Ib' : current_Ib,
        'angle':cap_list[3],
        'rpm':  cap_list[2]}

df = pd.DataFrame(data, columns = ['Ia', 'Ib', 'angle', 'rpm'])
