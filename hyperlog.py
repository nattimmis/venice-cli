#!/usr/bin/env python3
"""
Hyperlog - Venice AI CLI for Termux
====================================

A mobile-friendly CLI for Venice AI designed for Termux.

Features:
- Clean, compact UI for small screens
- Easy commands with short aliases
- Color support
- Streaming responses
- Login/Logout support

Usage:
    hyperlog

Commands:
    /h        Help
    /m        Change model
    /w        Toggle web search
    /t 0.8    Set temperature
    /s        Set system prompt
    /n        New conversation
    /c        Clear screen
    /login    Login with email
    /logout   Logout
    /status   Show login status
    /q        Quit
"""

import requests
import json
import random
import string
import sys
import os
import getpass
from datetime import datetime
from pathlib import Path

# ==================== Colors ====================

class Colors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Backgrounds
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"

    @classmethod
    def disable(cls):
        """Disable colors (for non-color terminals)"""
        cls.RESET = ""
        cls.BOLD = ""
        cls.DIM = ""
        cls.RED = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.BLUE = ""
        cls.MAGENTA = ""
        cls.CYAN = ""
        cls.WHITE = ""
        cls.BG_BLUE = ""
        cls.BG_GREEN = ""


C = Colors  # Short alias

# Session file location
SESSION_FILE = Path.home() / ".venice_session.json"


# ==================== Venice Client ====================

class Venice:
    """Venice AI Client"""

    MODELS = {
        "1": ("GLM-4", "zai-org-glm-4.6"),
        "2": ("Venice Uncensored 1.1", "dolphin-3.0-mistral-24b-1dot1"),
        "3": ("Venice Medium", "mistral-31-24b"),
    }

    CLERK_API = "https://clerk.venice.ai/v1"
    CLERK_VERSION = "2025-11-10"
    CLERK_JS_VERSION = "5.117.0"

    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://outerface.venice.ai/api/inference"

        # Settings
        self.model_id = "zai-org-glm-4.6"
        self.model_name = "GLM-4"
        self.temperature = 0.7
        self.top_p = 0.9
        self.web_search = True
        self.system_prompt = ""

        # Auth state
        self.logged_in = False
        self.user_email = None
        self.auth_token = None

        # State
        self.user_id = "user_anon_1234568910"
        self.conversation_id = self._gen_id()
        self.messages = []
        self.msg_count = 0

        # Headers
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
            "Origin": "https://venice.ai",
            "Referer": "https://venice.ai/",
            "x-venice-version": "interface@20260102.211941+d37d40c",
            "x-venice-locale": "en",
        }

        # Try to load saved session
        self._load_session()

    def _save_session(self):
        """Save session to file"""
        if self.logged_in and self.auth_token:
            data = {
                "email": self.user_email,
                "token": self.auth_token,
                "user_id": self.user_id
            }
            try:
                with open(SESSION_FILE, "w") as f:
                    json.dump(data, f)
            except:
                pass

    def _load_session(self):
        """Load saved session"""
        try:
            if SESSION_FILE.exists():
                with open(SESSION_FILE, "r") as f:
                    data = json.load(f)
                    self.user_email = data.get("email")
                    self.auth_token = data.get("token")
                    self.user_id = data.get("user_id", self.user_id)
                    if self.auth_token:
                        self.logged_in = True
                        self.headers["Authorization"] = f"Bearer {self.auth_token}"
        except:
            pass

    def _clear_session(self):
        """Clear saved session"""
        self.logged_in = False
        self.user_email = None
        self.auth_token = None
        self.headers.pop("Authorization", None)
        try:
            if SESSION_FILE.exists():
                SESSION_FILE.unlink()
        except:
            pass

    def login(self, email, password):
        """Login with email and password"""
        try:
            # Step 1: Send email to get sign_in ID
            url1 = f"{self.CLERK_API}/client/sign_ins?__clerk_api_version={self.CLERK_VERSION}&_clerk_js_version={self.CLERK_JS_VERSION}"
            resp1 = self.session.post(
                url1,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": self.headers["User-Agent"],
                    "Referer": "https://venice.ai/",
                },
                data=f"locale=en-US&identifier={requests.utils.quote(email)}",
                timeout=30
            )

            if resp1.status_code != 200:
                return False, f"Login failed: {resp1.status_code}"

            data1 = resp1.json()
            sign_in_id = data1.get("response", {}).get("id")

            if not sign_in_id:
                # Check for error
                errors = data1.get("errors", [])
                if errors:
                    return False, errors[0].get("message", "Email not found")
                return False, "Could not get sign-in ID"

            # Step 2: Send password
            url2 = f"{self.CLERK_API}/client/sign_ins/{sign_in_id}/attempt_first_factor?__clerk_api_version={self.CLERK_VERSION}&_clerk_js_version={self.CLERK_JS_VERSION}"
            resp2 = self.session.post(
                url2,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": self.headers["User-Agent"],
                    "Referer": "https://venice.ai/",
                },
                data=f"strategy=password&password={requests.utils.quote(password)}",
                timeout=30
            )

            if resp2.status_code != 200:
                return False, "Invalid password"

            data2 = resp2.json()

            # Get session token from response
            client_data = data2.get("client", {})
            sessions = client_data.get("sessions", [])

            if sessions:
                session_data = sessions[0]
                self.user_id = session_data.get("user", {}).get("id", self.user_id)

                # Get the JWT token
                last_token = session_data.get("last_active_token", {})
                jwt = last_token.get("jwt")

                if jwt:
                    self.auth_token = jwt
                    self.logged_in = True
                    self.user_email = email
                    self.headers["Authorization"] = f"Bearer {jwt}"
                    self._save_session()
                    return True, "Login successful!"

            return False, "Could not get session token"

        except requests.Timeout:
            return False, "Request timed out"
        except Exception as e:
            return False, str(e)

    def logout(self):
        """Logout and clear session"""
        try:
            if self.logged_in:
                # Call Venice signout endpoint
                self.session.post(
                    "https://venice.ai/api/auth/signout",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": self.headers["User-Agent"],
                        "Referer": "https://venice.ai/",
                    },
                    timeout=10
                )
        except:
            pass

        self._clear_session()
        return True, "Logged out"

    def get_status(self):
        """Get login status"""
        if self.logged_in:
            return f"Logged in as: {self.user_email}"
        return "Not logged in (anonymous)"

    def _gen_id(self, length=7):
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=length))

    def _timestamp(self):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:30")

    def set_model(self, choice):
        """Set model by number (1-3)"""
        if choice in self.MODELS:
            self.model_name, self.model_id = self.MODELS[choice]
            return True
        return False

    def new_chat(self):
        """Start fresh conversation"""
        self.conversation_id = self._gen_id()
        self.messages = []
        self.msg_count = 0

    def send(self, message, callback=None):
        """Send message and stream response"""
        self.messages.append({"content": message, "role": "user"})
        self.msg_count += 1

        self.headers["x-venice-timestamp"] = self._timestamp()

        payload = {
            "conversationId": self.conversation_id,
            "characterId": "",
            "clientProcessingTime": random.randint(1500, 2500),
            "conversationType": "text",
            "includeVeniceSystemPrompt": True,
            "isCharacter": False,
            "modelId": self.model_id,
            "prompt": self.messages.copy(),
            "reasoning": False,
            "requestId": self._gen_id(),
            "systemPrompt": self.system_prompt,
            "temperature": self.temperature,
            "topP": self.top_p,
            "userId": self.user_id,
            "webEnabled": self.web_search,
            "webScrapeEnabled": False,
        }

        try:
            resp = self.session.post(
                f"{self.base_url}/chat",
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=60
            )

            if resp.status_code == 429:
                return None, "Rate limited! Wait a bit."

            if resp.status_code != 200:
                return None, f"Error {resp.status_code}"

            # Parse stream
            full_text = ""
            buffer = ""

            for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                if not chunk:
                    continue

                buffer += chunk

                while buffer:
                    buffer = buffer.lstrip()
                    if not buffer:
                        break

                    try:
                        obj, idx = json.JSONDecoder().raw_decode(buffer)
                        if obj.get("kind") == "content":
                            content = obj.get("content", "")
                            full_text += content
                            if callback:
                                callback(content)
                        buffer = buffer[idx:]
                    except json.JSONDecodeError:
                        break

            self.messages.append({"content": full_text, "role": "assistant"})
            return full_text, None

        except requests.Timeout:
            return None, "Request timed out"
        except Exception as e:
            return None, str(e)


# ==================== UI Functions ====================

def clear():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(ai):
    """Print app header"""
    print(f"\n{C.BOLD}{C.CYAN}╔══════════════════════════════════╗{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}║{C.RESET}       {C.BOLD}{C.WHITE}HYPERLOG{C.RESET}  {C.DIM}Venice AI{C.RESET}       {C.BOLD}{C.CYAN}║{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}╚══════════════════════════════════╝{C.RESET}")

    # Login status
    if ai.logged_in:
        print(f"{C.GREEN}● {C.RESET}{C.DIM}{ai.user_email}{C.RESET}")
    else:
        print(f"{C.YELLOW}○ {C.RESET}{C.DIM}Anonymous{C.RESET}")

    print(f"{C.DIM}Model: {C.RESET}{C.GREEN}{ai.model_name}{C.RESET}")
    print(f"{C.DIM}Web: {C.RESET}{C.GREEN if ai.web_search else C.RED}{'ON' if ai.web_search else 'OFF'}{C.RESET}  {C.DIM}Temp: {C.RESET}{ai.temperature}")
    print(f"{C.DIM}{'─' * 36}{C.RESET}")


def print_help():
    """Print help menu"""
    print(f"\n{C.BOLD}{C.YELLOW}Commands:{C.RESET}")
    print(f"  {C.CYAN}/h{C.RESET}        Help")
    print(f"  {C.CYAN}/m{C.RESET}        Change model")
    print(f"  {C.CYAN}/w{C.RESET}        Toggle web search")
    print(f"  {C.CYAN}/t 0.8{C.RESET}    Set temperature")
    print(f"  {C.CYAN}/s{C.RESET}        Set system prompt")
    print(f"  {C.CYAN}/n{C.RESET}        New conversation")
    print(f"  {C.CYAN}/c{C.RESET}        Clear screen")
    print(f"\n{C.BOLD}{C.YELLOW}Account:{C.RESET}")
    print(f"  {C.CYAN}/login{C.RESET}    Login with email")
    print(f"  {C.CYAN}/logout{C.RESET}   Logout")
    print(f"  {C.CYAN}/status{C.RESET}   Show login status")
    print(f"\n  {C.CYAN}/q{C.RESET}        Quit")
    print()


def print_models(ai):
    """Print model selection menu"""
    print(f"\n{C.BOLD}{C.YELLOW}Select Model:{C.RESET}")
    for num, (name, mid) in ai.MODELS.items():
        current = " ←" if mid == ai.model_id else ""
        print(f"  {C.CYAN}{num}{C.RESET}) {name}{C.GREEN}{current}{C.RESET}")
    print(f"  {C.DIM}Enter number or 'x' to cancel{C.RESET}")


def print_thinking():
    """Print thinking indicator"""
    print(f"\n{C.DIM}Thinking...{C.RESET}", end="", flush=True)


def print_response_start():
    """Clear thinking and start response"""
    print(f"\r{' ' * 20}\r", end="")
    print(f"\n{C.GREEN}Hyperlog:{C.RESET} ", end="", flush=True)


def print_chunk(chunk):
    """Print response chunk"""
    print(chunk, end="", flush=True)


def print_error(msg):
    """Print error message"""
    print(f"\n{C.RED}Error: {msg}{C.RESET}")


def print_success(msg):
    """Print success message"""
    print(f"{C.GREEN}✓ {msg}{C.RESET}")


def print_info(msg):
    """Print info message"""
    print(f"{C.DIM}{msg}{C.RESET}")


def get_input():
    """Get user input with prompt"""
    try:
        return input(f"\n{C.BLUE}You:{C.RESET} ").strip()
    except EOFError:
        return "/q"


def get_multiline_input():
    """Get multiline input for system prompt"""
    print(f"{C.DIM}Enter prompt (empty line to finish):{C.RESET}")
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)


# ==================== Main App ====================

def main():
    # Check for --no-color flag
    if "--no-color" in sys.argv:
        Colors.disable()

    ai = Venice()
    clear()
    print_header(ai)
    print_help()

    while True:
        user_input = get_input()

        if not user_input:
            continue

        # ===== Commands =====

        # Quit
        if user_input.lower() in ("/q", "/quit", "exit", "quit"):
            print(f"\n{C.CYAN}Goodbye!{C.RESET}\n")
            break

        # Help
        if user_input.lower() in ("/h", "/help", "?"):
            print_help()
            continue

        # Clear
        if user_input.lower() in ("/c", "/clear"):
            clear()
            print_header(ai)
            continue

        # New conversation
        if user_input.lower() in ("/n", "/new"):
            ai.new_chat()
            clear()
            print_header(ai)
            print_success("New conversation started")
            continue

        # Toggle web search
        if user_input.lower() in ("/w", "/web"):
            ai.web_search = not ai.web_search
            status = "ON" if ai.web_search else "OFF"
            print_success(f"Web search: {status}")
            continue

        # Set temperature
        if user_input.lower().startswith("/t "):
            try:
                temp = float(user_input[3:].strip())
                if 0 <= temp <= 1:
                    ai.temperature = temp
                    print_success(f"Temperature: {temp}")
                else:
                    print_error("Must be 0.0 - 1.0")
            except ValueError:
                print_error("Invalid number")
            continue

        # Model selection
        if user_input.lower() in ("/m", "/model"):
            print_models(ai)
            choice = input(f"\n{C.CYAN}>{C.RESET} ").strip()
            if choice.lower() != 'x' and ai.set_model(choice):
                print_success(f"Model: {ai.model_name}")
            elif choice.lower() != 'x':
                print_error("Invalid choice")
            continue

        # System prompt
        if user_input.lower() in ("/s", "/system"):
            prompt = get_multiline_input()
            ai.system_prompt = prompt
            if prompt:
                print_success("System prompt set")
            else:
                print_success("System prompt cleared")
            continue

        # ===== Account Commands =====

        # Login
        if user_input.lower() in ("/login", "/l"):
            if ai.logged_in:
                print_info(f"Already logged in as {ai.user_email}")
                print_info("Use /logout first to switch accounts")
                continue

            print(f"\n{C.BOLD}{C.YELLOW}Login to Venice AI{C.RESET}")
            try:
                email = input(f"{C.DIM}Email: {C.RESET}").strip()
                if not email:
                    print_error("Cancelled")
                    continue

                password = getpass.getpass(f"{C.DIM}Password: {C.RESET}")
                if not password:
                    print_error("Cancelled")
                    continue

                print_info("Logging in...")
                success, msg = ai.login(email, password)

                if success:
                    print_success(msg)
                    clear()
                    print_header(ai)
                else:
                    print_error(msg)
            except KeyboardInterrupt:
                print_error("Cancelled")
            continue

        # Logout
        if user_input.lower() in ("/logout", "/lo"):
            if not ai.logged_in:
                print_info("Not logged in")
                continue

            success, msg = ai.logout()
            print_success(msg)
            clear()
            print_header(ai)
            continue

        # Status
        if user_input.lower() in ("/status", "/st"):
            status = ai.get_status()
            print_info(status)
            continue

        # ===== Chat =====

        print_thinking()

        def on_first_chunk(chunk):
            print_response_start()
            print_chunk(chunk)
            on_first_chunk.called = True
        on_first_chunk.called = False

        def on_chunk(chunk):
            if not on_first_chunk.called:
                on_first_chunk(chunk)
            else:
                print_chunk(chunk)

        response, error = ai.send(user_input, callback=on_chunk)

        if error:
            print_error(error)
        elif response:
            print()  # Newline after response
        else:
            print_error("No response received")


if __name__ == "__main__":
    main()
