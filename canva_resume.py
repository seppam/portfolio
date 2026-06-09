"""
Build: Septian Canva Portfolio
  - onepager.pdf  (A4, single page, resume style)
  - multipage.pdf (16:9 landscape, 7 slides, deck style)
"""
import sys, os
sys.path.insert(0, "/Users/macbook/Library/Application Support/QClaw/openclaw/config/skills/pdf/scripts")
from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

# ──────────────────────────────────────────────────────────────
# DESIGN TOKENS (matching old Canva portfolio style)
# ──────────────────────────────────────────────────────────────
ACCENT    = HexColor("#2563EB")   # blue
DARK      = HexColor("#18181B")   # near-black
MID       = HexColor("#52525B")  # mid-grey
LIGHT     = HexColor("#A1A1AA")   # light-grey
BG        = HexColor("#FAFAFA")  # off-white
WHITE     = colors.white
ACCENT_LIGHT = HexColor("#EFF6FF")

W, H = A4   # 595 x 842 pt

# ──────────────────────────────────────────────────────────────
# SHARED: draw accent sidebar + header bar on every page
# ──────────────────────────────────────────────────────────────
def draw_page_chrome(c, page_width, page_height, accent_width=6*mm, header_height=18*mm):
    """Left sidebar accent bar + top header strip."""
    # Left accent bar
    c.setFillColor(ACCENT)
    c.rect(0, 0, accent_width, page_height, fill=1, stroke=0)
    # Top header strip
    c.setFillColor(ACCENT)
    c.rect(0, page_height - 3*mm, page_width, 3*mm, fill=1, stroke=0)
    # Thin grey bottom line
    c.setStrokeColor(HexColor("#E4E4E7"))
    c.setLineWidth(0.5)
    c.line(accent_width + 5*mm, 12*mm, page_width - 10*mm, 12*mm)

def draw_header_text(c, page_width, page_height, label, name="Muhamad Septian Pamungkas"):
    """Top-left: name. Top-right: section label."""
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(ACCENT)
    c.drawString(page_width - 80*mm, page_height - 7*mm, label.upper())
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(MID)
    c.drawString(accent_width + 5*mm, page_height - 7*mm, name)

# ──────────────────────────────────────────────────────────────
# HELPER: paragraph styles factory
# ──────────────────────────────────────────────────────────────
cn_font = None
_styles = None

def get_styles():
    global cn_font, _styles
    if _styles is None:
        cn_font, _styles = setup_chinese_pdf()
    return cn_font, _styles

def ps(name, parent_name="Normal", **kw):
    cn, sty = get_styles()
    parent = sty[parent_name]
    return ParagraphStyle(name, parent=parent, **kw)

# ──────────────────────────────────────────────────────────────
# BUILD: ONE-PAGER (A4, single page, resume style)
# ──────────────────────────────────────────────────────────────
def build_onepager():
    cn, sty = get_styles()
    out = os.path.join(os.path.dirname(__file__), "Septian_Resume_OnePager.pdf")
    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=22*mm,
        rightMargin=10*mm,
        topMargin=22*mm,
        bottomMargin=15*mm,
    )

    # Colours for ParagraphStyles
    sName    = ps("sName",    fontSize=20, fontName="Helvetica-Bold",
                   textColor=DARK, spaceAfter=2, leading=24)
    sTitle   = ps("sTitle",   fontSize=9,  textColor=ACCENT,
                   spaceAfter=4, leading=12)
    sSection = ps("sSection", fontSize=8,  fontName="Helvetica-Bold",
                   textColor=WHITE, spaceAfter=2, leading=11)
    sBody    = ps("sBody",    fontSize=8.5, textColor=DARK, leading=12, spaceAfter=2)
    sLight   = ps("sLight",   fontSize=7.5, textColor=MID, leading=11)
    sBold    = ps("sBold",    fontSize=8.5, fontName="Helvetica-Bold",
                   textColor=DARK, leading=12)

    def section_bar(title):
        """Blue rounded-rect bar for section headers."""
        tbl = Table([[Paragraph(title.upper(), sSection)]], colWidths=[W - 32*mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), ACCENT),
            ("TOPPADDING",   (0,0), (-1,-1), 3),
            ("BOTTOMPADDING",(0,0), (-1,-1), 3),
            ("LEFTPADDING",  (0,0), (-1,-1), 5),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), [3,3,3,3]),
        ]))
        return tbl

    story = []

    # ── HEADER ROW ──────────────────────────────────────────
    # Name + title block
    header_data = [[
        Paragraph("Muhamad Septian Pamungkas", sName),
        Paragraph(
            "Application Support &nbsp;|&nbsp; Full-Stack Developer &nbsp;|&nbsp; AI Enthusiast",
            sTitle
        )
    ]]
    header_tbl = Table(header_data, colWidths=[90*mm, 83*mm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
        ("ALIGN",  (1,0), (1,0), "RIGHT"),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 2*mm))

    # Contact strip
    contacts = (
        '<b>Email:</b> muhseptianp@outlook.com &nbsp;&nbsp; '
        '<b>LinkedIn:</b> linkedin.com/in/muh-septian-pamungkas/ &nbsp;&nbsp; '
        '<b>GitHub:</b> github.com/seppam &nbsp;&nbsp; '
        '<b>Location:</b> Karawang, Indonesia'
    )
    story.append(Paragraph(contacts, sLight))
    story.append(Spacer(1, 4*mm))

    # Divider
    story.append(Table([[""]], colWidths=[W-32*mm], rowHeights=[0.5],
                        style=TableStyle([
                            ("BACKGROUND",(0,0),(-1,-1), HexColor("#E4E4E7")),
                            ("TOPPADDING",(0,0),(-1,-1),0),
                            ("BOTTOMPADDING",(0,0),(-1,-1),0),
                        ])))
    story.append(Spacer(1, 3*mm))

    # ── TWO COLUMN LAYOUT ────────────────────────────────────
    # Left col: Summary + Experience | Right col: Skills + Education + Projects
    left_w  = 95*mm
    right_w = 80*mm
    gap     = 5*mm

    # ── LEFT COLUMN ──────────────────────────────────────────
    left_items = []

    left_items.append(section_bar("Summary"))
    left_items.append(Spacer(1, 2*mm))
    left_items.append(Paragraph(
        "Result-oriented IT professional with 3+ years of enterprise experience in application support and "
        "software development, maintaining a 95% SLA. Recently completed intensive international training in "
        "<b>Full-Stack Development (MERN/Next.js)</b>, <b>Cloud Computing</b>, and <b>AI Implementation</b>. "
        "Proven track record in aligning complex business requirements with technical solutions and "
        "data-driven system monitoring.",
        sBody
    ))
    left_items.append(Spacer(1, 4*mm))

    left_items.append(section_bar("Experience"))
    left_items.append(Spacer(1, 2*mm))

    def exp_block(role, company, period, bullets):
        items = [Paragraph(f'<b>{role}</b> &nbsp;<font color="#52525B">{company}</font> &nbsp;<font color="#A1A1AA">· {period}</font>', sBold)]
        for b in bullets:
            items.append(Paragraph(f'<bullet>•</bullet> {b}', sBody))
        items.append(Spacer(1, 2*mm))
        return items

    left_items += exp_block(
        "Fullstack Dev & AI Trainee",
        "Korea ASEAN Digital Academy (KADA)",
        "Feb – Apr 2026",
        [
            "Led technical development as PM & Lead Developer for VeriHire — AI platform for CV analysis & job scam detection",
            "Engineered scalable solutions using React, Redux Toolkit, Node.js; integrated cloud & AI infrastructure",
        ]
    )
    left_items += exp_block(
        "Professional Upskilling (Career Break)",
        "Remote / Karawang",
        "Jan 2024 – Jan 2026",
        [
            "Completed DevSecOps Engineer track (Studi DevSecOps); Data Science Bootcamp graduated 'Great Grade' 86/100",
            "Built Bank Sampah Digital Dashboard using Google Data Studio + Python automation",
        ]
    )
    left_items += exp_block(
        "IT Application Support",
        "Astra Graphia IT – Astra International",
        "Feb – Jul 2021",
        [
            "Maintained 95% SLA for user ticketing; optimised SAP system reliability via T-Code synchronisation",
            "Generated operational dashboards via MicroStrategy for data-driven leadership decisions",
        ]
    )
    left_items += exp_block(
        "Software Developer",
        "Astra Graphia IT – Astra International",
        "Jul 2018 – Feb 2021",
        [
            "Engineered enterprise-scale ASP.Net applications; handled 50+ projects (Sales, HR, Operations)",
            "Authored Business Process Documents and Technical System Designs (TSD)",
        ]
    )

    # ── RIGHT COLUMN ─────────────────────────────────────────
    right_items = []

    right_items.append(section_bar("Technical Skills"))
    right_items.append(Spacer(1, 2*mm))

    def skill_group(title, skills):
        return [
            Paragraph(f'<b>{title}</b>', ps("sg", fontSize=8, fontName="Helvetica-Bold",
                                            textColor=ACCENT, spaceAfter=1)),
            Paragraph(", ".join(skills), sBody),
            Spacer(1, 2*mm),
        ]

    right_items += skill_group("Frontend", ["React", "Next.js", "TypeScript", "Redux Toolkit", "Tailwind CSS"])
    right_items += skill_group("Backend",  ["Node.js", "Express", "MongoDB", "Prisma/SQLite", "REST API"])
    right_items += skill_group("Enterprise", ["SAP", "ASP.Net", "MS SQL Server", "MicroStrategy", "Jira"])
    right_items += skill_group("AI & Data", ["Gemini API", "GPT-5", "Python", "R", "Data Analysis"])
    right_items += skill_group("DevOps",  ["Docker", "AWS", "Git", "CI/CD"])

    right_items.append(Spacer(1, 1*mm))
    right_items.append(section_bar("Education"))
    right_items.append(Spacer(1, 2*mm))
    right_items.append(Paragraph("<b>Gunadarma University</b>", sBold))
    right_items.append(Paragraph("Bachelor of Information Systems (S.Kom) &nbsp;·&nbsp; GPA 3.78 / 4.00", sBody))
    right_items.append(Paragraph("2013 – 2017 &nbsp;·&nbsp; Depok, Indonesia", sLight))
    right_items.append(Spacer(1, 2*mm))
    right_items.append(Paragraph("<b>DevSecOps Engineer</b> — Studi DevSecOps", sBody))
    right_items.append(Paragraph("<b>Data Science Bootcamp</b> — Digital Skola (86/100, Great Grade)", sBody))
    right_items.append(Paragraph("<b>Full-Stack MERN/Next.js</b> — KADA International Residency", sBody))

    right_items.append(Spacer(1, 3*mm))
    right_items.append(section_bar("Featured Projects"))
    right_items.append(Spacer(1, 2*mm))

    def proj_block(name, desc, tech):
        return [
            Paragraph(f'<b>{name}</b>', sBold),
            Paragraph(desc, sBody),
            Paragraph(f'<i>{tech}</i>', sLight),
            Spacer(1, 2*mm),
        ]

    right_items += proj_block(
        "BisaFit.AI",
        "Premium AI fitness assistant with Navy BFP calculator, localised Indonesian nutrition engine & circadian scheduling.",
        "React · TypeScript · Vite · Gemini Pro · Tailwind CSS"
    )
    right_items += proj_block(
        "VeriHire Enhanced",
        "AI-powered CV analysis & job scam detection platform. PM & Lead Dev during KADA residency.",
        "React · Node.js · MongoDB · Gemini/GPT-5 · OCR"
    )
    right_items += proj_block(
        "Executive Ledger",
        "AI expense tracker with Gemini receipt scanning, budget alerts, PDF/CSV export.",
        "React 19 · Node.js · Prisma · SQLite"
    )

    # ── ASSEMBLE TWO COLUMN TABLE ────────────────────────────
    col_table = Table(
        [[left_items, right_items]],
        colWidths=[left_w, right_w],
        hAlign="LEFT"
    )
    col_table.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ]))
    story.append(col_table)

    doc.build(story)
    print(f"✅ One-pager saved: {out}")
    return out


# ──────────────────────────────────────────────────────────────
# BUILD: MULTI-PAGE SLIDE DECK (16:9 landscape)
# ──────────────────────────────────────────────────────────────

SW, SH = landscape(A4)   # 842 x 595 pt

def make_slide_bg(c, page_width, page_height, page_num, total_pages):
    """Dark bg + accent sidebar for multipage."""
    # Background
    c.setFillColor(HexColor("#0F172A"))
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    # Left accent bar
    c.setFillColor(ACCENT)
    c.rect(0, 0, 5*mm, page_height, fill=1, stroke=0)
    # Bottom watermark
    c.setFillColor(HexColor("#1E293B"))
    c.rect(0, 0, page_width, 10*mm, fill=1, stroke=0)
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor("#64748B"))
    c.drawString(page_width/2 - 15*mm, 3*mm, "Muhamad Septian Pamungkas  ·  Portfolio 2026")
    c.drawRightString(page_width - 8*mm, 3*mm, f"{page_num} / {total_pages}")


def draw_cover_slide(c, pw, ph):
    make_slide_bg(c, pw, ph, 1, 7)
    c.setFillColor(HexColor("#0F172A"))
    c.rect(0, 0, pw, ph, fill=1, stroke=0)
    # Accent left bar
    c.setFillColor(ACCENT)
    c.rect(0, 0, 5*mm, ph, fill=1, stroke=0)
    # Gradient glow
    c.setFillColor(HexColor("#1E3A5F"))
    c.setFillAlpha(0.5)
    c.circle(pw*0.85, ph*0.7, 120, fill=1, stroke=0)
    c.setFillAlpha(1.0)
    # Name
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(WHITE)
    c.drawString(18*mm, ph*0.55, "Muhamad Septian")
    c.drawString(18*mm, ph*0.45, "Pamungkas")
    # Accent line under name
    c.setFillColor(ACCENT)
    c.rect(18*mm, ph*0.42, 60*mm, 2, fill=1, stroke=0)
    # Title
    c.setFont("Helvetica", 13)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawString(18*mm, ph*0.36, "Application Support  |  Full-Stack Developer  |  AI Enthusiast")
    # Tags
    c.setFillColor(HexColor("#1E293B"))
    tags = ["MERN / Next.js", "React · TypeScript", "AI & Gemini", "Cloud & DevSecOps"]
    x = 18*mm
    for tag in tags:
        tw = len(tag)*3.2 + 8
        c.roundRect(x, ph*0.28, tw, 8*mm, 4, fill=1, stroke=0)
        c.setFont("Helvetica", 7)
        c.setFillColor(HexColor("#60A5FA"))
        c.drawString(x+4, ph*0.28+2*mm, tag)
        x += tw + 4
    # Contact
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#64748B"))
    c.drawString(18*mm, 14*mm, "muhseptianp@outlook.com  ·  github.com/seppam  ·  linkedin.com/in/muh-septian-pamungkas")
    # Page footer bar
    c.setFillColor(HexColor("#1E293B"))
    c.rect(0, 0, pw, 12*mm, fill=1, stroke=0)
    c.setFillColor(HexColor("#64748B"))
    c.setFont("Helvetica", 7)
    c.drawString(18*mm, 4*mm, "Muhamad Septian Pamungkas  ·  Portfolio 2026")
    c.drawRightString(pw - 8*mm, 4*mm, "1 / 7")


def draw_section_slide(c, pw, ph, page_num, total_pages, title, subtitle=""):
    make_slide_bg(c, pw, ph, page_num, total_pages)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ACCENT)
    c.drawString(18*mm, ph - 15*mm, "PORTFOLIO 2026")
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(WHITE)
    c.drawString(18*mm, ph - 28*mm, title)
    if subtitle:
        c.setFont("Helvetica", 11)
        c.setFillColor(HexColor("#94A3B8"))
        c.drawString(18*mm, ph - 36*mm, subtitle)


def draw_about_slide(c, pw, ph):
    draw_section_slide(c, pw, ph, 2, 7, "About Me", "Who I Am & What I Bring")
    # Content boxes
    boxes = [
        ("Background", ACCENT_LIGHT, DARK,
         "Result-oriented IT professional with 3+ years in enterprise application support & software "
         "development at Astra International, maintaining a 95% SLA. Recently completed intensive "
         "international training at KADA (Korea ASEAN Digital Academy) in Full-Stack Development, "
         "Cloud Computing, and AI Implementation."),
        ("What I Bring", HexColor("#ECFDF5"), HexColor("#065F46"),
         "Production experience with SAP, ASP.Net & SQL Server for thousands of daily users. "
         "End-to-end app building with MERN/Next.js. AI integration with Gemini & GPT models. "
         "Strong grounding in system analysis and data-driven decision making."),
        ("What I'm Building Toward", HexColor("#FFF7ED"), HexColor("#9A3412"),
         "Senior Full-Stack or Backend roles where AI is part of the product. "
         "Teams that care about shipping quality, not just features. "
         "Continuous growth in Cloud (AWS), DevOps practices, and AI/ML implementation."),
        ("My Journey", HexColor("#F5F3FF"), HexColor("#4C1D95"),
         "From Software Developer → IT Support at Astra → Family caretaker period → "
         "Deliberate 2-year upskill (DevSecOps, Data Science, MERN) → KADA AI Residency. "
         "My break was intentional — and it's the best decision I ever made."),
    ]
    x_positions = [18*mm, pw/2 + 2*mm]
    y_positions = [ph*0.52, ph*0.22]
    for i, (title, bg, fg, text) in enumerate(boxes):
        x = x_positions[i % 2]
        y = y_positions[i // 2]
        bw = pw/2 - 22*mm
        bh = 13*mm
        c.setFillColor(bg)
        c.roundRect(x, y, bw, bh, 3, fill=1, stroke=0)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 4*mm, y + bh - 5*mm, title.upper())
        c.setFillColor(DARK)
        c.setFont("Helvetica", 7.5)
        # Wrap text manually
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, "Helvetica", 7.5) < bw - 10:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        ly = y + bh - 8*mm
        for l in lines[:5]:
            if ly > y + 2*mm:
                c.drawString(x + 4*mm, ly, l)
                ly -= 3.5*mm


def draw_education_slide(c, pw, ph):
    draw_section_slide(c, pw, ph, 3, 7, "Education", "Formal Study & Continuous Learning")
    # University card
    c.setFillColor(HexColor("#1E293B"))
    c.roundRect(18*mm, ph*0.52, pw - 36*mm, 14*mm, 4, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.roundRect(18*mm, ph*0.52 + 10*mm, 4, 4*mm, 0, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(WHITE)
    c.drawString(25*mm, ph*0.52 + 8*mm, "Gunadarma University")
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawString(25*mm, ph*0.52 + 5*mm, "Bachelor of Information Systems (S.Kom)   ·   GPA 3.78 / 4.00   ·   2013 – 2017")
    # Cert cards
    certs = [
        ("DevSecOps Engineer Track",       "Studi DevSecOps",              "2024",    ACCENT),
        ("Data Science Bootcamp",          "Digital Skola — Great Grade 86/100", "2024", HexColor("#22C55E")),
        ("Full-Stack MERN / Next.js",     "Korea ASEAN Digital Academy",  "2026",    HexColor("#F59E0B")),
        ("Project Management",             "Belajarlagi",                  "2022",    HexColor("#A855F7")),
        ("Digital Marketing",             "Belajarlagi",                  "2021",    HexColor("#EC4899")),
        ("AI & Cloud Computing Training", "Korea ASEAN Digital Academy",  "2025",    HexColor("#06B6D4")),
    ]
    card_w = (pw - 36*mm) / 3 - 3*mm
    for i, (name, org, year, col) in enumerate(certs):
        row = i // 3
        col_i = i % 3
        cx = 18*mm + col_i * (card_w + 3*mm)
        cy = ph*0.28 - row * 14*mm
        c.setFillColor(HexColor("#1E293B"))
        c.roundRect(cx, cy, card_w, 12*mm, 3, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(cx, cy + 8*mm, card_w, 0.5, 0, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(WHITE)
        c.drawString(cx + 3*mm, cy + 8*mm, name)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(HexColor("#94A3B8"))
        c.drawString(cx + 3*mm, cy + 4*mm, org)
        c.drawString(cx + card_w - 12*mm, cy + 4*mm, year)


def draw_experience_slide(c, pw, ph):
    draw_section_slide(c, pw, ph, 4, 7, "Work Experience", "Professional Journey")
    jobs = [
        ("Feb – Apr 2026", "Fullstack Dev & AI Trainee",
         "Korea ASEAN Digital Academy (KADA) — Bekasi",
         ACCENT,
         ["Led PM & Lead Dev on VeriHire — AI platform for CV analysis & scam detection",
          "Built with React, Redux Toolkit, Node.js; integrated cloud & Gemini AI",
          "International residency program with real production output"]),
        ("Jan 2024 – Jan 2026", "Professional Upskilling (Career Break)",
         "Remote / Karawang",
         HexColor("#22C55E"),
         ["Completed DevSecOps track (Studi DevSecOps)",
          "Data Science Bootcamp at Digital Skola — Great Grade 86/100",
          "Built Bank Sampah Digital Dashboard with Python + Google Data Studio"]),
        ("Feb – Jul 2021", "IT Application Support",
         "Astra Graphia IT — Astra International",
         HexColor("#F59E0B"),
         ["Maintained 95% SLA for user ticketing; SAP T-Code operations",
          "Generated operational dashboards via MicroStrategy for leadership",
          "Managed IT operation dashboards for Sales Operations division"]),
        ("Jul 2018 – Feb 2021", "Software Developer",
         "Astra Graphia IT — Astra International",
         HexColor("#A855F7"),
         ["Engineered ASP.Net enterprise-scale applications",
          "Handled 50+ projects: Sales & Aftersales systems, HR, Operations",
          "Authored Business Process Documents and Technical System Designs (TSD)"]),
    ]
    y_start = ph*0.68
    for i, (period, role, company, col, bullets) in enumerate(jobs):
        y = y_start - i * 12*mm
        # Period
        c.setFont("Helvetica", 7)
        c.setFillColor(HexColor("#64748B"))
        c.drawString(18*mm, y, period)
        # Role
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(WHITE)
        c.drawString(55*mm, y, role)
        # Company
        c.setFont("Helvetica", 7.5)
        c.setFillColor(col)
        c.drawString(55*mm, y - 3.5*mm, company)
        # Dot
        c.setFillColor(col)
        c.circle(16*mm, y + 1.5*mm, 2, fill=1, stroke=0)
        # Vertical line
        if i < len(jobs) - 1:
            c.setStrokeColor(HexColor("#1E293B"))
            c.setLineWidth(0.5)
            c.line(16*mm, y - 1*mm, 16*mm, y_start - (i+1)*12*mm + 1*mm)
        # Bullets
        c.setFont("Helvetica", 7)
        c.setFillColor(HexColor("#94A3B8"))
        for j, b in enumerate(bullets):
            c.drawString(55*mm, y - 6*mm - j*3*mm, f"• {b}")


def draw_projects_slide(c, pw, ph, page_num, total_pages):
    draw_section_slide(c, pw, ph, page_num, total_pages,
                       "Featured Projects", "Selected Work")
    projects = [
        ("BisaFit.AI",           ACCENT,          "React · TS · Vite · Gemini Pro · Tailwind",
         "Premium AI fitness assistant with Navy BFP/FFMI calculator, localised Indonesian nutrition "
         "engine (tempeh, tofu, local spices), circadian sleep mapping for shift workers, and "
         "browser PDF export. Solo developer — full architecture to deployment."),
        ("VeriHire Enhanced",   HexColor("#22C55E"), "React · Node.js · MongoDB · Gemini · GPT-5",
         "AI-powered CV analysis & job scam detection platform. PM & Lead Dev during KADA residency. "
         "Dual AI provider pipeline, JWT auth, OCR, premium token system, i18n (EN/ID)."),
        ("Executive Ledger",     HexColor("#F59E0B"), "React 19 · Node.js · Prisma · SQLite · Gemini",
         "AI expense tracker with Gemini receipt scanning, multi-user collaboration, recurring "
         "transactions, budget alerts, PDF/CSV export. Full CRUD, JWT auth, email reports."),
        ("Job Automation Studio",HexColor("#A855F7"), "Python · Gradio · YAML · AI Agents",
         "No-code tool generating personalised Python job automation scripts via AI. "
         "Answer 3 questions → download runnable script → execute with any AI agent."),
    ]
    card_w = (pw - 36*mm) / 2 - 4*mm
    for i, (name, col, tech, desc) in enumerate(projects):
        row = i // 2
        ci = i % 2
        cx = 18*mm + ci * (card_w + 6*mm)
        cy = ph*0.50 - row * 20*mm
        c.setFillColor(HexColor("#1E293B"))
        c.roundRect(cx, cy, card_w, 18*mm, 4, fill=1, stroke=0)
        # Colour top stripe
        c.setFillColor(col)
        c.roundRect(cx, cy + 16*mm, card_w, 2*mm, 0, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(WHITE)
        c.drawString(cx + 4*mm, cy + 14*mm, name)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(HexColor("#64748B"))
        c.drawString(cx + 4*mm, cy + 10*mm, tech)
        # Wrap desc
        words = desc.split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, "Helvetica", 6.5) < card_w - 10:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        ly = cy + 7*mm
        c.setFont("Helvetica", 6.5)
        c.setFillColor(HexColor("#CBD5E1"))
        for l in lines[:4]:
            if ly > cy + 2*mm:
                c.drawString(cx + 4*mm, ly, l)
                ly -= 3*mm


def draw_skills_slide(c, pw, ph):
    draw_section_slide(c, pw, ph, 6, 7, "Technical Skills", "The Full Stack of My Toolkit")
    groups = [
        ("Frontend",      ACCENT,    ["React 18 / Next.js", "TypeScript", "Redux Toolkit",
                                      "Tailwind CSS", "HTML5 / CSS3 / JavaScript"]),
        ("Backend",      HexColor("#22C55E"), ["Node.js / Express", "MongoDB / Prisma",
                                               "REST API Design", "JWT & Auth Systems",
                                               "Nodemailer / PDFKit"]),
        ("Enterprise",   HexColor("#F59E0B"), ["SAP (T-Code Operations)", "ASP.Net / MS SQL Server",
                                               "MicroStrategy", "Jira", "Business Analysis"]),
        ("AI & Data",    HexColor("#A855F7"), ["Google Gemini API", "GPT-5 Integration",
                                               "Python (AI/Data)", "R / Statistical Modeling",
                                               "Google Data Studio"]),
        ("DevOps",      HexColor("#06B6D4"), ["Docker", "AWS Cloud",
                                               "Git / Version Control", "CI/CD", "Linux"]),
    ]
    card_w = (pw - 36*mm) / len(groups) - 3*mm
    for i, (title, col, skills) in enumerate(groups):
        cx = 18*mm + i * (card_w + 3*mm)
        cy = ph*0.25
        ch = 22*mm
        c.setFillColor(HexColor("#1E293B"))
        c.roundRect(cx, cy, card_w, ch, 3, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(cx, cy + ch - 3*mm, card_w, 3*mm, 0, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(WHITE)
        c.drawCentredString(cx + card_w/2, cy + ch - 5*mm, title.upper())
        c.setFont("Helvetica", 6.5)
        c.setFillColor(HexColor("#94A3B8"))
        for j, s in enumerate(skills):
            c.drawString(cx + 3*mm, cy + ch - 7*mm - j*3*mm, f"• {s}")


def draw_contact_slide(c, pw, ph):
    make_slide_bg(c, pw, ph, 7, 7)
    c.setFillColor(HexColor("#0F172A"))
    c.rect(0, 0, pw, ph, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, 0, 5*mm, ph, fill=1, stroke=0)
    # Centered content
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(WHITE)
    c.drawCentredString(pw/2, ph*0.65, "Let's Connect")
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawCentredString(pw/2, ph*0.57, "Open to full-stack, backend, or AI-integrated roles.")
    c.setFillColor(ACCENT)
    c.rect(pw/2 - 40*mm, ph*0.55, 80*mm, 1, fill=1, stroke=0)
    contacts = [
        ("Email",    "muhseptianp@outlook.com"),
        ("LinkedIn", "linkedin.com/in/muh-septian-pamungkas"),
        ("GitHub",   "github.com/seppam"),
        ("Location", "Karawang, Jawa Barat, Indonesia"),
    ]
    for i, (label, val) in enumerate(contacts):
        y = ph*0.44 - i * 8*mm
        c.setFillColor(ACCENT)
        c.rect(pw/2 - 50*mm, y - 1*mm, 1.5*mm, 4*mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(HexColor("#64748B"))
        c.drawString(pw/2 - 46*mm, y, label)
        c.setFont("Helvetica", 8)
        c.setFillColor(WHITE)
        c.drawString(pw/2 - 46*mm, y - 3.5*mm, val)
    # Bottom bar
    c.setFillColor(HexColor("#1E293B"))
    c.rect(0, 0, pw, 12*mm, fill=1, stroke=0)
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#475569"))
    c.drawCentredString(pw/2, 4*mm, "Muhamad Septian Pamungkas  ·  Portfolio 2026  ·  muhseptianp@outlook.com")


def build_multipage():
    out = os.path.join(os.path.dirname(__file__), "Septian_Portfolio_MultiPage.pdf")
    c = canvas.Canvas(out, pagesize=landscape(A4))
    c.setTitle("Muhamad Septian Pamungkas — Portfolio 2026")
    c.setAuthor("Muhamad Septian Pamungkas")
    c.setSubject("Portfolio")

    draw_cover_slide(c, SW, SH)
    c.showPage()

    draw_about_slide(c, SW, SH)
    c.showPage()

    draw_education_slide(c, SW, SH)
    c.showPage()

    draw_experience_slide(c, SW, SH)
    c.showPage()

    draw_projects_slide(c, SW, SH, 5, 7)
    c.showPage()

    draw_skills_slide(c, SW, SH)
    c.showPage()

    draw_contact_slide(c, SW, SH)
    c.showPage()

    c.save()
    print(f"✅ Multi-page deck saved: {out}")
    return out


# ──────────────────────────────────────────────────────────────
# RUN
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    p1 = build_onepager()
    p2 = build_multipage()
    print("\nAll done! Files:")
    print(f"  📄 One-pager:  {p1}")
    print(f"  📄 Slide deck: {p2}")
