import axi
import math
import ephem

H, W = axi.A3_SIZE

def circle(x, y, r, num=60):
    path = []
    for i in range(num + 1):
        a = math.tau * i / num
        path.append((x + r * math.cos(a), y + r * math.sin(a)))
    return path

def main():
    paths = []

    planets = [ephem.Mercury(), ephem.Venus(), ephem.Sun(), ephem.Mars(), ephem.Jupiter(), ephem.Saturn(), ephem.Uranus(), ephem.Neptune()]
    radii = [2440, 6052, 6371, 3390, 69911, 58232, 25362, 24622]

    for n, p in enumerate(planets):
        path = []
        for i in range(365 * 10):
            date = ephem.Date('1995/8/30') + ephem.Date(i)
            p.compute(date)
            x = p.sun_distance * math.cos(p.hlat) * math.cos(p.hlon)
            y = p.sun_distance * math.cos(p.hlat) * math.sin(p.hlon)
            if i == 0:
                paths.append(circle(x, y, 500 * radii[n] * 1000 / ephem.meters_per_au))
            path.append((x, y))
        paths.append(path)

    d = axi.Drawing(paths)

    d = d.join_paths(0.01)
    d = d.simplify_paths(0.001)
    d = d.scale_to_fit(W, H)
    d = d.rotate(-90).move(H / 2, W / 2, 0.5, 0.5)

    d.dump('out.axi')
    d.render(bounds=axi.A3_BOUNDS, show_bounds=False).write_to_png('planets.png')

if __name__ == '__main__':
    main()
