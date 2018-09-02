import axi
import math
import random
import noise
from pprint import pprint as pp
from functools import partial
from itertools import groupby

A4_SIZE = (11.69, 8.27)
A4_BOUNDS = (0, 0, 11.69, 8.27)
H, W = A4_SIZE

def circle(r, a):
    return [(r * math.cos(math.tau * i / a), r * math.sin(math.tau * i / a)) for i in range(a)]
def grid(w, h, s):
    return [(x / s, y / s) for x in range(math.floor(w * s)) for y in range(math.floor(h * 10))]
def grid_random(w, h, n):
    return [(W * random.random(), H * random.random()) for i in range(n)]

def bound_circle(r, p):
    (x, y) = p
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2)) < r
def bound_box(W, H, p):
    (x, y) = p
    return x > 0 and x < W and y > 0 and y < H

def cull(f, paths):
    return [
        list(g)
        for path in paths
        for k, g in groupby([
            p if f(p) else None
            for p in path
        ])
        if k is not None
    ]

def smooth_line(p, unit=False):
    path = []
    (x, y) = p
    for j in range(400):
        scale0 = 0.01
        scale1 = 0.2
        dx = scale0 * noise.snoise2(scale1 * x, scale1 * y, octaves=2)
        dy = scale0 * noise.snoise2(1000 + scale1 * x, scale1 * y, octaves=4)
        if unit:
            len = math.sqrt(dx * dx + dy * dy)
            if len != 0:
                dx *= 0.01 / len
                dy *= 0.01 / len
        x += dx
        y += dy
        path.append((x, y))
    return path

def main():
    random.seed(0xfeed)

    paths = []

    sketch = 7
    if sketch == 0:
        for n in range(0, 100000):
            x = random.random() * W
            y = random.random() * H
            path = [
                (x, y)
            ]
            paths.append(path)

    elif sketch == 1:
        for n in range(0, 40000):
            x = random.random() * W
            y = random.random() * H
            angle = -0.1 + 0.2 * random.random()
            radius = 0.1 * random.random()
            path = [
                (x - radius * math.cos(angle), y - radius * math.sin(angle)),
                (x + radius * math.cos(angle), y + radius * math.sin(angle))
            ]
            paths.append(path)

    elif sketch == 2:
        for n in range(0, 40000):
            x = random.random() * W
            y = random.random() * H
            angle = math.tau * random.random()
            radius = 0.2 * random.random()
            path = [
                (x - radius * math.cos(angle), y - radius * math.sin(angle)),
                (x + radius * math.cos(angle), y + radius * math.sin(angle))
            ]
            paths.append(path)


    elif sketch == 3:
        for x_ in range(math.floor(W * 10)):
            for y_ in range(math.floor(H * 10)):
                x = x_ / 10
                y = y_ / 10
                angle = math.tau * random.random()
                radius = 0.1 * random.random()
                path = [
                    (x - radius * math.cos(angle), y - radius * math.sin(angle)),
                    (x + radius * math.cos(angle), y + radius * math.sin(angle))
                ]
                paths.append(path)

    elif sketch == 4:
        for x_ in range(math.floor(W * 10)):
            for y_ in range(math.floor(H * 10)):
                x = x_ / 10
                y = y_ / 10
                dx = math.sin((x - W/2) / W)
                dy = math.sin((y - H/2) / W)
                #toggle dy between cos and sin
                path = [
                    (x - dx, y - dy),
                    (x + dx, y + dy)
                ]
                paths.append(path)

    elif sketch == 5:
        for x_ in range(math.floor(W * 10)):
            for y_ in range(math.floor(H * 10)):
                x = x_ / 10
                y = y_ / 10
                dx = (y - H/2) / W
                dy = (x - W/2) / W
                #toggle dy positive and negative
                path = [
                    (x - dx, y - dy),
                    (x + dx, y + dy)
                ]
                paths.append(path)

    elif sketch == 6:
        for n in range(40000):
            x = W * random.random()
            y = H * random.random()
            angle = 8 / 16 * random.random()
            radius = 0.2 * noise.snoise2(x, y)
            dx = radius * math.cos(angle)
            dy = radius * math.sin(angle)
            path = [
                (x - dx, y - dy),
                (x + dx, y + dy)
            ]
            paths.append(path)

    elif sketch == 7:
        for x_ in range(math.floor(W * 10)):
            for y_ in range(math.floor(H * 10)):
                x = x_ / 10
                y = y_ / 10
                angle = math.tau / 16
                radius = 0.4 * noise.snoise2(x, y)
                dx = radius * math.cos(angle)
                dy = radius * math.sin(angle)
                path = [
                    (x - dx, y - dy),
                    (x + dx, y + dy)
                ]
                paths.append(path)

    elif sketch == 8:
        for m in range(4):
            x = W / 2
            y = H / 2
            path = [(x, y)]
            for n in range(4000):
                angle = math.tau / 6 * random.randrange(6)
                radius = 0.1
                dx = radius * math.cos(angle)
                dy = radius * math.sin(angle)
                x += dx
                y += dy
                path.append((x, y))
            paths.append(path)

    elif sketch == 9:
        for m in range(40):
            radius = random.gauss(W / 4, W / 12)
            path = []
            for n in range(360 + 1):
                angle = math.tau * n / 360
                path.append((W / 2 + radius * math.cos(angle), H / 2 + radius * math.sin(angle)))
            paths.append(path)

    elif sketch == 10:
        paths = cull(partial(bound_box, W, H), map(partial(smooth_line, unit=True), grid_random(W, H, 1000)))
    elif sketch == 11:
        paths = map(smooth_line, circle(0.3 * W, 300))
    elif sketch == 12:
        paths = map(smooth_line, grid_random(W, H, 1000))

    elif sketch == 13:
        def point_density(p):
            (x, y) = p
            scale0 = 0.2
            return random.random() < 0.5 + 0.5 * noise.snoise2(scale0 * x, scale0 * y, octaves=4, persistence=0.5)
        paths = [[l] for l in filter(point_density, grid_random(W, H, 1000000))]

    elif sketch == 14:
        for i in range(2):
            x, y = random.random() * W, random.random() * H
            path = []
            path.append((x, y))
            for angle in range(8000):
                radius = angle * 0.00004
                x += radius * math.cos(math.tau * angle * 0.01)
                y += radius * math.sin(math.tau * angle * 0.01)
                path.append((x, y))
            paths.append(path)

    d = axi.Drawing(paths)

    #d = d.sort_paths()
    #d = d.join_paths(0.01)
    #d = d.simplify_paths(0.001)
    d = d.rotate(-90).move(H / 2, W / 2, 0.5, 0.5)

    d.dump('out.axi')
    d.render(bounds=A4_BOUNDS, show_bounds=False).write_to_png('out.png'.format(sketch))

if __name__ == '__main__':
    main()
