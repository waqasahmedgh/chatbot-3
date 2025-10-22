import subprocess

def main() -> int:

    # args = ["uv", "run", "chainlit", "run", "src/agent/agent.py", "-w"]
    args = ["uv", "run", "chainlit", "run", "src/chat_ui/main.py", "-w"]

    return subprocess.run(args).returncode