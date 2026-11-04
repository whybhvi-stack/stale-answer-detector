import os
from llm import ask

print("CHEAP:", ask(os.getenv("CHEAP_MODEL"), "You are helpful.", "Say hi in 3 words."))
print("STRONG:", ask(os.getenv("STRONG_MODEL"), "You are helpful.", "Say hi in 3 words."))