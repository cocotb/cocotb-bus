`ifndef AVL_MM_MINI_IF
`define AVL_MM_MINI_IF

interface avl_mm_mini_if #(
    parameter int DATA_WIDTH = 32,  // width of data
    parameter int ADDR_WIDTH = 8    //  width of address
);

  logic read;
  logic write;
  logic waitrequest;
  logic readdatavalid;
  logic [ADDR_WIDTH - 1:0] address;
  logic [DATA_WIDTH - 1:0] readdata;
  logic [DATA_WIDTH - 1:0] writedata;

  modport hst(input waitrequest, readdata, readdatavalid, output read, write, address, writedata);

  modport agnt(input read, write, address, writedata, output waitrequest, readdata, readdatavalid);
endinterface  // avl_mm_mini_if

`endif
