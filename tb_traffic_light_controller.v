`timescale 1ns/1ps

module tb_priority_traffic_light;

    reg clk = 0;
    reg rst;
    reg priority_in;

    wire [2:0] road_A;
    wire [2:0] road_B;

    // Device Under Test (DUT)
    priority_traffic_light DUT (
        .clk(clk),
        .rst(rst),
        .priority_in(priority_in),
        .road_A(road_A),
        .road_B(road_B)
    );

    // Clock generation: 10 ns period (100 MHz)
    always #5 clk = ~clk;

    initial begin
        // VCD Dump for EDA Playground EPWave
        $dumpfile("dump.vcd");
        $dumpvars(0, tb_priority_traffic_light);

        // Initial setup
        rst = 1;
        priority_in = 0;

        // Apply reset for 10 ns
        #10 rst = 0;

        // Stage 1: Normal alternating traffic (50 ns)
        #50;

        // Stage 2: Emergency vehicle detected on Road A (holds Road A Green)
        priority_in = 1;
        #50;

        // Stage 3: Emergency vehicle leaves (resumes normal traffic)
        priority_in = 0;
        #50;

        // Finish simulation
        $display("[TIME: %0t ns] Simulation finished successfully.", $time);
        $finish;
    end

    // Monitor outputs using simple signals (compatible across all Icarus Verilog versions)
    initial begin
        $monitor("Time=%0t ns | Priority=%b | Road A=%b | Road B=%b",
                 $time, priority_in, road_A, road_B);
    end

endmodule
