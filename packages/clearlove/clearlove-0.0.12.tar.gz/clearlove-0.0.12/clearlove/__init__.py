import os
import sys
import time
WIDTH = 79
message = "4396"
printedMessage = ["", "", "", "", "", "", ""]
characters = {
    " ": [	" ",
           " ",
           " ",
           " ",
           " ",
           " ",
           " "],
    "4": [	"*    *",
           "*    *",
           "*    *",
           "******",
           "     *",
           "     *",
           "     *"],
    "3": [	"******",
           "     *",
           "     *",
           "******",
           "     *",
           "     *",
           "******"],
    "9": [	"******",
           "*    *",
           "*    *",
           "******",
           "     *",
           "     *",
           "******"],
    "6": [	"******",
           "*     ",
           "*     ",
           "******",
           "*    *",
           "*    *",
           "******"],

}


def clearlove():
	for row in range(7):
		for char in message:
			printedMessage[row] += (str(characters[char][row])+"  ")

	offset = WIDTH
	##操作系统判断
	import platform
	if "Windows" in str(platform.architecture()):
		command = "cls"
	else:
		command = "clear"
	while True:
		try:
			os.system(command)
			for row in range(7):
				print(" "*offset+printedMessage[row][max(0, offset*-1):WIDTH-offset])
			offset -= 1
			if offset <= ((len(message)+2)*6)-1:
				offset = WIDTH
			time.sleep(0.05)
		except KeyboardInterrupt:
			print("User use Ctrl-C to break...")
			sys.exit(1)
