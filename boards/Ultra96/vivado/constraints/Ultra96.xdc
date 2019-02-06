#ULTRA96 PORT CONSTRAINT
# J7 <-> PMODA
set_property PACKAGE_PIN D7 [get_ports SCLK]
set_property PACKAGE_PIN F8 [get_ports SDI1]
set_property PACKAGE_PIN F7 [get_ports SDI2]
set_property PACKAGE_PIN G7 [get_ports SDI3]
set_property PACKAGE_PIN F6 [get_ports SDV]
set_property PACKAGE_PIN G5 [get_ports ENC_A]
set_property PACKAGE_PIN A6 [get_ports ENC_B]
set_property PACKAGE_PIN A7 [get_ports ENC_I]
set_property IOSTANDARD LVCMOS18 [get_ports SCLK]
set_property IOSTANDARD LVCMOS18 [get_ports SDI*]
set_property IOSTANDARD LVCMOS18 [get_ports SDV]
set_property IOSTANDARD LVCMOS18 [get_ports ENC_*]

# J7 <-> PMODB
set_property PACKAGE_PIN G6 [get_ports {GH[0]}]
set_property PACKAGE_PIN E6 [get_ports {GH[1]}]
set_property PACKAGE_PIN E5 [get_ports {GH[2]}]
set_property PACKAGE_PIN D6 [get_ports {GL[0]}]
set_property PACKAGE_PIN D5 [get_ports {GL[1]}]
set_property PACKAGE_PIN C7 [get_ports {GL[2]}]
set_property IOSTANDARD LVCMOS18 [get_ports GH*]
set_property IOSTANDARD LVCMOS18 [get_ports GL*]
set_property DRIVE 4 [get_ports GL*]
set_property DRIVE 4 [get_ports GH*]
set_property DRIVE 4 [get_ports SCLK]
set_property SLEW SLOW [get_ports SCLK]
set_property SLEW SLOW [get_ports GL*]
set_property SLEW SLOW [get_ports GH*]

#THESE LED PORTS CAN NOT ACCESS THE ULTRA96 LED'S BECAUSE THE ULRTS96 LEDS ARE DRIVEN BY THE MIO PORTS
#set_property PACKAGE_PIN R14 [get_ports {led[0]}]
#set_property PACKAGE_PIN P14 [get_ports {led[1]}]
#set_property PACKAGE_PIN N16 [get_ports {led[2]}]
#set_property PACKAGE_PIN M14 [get_ports {led[3]}]
#set_property IOSTANDARD LVCMOS18 [get_ports led*]

#set_property PACKAGE_PIN XXX [get_ports BTN0]
#set_property PACKAGE_PIN XXX [get_ports BTN1]
#set_property PACKAGE_PIN XXX [get_ports BTN2]
#set_property PACKAGE_PIN XXX [get_ports BTN3]
#set_property IOSTANDARD LVCMOS18 [get_ports BTN*]

#set_property PACKAGE_PIN M20 [get_ports SW0]
#set_property IOSTANDARD LVCMOS18 [get_ports SW*]


create_generated_clock -name clk_fpga_0_ss -source [get_pins zsys_i/clk_wiz_0/inst/mmcme4_adv_inst/CLKIN1] -master_clock zsys_i/clk_wiz_0/inst/clk_in1 [get_pins zsys_i/clk_wiz_0/inst/mmcme4_adv_inst/CLKOUT0]
set_clock_groups -name exclusive_clks -physically_exclusive -group [get_clocks clk_pl_0] -group [get_clocks clk_fpga_0_ss]


set_property IOSTANDARD LVCMOS18 [get_ports BT*]

#BT_HCI_RTS on FPGA /  emio_uart0_ctsn connect to 
set_property PACKAGE_PIN B7 [get_ports BT_ctsn]
#BT_HCI_CTS on FPGA / emio_uart0_rtsn
set_property PACKAGE_PIN B5 [get_ports BT_rtsn]

