"""Genera el icono minimalista de reloj para SHIFTMODE."""
from PIL import Image, ImageDraw

WIDTH, HEIGHT = 256, 256
img = Image.new("RGBA", (WIDTH, HEIGHT), (243, 245, 248, 255))
draw = ImageDraw.Draw(img)

# Círculo exterior
outer = (20, 20, 236, 236)
draw.ellipse(outer, outline=(0, 102, 255, 255), width=14, fill=(255, 255, 255, 255))

# Reloj
clock_center = (128, 128)
clock_radius = 92
draw.ellipse((36, 36, 220, 220), outline=(18, 18, 18, 255), width=10)

# Agujas
hand_long = (128, 128, 128, 67)
hand_short = (128, 128, 167, 108)
draw.line(hand_long, fill=(18, 18, 18, 255), width=10)
draw.line(hand_short, fill=(255, 107, 87, 255), width=10)

# Centro
draw.ellipse((118, 118, 138, 138), fill=(255, 107, 87, 255))

# Horas marcadas
for angle in range(0, 360, 30):
    radians = angle * 3.14159 / 180
    x1 = 128 + int((clock_radius - 20) * __import__('math').cos(radians))
    y1 = 128 + int((clock_radius - 20) * __import__('math').sin(radians))
    x2 = 128 + int((clock_radius) * __import__('math').cos(radians))
    y2 = 128 + int((clock_radius) * __import__('math').sin(radians))
    draw.line((x1, y1, x2, y2), fill=(18, 18, 18, 255), width=4)

# Guardar ICO
img.save("assets/icon.ico")
print("Icono generado: assets/icon.ico")
