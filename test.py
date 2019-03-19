from World import *

def main():
    size = (1000, 1000)
    world = World(size[0], size[1])
    world.addRndBoids(40)
    world.BoidTrackbars()
    world.WorldTrackbars()

    world.simulate()


if __name__ == '__main__':
    main()
