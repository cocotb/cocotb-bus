// Copyright cocotb contributors
// Copyright (c) 2024 davekeeshan
// Licensed under the Revised BSD License, see LICENSE for details.
// SPDX-License-Identifier: BSD-3-Clause

// The following module is using mix of upper and lower cases
// for port declarations
module and_gate (
      input    clk,
      input    a,
      input    b,
      output   c
);

reg r_c;

always @(posedge clk) begin
   r_c  <= a & b;
end

assign c = r_c;

endmodule


