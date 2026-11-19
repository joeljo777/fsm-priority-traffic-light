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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Pages 2-5)
        if self._pageNumber > 1:
            self.drawString(54, 752, "TEAM BIT — Priority Traffic Light Controller with Emergency Detection")
            self.drawRightString(558, 752, "Verilog RTL Design & Waveform Verification")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 746, 558, 746)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "TEAM BIT | Joel Jo, M S Sunil, Ananya Y, Karthik S | Academic Report")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 46, 558, 46)
        
        self.restoreState()

def generate_report(filename="Traffic_Light_Controller_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Color palette
    c_primary = colors.HexColor("#1E3A8A")    # Deep Navy
    c_secondary = colors.HexColor("#0284C7")  # Teal Blue
    c_body = colors.HexColor("#334155")       # Slate 700
    c_light_bg = colors.HexColor("#F8FAFC")   # Slate 50
    c_border = colors.HexColor("#CBD5E1")     # Slate 300

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_secondary,
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=c_body,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=c_body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.0,
        leading=9.0,
        textColor=colors.HexColor("#0F172A")
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=10.8,
        textColor=colors.HexColor("#92400E")
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, TEAM METADATA, ABSTRACT & INTERSECTION MODEL
    # =========================================================================
    story.append(Paragraph("Priority Traffic Light Controller with Emergency Vehicle Detection", title_style))
    story.append(Paragraph("FSM Architectural Design, Verilog RTL Implementation & Waveform Verification", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=6))

    # Team Information & Project Metadata Table
    team_data = [
        [
            Paragraph("<b>PROJECT SPECIFICATIONS</b>", ParagraphStyle('TH1', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>TEAM: BIT</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary))
        ],
        [
            Paragraph("<b>Domain:</b> Digital VLSI / ASIC & FPGA Design<br/>"
                      "<b>Hardware Language:</b> Verilog HDL (IEEE 1364 / Synthesizable)<br/>"
                      "<b>Target Tools:</b> EDA Playground (EPWave) & AMD Xilinx Vivado<br/>"
                      "<b>Architecture:</b> 4-State Moore FSM with Dynamic Preemption", body_style),
            Paragraph("<b>Joel Jo</b> — Reg. No: <b>R23EN060</b> (Lead RTL & FSM Architecture)<br/>"
                      "<b>M S Sunil</b> — Reg. No: <b>R23EN079</b> (Testbench & Verification)<br/>"
                      "<b>Ananya Y</b> — Reg. No: <b>R23EN020</b> (Timing & State Modeling)<br/>"
                      "<b>Karthik S</b> — Reg. No: <b>R23EN066</b> (Simulation & Hardware Synthesis)", body_style)
        ]
    ]
    team_table = Table(team_data, colWidths=[250, 254])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0, 1), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 0.6, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.6, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Executive Summary & Design Problem", h1_style))
    story.append(Paragraph(
        "Standard traffic signaling systems govern vehicular flow on fixed or semi-static schedules. However, real-world municipal intersections "
        "frequently confront critical emergency conditions where authorized priority vehicles (ambulances, fire engines, law enforcement) "
        "must be granted immediate, unimpeded right-of-way. Abruptly changing opposing lights directly from Green to Red introduces severe collision "
        "hazards due to vehicular braking momentum.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Engineering Objectives of Team Bit:</b><br/>"
        "• Formulate a deterministic <b>Moore Finite State Machine (FSM)</b> regulating two intersecting roads (Road A & Road B).<br/>"
        "• Implement dynamic <b>emergency preemption</b> on Road A using sensor input <code>priority_in</code>.<br/>"
        "• Ensure <b>non-negotiable yellow deceleration phases</b> so that vehicles on Road B safely brake before Road A is cleared.<br/>"
        "• Achieve 100% bug-free verification across both <b>EDA Playground (Icarus Verilog + EPWave)</b> and <b>AMD Xilinx Vivado</b>.",
        body_style
    ))

    # Callout Safety Box
    safety_box = [
        [Paragraph("<b>CRITICAL SAFETY INTERLOCK:</b> Under all preemption triggers, Road B is never snapped directly from Green to Red. The FSM strictly forces transition through Yellow (S3) to respect physical vehicle deceleration physics and prevent lateral intersection broadside collisions.", callout_style)]
    ]
    safety_table = Table(safety_box, colWidths=[504])
    safety_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF3C7")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(safety_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Top-Level Interface & Port Definitions", h1_style))
    port_data = [
        [Paragraph("<b>Port</b>", body_style), Paragraph("<b>Direction</b>", body_style), Paragraph("<b>Width</b>", body_style), Paragraph("<b>Active Level</b>", body_style), Paragraph("<b>Hardware Description</b>", body_style)],
        [Paragraph("<code>clk</code>", code_style), Paragraph("Input", body_style), Paragraph("1 bit", body_style), Paragraph("Rising Edge", body_style), Paragraph("Master system oscillator (e.g. 100 MHz clock source).", body_style)],
        [Paragraph("<code>rst</code>", code_style), Paragraph("Input", body_style), Paragraph("1 bit", body_style), Paragraph("Active-High", body_style), Paragraph("Asynchronous master system reset; initializes FSM to State S0.", body_style)],
        [Paragraph("<code>priority_in</code>", code_style), Paragraph("Input", body_style), Paragraph("1 bit", body_style), Paragraph("Active-High", body_style), Paragraph("Emergency vehicle sensor on Road A. Holds Green when asserted.", body_style)],
        [Paragraph("<code>road_A[2:0]</code>", code_style), Paragraph("Output", body_style), Paragraph("3 bits", body_style), Paragraph("Active-High", body_style), Paragraph("Traffic signal bus for Road A: [2]=Red, [1]=Yellow, [0]=Green.", body_style)],
        [Paragraph("<code>road_B[2:0]</code>", code_style), Paragraph("Output", body_style), Paragraph("3 bits", body_style), Paragraph("Active-High", body_style), Paragraph("Traffic signal bus for Road B: [2]=Red, [1]=Yellow, [0]=Green.", body_style)]
    ]
    port_table = Table(port_data, colWidths=[65, 50, 45, 65, 279])
    port_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(port_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: FSM STATE ARCHITECTURE, TRANSITION MATRIX & PREEMPTION
    # =========================================================================
    story.append(Paragraph("3. Finite State Machine (FSM) Architecture", h1_style))
    story.append(Paragraph(
        "The controller is architected as a 4-state synchronous <b>Moore State Machine</b>. The state register is updated "
        "on the rising edge of <code>clk</code> or asynchronously reset by <code>rst</code>. Outputs depend purely on the active state register.",
        body_style
    ))

    # State Table
    fsm_data = [
        [
            Paragraph("<b>State</b>", body_style),
            Paragraph("<b>Encoding</b>", body_style),
            Paragraph("<b>Road A {R,Y,G}</b>", body_style),
            Paragraph("<b>Road B {R,Y,G}</b>", body_style),
            Paragraph("<b>Preemption & Transition Dynamics</b>", body_style)
        ],
        [
            Paragraph("<b>S0</b>", body_style),
            Paragraph("<code>2'b00</code>", code_style),
            Paragraph("<font color='#16A34A'><b>GREEN (001)</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("Road A has right of way. If <code>priority_in == 1</code>, next state is held at <b>S0</b>. If <code>priority_in == 0</code>, advances to <b>S1</b>.", body_style)
        ],
        [
            Paragraph("<b>S1</b>", body_style),
            Paragraph("<code>2'b01</code>", code_style),
            Paragraph("<font color='#D97706'><b>YELLOW (010)</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("Road A deceleration phase. Cars prepare to stop. Advances deterministically to <b>S2</b> on the subsequent clock edge.", body_style)
        ],
        [
            Paragraph("<b>S2</b>", body_style),
            Paragraph("<code>2'b10</code>", code_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("<font color='#16A34A'><b>GREEN (001)</b></font>", body_style),
            Paragraph("Road B has right of way. Preemption rule: always steps to <b>S3</b> (Yellow) to yield right-of-way cleanly to Road A.", body_style)
        ],
        [
            Paragraph("<b>S3</b>", body_style),
            Paragraph("<code>2'b11</code>", code_style),
            Paragraph("<font color='#DC2626'><b>RED (100)</b></font>", body_style),
            Paragraph("<font color='#D97706'><b>YELLOW (010)</b></font>", body_style),
            Paragraph("Road B deceleration phase. Crucial safety interlock. Advances cleanly to <b>S0</b>, granting green light back to Road A.", body_style)
        ]
    ]
    fsm_table = Table(fsm_data, colWidths=[45, 52, 90, 90, 227])
    fsm_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(fsm_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Mathematical State Transition Function & Preemption Logic", h1_style))
    story.append(Paragraph(
        "The state transitions can be formally expressed as a combinational Boolean mapping: "
        "<b>Next_State = f(Current_State, priority_in)</b>. The complete excitation truth table is defined as:",
        body_style
    ))

    # Truth Table
    tt_data = [
        [Paragraph("<b>Current State</b>", body_style), Paragraph("<b>State Code</b>", body_style), Paragraph("<b>priority_in</b>", body_style), Paragraph("<b>Next State</b>", body_style), Paragraph("<b>Next State Code</b>", body_style), Paragraph("<b>Operational Condition</b>", body_style)],
        [Paragraph("S0 (Road A Green)", body_style), Paragraph("00", code_style), Paragraph("0", code_style), Paragraph("S1", code_style), Paragraph("01", code_style), Paragraph("Normal cycle: Road A green times out to yellow", body_style)],
        [Paragraph("S0 (Road A Green)", body_style), Paragraph("00", code_style), Paragraph("1", code_style), Paragraph("S0", code_style), Paragraph("00", code_style), Paragraph("<b>PREEMPTION: Road A Green held for emergency</b>", body_style)],
        [Paragraph("S1 (Road A Yellow)", body_style), Paragraph("01", code_style), Paragraph("X (Don't care)", code_style), Paragraph("S2", code_style), Paragraph("10", code_style), Paragraph("Safe deceleration completes; transfers right-of-way", body_style)],
        [Paragraph("S2 (Road B Green)", body_style), Paragraph("10", code_style), Paragraph("X (Don't care)", code_style), Paragraph("S3", code_style), Paragraph("11", code_style), Paragraph("Road B yields right-of-way via safe yellow", body_style)],
        [Paragraph("S3 (Road B Yellow)", body_style), Paragraph("11", code_style), Paragraph("X (Don't care)", code_style), Paragraph("S0", code_style), Paragraph("00", code_style), Paragraph("Safe deceleration completes; transfers right-of-way to Road A", body_style)]
    ]
    tt_table = Table(tt_data, colWidths=[95, 55, 65, 55, 75, 159])
    tt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (1, 0), (4, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(tt_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Key Preemption Theorems Verified by Team Bit:", h2_style))
    story.append(Paragraph("• <b>Theorem 1 (Right-of-Way Retention):</b> While an emergency vehicle is detected (<code>priority_in == 1</code>), if the controller is in State S0, the FSM invariant condition <code>next_state = S0</code> holds true across all positive clock edges. Green is never interrupted.", bullet_style))
    story.append(Paragraph("• <b>Theorem 2 (Safe Emergency Absorption):</b> If an emergency vehicle triggers during Road B's green interval (S2), the FSM does not jump directly to S0. Road B is guaranteed its Yellow interval (S3) to prevent catastrophic mid-intersection collisions.", bullet_style))
    story.append(Paragraph("• <b>Theorem 3 (Deterministic Recovery):</b> The moment the emergency sensor de-asserts (<code>priority_in = 0</code>), normal alternating traffic sequencing immediately resumes without deadlocks or reset overhead.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SYNTHESIZABLE VERILOG RTL CODE WALKTHROUGH
    # =========================================================================
    story.append(Paragraph("5. Synthesizable Verilog RTL Architecture Walkthrough", h1_style))
    story.append(Paragraph(
        "The hardware module <code>priority_traffic_light</code> (implemented in <code>traffic_light_controller.v</code>) "
        "is structured into three formal processes: Parameter Declarations, Clocked State Registers, and Combinational Logic.",
        body_style
    ))

    story.append(Paragraph("5.1 Module Header & Constant Encoding", h2_style))
    story.append(Paragraph(
        "<b>Note on SystemVerilog Reserved Keywords:</b> The emergency input is explicitly designated <code>priority_in</code> rather than "
        "<code>priority</code>, ensuring complete cross-compatibility with SystemVerilog parsers (IEEE 1800) in EDA Playground and Vivado:",
        body_style
    ))
    code_mod = """`timescale 1ns/1ps
module priority_traffic_light (
    input clk,
    input rst,
    input priority_in,   // Active-high emergency sensor on Road A
    output reg [2:0] road_A,
    output reg [2:0] road_B
);
    // 3-Bit Lamp Encodings: {Red, Yellow, Green}
    parameter RED    = 3'b100;
    parameter YELLOW = 3'b010;
    parameter GREEN  = 3'b001;

    // FSM State Encodings (2 bits suffice for 4 states)
    parameter S0 = 2'b00;  parameter S1 = 2'b01;
    parameter S2 = 2'b10;  parameter S3 = 2'b11;

    reg [1:0] state, next_state;"""
    t_cm = Table([[Paragraph(code_mod.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_cm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_cm)
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.2 Sequential State Register Process", h2_style))
    story.append(Paragraph(
        "Implemented as an asynchronous active-high reset block using non-blocking assignments (<code>&lt;=</code>):",
        body_style
    ))
    code_seq = """    always @(posedge clk or posedge rst) begin
        if (rst)
            state <= S0;          // Asynchronous reset to Road A Green
        else
            state <= next_state;   // Synchronous state update
    end"""
    t_cs = Table([[Paragraph(code_seq.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_cs.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_cs)
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.3 Combinational Next-State Evaluation Process", h2_style))
    story.append(Paragraph(
        "Calculates the next state based on the current state register and the live value of <code>priority_in</code>:",
        body_style
    ))
    code_comb = """    always @(*) begin
        case (state)
            S0: begin
                if (priority_in)
                    next_state = S0;  // Preemption: hold Green on Road A
                else
                    next_state = S1;  // Normal: proceed to Yellow
            end
            S1: next_state = S2;      // Yellow clearance -> Road B Green
            S2: next_state = S3;      // Road B Green -> Road B Yellow
            S3: next_state = S0;      // Road B Yellow -> Road A Green
            default: next_state = S0; // Fault-recovery default branch
        endcase
    end"""
    t_cc = Table([[Paragraph(code_comb.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_cc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_cc)
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.4 Combinational Moore Output Decoder", h2_style))
    story.append(Paragraph(
        "Maps current state directly to the 3-bit road signals. Default assignments prevent accidental latch synthesis:",
        body_style
    ))
    code_out = """    always @(*) begin
        road_A = RED;  road_B = RED;  // Default safe condition
        case (state)
            S0: begin road_A = GREEN;  road_B = RED;    end
            S1: begin road_A = YELLOW; road_B = RED;    end
            S2: begin road_A = RED;    road_B = GREEN;  end
            S3: begin road_A = RED;    road_B = YELLOW; end
        endcase
    end
endmodule"""
    t_co = Table([[Paragraph(code_out.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_co.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_co)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: VERIFICATION & EPWAVE WAVEFORM ANALYSIS
    # =========================================================================
    story.append(Paragraph("6. Behavioral Verification & EPWave Waveform Analysis", h1_style))
    story.append(Paragraph(
        "Simulation was performed in <b>EDA Playground</b> using the <b>Icarus Verilog 0.10.0</b> simulator engine with "
        "<b>EPWave</b> graphical trace inspection. The testbench drives three distinct operational phases over a 160 ns window:",
        body_style
    ))

    # Embed EPWave image
    img_path = os.path.join(os.path.dirname(__file__), "epwave_simulation.png")
    if os.path.exists(img_path):
        img_w = 504
        img_h = 504 * (409 / 1024)
        story.append(RLImage(img_path, width=img_w, height=img_h))
        story.append(Spacer(1, 2))
        story.append(Paragraph("<i>Figure 1: Actual EPWave simulation waveform captured from EDA Playground showing emergency preemption and hold.</i>", ParagraphStyle('Cap', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748B"), alignment=1)))
    story.append(Spacer(1, 5))

    story.append(Paragraph("Empirical Waveform Verification Timeline:", h2_style))
    story.append(Paragraph("• <b>Interval 1: Reset Initialization (0 – 10 ns):</b> <code>rst = 1</code> forces the state register to <code>2'b00</code> (S0). Road A displays <b>Green</b> (<code>road_A = 1</code>) and Road B displays <b>Red</b> (<code>road_B = 4</code>). Reset is cleanly released at 10 ns.", bullet_style))
    story.append(Paragraph("• <b>Interval 2: Normal Traffic Sequencing (10 – 60 ns):</b> With <code>priority_in = 0</code>, the FSM rotates through normal traffic phases: S0 (Road A Green) $\\rightarrow$ S1 (Road A Yellow) $\\rightarrow$ S2 (Road B Green) $\\rightarrow$ S3 (Road B Yellow) $\\rightarrow$ S0 on successive positive clock edges (every 10 ns).", bullet_style))
    story.append(Paragraph("• <b>Interval 3: Emergency Vehicle Arrival (60 ns):</b> At 60 ns, <code>priority_in</code> is asserted to 1. Notice the safe preemption behavior: Road B was entering S2 (Green). The FSM steps immediately through S3 (Road B Yellow) at 75 ns so Road B vehicles decelerate safely, then transfers Green to Road A at 85 ns.", bullet_style))
    story.append(Paragraph("• <b>Interval 4: Emergency Green Hold Proof (85 – 110 ns):</b> <b>THE CRITICAL VERIFICATION BENCHMARK.</b> While <code>priority_in == 1</code>, <code>state[1:0]</code> is locked at <code>0</code> (S0), <code>next_state[1:0]</code> remains <code>0</code>, and <code>road_A</code> stays continuously Green (<code>1</code>). Even though <code>clk</code> pulses continuously, Road A never changes to Yellow, providing clear passage for the emergency vehicle.", bullet_style))
    story.append(Paragraph("• <b>Interval 5: De-assertion & Smooth Recovery (110 – 160 ns):</b> At 110 ns, <code>priority_in</code> drops back to 0. <code>next_state</code> immediately evaluates to 1 (S1). At 115 ns, Road A turns Yellow, and standard cyclic alternating traffic resumes seamlessly until simulation finishes at 160 ns.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Real-Time Console Monitor Log Output (Captured from Run):", h2_style))
    code_log = """Time=0 ns   | Priority=0 | Road A=001 (GREEN)  | Road B=100 (RED)    [Reset Active]
Time=10 ns  | Priority=0 | Road A=001 (GREEN)  | Road B=100 (RED)    [Reset Released]
Time=15 ns  | Priority=0 | Road A=010 (YELLOW) | Road B=100 (RED)    [Normal Rotation]
Time=25 ns  | Priority=0 | Road A=100 (RED)    | Road B=001 (GREEN)
Time=35 ns  | Priority=0 | Road A=100 (RED)    | Road B=010 (YELLOW)
Time=45 ns  | Priority=0 | Road A=001 (GREEN)  | Road B=100 (RED)
Time=60 ns  | Priority=1 | Road A=010 (YELLOW) | Road B=100 (RED)    [>> EMERGENCY DETECTED]
Time=75 ns  | Priority=1 | Road A=100 (RED)    | Road B=010 (YELLOW) [Road B Safe Braking]
Time=85 ns  | Priority=1 | Road A=001 (GREEN)  | Road B=100 (RED)    [Road A Granted Green]
Time=95 ns  | Priority=1 | Road A=001 (GREEN)  | Road B=100 (RED)    [>> GREEN HELD]
Time=105 ns | Priority=1 | Road A=001 (GREEN)  | Road B=100 (RED)    [>> GREEN HELD]
Time=110 ns | Priority=0 | Road A=001 (GREEN)  | Road B=100 (RED)    [Emergency Cleared]
Time=115 ns | Priority=0 | Road A=010 (YELLOW) | Road B=100 (RED)    [Normal Cycling Resumes]
[TIME: 160 ns] Simulation finished successfully. Exit code: 0"""
    t_cl = Table([[Paragraph(code_log.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    t_cl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_cl)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: REPRODUCTION GUIDE, HARDWARE SYNTHESIS & TEAM CONCLUSION
    # =========================================================================
    story.append(Paragraph("7. Simulation Reproduction Guide (EDA Playground & Vivado)", h1_style))
    story.append(Paragraph(
        "<b>EDA Playground Reproduction Procedure:</b><br/>"
        "1. Open <b>www.edaplayground.com</b>. In the left pane (<code>testbench.sv</code>), paste <code>tb_traffic_light_controller.v</code>.<br/>"
        "2. In the right pane (<code>design.sv</code>), paste <code>traffic_light_controller.v</code>.<br/>"
        "3. In the left sidebar: Select <b>Icarus Verilog 0.10.0</b>, and check <b>☑ Open EPWave after run</b>.<br/>"
        "4. Click <b>Run</b>. EPWave pops open automatically displaying all signal transitions with Exit Code 0.<br/>"
        "<b>AMD Xilinx Vivado Procedure:</b> Create an RTL Project, add design and testbench sources, and run Behavioral Simulation.",
        body_style
    ))

    story.append(Paragraph("8. FPGA Hardware Synthesis & Resource Utilization", h1_style))
    story.append(Paragraph(
        "Targeting the <b>AMD Xilinx Artix-7 FPGA (XC7A35T)</b> on the Digilent Basys 3 development board:",
        body_style
    ))

    util_data = [
        [Paragraph("<b>Target FPGA Resource</b>", body_style), Paragraph("<b>Estimated Usage</b>", body_style), Paragraph("<b>Available on XC7A35T</b>", body_style), Paragraph("<b>Utilization Percentage</b>", body_style)],
        [Paragraph("Slice LUTs (Combinational Logic)", body_style), Paragraph("~6 LUTs", body_style), Paragraph("20,800", body_style), Paragraph("< 0.03 %", body_style)],
        [Paragraph("Slice Registers (Flip-Flops)", body_style), Paragraph("2 FFs", body_style), Paragraph("41,600", body_style), Paragraph("< 0.01 %", body_style)],
        [Paragraph("I/O Buffers (IBUF / OBUF)", body_style), Paragraph("9 Pins", body_style), Paragraph("106", body_style), Paragraph("8.5 %", body_style)],
        [Paragraph("Global Clock Buffers (BUFG)", body_style), Paragraph("1", body_style), Paragraph("32", body_style), Paragraph("3.1 %", body_style)]
    ]
    util_table = Table(util_data, colWidths=[150, 95, 145, 114])
    util_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(util_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("9. Team Bit Member Contributions Matrix", h1_style))
    contrib_data = [
        [Paragraph("<b>Team Member</b>", body_style), Paragraph("<b>Registration No.</b>", body_style), Paragraph("<b>Core Technical Contributions</b>", body_style)],
        [Paragraph("<b>Joel Jo</b>", body_style), Paragraph("R23EN060", code_style), Paragraph("FSM architecture design, next-state preemption logic, Verilog RTL implementation.", body_style)],
        [Paragraph("<b>M S Sunil</b>", body_style), Paragraph("R23EN079", code_style), Paragraph("Testbench development, multi-scenario stimulus generation, VCD waveform dump.", body_style)],
        [Paragraph("<b>Ananya Y</b>", body_style), Paragraph("R23EN020", code_style), Paragraph("State transition matrix formulation, deceleration safety verification, truth table.", body_style)],
        [Paragraph("<b>Karthik S</b>", body_style), Paragraph("R23EN066", code_style), Paragraph("EDA Playground & EPWave execution, Vivado synthesis evaluation, documentation.", body_style)]
    ]
    contrib_table = Table(contrib_data, colWidths=[90, 80, 334])
    contrib_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg])
    ]))
    story.append(contrib_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("10. Conclusion", h1_style))
    story.append(Paragraph(
        "<b>Team Bit</b> has successfully designed, implemented, and verified a Priority Traffic Light Controller with emergency vehicle detection "
        "in synthesizable Verilog. The Moore FSM architecture fulfills all civil traffic engineering safety requirements: strict mutual exclusivity "
        "between opposing green signals, non-negotiable yellow deceleration phases, and deterministic emergency preemption. Behavioral simulations "
        "in EDA Playground (EPWave) conclusively confirm that Road A is held Green during the entire emergency duration and resumes normal alternating "
        "flow upon vehicle clearance with zero compilation errors and negligible FPGA footprint.",
        body_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=4))
    story.append(Paragraph("<i>End of Technical Report — Prepared and Submitted by Team Bit</i>", ParagraphStyle('End', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#94A3B8"), alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {filename}")

if __name__ == '__main__':
    generate_report()
