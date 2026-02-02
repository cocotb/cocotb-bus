// Copyright cocotb contributors
// Copyright (c) 2025 Benycze
// Licensed under the Revised BSD License, see LICENSE for details.
// SPDX-License-Identifier: BSD-3-Clause

// Simplified read/write interface with structures on the interface.
//
// Read:
// ========
// 1) Assert ADDR, CMD = CMD_READ, VLD = 1
// 2) Data will be returned on the output interface in the next clock cycle.
//    Read data will be available till the next clock cycle.
//
// Write:
// ========
// 1] Assert ADDR, CMD =  CMD_WRITE, VLD = 1, DATA you want to write
// 2] The write status is returned in the next clock cycle using the WR_STATUS
//    output. The signal is valid till the next clock cycle.
//

`define CMD_READ       0
`define CMD_WRITE      1
`define STATUS_WR_DONE 0
`define STATUS_WR_ERR  1

interface mem_in_interface_t (input logic CLK, RESET);
    logic [31:0]    DATA;
    logic           CMD;
    logic [5:0]     ADDR;
    logic           VLD;

    modport rx (input DATA, CMD, ADDR, VLD);
endinterface //mem_in_interface_t

interface mem_out_interface_t (input CLK);
    logic [31:0]    DATA;
    logic           VLD;
    logic           WR_STATUS;

    modport tx (output DATA, VLD, WR_STATUS);
endinterface //mem_out_interface_t

module test_struct_reg (
    input logic CLK,
    input logic RESET,
    mem_in_interface_t.rx I_REG,
    mem_out_interface_t.tx O_REG
);

logic [31:0]    reg_arr[2**6-1:0];
logic [31:0]    o_data;
logic           o_vld;
logic           o_status;

always @(posedge CLK) begin : process_p
    o_vld       <= '0;
    o_status    <= `STATUS_WR_DONE;
    o_data      <= '0;
    if (I_REG.VLD) begin
        o_vld <= 1;
        if (I_REG.CMD == `CMD_WRITE) begin
            reg_arr[I_REG.ADDR] <= I_REG.DATA;
            // Simplified model, no error by default
        end else if(I_REG.CMD == `CMD_READ) begin
            o_data <= reg_arr[I_REG.ADDR];
        end
    end
end

always @(posedge CLK) begin : output_p
   if (RESET)  begin
       O_REG.DATA       <= '0;
       O_REG.VLD        <= '0;
       O_REG.WR_STATUS  <= '0;
   end else begin
       O_REG.DATA       <= o_data;
       O_REG.VLD        <= o_vld;
       O_REG.WR_STATUS  <= o_status;
   end
end

endmodule

module top (
    input logic CLK,
    input logic RESET
);

// Prepare interface
mem_in_interface_t I_REG(.*);
mem_out_interface_t O_REG(.*);

// Connect DUT
test_struct_reg reg_inst(
    .CLK(CLK),
    .RESET(RESET),
    .I_REG(I_REG),
    .O_REG(O_REG)
);
endmodule
