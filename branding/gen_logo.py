import math, os

NAVY = "#0F3A4A"
TEAL = "#0E7C86"
TEAL_LIGHT = "#1FBFAE"
WHITE = "#FFFFFF"

OUT = "/sessions/vigilant-amazing-hawking/mnt/outputs/branding"
os.makedirs(OUT, exist_ok=True)

def pt(cx, cy, r, deg):
    rad = math.radians(deg)
    return cx + r*math.cos(rad), cy + r*math.sin(rad)

def radar_icon(navy=NAVY, teal=TEAL, teal_light=TEAL_LIGHT, bg=None):
    cx, cy = 50, 50
    R = 42
    x0, y0 = pt(cx, cy, R, -90)   # top
    x1, y1 = pt(cx, cy, R, 0)     # right
    ticks = ""
    for ang in (-90, 0, 90, 180):
        xa, ya = pt(cx, cy, R+1, ang)
        xb, yb = pt(cx, cy, R+7, ang)
        ticks += f'<line x1="{xa:.2f}" y1="{ya:.2f}" x2="{xb:.2f}" y2="{yb:.2f}" stroke="{teal}" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/>\n'
    blip_ang = -25
    bx, by = pt(cx, cy, 27, blip_ang)
    bg_rect = f'<rect x="0" y="0" width="100" height="100" fill="{bg}"/>' if bg else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="sweep" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x0:.2f}" y2="{y0:.2f}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{teal_light}" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="{teal_light}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  {bg_rect}
  {ticks}
  <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{teal}" stroke-width="2.6" opacity="0.9"/>
  <circle cx="{cx}" cy="{cy}" r="29" fill="none" stroke="{teal}" stroke-width="1.6" opacity="0.5"/>
  <circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="{teal}" stroke-width="1.2" opacity="0.35"/>
  <path d="M {cx} {cy} L {x0:.2f} {y0:.2f} A {R} {R} 0 0 1 {x1:.2f} {y1:.2f} Z" fill="url(#sweep)"/>
  <line x1="{cx}" y1="{cy}" x2="{x1:.2f}" y2="{y1:.2f}" stroke="{teal_light}" stroke-width="1.6" opacity="0.85"/>
  <circle cx="{bx:.2f}" cy="{by:.2f}" r="10" fill="{teal_light}" opacity="0.18"/>
  <circle cx="{bx:.2f}" cy="{by:.2f}" r="5.2" fill="{WHITE}"/>
  <circle cx="{bx:.2f}" cy="{by:.2f}" r="5.2" fill="none" stroke="{navy}" stroke-width="1.4"/>
  <circle cx="{cx}" cy="{cy}" r="2.6" fill="{navy}"/>
</svg>'''
    return svg

def wordmark(navy=NAVY, teal_light=TEAL_LIGHT, y=68, size=44):
    return f'''<text x="118" y="{y}" font-family="Poppins" font-weight="700" font-size="{size}" fill="{navy}">Fit<tspan fill="{navy}">Radar</tspan><tspan fill="{teal_light}">HR</tspan></text>'''

def logo_horizontal(navy=NAVY, teal=TEAL, teal_light=TEAL_LIGHT, filename="logo-horizontal-color.svg", tagline=False, bg=None):
    icon = radar_icon(navy, teal, teal_light)
    inner = icon.split(">",1)[1].rsplit("</svg>",1)[0]
    bg_rect = f'<rect x="0" y="0" width="620" height="120" fill="{bg}"/>' if bg else ""
    tag = ''
    if tagline:
        tag = f'<text x="120" y="98" font-family="Poppins" font-weight="400" font-size="15" fill="{teal}" opacity="0.85">Big Five fit, human in the loop</text>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 120">
  {bg_rect}
  <g transform="translate(0,10) scale(1.0)">
    <svg x="0" y="0" width="100" height="100" viewBox="0 0 100 100">{inner}</svg>
  </g>
  <text x="118" y="66" font-family="Poppins" font-weight="700" font-size="42" fill="{navy}">Fit<tspan>Radar</tspan><tspan fill="{teal_light}">HR</tspan></text>
  {tag}
</svg>'''
    with open(f"{OUT}/{filename}", "w") as f:
        f.write(svg)
    return svg

# 1. Color icon (square) - for favicon / GitHub avatar / social pfp
with open(f"{OUT}/icon-color.svg", "w") as f:
    f.write(radar_icon())

# 2. White icon on navy bg circle - for dark backgrounds / avatar alt
white_on_navy = radar_icon(navy=WHITE, teal=WHITE, teal_light=TEAL_LIGHT, bg=None).replace(
    '<circle cx="50" cy="50" r="42"', f'<circle cx="50" cy="50" r="49" fill="{NAVY}"/>\n  <circle cx="50" cy="50" r="42"'
)
with open(f"{OUT}/icon-reversed-navy-bg.svg", "w") as f:
    f.write(white_on_navy)

# 3. Horizontal color logo (for website header, README light bg)
logo_horizontal(filename="logo-horizontal-color.svg")

# 4. Horizontal white logo (for dark backgrounds)
logo_horizontal(navy=WHITE, teal=WHITE, teal_light=TEAL_LIGHT, filename="logo-horizontal-white.svg")

# 5. Social banner 1200x630 (GitHub social preview / LinkedIn OG image)
from PIL import ImageFont
FONT_PATH = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

def measure(text, size):
    f = ImageFont.truetype(FONT_PATH, size)
    return f.getlength(text)

icon_svg = radar_icon()
icon_inner = icon_svg.split(">",1)[1].rsplit("</svg>",1)[0]

CANVAS_W, CANVAS_H = 1200, 630
ICON_SIZE = 150
GAP = 28
WM_SIZE = 62

w_fit = measure("Fit", WM_SIZE)
w_radar = measure("Radar", WM_SIZE)
w_hr = measure("HR", WM_SIZE)
wm_width = w_fit + w_radar + w_hr

lockup_width = ICON_SIZE + GAP + wm_width
lockup_x = (CANVAS_W - lockup_width) / 2
lockup_y = 210  # top of icon

icon_x = lockup_x
icon_y = lockup_y
icon_cy = icon_y + ICON_SIZE/2

text_x0 = icon_x + ICON_SIZE + GAP
baseline_y = icon_cy + WM_SIZE * 0.34

x_fit = text_x0
x_radar = x_fit + w_fit
x_hr = x_radar + w_radar

tagline = "\u00c9valuez la compatibilit\u00e9 poste &amp; \u00e9quipe, en toute transparence"
tagline_y = icon_y + ICON_SIZE + 70

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}">
  <defs>
    <radialGradient id="bgfade" cx="50%" cy="42%" r="75%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#E7F3F3"/>
    </radialGradient>
  </defs>
  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#bgfade)"/>
  <g transform="translate({icon_x:.2f},{icon_y:.2f}) scale({ICON_SIZE/100:.4f})">
    <svg x="0" y="0" width="100" height="100" viewBox="0 0 100 100">{icon_inner}</svg>
  </g>
  <text x="{x_fit:.2f}" y="{baseline_y:.2f}" font-family="Poppins" font-weight="700" font-size="{WM_SIZE}" fill="{NAVY}">Fit</text>
  <text x="{x_radar:.2f}" y="{baseline_y:.2f}" font-family="Poppins" font-weight="700" font-size="{WM_SIZE}" fill="{NAVY}">Radar</text>
  <text x="{x_hr:.2f}" y="{baseline_y:.2f}" font-family="Poppins" font-weight="700" font-size="{WM_SIZE}" fill="{TEAL_LIGHT}">HR</text>
  <text x="{CANVAS_W/2:.2f}" y="{tagline_y:.2f}" text-anchor="middle" font-family="Poppins" font-weight="400" font-size="23" fill="{TEAL}" opacity="0.9">{tagline}</text>
</svg>'''
with open(f"{OUT}/social-banner.svg", "w") as f:
    f.write(banner)

print("done")
