
`timescale 1ns/1ps

module tb_priority_traffic_light;

    reg clk;
    reg rst;
    reg priority;

    wire [2:0] road_A;
    wire [2:0] road_B;

    // DUT
    priority_traffic_light DUT (
        .clk(clk),
        .rst(rst),
        .priority(priority),
        .road_A(road_A),
        .road_B(road_B)
    );

    // Clock generation
    always #5 clk = ~clk;

    initial begin

        clk = 0;
        rst = 1;
        priority = 0;

        // Apply reset
        #10 rst = 0;

        // Normal traffic
        #50;

        // Emergency vehicle detected
        priority = 1;
        #50;

        // Emergency vehicle leaves
        priority = 0;
        #50;

        // Finish simulation
        $finish;

    end

    // Monitor outputs
    initial begin
        $monitor("Time=%0t | Priority=%b | Road A=%b | Road B=%b",
                  $time, priority, road_A, road_B);
    end

endmodule
