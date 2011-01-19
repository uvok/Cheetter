from termcolor import colored

def color(fore, back, attrib=None):
    return lambda txt: colored(txt, fore, back, attrib)

#x = color(fore, black)

#nickname = color("blue", "on_yellow", ["bold"])
nickname = color("red", None, ["bold"])
time = color("cyan", None, None)
