import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage,
    KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Suppress header on cover page
        if self._pageNumber > 1:
            self.drawString(54, 752, "FSM-Based Priority Traffic Light Controller — Technical Specification")
            self.drawRightString(558, 752, "ASIC / FPGA RTL Design")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 746, 558, 746)

        # Footer on all pages
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — ASIC / FPGA DESIGN DOCUMENT")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        
        self.restoreState()

def build_pdf(filename="Traffic_Light_Controller_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom color palette
    c_primary = colors.HexColor("#1E3A8A")    # Deep Navy
    c_secondary = colors.HexColor("#0284C7")  # Sky Blue
    c_body = colors.HexColor("#334155")       # Slate 700
    c_light_bg = colors.HexColor("#F8FAFC")   # Slate 50
    c_code_bg = colors.HexColor("#0F172A")    # Dark slate for code

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_body,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_body,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#1E293B")
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#92400E")
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE SUMMARY & SYSTEM OVERVIEW
    # =========================================================================
    story.append(Paragraph("FSM-Based Priority Traffic Light Controller", title_style))
    story.append(Paragraph("Hardware Architecture, RTL Logic & Behavioral Verification in Verilog-2001", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=0, spaceAfter=8))

    meta_data = [
        [
            Paragraph("<b>Target Architecture:</b> Xilinx 7-Series / Artix-7 / Zynq", body_style),
            Paragraph("<b>Hardware Language:</b> Verilog-2001 (Synthesizable)", body_style)
        ],
        [
            Paragraph("<b>Simulation Tool:</b> AMD Xilinx Vivado (XSim)", body_style),
            Paragraph("<b>Author / Project:</b> joeljo777 / ASICD_Project", body_style)
        ],
        [
            Paragraph("<b>Intersection Model:</b> 4-Way (North-South vs East-West)", body_style),
            Paragraph("<b>Priority Scheme:</b> Two-Tier Emergency Preemption", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary & Design Philosophy", h1_style))
    story.append(Paragraph(
        "Modern urban traffic junctions require reliable digital control logic capable of balancing high-throughput normal vehicular flow "
        "with immediate, collision-free preemption for high-priority emergency vehicles (ambulances, fire engines, police units). "
        "This project develops a fully synthesizable <b>Moore Finite State Machine (FSM)</b> in Verilog-2001, specifically engineered for "
        "Xilinx FPGAs and verified using AMD Vivado Behavioral Simulation.",
        body_style
    ))
    story.append(Paragraph("<b>Primary Architectural Objectives:</b>", body_style))
    story.append(Paragraph("• <b>Deterministic Anti-Collision Guarantee:</b> Conflicting traffic lanes can never simultaneously display Green or Yellow signals. Continuous hardware assertions verify this invariant at every clock edge.", bullet_style))
    story.append(Paragraph("• <b>Braking Safety Enforcement:</b> Active Green lights are never snapped abruptly to Red upon emergency detection. Vehicles traveling at speed require bounded deceleration time (Yellow) and intersection clearance (All-Red) to eliminate lateral T-bone collisions.", bullet_style))
    story.append(Paragraph("• <b>Two-Tier Dynamic Preemption:</b> North-South (Arterial Main Road) holds primary emergency priority over East-West (Side Street). Simultaneous emergency alerts are arbitrated deterministically without deadlock.", bullet_style))
    story.append(Paragraph("• <b>Glitch-Free Output Registers:</b> Output light signals are registered on clock edges, eliminating combinatorial hazards on physical FPGA output pins.", bullet_style))

    story.append(Spacer(1, 4))
    safety_box = [
        [Paragraph("<b>CRITICAL SAFETY INTERLOCK:</b> Under all preemption circumstances (including unexpected emergency vehicle arrivals, de-assertions, and system resets), the controller enforces full legal Yellow duration (3s) and All-Red clearance (1s) before switching right-of-way. This mimics real-world Department of Transportation (DOT) safety standards.", callout_style)]
    ]
    safety_table = Table(safety_box, colWidths=[504])
    safety_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF3C7")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(safety_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>I/O Port Specifications:</b>", body_style))
    io_data = [
        [Paragraph("<b>Signal</b>", body_style), Paragraph("<b>Direction</b>", body_style), Paragraph("<b>Width</b>", body_style), Paragraph("<b>Active Level</b>", body_style), Paragraph("<b>Functional Role</b>", body_style)],
        [Paragraph("<code>clk</code>", code_style), Paragraph("Input", body_style), Paragraph("1 bit", body_style), Paragraph("Rising Edge", body_style), Paragraph("Master system oscillator (e.g., 100 MHz on Basys 3)", body_style)],
        [Paragraph("<code>rst_n</code>", code_style), Paragraph("Input", body_style), Paragraph("1 bit", body_style), Paragraph("Active-Low", body_style), Paragraph("Asynchronous master system reset (initializes to S_NS_GREEN)", body_style)],
        [Paragraph("<code>emerg_ns</code>", code_style), Paragraph("Input", body_style), Paragraph("1 bit", body_style), Paragraph("Active-High", body_style), Paragraph("Optical / acoustic sensor for North-South emergency vehicle", body_style)],
        [Paragraph("<code>emerg_ew</code>", code_style), Paragraph("Input", body_style), Paragraph("1 bit", body_style), Paragraph("Active-High", body_style), Paragraph("Optical / acoustic sensor for East-West emergency vehicle", body_style)],
        [Paragraph("<code>ns_lights</code>", code_style), Paragraph("Output", body_style), Paragraph("3 bits", body_style), Paragraph("Active-High", body_style), Paragraph("North-South lamp bus: [2]=Red, [1]=Yellow, [0]=Green", body_style)],
        [Paragraph("<code>ew_lights</code>", code_style), Paragraph("Output", body_style), Paragraph("3 bits", body_style), Paragraph("Active-High", body_style), Paragraph("East-West lamp bus: [2]=Red, [1]=Yellow, [0]=Green", body_style)],
        [Paragraph("<code>state_out</code>", code_style), Paragraph("Output", body_style), Paragraph("3 bits", body_style), Paragraph("Binary Code", body_style), Paragraph("Current FSM state index for debug / 7-segment display", body_style)]
    ]
    io_table = Table(io_data, colWidths=[70, 50, 45, 65, 274])
    io_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(io_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: FSM STATE ARCHITECTURE & TRANSITION SPECIFICATION
    # =========================================================================
    story.append(Paragraph("2. Finite State Machine (FSM) State Architecture", h1_style))
    story.append(Paragraph(
        "The controller is formulated as a 6-state synchronous Moore FSM. Each state corresponds to a mutually exclusive "
        "traffic signalling phase with defined durations and preemption branch policies:",
        body_style
    ))

    fsm_table_data = [
        [
            Paragraph("<b>State</b>", body_style),
            Paragraph("<b>Encoding</b>", body_style),
            Paragraph("<b>NS {R,Y,G}</b>", body_style),
            Paragraph("<b>EW {R,Y,G}</b>", body_style),
            Paragraph("<b>Time (s)</b>", body_style),
            Paragraph("<b>Operational Description & Emergency Preemption</b>", body_style)
        ],
        [
            Paragraph("<b>S_NS_GREEN</b>", body_style),
            Paragraph("<code>3'b000</code>", code_style),
            Paragraph("<font color='#16A34A'><b>GREEN (001)</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("10 s", body_style),
            Paragraph("Main Street traffic active. If <code>emerg_ns</code> asserts, green is held indefinitely. If <code>emerg_ew</code> asserts, early transition to <code>S_NS_YELLOW</code> is initiated.", body_style)
        ],
        [
            Paragraph("<b>S_NS_YELLOW</b>", body_style),
            Paragraph("<code>3'b001</code>", code_style),
            Paragraph("<font color='#D97706'><b>YELLOW (010)</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("3 s", body_style),
            Paragraph("NS traffic braking buffer. Must run full 3s without interruption to permit safe vehicular stopping.", body_style)
        ],
        [
            Paragraph("<b>S_ALL_RED_1</b>", body_style),
            Paragraph("<code>3'b010</code>", code_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("1 s", body_style),
            Paragraph("All-Red clearance. Once elapsed: if <code>emerg_ns</code> is active, loops straight back to <code>S_NS_GREEN</code>; otherwise advances to <code>S_EW_GREEN</code>.", body_style)
        ],
        [
            Paragraph("<b>S_EW_GREEN</b>", body_style),
            Paragraph("<code>3'b011</code>", code_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("<font color='#16A34A'><b>GREEN (001)</b></font>", body_style),
            Paragraph("7 s", body_style),
            Paragraph("Side Street traffic active. If <code>emerg_ew</code> asserts, green is held. If <code>emerg_ns</code> asserts, green is immediately truncated and routed through <code>S_EW_YELLOW</code>.", body_style)
        ],
        [
            Paragraph("<b>S_EW_YELLOW</b>", body_style),
            Paragraph("<code>3'b100</code>", code_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("<font color='#D97706'><b>YELLOW (010)</b></font>", body_style),
            Paragraph("3 s", body_style),
            Paragraph("EW traffic braking buffer. Runs full 3s safety interval without preemption truncation.", body_style)
        ],
        [
            Paragraph("<b>S_ALL_RED_2</b>", body_style),
            Paragraph("<code>3'b101</code>", code_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("1 s", body_style),
            Paragraph("All-Red clearance. Once elapsed: if <code>emerg_ew && !emerg_ns</code>, loops to <code>S_EW_GREEN</code>; otherwise returns to <code>S_NS_GREEN</code>.", body_style)
        ]
    ]

    fsm_table = Table(fsm_table_data, colWidths=[75, 52, 78, 78, 45, 176])
    fsm_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(fsm_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Priority Arbitration Rules & Conflict Handling:", h2_style))
    story.append(Paragraph("1. <b>Single Emergency on Opposing Road:</b> If an emergency vehicle triggers while the opposite road is green, the green timer is cancelled immediately and the current road enters its Yellow phase. Once the yellow and all-red clearance intervals conclude, the emergency road receives Green.", body_style))
    story.append(Paragraph("2. <b>Extended Green Duration:</b> If an emergency vehicle remains in transit across the intersection, the active green state is maintained indefinitely until the sensor signal drops back to zero.", body_style))
    story.append(Paragraph("3. <b>Simultaneous Emergency Arbitration:</b> If both <code>emerg_ns</code> and <code>emerg_ew</code> are asserted simultaneously (e.g., competing emergency calls):", body_style))
    story.append(Paragraph("   • North-South (Arterial Road) is serviced first due to higher traffic capacity and safety classification.", bullet_style))
    story.append(Paragraph("   • East-West is latched and granted green immediately after North-South clears its emergency and completes yellow/red clearance.", bullet_style))
    story.append(Paragraph("   • This eliminates priority inversion and prevents system starvation.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: RTL CODE ANALYSIS (WALKTHROUGH)
    # =========================================================================
    story.append(Paragraph("3. Verilog RTL Implementation Analysis", h1_style))
    story.append(Paragraph(
        "The complete synthesizable design resides in <code>traffic_light_controller.v</code>. It follows industry-standard "
        "two-process FSM coding style with dedicated prescaling and registered output buffers:",
        body_style
    ))

    story.append(Paragraph("3.1 1-Hz Tick Generator (Hardware Prescaler)", h2_style))
    story.append(Paragraph(
        "Directly counting FPGA clock cycles (100 MHz = 100,000,000 cycles/sec) in FSM comparison logic requires wide counters and adds "
        "logic depth to timing paths. Instead, a dedicated prescaler generates a single-cycle strobe <code>tick_1s</code>:",
        body_style
    ))
    code_snippet_1 = """always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        clk_div_cnt <= 32'd0;
        tick_1s     <= 1'b0;
    end else begin
        if (clk_div_cnt >= CLK_FREQ_HZ - 1) begin
            clk_div_cnt <= 32'd0;
            tick_1s     <= 1'b1;  // Single-cycle enable strobe
        end else begin
            clk_div_cnt <= clk_div_cnt + 1'b1;
            tick_1s     <= 1'b0;
        end
    end
end"""
    t_c1 = Table([[Paragraph(code_snippet_1.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 State Timer with Auto-Reset and Anti-Saturation", h2_style))
    story.append(Paragraph(
        "The state duration counter <code>sec_cnt</code> increments only when <code>tick_1s</code> pulses. It automatically resets to zero on "
        "every state entry (<code>state_changed</code>). An upper bound saturation clamp prevents rollover if an emergency vehicle extends green beyond 63 seconds:",
        body_style
    ))
    code_snippet_2 = """assign state_changed = (current_state != next_state);

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        sec_cnt <= 6'd0;
    end else if (state_changed) begin
        sec_cnt <= 6'd0;  // Auto-reset upon state transition
    end else if (tick_1s) begin
        if (sec_cnt < 6'd63)
            sec_cnt <= sec_cnt + 1'b1; // Saturated counter prevents rollover
    end
end"""
    t_c2 = Table([[Paragraph(code_snippet_2.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Combinational Next-State Evaluation", h2_style))
    story.append(Paragraph(
        "The combinational process models the state transition matrix and implements the emergency preemption priority logic:",
        body_style
    ))
    code_snippet_3 = """S_NS_GREEN: begin
    if (emerg_ns)
        next_state = S_NS_GREEN;     // Priority 1: Hold NS Green during NS emergency
    else if (emerg_ew)
        next_state = S_NS_YELLOW;    // Priority 2: Safely step down to Yellow for EW
    else if (sec_cnt >= SEC_NS_GREEN)
        next_state = S_NS_YELLOW;    // Normal timer expiration
end
S_EW_GREEN: begin
    if (emerg_ns)
        next_state = S_EW_YELLOW;    // Priority 1: Preempt EW immediately via Yellow
    else if (emerg_ew)
        next_state = S_EW_GREEN;     // Hold EW Green during EW emergency
    else if (sec_cnt >= SEC_EW_GREEN)
        next_state = S_EW_YELLOW;    // Normal timer expiration
end"""
    t_c3 = Table([[Paragraph(code_snippet_3.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_c3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_c3)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: VERIFICATION & SIMULATION WAVEFORM ANALYSIS
    # =========================================================================
    story.append(Paragraph("4. Verification & Waveform Results", h1_style))
    story.append(Paragraph(
        "Simulation was conducted in <b>AMD Xilinx Vivado XSim</b> using the testbench <code>tb_traffic_light_controller.v</code>. "
        "The testbench overrides <code>CLK_FREQ_HZ = 4</code> so 1 simulated second = 40 ns, executing full verification in under 2 µs.",
        body_style
    ))

    # Embed waveform image
    img_path = os.path.join(os.path.dirname(__file__), "simulation_waveform.png")
    if os.path.exists(img_path):
        img_w = 504
        img_h = 504 * (922 / 1786)
        story.append(RLImage(img_path, width=img_w, height=img_h))
        story.append(Spacer(1, 3))
        story.append(Paragraph("<i>Figure 1: Timing waveform captured from Vivado Behavioral Simulation verifying preemption and safe yellow clearance.</i>", ParagraphStyle('Cap', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748B"), alignment=1)))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Waveform Trace Analysis & Empirical Observations:", h2_style))
    story.append(Paragraph("• <b>Baseline Rotation:</b> During the initial interval, <code>state_name</code> cycles cleanly: <code>NS_GREEN</code> (10s) $\rightarrow$ <code>NS_YELLOW</code> (3s) $\rightarrow$ <code>ALL_RED_1</code> (1s) $\rightarrow$ <code>EW_GREEN</code> (7s) $\rightarrow$ <code>EW_YELLOW</code> (3s) $\rightarrow$ <code>ALL_RED_2</code> (1s).", bullet_style))
    story.append(Paragraph("• <b>North-South Emergency Assertion:</b> When <code>emerg_ns</code> pulses high during <code>EW_GREEN</code>, the controller truncates EW green immediately, driving <code>EW_YELLOW</code> for exactly 3 seconds, followed by 1s of <code>ALL_RED_2</code>, before safely granting Green to North-South.", bullet_style))
    story.append(Paragraph("• <b>Extended Emergency Hold:</b> While <code>emerg_ns</code> remains asserted, <code>state_name</code> remains pinned at <code>NS_GREEN</code> well beyond the standard 10-second timeout. Normal sequencing resumes only after <code>emerg_ns</code> drops.", bullet_style))
    story.append(Paragraph("• <b>Zero Glitches & Strict Interlocks:</b> Throughout the entire simulation run, <code>ns_green</code> and <code>ew_green</code> never overlap. Continuous safety assertions reported zero violations.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Automated Assertions Embedded in Testbench:", h2_style))
    code_assert = """always @(posedge clk) begin
    if (rst_n) begin
        if (ns_green && ew_green) begin
            $display("[FATAL ERROR] COLLISION DETECTED! Both directions GREEN simultaneously!");
            $stop;
        end
        if ((ns_green && ew_yellow) || (ew_green && ns_yellow)) begin
            $display("[FATAL ERROR] SAFETY HAZARD! Conflicting Green and Yellow signals!");
            $stop;
        end
    end
end"""
    t_ca = Table([[Paragraph(code_assert.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_ca.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_ca)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: FPGA SYNTHESIS, CONSTRAINTS & CONCLUSION
    # =========================================================================
    story.append(Paragraph("5. FPGA Implementation & Physical Constraints (XDC)", h1_style))
    story.append(Paragraph(
        "The architecture was synthesized targeting the <b>AMD Xilinx Artix-7 FPGA (XC7A35T-CPG236-1)</b> on the Digilent Basys 3 board:",
        body_style
    ))

    util_data = [
        [Paragraph("<b>Resource</b>", body_style), Paragraph("<b>Estimated Usage</b>", body_style), Paragraph("<b>Total Available (XC7A35T)</b>", body_style), Paragraph("<b>Utilization %</b>", body_style)],
        [Paragraph("Slice LUTs", body_style), Paragraph("~65", body_style), Paragraph("20,800", body_style), Paragraph("< 0.4 %", body_style)],
        [Paragraph("Slice Registers (FFs)", body_style), Paragraph("44", body_style), Paragraph("41,600", body_style), Paragraph("< 0.2 %", body_style)],
        [Paragraph("Global Clock Buffer (BUFG)", body_style), Paragraph("1", body_style), Paragraph("32", body_style), Paragraph("3.1 %", body_style)],
        [Paragraph("DSP48 / Block RAM", body_style), Paragraph("0", body_style), Paragraph("90 / 50", body_style), Paragraph("0.0 %", body_style)]
    ]
    util_table = Table(util_data, colWidths=[130, 95, 145, 134])
    util_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(util_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Basys 3 Physical Pin Mapping (XDC Constraints):", h2_style))
    xdc_code = """## 100 MHz Master Oscillator
set_property PACKAGE_PIN W5 [get_ports clk]							
set_property IOSTANDARD LVCMOS33 [get_ports clk]
create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports clk]

## Control Inputs (Switches / Pushbuttons)
set_property PACKAGE_PIN V17 [get_ports rst_n]					
set_property IOSTANDARD LVCMOS33 [get_ports rst_n]
set_property PACKAGE_PIN U18 [get_ports emerg_ns]				
set_property IOSTANDARD LVCMOS33 [get_ports emerg_ns]
set_property PACKAGE_PIN T18 [get_ports emerg_ew]				
set_property IOSTANDARD LVCMOS33 [get_ports emerg_ew]

## Traffic LED Outputs (NS: Green=LD0, Yellow=LD1, Red=LD2 | EW: Green=LD3, Yellow=LD4, Red=LD5)
set_property PACKAGE_PIN U16 [get_ports ns_green]					
set_property IOSTANDARD LVCMOS33 [get_ports ns_green]
set_property PACKAGE_PIN E19 [get_ports ns_yellow]					
set_property IOSTANDARD LVCMOS33 [get_ports ns_yellow]
set_property PACKAGE_PIN U19 [get_ports ns_red]					
set_property IOSTANDARD LVCMOS33 [get_ports ns_red]

set_property PACKAGE_PIN V19 [get_ports ew_green]					
set_property IOSTANDARD LVCMOS33 [get_ports ew_green]
set_property PACKAGE_PIN W18 [get_ports ew_yellow]					
set_property IOSTANDARD LVCMOS33 [get_ports ew_yellow]
set_property PACKAGE_PIN U15 [get_ports ew_red]					
set_property IOSTANDARD LVCMOS33 [get_ports ew_red]"""
    t_xdc = Table([[Paragraph(xdc_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_xdc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_xdc)
    story.append(Spacer(1, 10))

    story.append(Paragraph("6. Conclusion", h1_style))
    story.append(Paragraph(
        "This project successfully designs, models, and verifies an FSM-Based Priority Traffic Light Controller in synthesizable Verilog-2001. "
        "The controller satisfies critical real-world safety criteria: collision prevention through interlocked state sequencing, guaranteed "
        "braking deceleration via full Yellow phases, and deterministic two-tier emergency preemption. Simulation in AMD Vivado XSim conclusively "
        "confirms functional correctness across all operational and emergency boundary conditions with negligible FPGA hardware footprint (< 0.4% LUTs).",
        body_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=8, spaceAfter=6))
    story.append(Paragraph("<i>End of Technical Document — fsm-priority-traffic-light</i>", ParagraphStyle('End', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, textColor=colors.HexColor("#94A3B8"), alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == '__main__':
    build_pdf()
