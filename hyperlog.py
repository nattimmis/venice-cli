#!/usr/bin/env python3
"""
HYPERLOG - AI Terminal for S24
==============================
Powered by Venice AI
"""

import requests
import json
import random
import string
import sys
import os
import time
import getpass
from datetime import datetime
from pathlib import Path

# ==================== Config ====================

VENICE_API_KEY = "P2GL04w8H7acJZcGbOH1WhSSCgFjvYi7Xo1rRjbKJ1"

# ==================== Colors ====================

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Extended colors
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;198m"
    PURPLE = "\033[38;5;135m"
    LIME = "\033[38;5;118m"
    TEAL = "\033[38;5;43m"
    GOLD = "\033[38;5;220m"

    BG_BLACK = "\033[40m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"

    @classmethod
    def disable(cls):
        for attr in dir(cls):
            if not attr.startswith('_') and attr != 'disable':
                setattr(cls, attr, "")

C = Colors

SESSION_FILE = Path.home() / ".hyperlog_session.json"

# ==================== ASCII Art & Animation ====================

LOGO_FRAMES = [
    # Frame 1 - Building up
    f"""{C.CYAN}
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    {C.RESET}""",

    # Frame 2
    f"""{C.CYAN}
    ██╗  ██╗
    ██║  ██║
    {C.RESET}""",

    # Frame 3
    f"""{C.CYAN}
    ██╗  ██╗██╗   ██╗
    ██║  ██║╚██╗ ██╔╝
    ███████║ ╚████╔╝
    {C.RESET}""",

    # Frame 4
    f"""{C.CYAN}
    ██╗  ██╗██╗   ██╗██████╗ ███████╗
    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝
    ███████║ ╚████╔╝ ██████╔╝█████╗
    ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝
    {C.RESET}""",

    # Frame 5 - Full HYPER
    f"""{C.CYAN}
    ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗
    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
    ███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝
    ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗
    ██║  ██║   ██║   ██║     ███████╗██║  ██║
    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝
    {C.RESET}""",
]

LOGO_FULL = f"""
{C.BOLD}{C.CYAN}    ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ {C.MAGENTA}██╗      ██████╗  ██████╗
{C.CYAN}    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗{C.MAGENTA}██║     ██╔═══██╗██╔════╝
{C.CYAN}    ███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝{C.MAGENTA}██║     ██║   ██║██║  ███╗
{C.CYAN}    ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗{C.MAGENTA}██║     ██║   ██║██║   ██║
{C.CYAN}    ██║  ██║   ██║   ██║     ███████╗██║  ██║{C.MAGENTA}███████╗╚██████╔╝╚██████╔╝
{C.CYAN}    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝{C.MAGENTA}╚══════╝ ╚═════╝  ╚═════╝ {C.RESET}
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_intro():
    """Play the intro animation"""
    clear()

    # Matrix-style rain effect
    width = 50
    rain_chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"

    for frame in range(8):
        clear()
        rain = ""
        for _ in range(3):
            line = ""
            for _ in range(width):
                if random.random() < 0.3:
                    line += f"{C.GREEN}{random.choice(rain_chars)}{C.RESET}"
                else:
                    line += " "
            rain += "    " + line + "\n"
        print(rain)
        time.sleep(0.05)

    # Build up the logo
    for i, frame in enumerate(LOGO_FRAMES):
        clear()
        print(frame)
        time.sleep(0.08)

    # Final logo with effects
    clear()
    print(LOGO_FULL)
    time.sleep(0.15)

    # Glitch effect
    glitch_chars = "█▓▒░"
    for _ in range(3):
        clear()
        glitched = LOGO_FULL
        for char in glitch_chars:
            if random.random() < 0.1:
                pos = random.randint(0, len(glitched) - 1)
                glitched = glitched[:pos] + random.choice(glitch_chars) + glitched[pos+1:]
        print(glitched)
        time.sleep(0.04)

    # Final clean logo
    clear()
    print(LOGO_FULL)

    # Tagline animation
    tagline = "    [ NEURAL INTERFACE ACTIVE ]"
    print(f"\n{C.DIM}", end="")
    for char in tagline:
        print(char, end="", flush=True)
        time.sleep(0.02)
    print(C.RESET)

    # System boot messages
    boot_msgs = [
        ("INIT", "Venice AI Core", C.GREEN),
        ("LOAD", "Neural Networks", C.CYAN),
        ("SYNC", "Knowledge Base", C.MAGENTA),
        ("READY", "S24 Terminal", C.YELLOW),
    ]

    print()
    for status, msg, color in boot_msgs:
        print(f"    {C.DIM}[{C.RESET}{color}{status}{C.RESET}{C.DIM}]{C.RESET} {msg}...", end="", flush=True)
        time.sleep(0.15)
        print(f" {C.GREEN}OK{C.RESET}")
        time.sleep(0.08)

    print(f"\n    {C.BOLD}{C.GREEN}>>> HYPERLOG ONLINE <<<{C.RESET}\n")
    time.sleep(0.3)


# ==================== Venice Client ====================

class Venice:
    MODELS = {
        "1": ("GLM-4", "zai-org-glm-4.6"),
        "2": ("Uncensored", "dolphin-3.0-mistral-24b-1dot1"),
        "3": ("Medium", "mistral-31-24b"),
        "4": ("DeepSeek R1", "deepseek-r1-distill-llama-70b"),
        "5": ("Llama 3.3 70B", "llama-3.3-70b"),
    }

    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://api.venice.ai/api/v1"

        self.model_id = "llama-3.3-70b"
        self.model_name = "Llama 3.3 70B"
        self.temperature = 0.7
        self.top_p = 0.9
        self.web_search = False
        self.system_prompt = "You are Hyperlog, an advanced AI assistant running on a Samsung S24. Be concise, helpful, and technically proficient."

        self.api_key = VENICE_API_KEY
        self.messages = []
        self.msg_count = 0

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def set_model(self, choice):
        if choice in self.MODELS:
            self.model_name, self.model_id = self.MODELS[choice]
            return True
        return False

    def new_chat(self):
        self.messages = []
        self.msg_count = 0

    def send(self, message, callback=None):
        self.messages.append({"role": "user", "content": message})
        self.msg_count += 1

        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                *self.messages
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": True,
            "max_tokens": 4096,
        }

        try:
            resp = self.session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=120
            )

            if resp.status_code == 429:
                return None, "Rate limited! Wait a moment."

            if resp.status_code != 200:
                return None, f"Error {resp.status_code}: {resp.text[:100]}"

            full_text = ""

            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        obj = json.loads(data)
                        delta = obj.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            full_text += content
                            if callback:
                                callback(content)
                    except json.JSONDecodeError:
                        continue

            self.messages.append({"role": "assistant", "content": full_text})
            return full_text, None

        except requests.Timeout:
            return None, "Request timed out"
        except Exception as e:
            return None, str(e)


# ==================== UI ====================

def print_header(ai):
    print(f"\n{C.BOLD}{C.CYAN}╔{'═'*44}╗{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}║{C.RESET}  {C.BOLD}{C.WHITE}HYPERLOG{C.RESET} {C.DIM}v1.0{C.RESET}  {C.MAGENTA}●{C.RESET} {C.GREEN}{ai.model_name}{C.RESET}".ljust(57) + f"{C.BOLD}{C.CYAN}║{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}╚{'═'*44}╝{C.RESET}")

    status_line = f"  {C.DIM}Web:{C.RESET} "
    status_line += f"{C.GREEN}ON{C.RESET}" if ai.web_search else f"{C.RED}OFF{C.RESET}"
    status_line += f"  {C.DIM}Temp:{C.RESET} {ai.temperature}"
    status_line += f"  {C.DIM}Msgs:{C.RESET} {ai.msg_count}"
    print(status_line)
    print(f"  {C.DIM}{'─'*42}{C.RESET}")


def print_help():
    print(f"""
{C.BOLD}{C.GOLD}━━━ Commands ━━━{C.RESET}
  {C.CYAN}/m{C.RESET}        Models      {C.CYAN}/w{C.RESET}  Web toggle
  {C.CYAN}/t{C.RESET} <0-1>  Temperature {C.CYAN}/s{C.RESET}  System prompt
  {C.CYAN}/n{C.RESET}        New chat    {C.CYAN}/c{C.RESET}  Clear screen
  {C.CYAN}/h{C.RESET}        Help        {C.CYAN}/q{C.RESET}  Quit
""")


def print_models(ai):
    print(f"\n{C.BOLD}{C.GOLD}━━━ Models ━━━{C.RESET}")
    for num, (name, mid) in ai.MODELS.items():
        marker = f" {C.GREEN}◄{C.RESET}" if mid == ai.model_id else ""
        print(f"  {C.CYAN}{num}{C.RESET}) {name}{marker}")


def spinner_frames():
    return ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def print_thinking():
    print(f"\n{C.DIM}◐ Processing...{C.RESET}", end="", flush=True)


def print_response_start():
    print(f"\r{' '*30}\r", end="")
    print(f"\n{C.MAGENTA}▸{C.RESET} ", end="", flush=True)


def print_chunk(chunk):
    print(chunk, end="", flush=True)


def print_error(msg):
    print(f"\n{C.RED}✗ {msg}{C.RESET}")


def print_success(msg):
    print(f"{C.GREEN}✓ {msg}{C.RESET}")


def get_input():
    try:
        return input(f"\n{C.CYAN}▶{C.RESET} ").strip()
    except EOFError:
        return "/q"
    except KeyboardInterrupt:
        return "/q"


# ==================== Main ====================

def main():
    if "--no-color" in sys.argv:
        Colors.disable()

    skip_intro = "--fast" in sys.argv or "-f" in sys.argv

    if not skip_intro:
        try:
            animate_intro()
        except KeyboardInterrupt:
            pass

    ai = Venice()
    clear()
    print_header(ai)
    print_help()

    while True:
        try:
            user_input = get_input()
        except KeyboardInterrupt:
            print(f"\n{C.CYAN}Disconnecting...{C.RESET}\n")
            break

        if not user_input:
            continue

        # Commands
        cmd = user_input.lower()

        if cmd in ("/q", "/quit", "exit", "quit"):
            print(f"\n{C.MAGENTA}▸ Session terminated.{C.RESET}")
            print(f"{C.DIM}  Hyperlog signing off...{C.RESET}\n")
            break

        if cmd in ("/h", "/help", "?"):
            print_help()
            continue

        if cmd in ("/c", "/clear"):
            clear()
            print_header(ai)
            continue

        if cmd in ("/n", "/new"):
            ai.new_chat()
            clear()
            print_header(ai)
            print_success("New session started")
            continue

        if cmd in ("/w", "/web"):
            ai.web_search = not ai.web_search
            print_success(f"Web search: {'ON' if ai.web_search else 'OFF'}")
            continue

        if cmd.startswith("/t "):
            try:
                temp = float(cmd[3:].strip())
                if 0 <= temp <= 2:
                    ai.temperature = temp
                    print_success(f"Temperature: {temp}")
                else:
                    print_error("Range: 0.0 - 2.0")
            except ValueError:
                print_error("Invalid number")
            continue

        if cmd in ("/m", "/model"):
            print_models(ai)
            choice = input(f"\n{C.DIM}Select:{C.RESET} ").strip()
            if ai.set_model(choice):
                print_success(f"Model: {ai.model_name}")
                clear()
                print_header(ai)
            elif choice.lower() != 'x':
                print_error("Invalid choice")
            continue

        if cmd in ("/s", "/system"):
            print(f"{C.DIM}Enter system prompt (empty=default):{C.RESET}")
            prompt = input().strip()
            if prompt:
                ai.system_prompt = prompt
                print_success("System prompt updated")
            else:
                ai.system_prompt = "You are Hyperlog, an advanced AI assistant."
                print_success("System prompt reset")
            continue

        # Chat
        print_thinking()

        first_chunk = [True]
        def on_chunk(chunk):
            if first_chunk[0]:
                print_response_start()
                first_chunk[0] = False
            print_chunk(chunk)

        response, error = ai.send(user_input, callback=on_chunk)

        if error:
            print_error(error)
        elif response:
            print()
        else:
            print_error("No response")


if __name__ == "__main__":
    main()
