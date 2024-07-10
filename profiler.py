# easy way to access python build-in profiler to analize the game and find out where optimizations should be made

import cProfile
import bin

cProfile.run('bin.Game((1280,720))')