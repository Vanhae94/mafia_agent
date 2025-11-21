
try:
    from langgraph.types import Command
    print("Command is available")
except ImportError:
    print("Command is NOT available")
