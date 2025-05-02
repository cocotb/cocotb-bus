`ifndef AVL_ST_MINI_IF
`define AVL_ST_MINI_IF

interface avl_st_mini_if #(
    parameter int DATA_WIDTH = 32
);
  logic ready;
  logic valid;
  logic startofpacket;
  logic endofpacket;
  logic [DATA_WIDTH-1:0] data;

  modport src(input ready, output valid, startofpacket, endofpacket, data);

  modport dst(input valid, startofpacket, endofpacket, data, output ready);

endinterface : avl_st_mini_if

`endif
