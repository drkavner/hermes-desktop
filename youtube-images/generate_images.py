#!/usr/bin/env python3
"""Generate crude MS Paint-style images for YouTube video timestamps."""

import random
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BG = "white"

def get_font(size=28):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def wobbly_line(draw, x1, y1, x2, y2, fill="black", width=3):
    """Draw a wobbly hand-drawn line."""
    steps = max(10, int(math.hypot(x2-x1, y2-y1) / 8))
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = x1 + (x2 - x1) * t + random.randint(-3, 3)
        y = y1 + (y2 - y1) * t + random.randint(-3, 3)
        points.append((x, y))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=fill, width=width)

def wobbly_rect(draw, x1, y1, x2, y2, fill=None, outline="black", width=3):
    wobbly_line(draw, x1, y1, x2, y1, outline, width)
    wobbly_line(draw, x2, y1, x2, y2, outline, width)
    wobbly_line(draw, x2, y2, x1, y2, outline, width)
    wobbly_line(draw, x1, y2, x1, y1, outline, width)
    if fill:
        draw.rectangle([x1+4, y1+4, x2-4, y2-4], fill=fill)

def wobbly_circle(draw, cx, cy, r, fill=None, outline="black", width=3):
    points = []
    for i in range(40):
        angle = 2 * math.pi * i / 40
        x = cx + (r + random.randint(-3, 3)) * math.cos(angle)
        y = cy + (r + random.randint(-3, 3)) * math.sin(angle)
        points.append((x, y))
    points.append(points[0])
    if fill:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=outline, width=width)

def stick_figure(draw, cx, cy, scale=1.0, color="black"):
    """Draw a stick figure centered at cx, cy."""
    s = scale
    # Head
    wobbly_circle(draw, cx, cy - int(60*s), int(20*s), outline=color)
    # Body
    wobbly_line(draw, cx, cy - int(40*s), cx, cy + int(20*s), color)
    # Arms
    wobbly_line(draw, cx, cy - int(20*s), cx - int(30*s), cy + int(10*s), color)
    wobbly_line(draw, cx, cy - int(20*s), cx + int(30*s), cy + int(10*s), color)
    # Legs
    wobbly_line(draw, cx, cy + int(20*s), cx - int(25*s), cy + int(60*s), color)
    wobbly_line(draw, cx, cy + int(20*s), cx + int(25*s), cy + int(60*s), color)

def robot(draw, cx, cy, scale=1.0, color="blue"):
    """Draw a simple robot."""
    s = scale
    # Head (square)
    wobbly_rect(draw, cx-int(20*s), cy-int(65*s), cx+int(20*s), cy-int(35*s), outline=color)
    # Eyes
    draw.rectangle([cx-int(12*s), cy-int(57*s), cx-int(6*s), cy-int(47*s)], fill=color)
    draw.rectangle([cx+int(6*s), cy-int(57*s), cx+int(12*s), cy-int(47*s)], fill=color)
    # Antenna
    wobbly_line(draw, cx, cy-int(65*s), cx, cy-int(80*s), color, 2)
    wobbly_circle(draw, cx, cy-int(83*s), int(4*s), fill=color, outline=color)
    # Body
    wobbly_rect(draw, cx-int(25*s), cy-int(35*s), cx+int(25*s), cy+int(15*s), outline=color)
    # Legs
    wobbly_line(draw, cx-int(15*s), cy+int(15*s), cx-int(15*s), cy+int(55*s), color)
    wobbly_line(draw, cx+int(15*s), cy+int(15*s), cx+int(15*s), cy+int(55*s), color)
    # Arms
    wobbly_line(draw, cx-int(25*s), cy-int(20*s), cx-int(45*s), cy+int(5*s), color)
    wobbly_line(draw, cx+int(25*s), cy-int(20*s), cx+int(45*s), cy+int(5*s), color)

def messy_text(draw, x, y, text, size=40, color="black"):
    font = get_font(size)
    # slight random offset for messy feel
    draw.text((x + random.randint(-2,2), y + random.randint(-2,2)), text, fill=color, font=font)

def arrow(draw, x1, y1, x2, y2, color="black", width=4):
    wobbly_line(draw, x1, y1, x2, y2, color, width)
    angle = math.atan2(y2-y1, x2-x1)
    hl = 20
    draw.line([(x2, y2), (x2 - hl*math.cos(angle - 0.4), y2 - hl*math.sin(angle - 0.4))], fill=color, width=width)
    draw.line([(x2, y2), (x2 - hl*math.cos(angle + 0.4), y2 - hl*math.sin(angle + 0.4))], fill=color, width=width)

def new_image():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    return img, draw

# ============ IMAGE DEFINITIONS ============

images = {}

def img_0_00():
    img, draw = new_image()
    messy_text(draw, 280, 200, "AGENTIC", size=90, color="black")
    messy_text(draw, 920, 180, "?", size=120, color="red")
    messy_text(draw, 350, 420, "what does it mean??", size=35, color="gray")
    return img

def img_0_13():
    img, draw = new_image()
    # Person at computer with chatbot
    stick_figure(draw, 350, 380)
    wobbly_rect(draw, 450, 250, 600, 380, outline="black")
    messy_text(draw, 465, 290, "Hello!", size=30, color="blue")
    messy_text(draw, 460, 330, ":)", size=30, color="blue")
    wobbly_rect(draw, 450, 390, 600, 430, outline="gray")
    messy_text(draw, 200, 550, "AI = chatbots (for a decade)", size=30, color="gray")
    return img

def img_0_28():
    img, draw = new_image()
    wobbly_rect(draw, 100, 280, 300, 380, outline="blue")
    messy_text(draw, 140, 310, "INPUT", size=35, color="blue")
    arrow(draw, 310, 330, 450, 330, "black", 4)
    wobbly_rect(draw, 460, 280, 620, 380, outline="red")
    messy_text(draw, 510, 310, "AI", size=40, color="red")
    arrow(draw, 630, 330, 770, 330, "black", 4)
    wobbly_rect(draw, 780, 280, 1000, 380, outline="green")
    messy_text(draw, 810, 310, "OUTPUT", size=35, color="green")
    return img

def img_0_37():
    img, draw = new_image()
    robot(draw, 640, 380, 1.2, "blue")
    messy_text(draw, 590, 220, "Z Z Z", size=40, color="gray")
    stick_figure(draw, 400, 380)
    messy_text(draw, 300, 550, "AI waits. You act, it responds.", size=30, color="gray")
    return img

def img_0_43():
    img, draw = new_image()
    robot(draw, 400, 380, 1.2, "blue")
    # Walking legs
    wobbly_line(draw, 400, 395, 440, 440, "blue", 3)
    # Flag/goal
    wobbly_line(draw, 850, 250, 850, 450, "red", 4)
    draw.polygon([(850, 250), (950, 290), (850, 330)], fill="red")
    messy_text(draw, 870, 340, "GOAL", size=35, color="red")
    arrow(draw, 470, 370, 800, 370, "green", 4)
    messy_text(draw, 250, 560, "Agentic AI PURSUES goals", size=35, color="black")
    return img

def img_0_52():
    img, draw = new_image()
    robot(draw, 640, 350, 1.3, "blue")
    # Multiple arms with items
    wobbly_line(draw, 590, 310, 450, 200, "blue", 3)
    wobbly_rect(draw, 410, 170, 470, 210, outline="red")  # envelope
    messy_text(draw, 415, 175, "@", size=25, color="red")

    wobbly_line(draw, 690, 310, 830, 200, "blue", 3)
    wobbly_rect(draw, 810, 170, 900, 220, outline="green")  # code
    messy_text(draw, 815, 175, "</>", size=25, color="green")

    wobbly_line(draw, 590, 340, 430, 400, "blue", 3)
    wobbly_rect(draw, 380, 390, 450, 440, outline="purple")  # calendar
    messy_text(draw, 385, 395, "CAL", size=20, color="purple")

    wobbly_line(draw, 690, 340, 850, 400, "blue", 3)
    wobbly_rect(draw, 830, 390, 910, 440, outline="orange")  # file
    messy_text(draw, 835, 395, "FILE", size=20, color="orange")

    messy_text(draw, 300, 550, "emails, code, files, calendar...", size=30, color="gray")
    return img

def img_1_15():
    img, draw = new_image()
    messy_text(draw, 150, 280, "TOOL", size=70, color="blue")
    arrow(draw, 450, 320, 700, 320, "red", 6)
    messy_text(draw, 750, 280, "AGENT", size=70, color="red")
    messy_text(draw, 300, 470, "a philosophical shift", size=35, color="gray")
    return img

def img_1_29():
    img, draw = new_image()
    # Calculator
    wobbly_rect(draw, 150, 250, 300, 400, outline="blue")
    messy_text(draw, 170, 270, "1+1=2", size=25, color="blue")
    messy_text(draw, 180, 420, "calc", size=22, color="gray")
    # Magnifying glass
    wobbly_circle(draw, 530, 310, 50, outline="green")
    wobbly_line(draw, 565, 345, 610, 400, "green", 4)
    messy_text(draw, 480, 420, "search", size=22, color="gray")
    # Camera
    wobbly_rect(draw, 780, 270, 950, 390, outline="red")
    wobbly_circle(draw, 865, 330, 30, outline="red")
    messy_text(draw, 820, 420, "camera", size=22, color="gray")
    messy_text(draw, 300, 520, "TOOLS EXTEND CAPABILITY", size=35, color="black")
    return img

def img_1_45():
    img, draw = new_image()
    # Person relaxing
    stick_figure(draw, 300, 380)
    messy_text(draw, 260, 460, "*chill*", size=22, color="gray")
    # Robot working
    robot(draw, 700, 350, 1.1, "blue")
    wobbly_rect(draw, 800, 300, 900, 370, outline="blue")
    messy_text(draw, 810, 310, "WORK", size=22, color="blue")
    messy_text(draw, 300, 560, "AGENTS EXTEND AGENCY", size=38, color="red")
    return img

def img_2_07():
    img, draw = new_image()
    stick_figure(draw, 350, 380)
    wobbly_rect(draw, 500, 250, 700, 380, outline="black")
    messy_text(draw, 530, 280, "2+2", size=35, color="black")
    messy_text(draw, 530, 320, "= 5", size=35, color="red")
    # Big X
    wobbly_line(draw, 750, 240, 850, 380, "red", 6)
    wobbly_line(draw, 850, 240, 750, 380, "red", 6)
    messy_text(draw, 730, 400, "NOPE!", size=30, color="red")
    messy_text(draw, 280, 560, "tool failure = local, easy to reject", size=28, color="gray")
    return img

def img_2_25():
    img, draw = new_image()
    # Dominoes falling
    for i in range(6):
        x = 180 + i * 140
        angle = i * 12
        h = 120
        w = 30
        x1 = x - w//2
        y1 = 280
        # Tilted rectangles
        tilt = angle * 0.5
        wobbly_rect(draw, x1+int(tilt), y1-int(tilt*0.5), x1+w+int(tilt), y1+h, outline="red" if i<3 else "darkred")
    arrow(draw, 200, 230, 950, 230, "red", 3)
    messy_text(draw, 300, 480, "failure COMPOUNDS", size=45, color="red")
    messy_text(draw, 350, 540, "hard to trace, hard to reverse", size=28, color="gray")
    return img

def img_2_34():
    img, draw = new_image()
    stick_figure(draw, 350, 380)
    # Thought bubble
    wobbly_circle(draw, 550, 220, 100, outline="gray")
    robot(draw, 550, 220, 0.6, "blue")
    messy_text(draw, 530, 190, "?", size=50, color="red")
    messy_text(draw, 250, 540, "when to trust? when to override?", size=30, color="gray")
    return img

def img_2_54():
    img, draw = new_image()
    stick_figure(draw, 350, 380, 1.0, "brown")
    messy_text(draw, 280, 470, "Herbert Simon", size=35, color="black")
    messy_text(draw, 600, 250, "1955", size=70, color="blue")
    # Nobel prize medal
    wobbly_circle(draw, 800, 420, 50, fill="gold", outline="darkgoldenrod")
    messy_text(draw, 770, 400, "NOBEL", size=22, color="brown")
    return img

def img_3_07():
    img, draw = new_image()
    stick_figure(draw, 640, 250, 0.8)
    # Balance scale
    wobbly_line(draw, 640, 350, 640, 450, "black", 4)
    wobbly_line(draw, 480, 390, 800, 390, "black", 4)
    # Pans
    wobbly_circle(draw, 500, 410, 30, outline="blue")
    messy_text(draw, 480, 430, "A", size=25, color="blue")
    wobbly_circle(draw, 780, 410, 30, outline="green")
    messy_text(draw, 770, 430, "B", size=25, color="green")
    messy_text(draw, 320, 530, '"rational agent" model', size=35, color="gray")
    messy_text(draw, 320, 580, "weigh all options, pick the best", size=25, color="gray")
    return img

def img_3_33():
    img, draw = new_image()
    # The rational model
    stick_figure(draw, 640, 300, 0.7)
    wobbly_line(draw, 640, 370, 640, 430, "gray", 3)
    wobbly_line(draw, 520, 400, 760, 400, "gray", 3)
    # BIG RED X over everything
    wobbly_line(draw, 350, 180, 950, 520, "red", 10)
    wobbly_line(draw, 950, 180, 350, 520, "red", 10)
    messy_text(draw, 200, 560, "Simon said: NO. That's NOT what we do.", size=32, color="red")
    return img

def img_3_41():
    img, draw = new_image()
    # Brain in a box
    wobbly_circle(draw, 640, 300, 80, fill="pink", outline="hotpink")
    messy_text(draw, 600, 275, "BRAIN", size=30, color="darkred")
    # Box around it
    wobbly_rect(draw, 500, 180, 780, 420, outline="black", width=5)
    # Walls/limits labels
    messy_text(draw, 380, 190, "limited", size=22, color="gray")
    messy_text(draw, 380, 230, "attention", size=22, color="gray")
    messy_text(draw, 790, 190, "limited", size=22, color="gray")
    messy_text(draw, 790, 230, "memory", size=22, color="gray")
    messy_text(draw, 560, 440, "limited time", size=22, color="gray")
    messy_text(draw, 370, 550, "WE ARE BOUNDED", size=50, color="black")
    return img

def img_4_03():
    img, draw = new_image()
    # Options A B C D
    for i, letter in enumerate("ABCD"):
        x = 200 + i * 220
        wobbly_rect(draw, x, 250, x+120, 340, outline="blue" if letter != "B" else "green", width=3 if letter != "B" else 6)
        messy_text(draw, x+35, 260, letter, size=45, color="blue" if letter != "B" else "green")
    # Circle around B
    wobbly_circle(draw, 480, 295, 80, outline="green", width=5)
    messy_text(draw, 370, 400, '"good enough!"', size=45, color="green")
    messy_text(draw, 380, 520, "SATISFICING", size=50, color="black")
    return img

def img_4_23():
    img, draw = new_image()
    messy_text(draw, 150, 250, "NOT optimizers", size=50, color="red")
    # Strike through
    wobbly_line(draw, 140, 285, 650, 285, "red", 4)
    arrow(draw, 400, 340, 600, 340, "black", 5)
    messy_text(draw, 400, 380, "ADAPTERS", size=60, color="green")
    return img

def img_4_40():
    img, draw = new_image()
    # Clipboard
    wobbly_rect(draw, 350, 130, 930, 580, outline="brown")
    wobbly_rect(draw, 570, 110, 710, 150, outline="brown")
    messy_text(draw, 580, 112, "BIASES", size=28, color="brown")
    biases = ["overconfidence", "anchoring", "availability", "confirmation bias"]
    for i, b in enumerate(biases):
        y = 190 + i * 90
        wobbly_circle(draw, 400, y+15, 8, fill="red", outline="red")
        messy_text(draw, 420, y, b, size=32, color="black")
    messy_text(draw, 380, 560, "let's catalog them!", size=25, color="gray")
    return img

def img_4_59():
    img, draw = new_image()
    # Fast brain - big
    wobbly_circle(draw, 350, 320, 110, fill="yellow", outline="orange")
    messy_text(draw, 290, 290, "FAST", size=40, color="red")
    messy_text(draw, 280, 340, "intuitive", size=25, color="darkred")
    # Lightning bolt
    draw.polygon([(340, 180), (370, 250), (350, 250), (380, 200)], fill="yellow", outline="orange")
    # Slow brain - small
    wobbly_circle(draw, 850, 350, 70, fill="lightblue", outline="blue")
    messy_text(draw, 815, 330, "SLOW", size=28, color="blue")
    messy_text(draw, 810, 370, "effortful", size=18, color="darkblue")
    messy_text(draw, 300, 530, "Kahneman: System 1 & System 2", size=30, color="gray")
    return img

def img_5_16():
    img, draw = new_image()
    # HUGE fast brain
    wobbly_circle(draw, 400, 320, 160, fill="yellow", outline="orange", width=5)
    messy_text(draw, 330, 280, "FAST", size=60, color="red")
    messy_text(draw, 310, 350, "SYSTEM", size=40, color="darkred")
    # Tiny slow brain
    wobbly_circle(draw, 850, 380, 35, fill="lightblue", outline="blue")
    messy_text(draw, 830, 370, "slow", size=18, color="blue")
    messy_text(draw, 300, 560, "we lean on the fast one WAY too much", size=28, color="gray")
    return img

def img_5_29():
    img, draw = new_image()
    # Thumbs up hand (crude)
    wobbly_rect(draw, 300, 280, 380, 400, outline="black")
    wobbly_rect(draw, 340, 240, 400, 300, outline="black")
    messy_text(draw, 450, 270, "HEURISTICS", size=45, color="green")
    messy_text(draw, 450, 330, "= adaptations!", size=40, color="green")
    messy_text(draw, 400, 440, "- Gigerenzer", size=30, color="gray")
    messy_text(draw, 280, 540, "not just flaws, they're useful!", size=28, color="gray")
    return img

def img_5_48():
    img, draw = new_image()
    # Doctor stick figure
    stick_figure(draw, 400, 350, 1.0, "blue")
    # White coat hint
    wobbly_rect(draw, 370, 310, 430, 400, outline="blue")
    # Glowing gut
    wobbly_circle(draw, 400, 360, 25, fill="yellow", outline="orange")
    messy_text(draw, 380, 350, "GUT", size=18, color="red")
    # Checkmark
    wobbly_line(draw, 600, 340, 640, 380, "green", 6)
    wobbly_line(draw, 640, 380, 720, 280, "green", 6)
    messy_text(draw, 600, 400, "20 years of", size=28, color="gray")
    messy_text(draw, 600, 440, "pattern recognition", size=28, color="gray")
    messy_text(draw, 280, 560, "sometimes the gut IS right", size=30, color="black")
    return img

def img_6_02():
    img, draw = new_image()
    # Same shortcut, two situations
    # Left: fits
    wobbly_rect(draw, 100, 200, 550, 450, outline="green")
    messy_text(draw, 200, 210, "FITS", size=40, color="green")
    messy_text(draw, 150, 280, "shortcut", size=30, color="black")
    arrow(draw, 350, 310, 350, 380, "green")
    wobbly_line(draw, 310, 380, 340, 420, "green", 5)
    wobbly_line(draw, 340, 420, 410, 350, "green", 5)
    # Right: doesn't fit
    wobbly_rect(draw, 630, 200, 1100, 450, outline="red")
    messy_text(draw, 700, 210, "DOESN'T FIT", size=40, color="red")
    messy_text(draw, 700, 280, "same shortcut", size=30, color="black")
    arrow(draw, 870, 310, 870, 380, "red")
    wobbly_line(draw, 830, 360, 910, 430, "red", 5)
    wobbly_line(draw, 910, 360, 830, 430, "red", 5)
    messy_text(draw, 250, 520, "we use heuristics INDISCRIMINATELY", size=30, color="black")
    return img

def img_6_29():
    img, draw = new_image()
    messy_text(draw, 200, 200, "TRAGEDY of", size=45, color="gray")
    messy_text(draw, 200, 280, "BOUNDED", size=65, color="red")
    messy_text(draw, 200, 370, "RATIONALITY", size=65, color="red")
    # Sad face
    wobbly_circle(draw, 950, 350, 60, outline="black")
    draw.arc([910, 370, 990, 410], 0, 180, fill="black", width=3)
    draw.ellipse([925, 320, 940, 340], fill="black")
    draw.ellipse([960, 320, 975, 340], fill="black")
    messy_text(draw, 300, 520, "we can't see our own limits", size=30, color="gray")
    return img

def img_6_41():
    img, draw = new_image()
    stick_figure(draw, 500, 350)
    # Blind spot behind them (dark area)
    draw.ellipse([650, 250, 900, 450], fill="lightgray", outline="gray")
    messy_text(draw, 700, 320, "BLIND", size=30, color="gray")
    messy_text(draw, 700, 360, "SPOT", size=30, color="gray")
    # Person looking other way
    arrow(draw, 460, 290, 350, 250, "black", 3)
    messy_text(draw, 310, 230, "looking", size=22, color="black")
    messy_text(draw, 300, 520, "you don't notice what you're not attending to", size=25, color="gray")
    return img

def img_6_51():
    img, draw = new_image()
    # Brain
    wobbly_circle(draw, 400, 300, 80, fill="pink", outline="hotpink")
    # Tape recorder glitching
    wobbly_rect(draw, 600, 250, 900, 380, outline="black")
    messy_text(draw, 620, 260, "MEMORY", size=28, color="black")
    # Squiggly broken tape
    for i in range(8):
        x = 620 + i * 30
        wobbly_line(draw, x, 320+random.randint(-15,15), x+30, 320+random.randint(-15,15), "red", 2)
    messy_text(draw, 650, 340, "~glitch~", size=22, color="red")
    messy_text(draw, 280, 480, "memory RECONSTRUCTS, doesn't replay", size=28, color="black")
    messy_text(draw, 280, 530, "it feels like remembering even when you're making it up", size=22, color="gray")
    return img

def img_7_01():
    img, draw = new_image()
    stick_figure(draw, 640, 350)
    # Invisible glasses labeled BIAS
    wobbly_rect(draw, 590, 270, 690, 300, outline="red", width=2)
    messy_text(draw, 600, 272, "BIAS", size=20, color="red")
    # Dotted/invisible glasses
    for i in range(5):
        x = 595 + i*20
        draw.ellipse([x, 273, x+5, 278], fill="red")
    messy_text(draw, 350, 500, "the bias is INVISIBLE from the inside", size=30, color="red")
    messy_text(draw, 380, 550, "you feel appropriately confident", size=25, color="gray")
    return img

def img_7_05():
    img, draw = new_image()
    # Scientist in lab
    stick_figure(draw, 400, 350, 1.0, "blue")
    wobbly_rect(draw, 370, 310, 430, 400, outline="white")  # lab coat
    # Clipboard
    wobbly_rect(draw, 280, 320, 350, 400, outline="brown")
    wobbly_line(draw, 290, 340, 340, 340, "black", 1)
    wobbly_line(draw, 290, 360, 340, 360, "black", 1)
    # Microscope
    wobbly_line(draw, 700, 250, 700, 400, "gray", 4)
    wobbly_circle(draw, 700, 240, 15, outline="gray")
    wobbly_rect(draw, 660, 400, 740, 420, outline="gray")
    messy_text(draw, 300, 500, "cognitive science in the LAB", size=35, color="black")
    messy_text(draw, 300, 550, "we know so much about how we fail", size=25, color="gray")
    return img

def img_7_25():
    img, draw = new_image()
    # Canyon/gap
    wobbly_rect(draw, 100, 250, 450, 420, outline="blue")
    messy_text(draw, 140, 280, "LAB", size=35, color="blue")
    messy_text(draw, 140, 330, "KNOWLEDGE", size=30, color="blue")
    # Gap
    messy_text(draw, 520, 300, "???", size=60, color="red")
    wobbly_rect(draw, 700, 250, 1100, 420, outline="green")
    messy_text(draw, 730, 280, "REAL", size=35, color="green")
    messy_text(draw, 730, 330, "DECISIONS", size=30, color="green")
    messy_text(draw, 250, 520, "no way to use this knowledge in REAL TIME", size=28, color="gray")
    return img

def img_7_35():
    img, draw = new_image()
    # Dr. Chen
    stick_figure(draw, 350, 380, 1.0, "blue")
    messy_text(draw, 300, 470, "Dr. Chen", size=28, color="blue")
    # X-ray lightbox
    wobbly_rect(draw, 550, 200, 900, 450, fill="lightcyan", outline="gray")
    # Simple lung/body outline on scan
    wobbly_circle(draw, 725, 300, 60, outline="darkgray")
    wobbly_line(draw, 700, 250, 700, 370, "darkgray", 2)
    wobbly_line(draw, 750, 250, 750, 370, "darkgray", 2)
    # Subtle spot
    draw.ellipse([730, 310, 750, 330], fill="darkgray")
    messy_text(draw, 560, 460, "reviewing the scan...", size=25, color="gray")
    return img

def img_8_08():
    img, draw = new_image()
    stick_figure(draw, 500, 380, 1.0, "blue")
    messy_text(draw, 440, 470, "Dr. Chen", size=25, color="blue")
    # Question marks everywhere
    for pos in [(350,200), (550,180), (700,220), (380,280), (650,270)]:
        messy_text(draw, pos[0], pos[1], "?", size=50, color="red")
    messy_text(draw, 280, 560, "she needed something we didn't have", size=30, color="gray")
    return img

def img_8_14():
    img, draw = new_image()
    # Robot hand reaching out
    robot(draw, 800, 350, 1.2, "blue")
    wobbly_line(draw, 750, 330, 550, 350, "blue", 5)
    # Open hand at end
    wobbly_line(draw, 550, 350, 520, 320, "blue", 3)
    wobbly_line(draw, 550, 350, 510, 350, "blue", 3)
    wobbly_line(draw, 550, 350, 520, 380, "blue", 3)
    stick_figure(draw, 350, 380, 0.8)
    messy_text(draw, 250, 530, "agentic AI might provide it", size=35, color="green")
    return img

def img_8_41():
    img, draw = new_image()
    # Brain looking at itself in mirror
    wobbly_circle(draw, 400, 320, 80, fill="pink", outline="hotpink")
    messy_text(draw, 365, 300, "BRAIN", size=28, color="darkred")
    # Mirror
    wobbly_rect(draw, 650, 200, 900, 450, outline="gray", width=4)
    wobbly_circle(draw, 775, 320, 70, fill="pink", outline="hotpink")
    messy_text(draw, 745, 300, "BRAIN", size=24, color="darkred")
    arrow(draw, 490, 320, 640, 320, "black", 3)
    messy_text(draw, 250, 520, "METACOGNITIVE AUGMENTATION", size=35, color="black")
    messy_text(draw, 300, 570, "thinking about your own thinking", size=25, color="gray")
    return img

def img_9_03():
    img, draw = new_image()
    # Graph axes
    wobbly_line(draw, 200, 100, 200, 480, "black", 3)
    wobbly_line(draw, 200, 480, 1000, 480, "black", 3)
    # Confidence line going up
    wobbly_line(draw, 250, 420, 900, 150, "red", 4)
    messy_text(draw, 880, 120, "confidence", size=22, color="red")
    # Accuracy line going down
    wobbly_line(draw, 250, 200, 900, 440, "blue", 4)
    messy_text(draw, 880, 440, "accuracy", size=22, color="blue")
    # X mark where they cross
    messy_text(draw, 530, 280, "X", size=40, color="black")
    messy_text(draw, 300, 560, "most confident = often least accurate", size=28, color="gray")
    return img

def img_9_26():
    img, draw = new_image()
    # Person at desk
    stick_figure(draw, 400, 380)
    wobbly_rect(draw, 450, 300, 650, 400, outline="black")
    messy_text(draw, 470, 330, "work", size=25, color="black")
    # Robot sitting next to them watching
    robot(draw, 800, 350, 1.0, "blue")
    # Robot's eyes looking at screen
    arrow(draw, 770, 310, 660, 340, "blue", 2)
    # Notepad
    wobbly_rect(draw, 870, 310, 950, 380, outline="blue")
    wobbly_line(draw, 880, 330, 940, 330, "blue", 1)
    wobbly_line(draw, 880, 350, 940, 350, "blue", 1)
    messy_text(draw, 250, 530, "AI operating ALONGSIDE you", size=32, color="black")
    return img

def img_9_46():
    img, draw = new_image()
    stick_figure(draw, 400, 380)
    robot(draw, 750, 350, 0.9, "blue")
    # Magnifying glass from robot
    wobbly_circle(draw, 580, 250, 40, outline="blue", width=3)
    wobbly_line(draw, 610, 280, 650, 320, "blue", 3)
    # Patterns around person's head (invisible to them)
    for pos in [(340,230), (460,220), (380,180), (420,260)]:
        wobbly_circle(draw, pos[0], pos[1], 15, outline="lightblue")
    messy_text(draw, 250, 520, "AI sees patterns YOU can't see", size=32, color="blue")
    return img

def img_9_57():
    img, draw = new_image()
    # Wrench
    wobbly_line(draw, 350, 250, 350, 400, "gray", 6)
    wobbly_circle(draw, 350, 240, 20, outline="gray", width=4)
    # Plus
    messy_text(draw, 440, 290, "+", size=60, color="black")
    # Brain
    wobbly_circle(draw, 600, 310, 60, fill="pink", outline="hotpink")
    messy_text(draw, 572, 290, "BRAIN", size=22, color="darkred")
    messy_text(draw, 250, 480, "the DESIGN challenge:", size=32, color="black")
    messy_text(draw, 250, 530, "useful, not annoying", size=30, color="gray")
    messy_text(draw, 250, 570, "enhance judgment, not create dependence", size=25, color="gray")
    return img

def img_10_21():
    img, draw = new_image()
    messy_text(draw, 250, 230, "CEREBROTECH", size=65, color="blue")
    messy_text(draw, 500, 320, "AI", size=80, color="red")
    wobbly_circle(draw, 900, 350, 60, fill="lightblue", outline="blue")
    messy_text(draw, 870, 330, "BRAIN", size=22, color="blue")
    messy_text(draw, 300, 480, "working on making this real", size=30, color="gray")
    return img

def img_10_40():
    img, draw = new_image()
    # Expert (tall, decorated)
    stick_figure(draw, 300, 350, 1.2, "blue")
    messy_text(draw, 250, 470, "EXPERT", size=30, color="blue")
    # Big gap
    messy_text(draw, 530, 300, "GAP", size=60, color="red")
    wobbly_line(draw, 480, 250, 480, 450, "red", 3)
    wobbly_line(draw, 780, 250, 780, 450, "red", 3)
    # Novice (small, plain)
    stick_figure(draw, 900, 370, 0.8, "gray")
    messy_text(draw, 860, 470, "NOVICE", size=30, color="gray")
    messy_text(draw, 250, 560, "EXPERTISE DEMOCRATIZATION", size=35, color="black")
    return img

def img_10_59():
    img, draw = new_image()
    # Rich person with expert
    stick_figure(draw, 250, 350, 1.0, "blue")
    messy_text(draw, 210, 140, "$$$", size=40, color="green")
    stick_figure(draw, 380, 350, 0.8, "blue")
    messy_text(draw, 340, 440, "expert", size=22, color="blue")
    # VS
    messy_text(draw, 530, 310, "vs", size=50, color="red")
    # Poor person alone
    stick_figure(draw, 800, 370, 1.0, "gray")
    messy_text(draw, 760, 470, "alone", size=28, color="gray")
    messy_text(draw, 250, 560, "access to expertise is radically UNEQUAL", size=28, color="black")
    return img

def img_11_18():
    img, draw = new_image()
    # Rural doctor + AI
    stick_figure(draw, 250, 350, 0.9, "blue")
    robot(draw, 370, 340, 0.6, "green")
    messy_text(draw, 200, 460, "rural doctor", size=22, color="blue")
    # Small biz owner + AI
    stick_figure(draw, 750, 350, 0.9, "brown")
    robot(draw, 870, 340, 0.6, "green")
    messy_text(draw, 700, 460, "small biz owner", size=22, color="brown")
    messy_text(draw, 300, 550, "AI can compress the expertise gap", size=30, color="green")
    return img

def img_11_45():
    img, draw = new_image()
    # Warning triangle
    draw.polygon([(640, 150), (480, 420), (800, 420)], outline="red")
    draw.polygon([(640, 170), (500, 400), (780, 400)], fill="yellow")
    messy_text(draw, 620, 250, "!", size=80, color="red")
    messy_text(draw, 350, 490, "naive version = SERIOUS RISKS", size=35, color="red")
    messy_text(draw, 280, 550, "cognitive science predicts them precisely", size=25, color="gray")
    return img

def img_11_59():
    img, draw = new_image()
    stick_figure(draw, 350, 380)
    # AI giving advice
    robot(draw, 700, 340, 0.9, "blue")
    arrow(draw, 660, 330, 450, 330, "blue", 3)
    messy_text(draw, 460, 290, "advice", size=25, color="blue")
    # Confused face on person
    messy_text(draw, 330, 240, "???", size=40, color="red")
    # No checkmark ability
    wobbly_line(draw, 280, 490, 340, 540, "red", 4)
    wobbly_line(draw, 340, 490, 280, 540, "red", 4)
    messy_text(draw, 350, 500, "can't sanity check!", size=25, color="red")
    messy_text(draw, 260, 580, "confidence without understanding", size=25, color="gray")
    return img

def img_12_08():
    img, draw = new_image()
    # Split: left = done well, right = done poorly
    wobbly_line(draw, 640, 150, 640, 550, "black", 3)
    # Left: done well
    messy_text(draw, 200, 170, "DONE WELL", size=35, color="green")
    wobbly_line(draw, 300, 340, 340, 380, "green", 6)
    wobbly_line(draw, 340, 380, 420, 280, "green", 6)
    messy_text(draw, 200, 420, "explains reasoning", size=22, color="green")
    messy_text(draw, 200, 460, "shows uncertainty", size=22, color="green")
    messy_text(draw, 200, 500, "builds understanding", size=22, color="green")
    # Right: done poorly
    messy_text(draw, 720, 170, "DONE POORLY", size=35, color="red")
    wobbly_line(draw, 830, 290, 910, 380, "red", 6)
    wobbly_line(draw, 910, 290, 830, 380, "red", 6)
    messy_text(draw, 720, 420, "black box", size=22, color="red")
    messy_text(draw, 720, 460, "no explanation", size=22, color="red")
    messy_text(draw, 720, 500, "false confidence", size=22, color="red")
    return img

def img_12_36():
    img, draw = new_image()
    stick_figure(draw, 400, 350)
    robot(draw, 750, 340, 1.0, "blue")
    # Handshake in middle
    wobbly_line(draw, 440, 370, 550, 370, "black", 4)
    wobbly_line(draw, 700, 340, 600, 370, "blue", 4)
    wobbly_circle(draw, 575, 370, 20, outline="green", width=4)
    messy_text(draw, 280, 520, "HUMAN-AI COMPLEMENTARITY", size=35, color="black")
    messy_text(draw, 350, 580, "they fail DIFFERENTLY", size=28, color="gray")
    return img

def img_12_52():
    img, draw = new_image()
    # Human errors going left
    messy_text(draw, 150, 200, "HUMAN errors", size=32, color="red")
    for i in range(3):
        arrow(draw, 500, 260+i*40, 200, 260+i*40, "red", 3)
    # AI errors going right
    messy_text(draw, 700, 200, "AI errors", size=32, color="blue")
    for i in range(3):
        arrow(draw, 700, 260+i*40, 1050, 260+i*40, "blue", 3)
    messy_text(draw, 300, 480, "they fail in DIFFERENT directions", size=30, color="black")
    messy_text(draw, 350, 530, "consequence of how they're built", size=25, color="gray")
    return img

def img_12_59():
    img, draw = new_image()
    messy_text(draw, 200, 150, "HUMAN BIASES:", size=40, color="red")
    biases = ["anchoring on first number", "weigh recent info too heavily", "bad at probabilities", "motivated reasoning"]
    for i, b in enumerate(biases):
        wobbly_circle(draw, 230, 240+i*70, 8, fill="red", outline="red")
        messy_text(draw, 250, 225+i*70, b, size=28, color="black")
    messy_text(draw, 250, 540, "systematic, predictable, consistent", size=28, color="gray")
    return img

def img_13_11():
    img, draw = new_image()
    stick_figure(draw, 450, 380)
    # Colored glasses
    wobbly_rect(draw, 410, 300, 490, 320, fill="red", outline="darkred")
    # Evidence on left (agrees) - green check
    wobbly_rect(draw, 150, 250, 350, 350, outline="green")
    messy_text(draw, 170, 270, "agrees w/", size=22, color="green")
    messy_text(draw, 170, 300, "my belief", size=22, color="green")
    messy_text(draw, 250, 360, "sure!", size=22, color="green")
    # Evidence on right (disagrees) - red X
    wobbly_rect(draw, 600, 250, 850, 350, outline="red")
    messy_text(draw, 620, 270, "contradicts", size=22, color="red")
    messy_text(draw, 620, 300, "my belief", size=22, color="red")
    messy_text(draw, 700, 360, "SKEPTICAL", size=25, color="red")
    messy_text(draw, 280, 530, "MOTIVATED REASONING", size=35, color="red")
    return img

def img_13_30():
    img, draw = new_image()
    robot(draw, 640, 320, 1.3, "blue")
    # Speech bubble
    wobbly_circle(draw, 500, 180, 90, outline="blue")
    messy_text(draw, 440, 150, "2+2", size=35, color="blue")
    messy_text(draw, 450, 190, "= 5 !", size=35, color="red")
    # Confident pose
    messy_text(draw, 780, 300, "100%", size=30, color="blue")
    messy_text(draw, 780, 340, "sure!", size=30, color="blue")
    messy_text(draw, 280, 530, "AI fails in BIZARRE ways", size=35, color="red")
    messy_text(draw, 350, 580, "confidently wrong", size=25, color="gray")
    return img

def img_13_53():
    img, draw = new_image()
    # Venn diagram - barely overlapping
    wobbly_circle(draw, 420, 320, 150, fill=None, outline="red", width=4)
    messy_text(draw, 340, 250, "HUMAN", size=25, color="red")
    messy_text(draw, 340, 290, "failures", size=25, color="red")
    wobbly_circle(draw, 780, 320, 150, fill=None, outline="blue", width=4)
    messy_text(draw, 720, 250, "AI", size=25, color="blue")
    messy_text(draw, 700, 290, "failures", size=25, color="blue")
    # Tiny overlap
    messy_text(draw, 560, 310, "tiny", size=20, color="gray")
    messy_text(draw, 545, 340, "overlap", size=20, color="gray")
    messy_text(draw, 300, 530, "failure profiles DON'T OVERLAP much", size=28, color="black")
    return img

def img_14_18():
    img, draw = new_image()
    # Human + AI
    stick_figure(draw, 250, 300, 0.7)
    messy_text(draw, 300, 290, "+", size=40, color="black")
    robot(draw, 400, 300, 0.6, "blue")
    # Greater than
    messy_text(draw, 500, 270, ">", size=80, color="green")
    # Human alone
    stick_figure(draw, 700, 300, 0.6, "gray")
    messy_text(draw, 780, 310, "or", size=30, color="gray")
    robot(draw, 900, 300, 0.5, "gray")
    messy_text(draw, 250, 450, "TEAMS > either alone", size=40, color="green")
    messy_text(draw, 300, 520, "each checks the other where they fail", size=25, color="gray")
    return img

def img_14_45():
    img, draw = new_image()
    # Stethoscope
    wobbly_circle(draw, 250, 300, 30, outline="red")
    wobbly_line(draw, 250, 270, 220, 200, "red", 3)
    wobbly_line(draw, 250, 270, 280, 200, "red", 3)
    messy_text(draw, 200, 370, "medical", size=25, color="red")
    # Gavel
    wobbly_rect(draw, 560, 250, 620, 290, fill="brown", outline="brown")
    wobbly_line(draw, 590, 290, 590, 360, "brown", 4)
    messy_text(draw, 540, 370, "legal", size=25, color="brown")
    # Shield
    draw.polygon([(900, 230), (850, 280), (870, 360), (900, 380), (930, 360), (950, 280)], outline="blue")
    messy_text(draw, 850, 390, "cyber", size=25, color="blue")
    messy_text(draw, 250, 500, "paired systems OUTPERFORM", size=35, color="green")
    messy_text(draw, 300, 550, "best human + best AI alone", size=28, color="gray")
    return img

def img_14_59():
    img, draw = new_image()
    messy_text(draw, 200, 220, "AUGMENTATION", size=55, color="green")
    # Circle around it
    wobbly_circle(draw, 550, 260, 180, outline="green", width=4)
    messy_text(draw, 350, 380, "not", size=40, color="gray")
    messy_text(draw, 200, 440, "REPLACEMENT", size=55, color="red")
    # Strikethrough
    wobbly_line(draw, 190, 475, 780, 475, "red", 5)
    return img

def img_15_20():
    img, draw = new_image()
    # Caution sign
    draw.polygon([(640, 130), (430, 400), (850, 400)], outline="orange", width=4)
    draw.polygon([(640, 160), (460, 380), (820, 380)], fill="yellow")
    messy_text(draw, 590, 220, "BUT...", size=50, color="red")
    messy_text(draw, 350, 470, "there's a CONDITION attached", size=32, color="black")
    messy_text(draw, 300, 530, "to everything I just said", size=28, color="gray")
    return img

def img_15_32():
    img, draw = new_image()
    stick_figure(draw, 400, 380)
    # Mirror
    wobbly_rect(draw, 650, 200, 900, 480, outline="gray", width=5)
    # Reflection
    stick_figure(draw, 775, 380, 0.9, "lightblue")
    messy_text(draw, 350, 530, "requires WANTING to see ourselves clearly", size=28, color="black")
    messy_text(draw, 350, 580, "...one of the hardest things to want", size=25, color="gray")
    return img

def img_15_54():
    img, draw = new_image()
    # Big happy face
    wobbly_circle(draw, 640, 280, 120, fill="yellow", outline="orange", width=4)
    # Smile
    draw.arc([570, 280, 710, 360], 0, 180, fill="black", width=4)
    # Eyes
    draw.ellipse([590, 240, 615, 270], fill="black")
    draw.ellipse([665, 240, 690, 270], fill="black")
    messy_text(draw, 380, 440, "OVERCONFIDENCE", size=45, color="red")
    messy_text(draw, 400, 510, "it feels GOOD", size=35, color="gray")
    messy_text(draw, 350, 570, "provides motivation, simplifies decisions", size=22, color="gray")
    return img

def img_16_07():
    img, draw = new_image()
    # Confident leader on podium
    wobbly_rect(draw, 250, 400, 450, 460, outline="black")
    stick_figure(draw, 350, 340, 0.8, "blue")
    messy_text(draw, 310, 250, "I KNOW", size=25, color="blue")
    # Uncertain person
    stick_figure(draw, 750, 400, 0.7, "gray")
    messy_text(draw, 700, 340, "um...", size=25, color="gray")
    messy_text(draw, 700, 480, "I'm not sure", size=22, color="gray")
    # Hand raised
    wobbly_line(draw, 780, 370, 810, 310, "gray", 3)
    messy_text(draw, 250, 540, "social REWARDS for confidence", size=30, color="black")
    messy_text(draw, 280, 580, "social COSTS for uncertainty", size=28, color="gray")
    return img

def img_16_20():
    img, draw = new_image()
    # Wolf in sheep's clothing
    wobbly_circle(draw, 640, 300, 100, fill="white", outline="gray", width=3)
    messy_text(draw, 580, 260, "GOOD", size=30, color="gray")
    messy_text(draw, 560, 300, "JUDGMENT", size=30, color="gray")
    # Scary eyes peeking
    draw.ellipse([600, 335, 630, 355], fill="red")
    draw.ellipse([660, 335, 690, 355], fill="red")
    messy_text(draw, 580, 370, "(actually bias)", size=22, color="red")
    messy_text(draw, 300, 500, "biases DISGUISED as expertise", size=32, color="red")
    return img

def img_16_26():
    img, draw = new_image()
    # Person in bubble
    stick_figure(draw, 640, 350)
    wobbly_circle(draw, 640, 330, 150, outline="red", width=4)
    # Echo arrows bouncing inside
    arrow(draw, 530, 270, 610, 320, "orange", 2)
    arrow(draw, 680, 250, 650, 300, "orange", 2)
    arrow(draw, 750, 310, 700, 350, "orange", 2)
    messy_text(draw, 300, 530, "BIGGEST RISK: echo chamber", size=32, color="red")
    messy_text(draw, 280, 580, "AI reinforcing what you already believe", size=25, color="gray")
    return img

def img_17_01():
    img, draw = new_image()
    # Big eyeball
    wobbly_circle(draw, 640, 280, 100, fill="white", outline="black", width=4)
    wobbly_circle(draw, 640, 280, 50, fill="brown", outline="saddlebrown")
    wobbly_circle(draw, 640, 280, 20, fill="black", outline="black")
    messy_text(draw, 400, 430, "OBSERVABLE", size=50, color="red")
    messy_text(draw, 500, 500, "NOW", size=60, color="red")
    messy_text(draw, 350, 590, "not hypothetical - happening TODAY", size=25, color="gray")
    return img

def img_17_11():
    img, draw = new_image()
    # Hiring conveyor belt
    wobbly_line(draw, 150, 350, 1100, 350, "gray", 5)
    # Resumes on belt
    for i, color in enumerate(["green", "green", "red", "green", "red"]):
        x = 200 + i * 180
        wobbly_rect(draw, x, 300, x+80, 345, outline=color)
        stick_figure(draw, x+40, 290, 0.3, color)
    messy_text(draw, 400, 180, "HIRING ALGORITHM", size=35, color="black")
    arrow(draw, 640, 230, 640, 290, "black", 3)
    messy_text(draw, 300, 420, "replicating historical biases", size=30, color="red")
    messy_text(draw, 280, 480, "recommendation systems distorting reality", size=25, color="gray")
    return img

def img_17_30():
    img, draw = new_image()
    stick_figure(draw, 450, 350, 1.0, "blue")
    messy_text(draw, 400, 250, "???", size=50, color="blue")
    # Complex structure
    wobbly_rect(draw, 650, 200, 1000, 480, outline="gray")
    for i in range(4):
        for j in range(3):
            wobbly_rect(draw, 670+j*100, 220+i*60, 730+j*100, 260+i*60, outline="gray")
    messy_text(draw, 250, 530, "not MALICIOUS, just genuinely HARD", size=30, color="black")
    return img

def img_17_46():
    img, draw = new_image()
    # Balance scale
    wobbly_line(draw, 640, 180, 640, 280, "black", 4)
    wobbly_line(draw, 400, 250, 880, 250, "black", 4)
    # HOPE side
    wobbly_circle(draw, 430, 300, 60, fill="lightyellow", outline="green")
    messy_text(draw, 395, 280, "HOPE", size=28, color="green")
    # SCIENCE side
    wobbly_circle(draw, 850, 300, 60, fill="lightcyan", outline="blue")
    messy_text(draw, 800, 280, "SCIENCE", size=22, color="blue")
    messy_text(draw, 300, 430, "hopeful IF we take the science seriously", size=30, color="black")
    return img

def img_18_00():
    img, draw = new_image()
    # Blueprint paper
    wobbly_rect(draw, 200, 150, 1050, 450, fill="lightcyan", outline="blue")
    # Grid lines
    for i in range(5):
        wobbly_line(draw, 200, 210+i*50, 1050, 210+i*50, "lightblue", 1)
    for i in range(7):
        wobbly_line(draw, 320+i*100, 150, 320+i*100, 450, "lightblue", 1)
    messy_text(draw, 280, 250, "DESIGN FOR", size=40, color="blue")
    messy_text(draw, 280, 320, "BOUNDED REASONERS", size=40, color="blue")
    messy_text(draw, 300, 520, "make cognitive failure VISIBLE", size=28, color="black")
    return img

def img_18_32():
    img, draw = new_image()
    # Waving hand (crude)
    wobbly_rect(draw, 500, 200, 580, 350, outline="black")
    for i in range(4):
        wobbly_line(draw, 510+i*20, 200, 510+i*20, 160, "black", 3)
    messy_text(draw, 250, 400, "what I want to", size=40, color="gray")
    messy_text(draw, 250, 460, "LEAVE YOU WITH", size=50, color="black")
    return img

def img_18_52():
    img, draw = new_image()
    # Brain with chains
    wobbly_circle(draw, 640, 300, 100, fill="pink", outline="hotpink")
    messy_text(draw, 605, 280, "BRAIN", size=28, color="darkred")
    # Chains (zigzag lines)
    for angle_start in [0, 60, 120, 180, 240, 300]:
        a = math.radians(angle_start)
        x1 = 640 + int(100*math.cos(a))
        y1 = 300 + int(100*math.sin(a))
        x2 = 640 + int(150*math.cos(a))
        y2 = 300 + int(150*math.sin(a))
        wobbly_line(draw, x1, y1, x2, y2, "gray", 4)
    messy_text(draw, 300, 470, "WE ARE BOUNDED", size=45, color="red")
    messy_text(draw, 350, 540, "AND BIASED", size=45, color="red")
    return img

def img_19_04():
    img, draw = new_image()
    # Book
    wobbly_rect(draw, 150, 230, 330, 400, fill="lightblue", outline="blue")
    messy_text(draw, 170, 280, "research", size=22, color="blue")
    messy_text(draw, 170, 320, "paper", size=22, color="blue")
    # Classroom
    wobbly_rect(draw, 430, 200, 700, 380, fill="darkgreen", outline="green")
    messy_text(draw, 460, 240, "E = mc2", size=25, color="white")
    messy_text(draw, 450, 400, "classroom", size=22, color="gray")
    # Bestseller
    wobbly_rect(draw, 800, 230, 1000, 400, fill="lightyellow", outline="orange")
    messy_text(draw, 820, 270, "BEST", size=22, color="red")
    messy_text(draw, 820, 300, "SELLER", size=22, color="red")
    messy_text(draw, 250, 490, "for a long time: only ACADEMIC interest", size=28, color="gray")
    messy_text(draw, 280, 540, "you couldn't DO much with it in real time", size=25, color="gray")
    return img

def img_19_19():
    img, draw = new_image()
    # Old equation crossed out
    messy_text(draw, 200, 200, "old equation", size=35, color="gray")
    wobbly_line(draw, 190, 230, 520, 230, "red", 5)
    # Arrow down
    arrow(draw, 450, 280, 450, 350, "black", 4)
    # New equation with AI
    messy_text(draw, 200, 370, "NEW EQUATION", size=45, color="green")
    messy_text(draw, 750, 380, "+ AI", size=50, color="blue")
    messy_text(draw, 250, 520, "agentic AI CHANGES the equation", size=30, color="black")
    return img

def img_19_37():
    img, draw = new_image()
    # Lightbulb
    wobbly_circle(draw, 640, 250, 80, fill="yellow", outline="orange", width=4)
    wobbly_rect(draw, 615, 330, 665, 370, outline="gray")
    # Rays
    for angle_start in [0, 45, 90, 135, 180, 225, 270, 315]:
        a = math.radians(angle_start)
        x1 = 640 + int(90*math.cos(a))
        y1 = 250 + int(90*math.sin(a))
        x2 = 640 + int(130*math.cos(a))
        y2 = 250 + int(130*math.sin(a))
        wobbly_line(draw, x1, y1, x2, y2, "orange", 3)
    messy_text(draw, 300, 430, "making the INVISIBLE", size=40, color="black")
    messy_text(draw, 400, 490, "VISIBLE", size=55, color="green")
    return img

def img_19_52():
    img, draw = new_image()
    # Star
    draw.polygon([(640,120), (670,230), (780,230), (690,300), (720,410), (640,340), (560,410), (590,300), (500,230), (610,230)], fill="gold", outline="darkgoldenrod")
    messy_text(draw, 200, 460, "most SIGNIFICANT cognitive", size=35, color="black")
    messy_text(draw, 250, 510, "tool in HISTORY", size=40, color="black")
    return img

def img_20_15():
    img, draw = new_image()
    stick_figure(draw, 640, 350, 1.3, "blue")
    # Raised fist
    wobbly_line(draw, 670, 310, 700, 230, "blue", 5)
    wobbly_rect(draw, 685, 200, 720, 240, fill="blue", outline="blue")
    messy_text(draw, 350, 520, "WE WILL DO IT", size=55, color="green")
    return img

def img_20_26():
    img, draw = new_image()
    # Cave (dark area)
    draw.rectangle([0, 0, W, H], fill="dimgray")
    # Fire
    draw.polygon([(600, 500), (640, 300), (680, 500)], fill="orange")
    draw.polygon([(620, 500), (640, 350), (660, 500)], fill="yellow")
    # Light circle from fire
    for r in range(200, 50, -30):
        alpha_color = f"#{min(255,100+r):02x}{min(255,80+r):02x}{60:02x}"
        try:
            draw.ellipse([640-r, 400-r//2, 640+r, 400+r//2], fill=None, outline="orange", width=1)
        except:
            pass
    draw.ellipse([500, 300, 780, 530], fill=None, outline="orange", width=2)
    messy_text(draw, 300, 100, "FIRE didn't make us warm", size=35, color="white")
    messy_text(draw, 300, 160, "it made the dark VISIBLE", size=35, color="yellow")
    return img

def img_20_30():
    img, draw = new_image()
    # Scroll/paper
    wobbly_rect(draw, 200, 180, 500, 450, fill="lightyellow", outline="brown")
    for i in range(5):
        wobbly_line(draw, 230, 220+i*40, 470, 220+i*40, "gray", 1)
    # Two heads with thought transferring
    wobbly_circle(draw, 700, 250, 40, outline="blue")
    wobbly_circle(draw, 900, 250, 40, outline="green")
    # Thought bubbles between
    arrow(draw, 750, 250, 850, 250, "purple", 3)
    messy_text(draw, 740, 200, "THOUGHT", size=22, color="purple")
    messy_text(draw, 250, 520, "writing made thought TRANSFERABLE", size=30, color="black")
    return img

def img_20_40():
    img, draw = new_image()
    # Sunrise
    draw.rectangle([0, 400, W, H], fill="lightgreen")
    draw.rectangle([0, 0, W, 400], fill="lightyellow")
    # Sun peeking
    wobbly_circle(draw, 640, 400, 80, fill="yellow", outline="orange", width=4)
    # Rays
    for angle_start in range(180, 361, 30):
        a = math.radians(angle_start)
        x1 = 640 + int(90*math.cos(a))
        y1 = 400 + int(90*math.sin(a))
        x2 = 640 + int(160*math.cos(a))
        y2 = 400 + int(160*math.sin(a))
        wobbly_line(draw, x1, y1, x2, y2, "orange", 3)
    messy_text(draw, 350, 120, "THE BEGINNING", size=55, color="black")
    messy_text(draw, 300, 200, "of something remarkable", size=30, color="gray")
    return img

def img_20_52():
    img, draw = new_image()
    stick_figure(draw, 350, 380, 1.0, "blue")
    messy_text(draw, 300, 470, "Dr. Chen", size=25, color="blue")
    # Scan
    wobbly_rect(draw, 500, 250, 700, 420, fill="lightcyan", outline="gray")
    # Robot next to her
    robot(draw, 850, 360, 0.9, "green")
    messy_text(draw, 250, 540, "the radiologist and the patient who came back", size=25, color="gray")
    messy_text(draw, 250, 580, "the CENTRAL question of the next decade", size=25, color="black")
    return img

def img_21_09():
    img, draw = new_image()
    stick_figure(draw, 640, 380)
    # Old belief crossed out
    wobbly_rect(draw, 250, 200, 500, 280, outline="red")
    messy_text(draw, 270, 220, "old belief", size=30, color="red")
    wobbly_line(draw, 240, 240, 510, 240, "red", 5)
    # Arrow
    arrow(draw, 520, 240, 620, 240, "black", 3)
    # New belief
    wobbly_rect(draw, 650, 200, 950, 280, outline="green")
    messy_text(draw, 670, 220, "new belief", size=30, color="green")
    messy_text(draw, 250, 520, "what does it TAKE to UPDATE?", size=32, color="black")
    messy_text(draw, 280, 570, "to override yourself in the moment", size=25, color="gray")
    return img

def img_21_37():
    img, draw = new_image()
    messy_text(draw, 200, 200, "NEXT EPISODE:", size=45, color="gray")
    messy_text(draw, 200, 300, "THE SCIENCE", size=55, color="blue")
    messy_text(draw, 200, 390, "OF TRUST", size=60, color="blue")
    messy_text(draw, 250, 510, "when to trust an algorithm", size=30, color="gray")
    messy_text(draw, 250, 560, "and when NOT to", size=30, color="red")
    return img

def img_21_46():
    img, draw = new_image()
    stick_figure(draw, 640, 350, 1.3)
    # Waving arm
    wobbly_line(draw, 670, 310, 750, 230, "black", 4)
    wobbly_line(draw, 750, 230, 780, 210, "black", 3)
    wobbly_line(draw, 750, 230, 770, 240, "black", 3)
    wobbly_line(draw, 750, 230, 760, 250, "black", 3)
    messy_text(draw, 350, 520, "SEE YOU THEN!", size=55, color="blue")
    return img

# ============ GENERATE ALL ============

all_images = {
    "0-00": img_0_00,
    "0-13": img_0_13,
    "0-28": img_0_28,
    "0-37": img_0_37,
    "0-43": img_0_43,
    "0-52": img_0_52,
    "1-15": img_1_15,
    "1-29": img_1_29,
    "1-45": img_1_45,
    "2-07": img_2_07,
    "2-25": img_2_25,
    "2-34": img_2_34,
    "2-54": img_2_54,
    "3-07": img_3_07,
    "3-33": img_3_33,
    "3-41": img_3_41,
    "4-03": img_4_03,
    "4-23": img_4_23,
    "4-40": img_4_40,
    "4-59": img_4_59,
    "5-16": img_5_16,
    "5-29": img_5_29,
    "5-48": img_5_48,
    "6-02": img_6_02,
    "6-29": img_6_29,
    "6-41": img_6_41,
    "6-51": img_6_51,
    "7-01": img_7_01,
    "7-05": img_7_05,
    "7-25": img_7_25,
    "7-35": img_7_35,
    "8-08": img_8_08,
    "8-14": img_8_14,
    "8-41": img_8_41,
    "9-03": img_9_03,
    "9-26": img_9_26,
    "9-46": img_9_46,
    "9-57": img_9_57,
    "10-21": img_10_21,
    "10-40": img_10_40,
    "10-59": img_10_59,
    "11-18": img_11_18,
    "11-45": img_11_45,
    "11-59": img_11_59,
    "12-08": img_12_08,
    "12-36": img_12_36,
    "12-52": img_12_52,
    "12-59": img_12_59,
    "13-11": img_13_11,
    "13-30": img_13_30,
    "13-53": img_13_53,
    "14-18": img_14_18,
    "14-45": img_14_45,
    "14-59": img_14_59,
    "15-20": img_15_20,
    "15-32": img_15_32,
    "15-54": img_15_54,
    "16-07": img_16_07,
    "16-20": img_16_20,
    "16-26": img_16_26,
    "17-01": img_17_01,
    "17-11": img_17_11,
    "17-30": img_17_30,
    "17-46": img_17_46,
    "18-00": img_18_00,
    "18-32": img_18_32,
    "18-52": img_18_52,
    "19-04": img_19_04,
    "19-19": img_19_19,
    "19-37": img_19_37,
    "19-52": img_19_52,
    "20-15": img_20_15,
    "20-26": img_20_26,
    "20-30": img_20_30,
    "20-40": img_20_40,
    "20-52": img_20_52,
    "21-09": img_21_09,
    "21-37": img_21_37,
    "21-46": img_21_46,
}

output_dir = "/home/user/hermes-desktop/youtube-images/final"
import os
os.makedirs(output_dir, exist_ok=True)

for timestamp, func in all_images.items():
    random.seed(42)  # Reset seed for consistency within each image
    img = func()
    filename = f"{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    print(f"Created: {filename}")

print(f"\nDone! {len(all_images)} images created in {output_dir}")
