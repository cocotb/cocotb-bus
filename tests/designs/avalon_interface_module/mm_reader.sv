module mm_reader #(
        parameter int DATA_WIDTH = 32,
        parameter int ADDR_WIDTH = 32
    ) (
        input logic clk,

        avl_mm_mini_if.agnt mem_port
    );
        logic [DATA_WIDTH - 1 : 0] mem [ADDR_WIDTH];

        always_ff @(posedge clk) begin
            // Write
            if (mem_port.write) begin
                mem[mem_port.address] <= mem_port.writedata;
            end
            if (mem_port.read) begin
                mem_port.readdata <= mem[mem_port.address];
                mem_port.readdatavalid <= 1;
            end
        end

endmodule
