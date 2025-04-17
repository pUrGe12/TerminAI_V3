# This is the generic output provider which can be used in any step in the LVS execution line
# Make sure you have your account setup correct. Refer to docs/setting_vertexai.md to learn how to do it
import sys
import os
from google.auth import default
import google.auth.transport.requests
import openai

# Set the root directory as a traversable path
DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if DIR_PATH not in sys.path:
    sys.path.insert(0, DIR_PATH)

from TerminAI.utils.config import Config


def build_prompt(prompt: str, LVS_result: list):
    """
    Not entirely sure if LVS_result is going to be a list or
    a dictionary.
    """
    return [
    {"role": "system", "content": Config.prompts.generic},
    {"role": "user", "content": Config.prompts.LVS_.format(LVS_result)},
    {"role": "user", "content": prompt}
    ]


def generate_generic_response(prompt: str, LVS_result: list):
    """
    Initialise the model and return results
    """

    project_id = Config.model.project_id
    location = Config.model.location

    # Programmatically get an access token

    credentials, _ = default(scopes=[Config.model.credentials_url])
    credentials.refresh(google.auth.transport.requests.Request())

    client = openai.OpenAI(
        base_url=Config.model.g_openai_url.format(location=location, project_id=project_id),
        api_key=credentials.token,
    )

    response = client.chat.completions.create(
        model=Config.model.model_,
        messages=build_prompt(prompt, LVS_result)
    )

    model_response = response.choices[0].message.content

    # not everyone will care for this, but I do
    tokens_used = response.usage.total_tokens
    model_used = response.model

    # for now returning only model's response
    return (model_response)