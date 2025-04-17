class Terminal:
	"""
	Settings for TerminAI
	"""
	title = "TerminAI_v3"
	d_length = 800
	d_breadth = 500
	font = "Monospace"
	font_size = 11
	stall_message = "Generating response..."
	Name = "TerminAI"

class PromptBar(Terminal):
	"""
	Display settings for the prompt bar
	"""
	color1 = "#000000"
	color2 = "#FFFFFF"

class Models:
	"""
	Model details here for VertexAI.
	
	Note: location MUST be us-central1 for now because VertexAI doesn't have
	any models in asia-central1 for example. Check if the model exists in your 
	region before using it. Else stick to the default.
	"""
	project_id = "terminai-456107"
	location = "us-central1"
	model_ = "google/gemini-2.0-flash-001"
	credentials_url = "https://www.googleapis.com/auth/cloud-platform"
	g_openai_url = "https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi"


class Prompts:
	# Make this better
	generic = """
	You are TerminAI, a terminal that has a backend of a Linked Vector System. This is a
	new way to perform RAG operations and you will be given the end result of the system along
	with the user's prompt.

	Your job is to use the prompt and the information retrieved, and craft the exact response
	the user is asking for.
	"""

	# Make this better
	LVS_ = """
	This is the output of the LVS system: {}.
	"""

class Config:
	terminal = Terminal()
	prompt = PromptBar()
	model = Models()
	prompts = Prompts()