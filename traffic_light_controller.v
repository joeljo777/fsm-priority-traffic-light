`timescale 1ns/1ps

module priority_traffic_light (
    input clk,
    input rst,
    input priority_in,   // Active-high emergency vehicle sensor for Road A

    output reg [2:0] road_A,
    output reg [2:0] road_B
);

    // Light encoding {Red, Yellow, Green}
    parameter RED    = 3'b100;
    parameter YELLOW = 3'b010;
    parameter GREEN  = 3'b001;

    // FSM states
    parameter S0 = 2'b00;
    parameter S1 = 2'b01;
    parameter S2 = 2'b10;
    parameter S3 = 2'b11;

    reg [1:0] state, next_state;

    // State transition (Sequential)
    always @(posedge clk or posedge rst) begin
        if (rst)
            state <= S0;
        else
            state <= next_state;
    end

    // Next state logic (Combinational)
    always @(*) begin

        case (state)

            // S0: Road A Green, Road B Red
            // If priority vehicle detected on Road A, hold Green; otherwise transition to Yellow
            S0: begin
                if (priority_in)
                    next_state = S0;
                else
                    next_state = S1;
            end

            // S1: Road A Yellow, Road B Red (Braking transition)
            S1: begin
                next_state = S2;
            end

            // S2: Road A Red, Road B Green
            // Transition to Yellow to yield back to Road A
            S2: begin
                next_state = S3;
            end

            // S3: Road A Red, Road B Yellow (Braking transition)
            S3: begin
                next_state = S0;
            end

            default: next_state = S0;

        endcase
    end

    // Output logic (Combinational)
    always @(*) begin

        road_A = RED;
        road_B = RED;

        case (state)

            S0: begin
                road_A = GREEN;
                road_B = RED;
            end

            S1: begin
                road_A = YELLOW;
                road_B = RED;
            end

            S2: begin
                road_A = RED;
                road_B = GREEN;
            end

            S3: begin
                road_A = RED;
                road_B = YELLOW;
            end

        endcase
    end

endmodule
