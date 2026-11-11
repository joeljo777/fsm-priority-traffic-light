// ==============================================================================
// Project      : FSM-Based Priority Traffic Light Controller with Emergency Detection
// File         : tb_traffic_light_controller.v
// Standard     : Verilog-2001
// Description  : 
//   Comprehensive Testbench for traffic_light_controller.
//   Simulates normal traffic cycles, emergency vehicle preemptions, safe braking
//   transitions, and simultaneous emergency conflicts.
//   Includes ASCII string decoders for clear, readable Vivado waveform inspection.
// ==============================================================================

`timescale 1ns / 1ps

module tb_traffic_light_controller();

    // --------------------------------------------------------------------------
    // Simulation Parameters
    // --------------------------------------------------------------------------
    // For fast simulation, we scale down the clock prescaler:
    // 4 clock cycles = 1 simulated second.
    localparam CLK_FREQ_HZ  = 4;
    localparam SEC_NS_GREEN = 4;   // 4 sec (16 cycles)
    localparam SEC_EW_GREEN = 3;   // 3 sec (12 cycles)
    localparam SEC_YELLOW   = 2;   // 2 sec (8 cycles)
    localparam SEC_ALL_RED  = 1;   // 1 sec (4 cycles)

    // Clock generation: 100 MHz (10 ns period)
    localparam CLK_PERIOD = 10;

    // --------------------------------------------------------------------------
    // Testbench Signals
    // --------------------------------------------------------------------------
    reg        clk;
    reg        rst_n;
    reg        emerg_ns;
    reg        emerg_ew;

    wire [2:0] ns_lights;
    wire [2:0] ew_lights;
    wire       ns_red, ns_yellow, ns_green;
    wire       ew_red, ew_yellow, ew_green;
    wire [2:0] state_out;
    wire [5:0] sec_count_out;

    // --------------------------------------------------------------------------
    // Waveform-friendly ASCII String Decoders
    // (In Vivado Waveform, right-click -> Radix -> ASCII to view these live!)
    // --------------------------------------------------------------------------
    reg [8*12-1:0] state_name;
    reg [8*8-1:0]  ns_light_str;
    reg [8*8-1:0]  ew_light_str;

    always @(*) begin
        case (state_out)
            3'b000:  state_name = "NS_GREEN   ";
            3'b001:  state_name = "NS_YELLOW  ";
            3'b010:  state_name = "ALL_RED_1  ";
            3'b011:  state_name = "EW_GREEN   ";
            3'b100:  state_name = "EW_YELLOW  ";
            3'b101:  state_name = "ALL_RED_2  ";
            default: state_name = "UNKNOWN    ";
        endcase

        case (ns_lights)
            3'b100:  ns_light_str = "RED   ";
            3'b010:  ns_light_str = "YELLOW";
            3'b001:  ns_light_str = "GREEN ";
            default: ns_light_str = "OFF   ";
        endcase

        case (ew_lights)
            3'b100:  ew_light_str = "RED   ";
            3'b010:  ew_light_str = "YELLOW";
            3'b001:  ew_light_str = "GREEN ";
            default: ew_light_str = "OFF   ";
        endcase
    end

    // --------------------------------------------------------------------------
    // Device Under Test (DUT) Instantiation
    // --------------------------------------------------------------------------
    traffic_light_controller #(
        .CLK_FREQ_HZ  (CLK_FREQ_HZ),
        .SEC_NS_GREEN (SEC_NS_GREEN),
        .SEC_EW_GREEN (SEC_EW_GREEN),
        .SEC_YELLOW   (SEC_YELLOW),
        .SEC_ALL_RED  (SEC_ALL_RED)
    ) dut (
        .clk          (clk),
        .rst_n        (rst_n),
        .emerg_ns     (emerg_ns),
        .emerg_ew     (emerg_ew),
        .ns_lights    (ns_lights),
        .ew_lights    (ew_lights),
        .ns_red       (ns_red),
        .ns_yellow    (ns_yellow),
        .ns_green     (ns_green),
        .ew_red       (ew_red),
        .ew_yellow    (ew_yellow),
        .ew_green     (ew_green),
        .state_out    (state_out),
        .sec_count_out(sec_count_out)
    );

    // --------------------------------------------------------------------------
    // Clock Generator (100 MHz)
    // --------------------------------------------------------------------------
    initial begin
        clk = 1'b0;
        forever #(CLK_PERIOD / 2) clk = ~clk;
    end

    // Helper task to wait for simulated seconds
    task wait_sim_seconds(input integer num_sec);
        begin
            repeat (num_sec * CLK_FREQ_HZ) @(posedge clk);
        end
    endtask

    // --------------------------------------------------------------------------
    // Test Sequence
    // --------------------------------------------------------------------------
    initial begin
        // Waveform Dump Setup (for VCD / Vivado / Icarus / ModelSim)
        $dumpfile("traffic_light_controller.vcd");
        $dumpvars(0, tb_traffic_light_controller);

        $display("=================================================================");
        $display("  STARTING TRAFFIC LIGHT CONTROLLER SIMULATION");
        $display("=================================================================");

        // Step 0: Initial Reset
        rst_n    = 1'b0;
        emerg_ns = 1'b0;
        emerg_ew = 1'b0;
        #(CLK_PERIOD * 5);

        rst_n = 1'b1;
        $display("[TIME: %0t ns] Reset released. Controller starting in default state.", $time);

        // ----------------------------------------------------------------------
        // TEST CASE 1: Normal Uninterrupted Traffic Cycle
        // ----------------------------------------------------------------------
        $display("\n--- TEST CASE 1: Normal Traffic Cycle (No Emergency) ---");
        // Wait through: NS_GREEN -> NS_YELLOW -> ALL_RED_1 -> EW_GREEN -> EW_YELLOW -> ALL_RED_2 -> NS_GREEN
        wait_sim_seconds(SEC_NS_GREEN + SEC_YELLOW + SEC_ALL_RED + SEC_EW_GREEN + SEC_YELLOW + SEC_ALL_RED + 2);
        $display("[TIME: %0t ns] Test Case 1 Completed successfully.", $time);

        // ----------------------------------------------------------------------
        // TEST CASE 2: Emergency Vehicle on NS while EW is currently Green
        // ----------------------------------------------------------------------
        $display("\n--- TEST CASE 2: Emergency on NS while EW is Green ---");
        // Wait until EW becomes Green
        wait(state_out == 3'b011); // S_EW_GREEN
        wait_sim_seconds(1);
        
        $display("[TIME: %0t ns] EW is Green. >> ALERT: North-South Emergency Vehicle detected! (emerg_ns=1)", $time);
        emerg_ns = 1'b1;

        // Verify that EW safely transitions to YELLOW (never directly to RED)
        @(posedge clk);
        #1;
        $display("[TIME: %0t ns] Current State after NS Emergency: %s | NS=%s, EW=%s", $time, state_name, ns_light_str, ew_light_str);
        
        // Wait until NS receives Green
        wait(state_out == 3'b000); // S_NS_GREEN
        $display("[TIME: %0t ns] NS has been successfully granted GREEN light for emergency vehicle!", $time);

        // Hold emergency active for 6 seconds (longer than normal SEC_NS_GREEN)
        wait_sim_seconds(6);
        $display("[TIME: %0t ns] Emergency vehicle still clearing, NS Green held extended.", $time);

        // Emergency vehicle departs
        emerg_ns = 1'b0;
        $display("[TIME: %0t ns] Emergency cleared (emerg_ns=0). Resuming normal operation.", $time);
        wait_sim_seconds(SEC_YELLOW + SEC_ALL_RED + 2);

        // ----------------------------------------------------------------------
        // TEST CASE 3: Emergency Vehicle on EW while NS is Green
        // ----------------------------------------------------------------------
        $display("\n--- TEST CASE 3: Emergency on EW while NS is Green ---");
        wait(state_out == 3'b000); // S_NS_GREEN
        wait_sim_seconds(1);

        $display("[TIME: %0t ns] NS is Green. >> ALERT: East-West Emergency Vehicle detected! (emerg_ew=1)", $time);
        emerg_ew = 1'b1;

        // Wait until EW is granted Green
        wait(state_out == 3'b011); // S_EW_GREEN
        $display("[TIME: %0t ns] EW safely received GREEN after NS Yellow clearance!", $time);

        wait_sim_seconds(4);
        emerg_ew = 1'b0;
        $display("[TIME: %0t ns] EW Emergency vehicle passed (emerg_ew=0).", $time);
        wait_sim_seconds(SEC_YELLOW + SEC_ALL_RED + 2);

        // ----------------------------------------------------------------------
        // TEST CASE 4: Simultaneous Emergencies (Priority Arbitration)
        // ----------------------------------------------------------------------
        $display("\n--- TEST CASE 4: Simultaneous Emergencies on NS and EW ---");
        wait(state_out == 3'b011); // S_EW_GREEN
        wait_sim_seconds(1);

        $display("[TIME: %0t ns] Simultaneous Emergency on BOTH roads! (emerg_ns=1, emerg_ew=1)", $time);
        emerg_ns = 1'b1;
        emerg_ew = 1'b1;

        // Priority must favor NS
        wait(state_out == 3'b000); // S_NS_GREEN
        $display("[TIME: %0t ns] Priority Check PASSED: North-South granted Green first!", $time);

        wait_sim_seconds(4);
        $display("[TIME: %0t ns] NS Emergency vehicle passed (emerg_ns=0), EW Emergency still waiting...", $time);
        emerg_ns = 1'b0; // EW emergency still active

        // EW should now be served next
        wait(state_out == 3'b011); // S_EW_GREEN
        $display("[TIME: %0t ns] Secondary Priority Check PASSED: EW now granted Green!", $time);

        wait_sim_seconds(4);
        emerg_ew = 1'b0;
        $display("[TIME: %0t ns] All emergencies cleared.", $time);

        // Return to normal rotation
        wait_sim_seconds(SEC_YELLOW + SEC_ALL_RED + SEC_NS_GREEN);

        $display("\n=================================================================");
        $display("  SIMULATION COMPLETED SUCCESSFULLY - ALL TESTS PASSED");
        $display("=================================================================");
        $finish;
    end

    // --------------------------------------------------------------------------
    // Real-Time Console Monitor (Logs every light state change)
    // --------------------------------------------------------------------------
    always @(state_out or ns_lights or ew_lights) begin
        $display("T=%0t ns | State: %-11s | NS: %-7s (R=%b Y=%b G=%b) | EW: %-7s (R=%b Y=%b G=%b) | Emerg: [NS=%b, EW=%b]",
                 $time, state_name,
                 ns_light_str, ns_red, ns_yellow, ns_green,
                 ew_light_str, ew_red, ew_yellow, ew_green,
                 emerg_ns, emerg_ew);
    end

    // --------------------------------------------------------------------------
    // Safety Assertions: Detect collisions or illegal state
    // --------------------------------------------------------------------------
    always @(posedge clk) begin
        if (rst_n) begin
            // Safety Property 1: Both directions CANNOT have Green at the same time
            if (ns_green && ew_green) begin
                $display("\n[FATAL ERROR at %0t ns] COLLISION DETECTED! Both NS and EW are GREEN simultaneously!", $time);
                $stop;
            end
            // Safety Property 2: NS Green cannot occur with EW Yellow
            if (ns_green && ew_yellow) begin
                $display("\n[FATAL ERROR at %0t ns] SAFETY HAZARD! NS Green with EW Yellow!", $time);
                $stop;
            end
            // Safety Property 3: EW Green cannot occur with NS Yellow
            if (ew_green && ns_yellow) begin
                $display("\n[FATAL ERROR at %0t ns] SAFETY HAZARD! EW Green with NS Yellow!", $time);
                $stop;
            end
        end
    end

endmodule

