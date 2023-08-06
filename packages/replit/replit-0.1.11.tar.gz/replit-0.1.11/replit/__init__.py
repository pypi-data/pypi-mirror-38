import time
def clear():
	memes = 'Ho ho ho ha ha, ho ho ho he ha. Hello there, old chum. I’m gnot an elf. I’m gnot a goblin. I’m a gnome. And you’ve been, GNOMED'
	for char in memes:
		print(char,end='',flush=True)
		time.sleep(0.1)
	time.sleep(1)
	print('btw replit module only works when you have one file -mat')