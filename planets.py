import axi
import math
import ephem

A4_SIZE = (11.69, 8.27)
A4_BOUNDS = (0, 0, 11.69, 8.27)
H, W = A4_SIZE

def circle(x, y, r, num=60):
    path = []
    for i in range(num + 1):
        a = math.tau * i / num
        path.append((x + r * math.cos(a), y + r * math.sin(a)))
    return path


def pos_at_date(planet, date):
    planet.compute(date)
    x = planet.sun_distance * math.cos(planet.hlat) * math.cos(planet.hlon)
    y = planet.sun_distance * math.cos(planet.hlat) * math.sin(planet.hlon)
    return (x, y)


def main():
    paths = []

    planets = [ephem.Mercury(), ephem.Venus(), ephem.Sun(), ephem.Mars(), ephem.Jupiter(), ephem.Saturn(), ephem.Uranus(), ephem.Neptune()]
    radii = [2440, 6052, 6371, 3390, 69911, 58232, 25362, 24622]

    for n, p in enumerate(planets):
        date = ephem.Date('1995/8/30')
        x, y = pos_at_date(p, date)
        start_angle = math.atan2(y, x)
        old_angle = start_angle
        paths.append(circle(x, y, 1000 * radii[n] * 1000 / ephem.meters_per_au))
        path = []
        end_date = ephem.Date('2018/8/30')
        i = 0
        round = False
        while date < end_date:
            date += ephem.Date(1)
            i += 1
            x, y = pos_at_date(p, date)
            angle = math.atan2(y, x)
            if math.copysign(1, angle - start_angle) != math.copysign(1, old_angle - start_angle):
                if not round:
                    round = True
                elif round:
                    path.append(path[0])
                    break
            path.append((x, y))
            old_angle = angle
        paths.append(path)

    d = axi.Drawing(paths)

    d = d.simplify_paths(0.001)
    d = d.scale_to_fit(W, H)
    d = d.rotate(-90).move(H / 2, W / 2, 0.5, 0.5)

    d.dump('out.axi')
    d.render(bounds=A4_BOUNDS, show_bounds=False).write_to_png('planets.png')

if __name__ == '__main__':
    main()
