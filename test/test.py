import cocotb
import struct

from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge

@cocotb.test()
async def test_PWM(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut._log.info("Start")
    dut.rst_n.value = 0
    dut.uio_in.value = 0b011
    dut.ui_in.value = 0b00000000

    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    # Test cases
    for bits_value in [0b011, 0b100, 0b111, 0b010, 0b000]:
        dut._log.info("25 Duty")
        dut.uio_in.value = bits_value
        #pad = binary_rep.zfill(len(dut.ui_in))
        btf = float(bits_value)
        ftn = int(0.5*(2**bits_value))
        
        dut.ui_in.value = ftn

        await ClockCycles(dut.clk, 400)  # Wait for some cycles

        dut._log.info("50 Duty")
        btf = float(bits_value)
        ftn = int(0.5*(2**bits_value))
        
        dut.ui_in.value = ftn
        await ClockCycles(dut.clk, 400)

        dut._log.info("75 Duty")
        btf = float(bits_value)
        ftn = int(0.5*(2**bits_value))
        
        dut.ui_in.value = ftn

        await ClockCycles(dut.clk, 400)

    # Wait for the simulation to complete
    await ClockCycles(dut.clk, 400)
    cocotb.log.info("Simulation complete")
