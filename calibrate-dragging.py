import axi

H, W = axi.A3_SIZE

def main():
    #these calibration tests move the motor and pen in various ways to test "dragging"
    #they start by making sure that running around the paper without using the pen results in the same position
    #then they gradually increase the number of lines drawn on the paper, checking that no dragging occurs
    #the output dashes at the top of the page should be at exactly the same Y coordinate if no dragging occurs

    y0 = 0.0
    y1 = 0.2
    y2 = 0.4
    y3 = 0.6
    y4 = 0.8
    y5 = 1.0
    paths = [
        #all around the page with no pen
        [(W / 2 - 0.2, y0), (W / 2 - 0.1, y0)],
        [(0, 0)], [(0, H)], [(W, H)], [(W, 0)],
        [(W / 2 + 0.2, y0), (W / 2 + 0.1, y0)],

        #all around the page with pen
        [(W / 2 - 0.2, y1), (W / 2 - 0.1, y1)],
        [(0, 0), (0, H), (W, H), (W, 0)],
        [(W / 2 + 0.2, y1), (W / 2 + 0.1, y1)],

        #+Y
        [(W / 2 - 0.2, y2), (W / 2 - 0.1, y2)],
        [(W / 2, 0), (W / 2, H)],
        [(W / 2 + 0.2, y2), (W / 2 + 0.1, y2)],

        #-Y
        [(W / 2 - 0.2, y3), (W / 2 - 0.1, y3)],
        [(W / 2, H), (W / 2, 0)],
        [(W / 2 + 0.2, y3), (W / 2 + 0.1, y3)],

        #+X
        [(W / 2 - 0.2, y4), (W / 2 - 0.1, y4)],
        [(0, H / 2), (W, H / 2)],
        [(W / 2 + 0.2, y4), (W / 2 + 0.1, y4)],

        #-X
        [(W / 2 - 0.2, y5), (W / 2 - 0.1, y5)],
        [(W, H / 2), (0, H / 2)],
        [(W / 2 + 0.2, y5), (W / 2 + 0.1, y5)],
    ]
    
    d = axi.Drawing(paths)

    d = d.rotate(-90).move(H / 2, W / 2, 0.5, 0.5)

    d.dump('out.axi')
    d.render(bounds=axi.A3_BOUNDS, show_bounds=False).write_to_png('out.png')

if __name__ == '__main__':
    main()
