// ==============================================================================
// Project      : FSM-Based Priority Traffic Light Controller with Emergency Detection
// File         : traffic_light_controller.v
// Standard     : Verilog-2001 (Synthesizable for Xilinx Vivado)
// Description  : 
//   4-Way intersection controller managing North-South (NS) and East-West (EW)
//   traffic with deterministic safety transitions (Yellow and All-Red buffer)
//   and preemption for emergency vehicles.
//
// Priority Scheme:
//   1. NS Emergency (emerg_ns) has highest priority.
//   2. EW Emergency (emerg_ew) has secondary priority.
//   3. Safe Yellow & All-Red transitions are guaranteed under all preemption events.
// ==============================================================================

module traffic_light_controller #(
    // Prescaler: number of clock cycles per second.
    // For 100 MHz board (Basys 3, Nexys A7): set to 100_000_000.
    // In Simulation: set to a small value (e.g. 4 or 10) for instant simulation.
    parameter CLK_FREQ_HZ   = 100_000_000,

    // Timing durations in seconds
    parameter SEC_NS_GREEN  = 10,   // North-South green duration
    parameter SEC_EW_GREEN  = 7,    // East-West green duration
    parameter SEC_YELLOW    = 3,    // Yellow clearance duration
    parameter SEC_ALL_RED   = 1     // All-Red intersection clearance buffer
)(
    input  wire       clk,          // System clock
    input  wire       rst_n,        // Active-low asynchronous reset
    input  wire       emerg_ns,     // North-South emergency vehicle sensor (active-high)
    input  wire       emerg_ew,     // East-West emergency vehicle sensor (active-high)

    // Bus light outputs: [2]=Red, [1]=Yellow, [0]=Green
    output reg  [2:0] ns_lights,
    output reg  [2:0] ew_lights,

    // Individual light outputs for direct board pin connection & waveform viewing
    output wire       ns_red,
    output wire       ns_yellow,
    output wire       ns_green,
    output wire       ew_red,
    output wire       ew_yellow,
    output wire       ew_green,

    // Debug / monitoring outputs
    output reg  [2:0] state_out,
    output reg  [5:0] sec_count_out
);

    // ==========================================================================
    // State Encoding
    // ==========================================================================
    localparam [2:0] 
        S_NS_GREEN  = 3'b000,   // NS: Green , EW: Red
        S_NS_YELLOW = 3'b001,   // NS: Yellow, EW: Red
        S_ALL_RED_1 = 3'b010,   // NS: Red   , EW: Red (Safety clearance)
        S_EW_GREEN  = 3'b011,   // NS: Red   , EW: Green
        S_EW_YELLOW = 3'b100,   // NS: Red   , EW: Yellow
        S_ALL_RED_2 = 3'b101;   // NS: Red   , EW: Red (Safety clearance)

    // Light encoding {Red, Yellow, Green}
    localparam [2:0]
        LIGHT_RED    = 3'b100,
        LIGHT_YELLOW = 3'b010,
        LIGHT_GREEN  = 3'b001;

    // FSM State Registers
    reg [2:0] current_state, next_state;

    // ==========================================================================
    // 1-Second Strobe Generator
    // ==========================================================================
    reg [31:0] clk_div_cnt;
    reg        tick_1s;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            clk_div_cnt <= 32'd0;
            tick_1s     <= 1'b0;
        end else begin
            if (clk_div_cnt >= CLK_FREQ_HZ - 1) begin
                clk_div_cnt <= 32'd0;
                tick_1s     <= 1'b1;
            end else begin
                clk_div_cnt <= clk_div_cnt + 1'b1;
                tick_1s     <= 1'b0;
            end
        end
    end

    // ==========================================================================
    // State Timer
    // ==========================================================================
    reg [5:0] sec_cnt;
    wire      state_changed;

    assign state_changed = (current_state != next_state);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sec_cnt <= 6'd0;
        end else if (state_changed) begin
            sec_cnt <= 6'd0; // Reset counter on entering new state
        end else if (tick_1s) begin
            if (sec_cnt < 6'd63) begin
                sec_cnt <= sec_cnt + 1'b1;
            end
        end
    end

    // Expose counter for monitoring / waveform
    always @(*) begin
        sec_count_out = sec_cnt;
    end

    // ==========================================================================
    // Sequential Process: State Register
    // ==========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            current_state <= S_NS_GREEN;
        end else begin
            current_state <= next_state;
        end
    end

    // ==========================================================================
    // Combinational Process: Next State Logic & Emergency Priority
    // ==========================================================================
    always @(*) begin
        next_state = current_state;

        case (current_state)

            // ------------------------------------------------------------------
            // State: North-South Green (East-West Red)
            // ------------------------------------------------------------------
            S_NS_GREEN: begin
                if (emerg_ns) begin
                    // Highest priority: Keep NS Green while NS emergency vehicle is active
                    next_state = S_NS_GREEN;
                end else if (emerg_ew) begin
                    // EW emergency: initiate safe transition immediately
                    next_state = S_NS_YELLOW;
                end else if (sec_cnt >= SEC_NS_GREEN) begin
                    // Normal timer expired
                    next_state = S_NS_YELLOW;
                end
            end

            // ------------------------------------------------------------------
            // State: North-South Yellow (East-West Red)
            // ------------------------------------------------------------------
            S_NS_YELLOW: begin
                // Yellow duration MUST be fully respected for vehicle braking safety
                if (sec_cnt >= SEC_YELLOW) begin
                    next_state = S_ALL_RED_1;
                end
            end

            // ------------------------------------------------------------------
            // State: All-Red Clearance 1 (Both Red)
            // ------------------------------------------------------------------
            S_ALL_RED_1: begin
                if (sec_cnt >= SEC_ALL_RED) begin
                    // If NS emergency is present, route straight back to NS Green
                    if (emerg_ns) begin
                        next_state = S_NS_GREEN;
                    end else begin
                        next_state = S_EW_GREEN;
                    end
                end
            end

            // ------------------------------------------------------------------
            // State: East-West Green (North-South Red)
            // ------------------------------------------------------------------
            S_EW_GREEN: begin
                if (emerg_ns) begin
                    // NS emergency has higher priority: truncate EW green safely
                    next_state = S_EW_YELLOW;
                end else if (emerg_ew) begin
                    // Hold EW green while EW emergency is active
                    next_state = S_EW_GREEN;
                end else if (sec_cnt >= SEC_EW_GREEN) begin
                    // Normal timer expired
                    next_state = S_EW_YELLOW;
                end
            end

            // ------------------------------------------------------------------
            // State: East-West Yellow (North-South Red)
            // ------------------------------------------------------------------
            S_EW_YELLOW: begin
                // Yellow safety duration
                if (sec_cnt >= SEC_YELLOW) begin
                    next_state = S_ALL_RED_2;
                end
            end

            // ------------------------------------------------------------------
            // State: All-Red Clearance 2 (Both Red)
            // ------------------------------------------------------------------
            S_ALL_RED_2: begin
                if (sec_cnt >= SEC_ALL_RED) begin
                    // If EW emergency is present and NO NS emergency, return to EW Green
                    if (emerg_ew && !emerg_ns) begin
                        next_state = S_EW_GREEN;
                    end else begin
                        next_state = S_NS_GREEN;
                    end
                end
            end

            default: begin
                next_state = S_NS_GREEN;
            end

        endcase
    end

    // ==========================================================================
    // Registered Output Logic (Glitch-Free)
    // ==========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ns_lights <= LIGHT_GREEN;
            ew_lights <= LIGHT_RED;
            state_out <= S_NS_GREEN;
        end else begin
            state_out <= current_state;
            case (current_state)
                S_NS_GREEN: begin
                    ns_lights <= LIGHT_GREEN;
                    ew_lights <= LIGHT_RED;
                end
                S_NS_YELLOW: begin
                    ns_lights <= LIGHT_YELLOW;
                    ew_lights <= LIGHT_RED;
                end
                S_ALL_RED_1: begin
                    ns_lights <= LIGHT_RED;
                    ew_lights <= LIGHT_RED;
                end
                S_EW_GREEN: begin
                    ns_lights <= LIGHT_RED;
                    ew_lights <= LIGHT_GREEN;
                end
                S_EW_YELLOW: begin
                    ns_lights <= LIGHT_RED;
                    ew_lights <= LIGHT_YELLOW;
                end
                S_ALL_RED_2: begin
                    ns_lights <= LIGHT_RED;
                    ew_lights <= LIGHT_RED;
                end
                default: begin
                    ns_lights <= LIGHT_RED;
                    ew_lights <= LIGHT_RED;
                end
            endcase
        end
    end

    // Individual light wire assignments for ease of connection
    assign ns_red    = ns_lights[2];
    assign ns_yellow = ns_lights[1];
    assign ns_green  = ns_lights[0];

    assign ew_red    = ew_lights[2];
    assign ew_yellow = ew_lights[1];
    assign ew_green  = ew_lights[0];

endmodule
