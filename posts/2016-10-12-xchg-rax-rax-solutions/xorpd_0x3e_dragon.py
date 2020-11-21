from __future__ import print_function
from PIL import Image, ImageDraw, ImageColor
import struct

# Utility function for mapping list of colors names
def get_colors(colors, mode='RGB'):
    if colors is None:
        colors = 'black'
    return list(map(lambda x: ImageColor.getcolor(x, mode), colors.split(',')))

def popcount(x):
    n = 0
    while x:
        n += 1
        x &= (x - 1)  # Clear the bottom-most set bit - cf snippet 0x2f
    return n

def floor_log2(x):
	if x < 0:
		raise ValueError('floor_log2(): argument must be positive')
	if x == 0:
		return 0		# A bit inconsistent
	return (struct.unpack('<L', struct.pack('<f', float(x)))[0] >> 23) - 127

def draw_dragon(n, size, mg, width=1, colors=None, mode='RGB'):
	# Directions in space
	dx = [ 0, 1,  0, -1 ]
	dy = [ 1, 0, -1,  0 ]

	img = Image.new(mode, (size, 5 * size / 6 + width - 2), get_colors('white', mode)[0])
	draw = ImageDraw.Draw(img)
	pos = (2 * size / 3, size / 6)
	colors = get_colors(colors, mode)

	for i in range(1 << n):
		dirn = popcount(i ^ (i >> 1)) & 3
		npos = (pos[0] + mg * dx[dirn], pos[1] - mg * dy[dirn])
		color = colors[floor_log2(i) % len(colors)]
		draw.line([ pos, npos ], fill=color, width=width)
		pos = npos
	return img

img = draw_dragon(13, size=512, mg=4, colors='blue,purple,orange,red,gold', width=3)
img.show()
img.save('xorpd_0x3e_dragon.png', 'PNG', optimize=True)


