
module priority_traffic_light (
    input clk,
    input rst,
    input priority,

    output reg [2:0] road_A,
    output reg [2:0] road_B
);

    // Light encoding
    parameter RED    = 3'b100;
    parameter YELLOW = 3'b010;
    parameter GREEN  = 3'b001;

    // FSM states
    parameter S0 = 2'b00;
    parameter S1 = 2'b01;
    parameter S2 = 2'b10;
    parameter S3 = 2'b11;

    reg [1:0] state, next_state;

    // State transition
    always @(posedge clk or posedge rst) begin
        if (rst)
            state <= S0;
        else
            state <= next_state;
    end

    // Next state logic
    always @(*) begin

        case (state)

            S0: next_state = S1;

            S1: next_state = S2;

            S2: begin
                if (priority)
                    next_state = S3;
                else
                    next_state = S3;
            end

            S3: begin
                if (priority)
                    next_state = S0;
                else
                    next_state = S0;
            end

            default: next_state = S0;

        endcase
    end

    // Output logic
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
