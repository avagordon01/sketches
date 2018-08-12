import axi
import math
import random
import noise

H, W = axi.A3_SIZE

def main():
    paths = []

    sketch = 8
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

    d = axi.Drawing(paths)

    d = d.join_paths(0.01)
    d = d.simplify_paths(0.001)
    d = d.rotate(-90).move(H / 2, W / 2, 0.5, 0.5)

    d.dump('out.axi')
    d.render(bounds=axi.A3_BOUNDS, show_bounds=False).write_to_png('{}.png'.format(sketch))

if __name__ == '__main__':
    main()
