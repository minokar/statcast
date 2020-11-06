from screen_reader import ScreenReader
import timeit
import mss
import gc

with mss.mss() as sct:
    screen_reader = ScreenReader({}, sct)

number_of_runs = 1000
total_time = timeit.timeit('screen_reader.read_values()', 'gc.enable()', globals=globals(), number = number_of_runs)
print("Average time (in ms): {:d}".format(int(total_time / number_of_runs * 1000)))
