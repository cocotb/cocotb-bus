// Copyright cocotb contributors
// Copyright (c) 2022 benycze
// Licensed under the Revised BSD License, see LICENSE for details.
// SPDX-License-Identifier: BSD-3-Clause

// The following module is using mix of upper and lower cases
// for port declarations
module case_insensitive (
      input    clk,
      input    IN_DATA,
      input    in_valid,
      input    in_tmp,
      output   out_data,
      output   OUT_VALID,
      output   OUT_TMP
);

reg tmp_data;
reg tmp_valid;
reg tmp_out;

initial begin
   tmp_data    = 1'b0;
   tmp_valid   = 1'b0;
   tmp_out     = 1'b0;
end

always @(posedge clk) begin
   tmp_data  <= IN_DATA;
   tmp_valid <= in_valid;
   tmp_out   <= in_tmp;
end

assign out_data   = tmp_data;
assign OUT_VALID  = tmp_valid;
assign OUT_TMP    = tmp_out;

endmodule

