from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import pptx.oxml.ns as nsmap
from lxml import etree

# Color palette
DARK_BLUE = RGBColor(0x1A, 0x37, 0x6C)     # 진한 파란색
SOLAR_YELLOW = RGBColor(0xFF, 0xC1, 0x07)   # 태양광 노란색
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)    # 연한 회색
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x28, 0xA7, 0x45)          # 친환경 초록색
TEXT_DARK = RGBColor(0x21, 0x21, 0x21)
ACCENT_BLUE = RGBColor(0x0D, 0x6E, 0xFD)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK_LAYOUT = prs.slide_layouts[6]  # blank

def add_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape

def add_text_box(slide, text, left, top, width, height, font_size=18, bold=False,
                 color=TEXT_DARK, align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_paragraph(tf, text, font_size=14, bold=False, color=TEXT_DARK, align=PP_ALIGN.LEFT, space_before=6):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p

# ─────────────────────────────────────────────
# SLIDE 1: Title
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)

# Background
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=DARK_BLUE)

# Yellow accent bar
add_rect(slide, 0, 5.8, 13.33, 0.15, fill_color=SOLAR_YELLOW)

# Main title
add_text_box(slide, "태양광 주차장", 1.5, 1.2, 10, 1.5,
             font_size=52, bold=True, color=SOLAR_YELLOW, align=PP_ALIGN.CENTER)

# Subtitle
add_text_box(slide, "지속가능한 미래를 위한 스마트 에너지 솔루션", 1.5, 2.8, 10, 0.8,
             font_size=22, bold=False, color=WHITE, align=PP_ALIGN.CENTER)

# Proposal tag
add_rect(slide, 5.2, 3.8, 2.9, 0.55, fill_color=SOLAR_YELLOW)
add_text_box(slide, "사업 제안서", 5.2, 3.82, 2.9, 0.5,
             font_size=16, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)

# Date
add_text_box(slide, "2026년 3월", 0, 6.2, 13.33, 0.5,
             font_size=14, color=WHITE, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────
# SLIDE 2: Table of Contents
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=DARK_BLUE)
add_text_box(slide, "목   차", 0, 0.15, 13.33, 0.8,
             font_size=30, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

items = [
    ("01", "사업 배경 및 필요성"),
    ("02", "태양광 주차장 개요"),
    ("03", "기대 효과 및 경제성 분석"),
    ("04", "설치 계획 및 일정"),
    ("05", "환경적 기여 & ESG"),
    ("06", "투자 및 수익 모델"),
    ("07", "결론 및 제안"),
]

cols = [(0.5, 5.8), (7.0, 5.8)]
for i, (num, title) in enumerate(items):
    col = i % 2
    row = i // 2
    lx = cols[col][0]
    ly = 1.4 + row * 1.1
    w = cols[col][1]
    add_rect(slide, lx, ly, w, 0.85, fill_color=WHITE, line_color=DARK_BLUE, line_width=1)
    add_text_box(slide, num, lx + 0.1, ly + 0.05, 0.7, 0.75,
                 font_size=22, bold=True, color=SOLAR_YELLOW, align=PP_ALIGN.CENTER)
    add_text_box(slide, title, lx + 0.85, ly + 0.15, w - 1.0, 0.6,
                 font_size=16, bold=True, color=DARK_BLUE, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────
# SLIDE 3: Background & Need
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=DARK_BLUE)
add_rect(slide, 0, 1.1, 0.08, 6.4, fill_color=SOLAR_YELLOW)
add_text_box(slide, "01  사업 배경 및 필요성", 0.3, 0.15, 10, 0.8,
             font_size=28, bold=True, color=WHITE)

cards = [
    ("🌡️ 기후위기 심화", "탄소중립 2050 목표 달성을 위해\n재생에너지 전환 필수"),
    ("⚡ 에너지 비용 상승", "전기요금 지속 인상으로\n자가발전 수요 급증"),
    ("🚗 주차 공간 활용", "유휴 주차장 부지를\n에너지 생산 공간으로 전환"),
    ("📋 정부 지원 확대", "태양광 설비 보조금·\nREC 제도 적극 운영 중"),
]
for i, (title, body) in enumerate(cards):
    cx = 0.4 + i * 3.2
    add_rect(slide, cx, 1.5, 2.9, 3.5, fill_color=LIGHT_GRAY, line_color=DARK_BLUE, line_width=0.5)
    add_text_box(slide, title, cx + 0.15, 1.65, 2.6, 0.8,
                 font_size=15, bold=True, color=DARK_BLUE)
    add_text_box(slide, body, cx + 0.15, 2.45, 2.6, 2.0,
                 font_size=13, color=TEXT_DARK)

add_rect(slide, 0.4, 5.3, 12.5, 0.9, fill_color=SOLAR_YELLOW)
add_text_box(slide, "✔  태양광 주차장은 공간 효율성 + 친환경 에너지 생산의 두 마리 토끼를 동시에 잡는 솔루션입니다.",
             0.5, 5.38, 12.3, 0.75, font_size=14, bold=True, color=DARK_BLUE)

# ─────────────────────────────────────────────
# SLIDE 4: Overview
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=DARK_BLUE)
add_rect(slide, 0, 1.1, 0.08, 6.4, fill_color=SOLAR_YELLOW)
add_text_box(slide, "02  태양광 주차장 개요", 0.3, 0.15, 10, 0.8,
             font_size=28, bold=True, color=WHITE)

# Left: what is it
add_rect(slide, 0.3, 1.3, 5.8, 5.8, fill_color=LIGHT_GRAY)
add_text_box(slide, "태양광 주차장이란?", 0.5, 1.45, 5.4, 0.6,
             font_size=18, bold=True, color=DARK_BLUE)
points = [
    "• 주차장 지붕·캐노피에 태양광 패널 설치",
    "• 발전된 전력을 건물·전기차 충전에 활용",
    "• 잉여 전력은 한전에 판매(전력 판매 수익)",
    "• 주차 차량 보호 + 에너지 생산 이중 효과",
    "• 지상형 / 지하 외부형 / 옥상형 다양한 형태",
]
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(2.2), Inches(5.4), Inches(4.5))
txBox.word_wrap = True
tf = txBox.text_frame
tf.word_wrap = True
tf.paragraphs[0].runs  # init
for j, pt in enumerate(points):
    if j == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run()
    run.text = pt
    run.font.size = Pt(14)
    run.font.color.rgb = TEXT_DARK

# Right: key specs
add_rect(slide, 6.5, 1.3, 6.5, 5.8, fill_color=DARK_BLUE)
add_text_box(slide, "주요 사양", 6.7, 1.45, 6.1, 0.6,
             font_size=18, bold=True, color=SOLAR_YELLOW)
specs = [
    ("패널 용량", "400W ~ 550W / 장"),
    ("시스템 용량", "100kW ~ 1MW (규모 조정 가능)"),
    ("연간 발전량", "약 130,000 kWh (100kW 기준)"),
    ("패널 수명", "25년 이상"),
    ("설치 면적", "주차면당 약 15~20㎡"),
    ("EV 충전기", "완속/급속 동시 연계 가능"),
]
for j, (k, v) in enumerate(specs):
    sy = 2.2 + j * 0.72
    add_rect(slide, 6.6, sy, 6.2, 0.6, fill_color=RGBColor(0x2A, 0x47, 0x7C))
    add_text_box(slide, k, 6.7, sy + 0.08, 2.2, 0.45,
                 font_size=13, bold=True, color=SOLAR_YELLOW)
    add_text_box(slide, v, 9.0, sy + 0.08, 3.6, 0.45,
                 font_size=13, color=WHITE)

# ─────────────────────────────────────────────
# SLIDE 5: Economic Analysis
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=DARK_BLUE)
add_rect(slide, 0, 1.1, 0.08, 6.4, fill_color=SOLAR_YELLOW)
add_text_box(slide, "03  기대 효과 및 경제성 분석", 0.3, 0.15, 10, 0.8,
             font_size=28, bold=True, color=WHITE)

# KPI boxes
kpis = [
    ("연간 발전량", "130,000 kWh", "100kW 시스템 기준"),
    ("연간 절감액", "약 2,300만원", "전기요금 절감 기준"),
    ("REC 판매수익", "약 500만원", "신재생에너지 공급인증서"),
    ("투자회수기간", "5~7년", "정부보조금 반영 시"),
]
for i, (label, value, sub) in enumerate(kpis):
    kx = 0.3 + i * 3.2
    add_rect(slide, kx, 1.3, 3.0, 1.8, fill_color=DARK_BLUE)
    add_text_box(slide, label, kx, 1.35, 3.0, 0.5,
                 font_size=13, color=SOLAR_YELLOW, align=PP_ALIGN.CENTER)
    add_text_box(slide, value, kx, 1.8, 3.0, 0.7,
                 font_size=19, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(slide, sub, kx, 2.5, 3.0, 0.45,
                 font_size=11, color=RGBColor(0xCC, 0xCC, 0xCC), align=PP_ALIGN.CENTER)

# Cost breakdown table
add_text_box(slide, "비용 구조 분석", 0.3, 3.3, 6, 0.5,
             font_size=16, bold=True, color=DARK_BLUE)
rows = [
    ("항목", "금액", "비고", True),
    ("태양광 패널 (100kW)", "약 1억 2천만원", "패널 + 인버터", False),
    ("구조물 (캐노피)", "약 6천만원", "철골 + 도장", False),
    ("EV 충전기 (4기)", "약 2천만원", "완속 기준", False),
    ("공사 및 설치", "약 2천만원", "전기공사 포함", False),
    ("합계", "약 2억 2천만원", "정부보조금 최대 50% 지원", True),
]
for j, (c1, c2, c3, is_header) in enumerate(rows):
    ry = 3.85 + j * 0.48
    bg = DARK_BLUE if is_header else (LIGHT_GRAY if j % 2 == 0 else WHITE)
    fg = WHITE if is_header else TEXT_DARK
    add_rect(slide, 0.3, ry, 12.7, 0.45, fill_color=bg)
    add_text_box(slide, c1, 0.4, ry + 0.03, 3.5, 0.4, font_size=13, bold=is_header, color=fg)
    add_text_box(slide, c2, 4.0, ry + 0.03, 4.0, 0.4, font_size=13, bold=is_header, color=fg)
    add_text_box(slide, c3, 8.2, ry + 0.03, 4.5, 0.4, font_size=13, bold=is_header, color=fg)

# ─────────────────────────────────────────────
# SLIDE 6: Installation Plan
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=DARK_BLUE)
add_rect(slide, 0, 1.1, 0.08, 6.4, fill_color=SOLAR_YELLOW)
add_text_box(slide, "04  설치 계획 및 일정", 0.3, 0.15, 10, 0.8,
             font_size=28, bold=True, color=WHITE)

phases = [
    ("1단계", "사전 조사\n및 설계", "1~2개월", "현장 조사\n구조 검토\n인허가 준비"),
    ("2단계", "인허가\n취득", "2~3개월", "전기사업허가\n건축신고\n환경영향평가"),
    ("3단계", "구조물\n설치", "1~2개월", "캐노피 시공\n배선 작업\n패널 설치"),
    ("4단계", "계통\n연계", "1개월", "한전 연계\n인버터 설치\n시운전"),
    ("5단계", "운영\n시작", "상시", "모니터링\n유지보수\n성과 분석"),
]

for i, (step, title, duration, detail) in enumerate(phases):
    px = 0.3 + i * 2.6
    # Arrow connector (except last)
    if i < 4:
        add_rect(slide, px + 2.25, 2.1, 0.35, 0.3, fill_color=DARK_BLUE)

    add_rect(slide, px, 1.3, 2.3, 1.1, fill_color=DARK_BLUE)
    add_text_box(slide, step, px, 1.35, 2.3, 0.45,
                 font_size=14, bold=True, color=SOLAR_YELLOW, align=PP_ALIGN.CENTER)
    add_text_box(slide, title, px, 1.75, 2.3, 0.55,
                 font_size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_rect(slide, px, 2.5, 2.3, 0.5, fill_color=SOLAR_YELLOW)
    add_text_box(slide, f"⏱ {duration}", px, 2.55, 2.3, 0.4,
                 font_size=13, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)

    add_rect(slide, px, 3.1, 2.3, 2.0, fill_color=LIGHT_GRAY)
    add_text_box(slide, detail, px + 0.1, 3.2, 2.1, 1.8,
                 font_size=12, color=TEXT_DARK)

# Gantt-like bar
add_text_box(slide, "총 프로젝트 기간: 약 7~8개월", 0, 5.35, 13.33, 0.5,
             font_size=16, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)
months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월"]
for i, m in enumerate(months):
    mx = 0.8 + i * 1.5
    c = DARK_BLUE if i < 7 else LIGHT_GRAY
    add_rect(slide, mx, 5.9, 1.3, 0.5, fill_color=c, line_color=WHITE, line_width=0.5)
    add_text_box(slide, m, mx, 5.95, 1.3, 0.4,
                 font_size=12, color=WHITE if i < 7 else TEXT_DARK, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────
# SLIDE 7: ESG
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=DARK_BLUE)
add_rect(slide, 0, 1.1, 0.08, 6.4, fill_color=SOLAR_YELLOW)
add_text_box(slide, "05  환경적 기여 & ESG", 0.3, 0.15, 10, 0.8,
             font_size=28, bold=True, color=WHITE)

esg_items = [
    ("E\n환경", GREEN, [
        "연간 CO₂ 약 58톤 감축",
        "(30년생 소나무 8,700그루 효과)",
        "화석연료 의존도 감소",
        "미세먼지 저감 기여",
    ]),
    ("S\n사회", ACCENT_BLUE, [
        "지역 일자리 창출",
        "에너지 복지 향상",
        "전기차 인프라 확충",
        "시민 환경 인식 제고",
    ]),
    ("G\n거버넌스", DARK_BLUE, [
        "탄소중립 경영 선언",
        "RE100 목표 달성 기여",
        "ESG 공시 의무 대응",
        "지속가능경영보고서 실적",
    ]),
]
for i, (letter, color, points) in enumerate(esg_items):
    ex = 0.5 + i * 4.2
    add_rect(slide, ex, 1.3, 3.8, 1.0, fill_color=color)
    add_text_box(slide, letter, ex, 1.35, 3.8, 0.85,
                 font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, ex, 2.4, 3.8, 4.5, fill_color=LIGHT_GRAY)
    txBox = slide.shapes.add_textbox(Inches(ex + 0.15), Inches(2.55), Inches(3.5), Inches(4.2))
    txBox.word_wrap = True
    tf = txBox.text_frame
    tf.word_wrap = True
    for j, pt in enumerate(points):
        if j == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = f"✓  {pt}"
        run.font.size = Pt(14)
        run.font.color.rgb = TEXT_DARK

# ─────────────────────────────────────────────
# SLIDE 8: Investment Model
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=DARK_BLUE)
add_rect(slide, 0, 1.1, 0.08, 6.4, fill_color=SOLAR_YELLOW)
add_text_box(slide, "06  투자 및 수익 모델", 0.3, 0.15, 10, 0.8,
             font_size=28, bold=True, color=WHITE)

# Revenue streams
add_text_box(slide, "수익 흐름", 0.3, 1.3, 6, 0.5,
             font_size=16, bold=True, color=DARK_BLUE)
revenues = [
    ("전력 판매 수익", "연간 약 1,400만원", "한전 계통 연계 판매"),
    ("전기요금 절감", "연간 약 1,300만원", "자가소비분 절감"),
    ("REC 판매", "연간 약 500만원", "신재생 공급인증서"),
    ("EV 충전 수익", "연간 약 600만원", "충전 서비스 이용료"),
    ("주차장 프리미엄", "연간 약 300만원", "서비스 가치 향상"),
]
for j, (item, amount, note) in enumerate(revenues):
    ry = 1.9 + j * 0.72
    add_rect(slide, 0.3, ry, 12.5, 0.65, fill_color=LIGHT_GRAY if j % 2 == 0 else WHITE,
             line_color=RGBColor(0xDD, 0xDD, 0xDD), line_width=0.3)
    add_rect(slide, 0.3, ry, 0.06, 0.65, fill_color=SOLAR_YELLOW)
    add_text_box(slide, item, 0.5, ry + 0.1, 4.5, 0.45, font_size=13, bold=True, color=TEXT_DARK)
    add_text_box(slide, amount, 5.2, ry + 0.1, 3.0, 0.45, font_size=13, bold=True, color=GREEN)
    add_text_box(slide, note, 8.4, ry + 0.1, 4.3, 0.45, font_size=12, color=RGBColor(0x66, 0x66, 0x66))

# Total
add_rect(slide, 0.3, 5.6, 12.5, 0.7, fill_color=DARK_BLUE)
add_text_box(slide, "연간 총 예상 수익", 0.5, 5.67, 5.0, 0.55,
             font_size=15, bold=True, color=WHITE)
add_text_box(slide, "약 4,100만원 / 년", 5.5, 5.67, 4.5, 0.55,
             font_size=18, bold=True, color=SOLAR_YELLOW)
add_text_box(slide, "※ 정부 보조금·세제혜택 별도", 10.2, 5.72, 2.8, 0.45,
             font_size=11, color=RGBColor(0xCC, 0xCC, 0xCC))

# ─────────────────────────────────────────────
# SLIDE 9: Conclusion
# ─────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=DARK_BLUE)
add_rect(slide, 0, 5.5, 13.33, 2.0, fill_color=RGBColor(0x10, 0x28, 0x50))
add_rect(slide, 0, 2.6, 13.33, 0.06, fill_color=SOLAR_YELLOW)

add_text_box(slide, "결론 및 제안", 1.5, 0.4, 10, 0.9,
             font_size=36, bold=True, color=SOLAR_YELLOW, align=PP_ALIGN.CENTER)
add_text_box(slide, "태양광 주차장은 단순한 발전 시설이 아닙니다.",
             1.0, 1.3, 11.33, 0.6,
             font_size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text_box(slide, "탄소중립 실현 · 에너지 자립 · 수익 창출을 동시에 달성하는\n미래 지향적 인프라 투자입니다.",
             1.0, 1.9, 11.33, 0.9,
             font_size=17, color=RGBColor(0xCC, 0xDD, 0xFF), align=PP_ALIGN.CENTER)

summary = [
    "✅  투자 회수 기간 5~7년 (정부 보조금 적용 시)",
    "✅  연간 약 4,100만원 수익 창출",
    "✅  CO₂ 연간 58톤 감축으로 ESG 경영 강화",
    "✅  EV 충전 인프라 선제 구축으로 미래 경쟁력 확보",
]
txBox = slide.shapes.add_textbox(Inches(2.5), Inches(2.9), Inches(9), Inches(2.4))
txBox.word_wrap = True
tf = txBox.text_frame
tf.word_wrap = True
for j, s in enumerate(summary):
    if j == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.space_before = Pt(10)
    run = p.add_run()
    run.text = s
    run.font.size = Pt(15)
    run.font.color.rgb = WHITE

add_text_box(slide, "지금 바로 시작하세요", 0, 5.65, 13.33, 0.7,
             font_size=24, bold=True, color=SOLAR_YELLOW, align=PP_ALIGN.CENTER)
add_text_box(slide, "문의 및 협의: solar@company.com  |  Tel. 02-0000-0000",
             0, 6.4, 13.33, 0.5,
             font_size=13, color=RGBColor(0xAA, 0xBB, 0xCC), align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────
output_path = "/home/user/SSD/태양광_주차장_제안서.pptx"
prs.save(output_path)
print(f"PPT saved: {output_path}")
