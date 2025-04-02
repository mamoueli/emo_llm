# print pip version
import pip
print(pip.__version__)
!pip install openai

import json
import os
import logging
import sys
import time
import openai
from openai import RateLimitError, APIError, Timeout, APIConnectionError, OpenAI
from pydantic import BaseModel
os.environ["OPENAI_API_KEY"] = "your-key"
openai.api_key = 'your-key'
client = OpenAI()
models = client.models.list()
models
