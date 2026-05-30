from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime

# ─── Brand Colors ────────────────────────────────────────────────
PRIMARY      = colors.HexColor("#1A1A2E")   # deep navy
ACCENT       = colors.HexColor("#E94560")   # vibrant red-pink
LIGHT_BG     = colors.HexColor("#F5F7FA")   # very light grey
SECTION_LINE = colors.HexColor("#E94560")
BODY_TEXT    = colors.HexColor("#2D2D2D")
MUTED        = colors.HexColor("#6B7280")

# Section icon / emoji map (Unicode, safe in Helvetica)
SECTION_ICONS = {
    "market_research_tool":   "Market Research",
    "competitor_scan_tool":   "Competitor Analysis",
    "persona_builder_tool":   "Customer Personas",
    "pricing_analysis_tool":  "Pricing Strategy",
    "gtm_strategy_tool":      "Go-To-Market Strategy",
    "risk_analysis_tool":     "Risk Analysis",
}


def _build_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title",
        fontName="Helvetica-Bold",
        fontSize=32,
        textColor=colors.white,
        leading=38,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    styles["cover_sub"] = ParagraphStyle(
        "cover_sub",
        fontName="Helvetica",
        fontSize=13,
        textColor=colors.HexColor("#CBD5E1"),
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    styles["cover_idea_label"] = ParagraphStyle(
        "cover_idea_label",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=ACCENT,
        leading=14,
        alignment=TA_CENTER,
        spaceBefore=20,
    )
    styles["cover_idea"] = ParagraphStyle(
        "cover_idea",
        fontName="Helvetica-Oblique",
        fontSize=14,
        textColor=colors.white,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    styles["section_heading"] = ParagraphStyle(
        "section_heading",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=PRIMARY,
        leading=22,
        spaceBefore=8,
        spaceAfter=4,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=10,
        textColor=BODY_TEXT,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=10,
        textColor=BODY_TEXT,
        leading=15,
        leftIndent=14,
        spaceAfter=2,
        bulletIndent=4,
    )
    styles["footer"] = ParagraphStyle(
        "footer",
        fontName="Helvetica",
        fontSize=8,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
    return styles


def _cover_page(startup_idea, styles):
    """Returns a list of flowables for a full-color cover page."""
    elements = []

    # Dark banner table that acts as a full-width header block
    cover_data = [[
        Paragraph("Startup Intelligence Report", styles["cover_title"])
    ]]
    cover_table = Table(cover_data, colWidths=[170 * mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING",  (0, 0), (-1, -1), 30),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [6]),
    ]))
    elements.append(cover_table)
    elements.append(Spacer(1, 8 * mm))

    # Subtitle
    subtitle_style = ParagraphStyle(
        "sub2",
        fontName="Helvetica",
        fontSize=12,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    elements.append(Paragraph("AI-Powered Startup Analysis", subtitle_style))
    elements.append(Spacer(1, 4 * mm))

    # Accent rule
    elements.append(HRFlowable(
        width="100%", thickness=2, color=ACCENT,
        spaceAfter=6, spaceBefore=2
    ))

    # Startup idea box
    idea_label_style = ParagraphStyle(
        "idea_label",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=ACCENT,
        alignment=TA_LEFT,
        spaceBefore=6,
    )
    idea_style = ParagraphStyle(
        "idea_text",
        fontName="Helvetica-Oblique",
        fontSize=12,
        textColor=PRIMARY,
        leading=18,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    idea_data = [[
        [
            Paragraph("STARTUP IDEA", idea_label_style),
            Spacer(1, 3),
            Paragraph(startup_idea, idea_style),
        ]
    ]]
    idea_table = Table(idea_data, colWidths=[170 * mm])
    idea_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("LINEABOVE",     (0, 0), (-1, 0),  2, ACCENT),
        ("ROUNDEDCORNERS", [4]),
    ]))
    elements.append(idea_table)
    elements.append(Spacer(1, 6 * mm))

    # Date + generated-by line
    date_style = ParagraphStyle(
        "date_s",
        fontName="Helvetica",
        fontSize=9,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
    date_str = datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(
        f"Generated on {date_str} &nbsp;|&nbsp; Powered by Autonomous AI Agents",
        date_style
    ))
    elements.append(Spacer(1, 4 * mm))
    elements.append(HRFlowable(
        width="100%", thickness=1, color=colors.HexColor("#E2E8F0"),
        spaceAfter=4
    ))

    # Executive summary box
    exec_label = ParagraphStyle(
        "exec_label",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=ACCENT,
        spaceBefore=6,
        spaceAfter=3,
    )
    exec_body = ParagraphStyle(
        "exec_body",
        fontName="Helvetica",
        fontSize=10,
        textColor=BODY_TEXT,
        leading=15,
        alignment=TA_JUSTIFY,
    )
    exec_text = (
        "This report was generated using autonomous AI agents. It covers "
        "market research, competitor analysis, customer personas, pricing "
        "strategies, go-to-market planning, and risk analysis — giving you "
        "a comprehensive 360° view of your startup opportunity."
    )
    exec_data = [[
        [
            Paragraph("EXECUTIVE SUMMARY", exec_label),
            Paragraph(exec_text, exec_body),
        ]
    ]]
    exec_table = Table(exec_data, colWidths=[170 * mm])
    exec_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#EEF2FF")),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("LINEBEFORE",    (0, 0), (0, -1),  3, ACCENT),
    ]))
    elements.append(exec_table)

    elements.append(PageBreak())
    return elements


def _section(tool_name, output, styles):
    """Returns flowables for one research section."""
    elements = []

    display_name = SECTION_ICONS.get(tool_name, tool_name.replace("_", " ").title())
    summary_raw  = output.get("summary", "No summary available.")

    # Section heading
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(display_name, styles["section_heading"]))
    elements.append(HRFlowable(
        width="100%", thickness=1.5, color=ACCENT,
        spaceBefore=1, spaceAfter=6
    ))

    # Parse and render lines
    for line in summary_raw.splitlines():
        line = line.strip()
        if not line:
            elements.append(Spacer(1, 3))
            continue

        # Clean markdown bold markers
        line = line.replace("**", "")

        if line.startswith("* ") or line.startswith("- ") or line.startswith("+ "):
            bullet_text = "&#x2022;&nbsp;&nbsp;" + line[2:]
            elements.append(Paragraph(bullet_text, styles["bullet"]))
        elif line.endswith(":") and len(line) < 60:
            # Sub-heading inside section
            sub_style = ParagraphStyle(
                "sub_h",
                fontName="Helvetica-Bold",
                fontSize=10,
                textColor=PRIMARY,
                leading=14,
                spaceBefore=5,
                spaceAfter=2,
            )
            elements.append(Paragraph(line, sub_style))
        else:
            elements.append(Paragraph(line, styles["body"]))

    elements.append(Spacer(1, 6 * mm))
    return elements


def generate_report(state):
    filename = "startup_report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Startup Intelligence Report",
        author="Startup Intelligence Agent",
    )

    styles   = _build_styles()
    elements = []

    # ── Cover page ──────────────────────────────────────────
    elements += _cover_page(state["startup_idea"], styles)

    # ── Research sections ────────────────────────────────────
    for tool_name, output in state["tool_outputs"].items():
        elements += _section(tool_name, output, styles)

    # ── Footer note ──────────────────────────────────────────
    elements.append(HRFlowable(
        width="100%", thickness=1, color=colors.HexColor("#E2E8F0"),
        spaceBefore=10
    ))
    elements.append(Paragraph(
        "Generated by Startup Intelligence Agent &nbsp;|&nbsp; "
        "For informational purposes only.",
        styles["footer"]
    ))

    doc.build(elements)
    return filename