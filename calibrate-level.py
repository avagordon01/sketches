import axi
import math

H, W = (11.69, 8.27)

def main():
    paths = [
        [(0, 0), (0, H)],
        [(W / 2, 0), (W / 2, H)],
        [(W, 0), (W, H)],

        [(0, 0), (W, 0)],
        [(0, H / 2), (W, H / 2)],
        [(0, H), (W, H)],

        [(0, 0), (W, H)],
        [(W, 0), (0, H)],
    ]
    
    d = axi.Drawing(paths)

    d = d.rotate(-90).move(H / 2, W / 2, 0.5, 0.5)

    d.dump('out.axi')
    d.render(bounds=(0, 0, H, W), show_bounds=False).write_to_png('out.png')

if __name__ == '__main__':
    main()
