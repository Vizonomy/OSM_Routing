#!/usr/bin/python3

import math
from PIL import Image, ImageDraw
import pygtfs

print("Transit access test")

sched = pygtfs.Schedule("gtfs.sqlite")

routes = []

for line in ("SILVER", "GREEN", "BLUE", "RED", "YELLOW", "ORANGE"):
	route = sched.routes_by_id(line)[0]
#for route in sched.routes:
#	if len(route.trips) < 11:
#		continue
	routes.append([])
	for stop_time in sorted(route.trips[10].stop_times,
			key=lambda a: a.stop_sequence):
		stop = stop_time.stop
		#print("%s: %s at %g %g" % (line, stop.stop_name, stop.stop_lat, stop.stop_lon))
		routes[-1].append((stop.stop_lat, stop.stop_lon))

print(routes)
#routes = (((25, 30), (25, 40), (35, 45), (45, 55), (55, 65), (70, 65),
#	(90, 65), (120, 65), (140, 65), (150, 50), (160, 40), (170, 30)),
#        ((150, 50), (150, 60), (150, 80), (150, 100), (150, 120), (150, 150),
#	(150, 250), (150, 300), (150, 350)))

min_lat = min(map(lambda x: min(map(lambda y: y[0], x)), routes))
max_lat = max(map(lambda x: max(map(lambda y: y[0], x)), routes))
min_lon = min(map(lambda x: min(map(lambda y: y[1], x)), routes))
max_lon = max(map(lambda x: max(map(lambda y: y[1], x)), routes))
print(min_lat, max_lat, min_lon, max_lon)
extent = max(max_lat - min_lat, max_lon - min_lon)
size = 1000
step = 5
scale = 0.8 * size / extent
min_lon -= 100 / scale
max_lat += 100 / scale
print(extent, scale)

im = Image.new("RGB", (size, size), "orange")

draw = ImageDraw.Draw(im)

def get_distance_to_stop(routes, x, y):
	distance = 10000000
	for route in routes:
		for station in route:
			sx, sy = station
			d = (sx - x) ** 2 + (sy - y) ** 2
			distance = min(d, distance)
	return math.sqrt(distance)

def get_colour(distance):
	green = max(0, int(0xff * (1.0 - distance / 50.)))
	return green << 8


for x in range(0, size, step):
	for y in range(0, size, step):
		lat = max_lat - (y + step * .5) / scale
		lon = min_lon + (x + step * .5) / scale
		distance = get_distance_to_stop(routes, lat, lon)
		#draw.point((x, y), fill=get_colour(distance))
		draw.rectangle((x, y, x + step, y + step),
				fill=get_colour(distance * scale))


for route in routes:
	line = map(lambda z: ((z[1] - min_lon) * scale, (max_lat - z[0]) * scale), route)
	draw.line(list(line), width=2)
	for station in route:
		x = (station[1] - min_lon) * scale
		y = (max_lat - station[0]) * scale
		draw.ellipse((x-3, y-3, x+3, y+3), fill=0x44ddff, outline=0x000000)

im.save("distance.png")


