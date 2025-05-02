module avl_feedback;

    localparam int DataWidth = 32;
    localparam int AddrWidth = 32;

    logic clk;

    avl_st_mini_if #(DataWidth) i_feedback_if ();
    avl_st_mini_if #(DataWidth) o_feedback_if ();

    avl_mm_mini_if #(
        .DATA_WIDTH(DataWidth),
        .ADDR_WIDTH(AddrWidth)
    ) mem_port_if ();

    st_feedback  #(
        .DATA_WIDTH(DataWidth)
    ) st_feedback_inst (
        .i_feedback_if(i_feedback_if),
        .o_feedback_if(o_feedback_if)
    );

    mm_reader #(
        .DATA_WIDTH(DataWidth),
        .ADDR_WIDTH(AddrWidth)
    ) mm_reader_inst (
        .clk(clk),
        .mem_port(mem_port_if)
    );

endmodule
