class Terminal:
	""" Settings for TerminAI """
	title = "TerminAI_v3"
	d_length = 800
	d_breadth = 500
	font = "Monospace"
	font_size = 11
	stall_message = "Generating response..."
	Name = "TerminAI"

class PromptBar(Terminal):
	""" Display settings for the prompt bar """
	color1 = "#000000"
	color2 = "#FFFFFF"

class Config:
	terminal = Terminal()
	prompt = PromptBar()