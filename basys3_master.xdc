## ==============================================================================
## Basys 3 Master XDC Constraints
## Project: FSM-Based Priority Traffic Light Controller
## Target Device: Artix-7 xc7a35tcpg236-1
## ==============================================================================

## Clock Signal (100 MHz Master Oscillator)
set_property PACKAGE_PIN W5 [get_ports clk]							
set_property IOSTANDARD LVCMOS33 [get_ports clk]
create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports clk]

## Control Inputs (Slide Switches & Center Pushbutton)
## Switch SW0: Active-Low Reset
set_property PACKAGE_PIN V17 [get_ports rst_n]					
set_property IOSTANDARD LVCMOS33 [get_ports rst_n]

## Pushbutton BTNC (Center): North-South Emergency Vehicle Sensor
set_property PACKAGE_PIN U18 [get_ports emerg_ns]				
set_property IOSTANDARD LVCMOS33 [get_ports emerg_ns]

## Pushbutton BTNU (Up): East-West Emergency Vehicle Sensor
set_property PACKAGE_PIN T18 [get_ports emerg_ew]				
set_property IOSTANDARD LVCMOS33 [get_ports emerg_ew]

## Traffic Light Outputs: North-South Direction (LEDs LD0 - LD2)
## LD0: North-South Green
set_property PACKAGE_PIN U16 [get_ports ns_green]					
set_property IOSTANDARD LVCMOS33 [get_ports ns_green]

## LD1: North-South Yellow
set_property PACKAGE_PIN E19 [get_ports ns_yellow]					
set_property IOSTANDARD LVCMOS33 [get_ports ns_yellow]

## LD2: North-South Red
set_property PACKAGE_PIN U19 [get_ports ns_red]					
set_property IOSTANDARD LVCMOS33 [get_ports ns_red]

## Traffic Light Outputs: East-West Direction (LEDs LD3 - LD5)
## LD3: East-West Green
set_property PACKAGE_PIN V19 [get_ports ew_green]					
set_property IOSTANDARD LVCMOS33 [get_ports ew_green]

## LD4: East-West Yellow
set_property PACKAGE_PIN W18 [get_ports ew_yellow]					
set_property IOSTANDARD LVCMOS33 [get_ports ew_yellow]

## LD5: East-West Red
set_property PACKAGE_PIN U15 [get_ports ew_red]					
set_property IOSTANDARD LVCMOS33 [get_ports ew_red]

## FSM State Debug Outputs (LEDs LD13 - LD15)
set_property PACKAGE_PIN N3 [get_ports {state_out[0]}]					
set_property IOSTANDARD LVCMOS33 [get_ports {state_out[0]}]
set_property PACKAGE_PIN P1 [get_ports {state_out[1]}]					
set_property IOSTANDARD LVCMOS33 [get_ports {state_out[1]}]
set_property PACKAGE_PIN L1 [get_ports {state_out[2]}]					
set_property IOSTANDARD LVCMOS33 [get_ports {state_out[2]}]
