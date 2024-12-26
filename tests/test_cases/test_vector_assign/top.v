module IOBUF (O, IO, I, T);
    output O;
    inout  IO;
    input  I, T;

    bufif0 T1 (IO, I, T);

    buf B1 (O, IO);
    
endmodule

module top (
      input    clk,
      input    a,
      input    b,
      output   c,
      inout [2:0]   ja
);

    logic [ 2:0] w_ja_in;
    logic [ 2:0] w_ja_out;
    logic [ 2:0] w_ja_t;

    logic  w_a;
    logic  w_b;
    logic  w_c;

    and_gate i_and_gate_0 (
        .*
    );

    and_gate i_and_gate_1 (
        .clk      (clk),
        .a (w_a),
        .b (w_b),
        .c (w_c)
    );

    assign w_a = w_ja_in[0] ;
    assign w_b = w_ja_in[1] ;
    assign w_ja_out[2] = w_c;
    assign w_ja_t      = 3'b011;
//     assign w_ja_in[2] = 1'b0;

    genvar i;
    generate
        for (i = 0; i < 3; i = i + 1) begin : g_iobuf
            IOBUF i_ja_iobuf (
                  .I (w_ja_out[i])
                , .IO(ja[i])
                , .O (w_ja_in[i])
                , .T (w_ja_t[i])
            );
        end
    endgenerate

    initial begin
        $dumpfile ("dut.vcd");
        $dumpvars (0, i_and_gate_0);
       /* verilator lint_off STMTDLY */
        #1;
        /* verilator lint_on STMTDLY */
    end
endmodule
