import light
import sys

light = light.Light()
light.write_value('bedroom', int(sys.argv[1]))


