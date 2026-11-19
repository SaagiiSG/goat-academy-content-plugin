#!/usr/bin/env python3
"""GOAT Academy SessionStart hook.

For a member's first few Claude Code sessions after installing the plugin, this
tells Claude to open with the Mongolian setup guide. It stops once setup is
marked done (by the goat-setup skill) or after MAX_GUIDED_SESSIONS sessions.

State lives in ~/.goat-academy/state.json. Nothing is sent anywhere.
"""
import json
import sys
from pathlib import Path

MAX_GUIDED_SESSIONS = 3
STATE_DIR = Path.home() / ".goat-academy"
STATE_FILE = STATE_DIR / "state.json"


def load_state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state):
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass  # never block a session because of state


def main():
    state = load_state()
    if state.get("setup_done"):
        return 0

    count = int(state.get("guided_sessions", 0)) + 1
    if count > MAX_GUIDED_SESSIONS:
        return 0
    state["guided_sessions"] = count
    save_state(state)

    if count == 1:
        stage = (
            "This is the member's FIRST session since installing the GOAT Academy plugin. "
            "Before anything else, greet them warmly in Mongolian (2-3 sentences: what the plugin "
            "does, that setup takes about 5 minutes) and offer to start setup right now by running "
            "the goat-setup skill. If they agree, invoke the goat-setup skill."
        )
    else:
        stage = (
            f"This is session {count} of {MAX_GUIDED_SESSIONS} since the member installed the GOAT "
            "Academy plugin, and setup is not finished yet. In your first reply, add ONE short "
            "Mongolian line reminding them that setup is unfinished and that typing /goat-setup "
            "continues it. Then help with whatever they asked. Do not push further if they decline."
        )

    context = (
        "[GOAT Academy plugin] " + stage + " If the member says setup is already done or asks you "
        "to stop these reminders, run the goat-setup skill's 'mark done' step."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
