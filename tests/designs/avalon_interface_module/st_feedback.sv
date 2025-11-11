    module st_feedback #(
        parameter int DATA_WIDTH = 32
    ) (
        avl_st_mini_if.dst i_feedback_if,
        avl_st_mini_if.src o_feedback_if
    );

        assign i_feedback_if.ready = o_feedback_if.ready;
        assign o_feedback_if.valid = i_feedback_if.valid;
        assign o_feedback_if.startofpacket = i_feedback_if.startofpacket;
        assign o_feedback_if.endofpacket = i_feedback_if.endofpacket;
        assign o_feedback_if.data = i_feedback_if.data;

    endmodule
