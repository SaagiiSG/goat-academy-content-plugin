#!/usr/bin/env python3
"""GOAT Academy SessionStart hook.

- Before setup: for the member's first few sessions, tells Claude to open with the
  Mongolian setup guide (goat-setup).
- After setup: tells Claude when a new content week is due (goat-week), and when the
  14-day learning period is over and it should ask about running on its own.

State lives in ~/.goat-academy/state.json. Nothing is sent anywhere.
"""
import json
import sys
from datetime import date
from pathlib import Path

MAX_GUIDED_SESSIONS = 3
WEEK_DUE_DAYS = 6
LEARNING_DAYS = 14
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


def days_since(iso):
    try:
        return (date.today() - date.fromisoformat(str(iso)[:10])).days
    except Exception:
        return None


def before_setup(state):
    count = int(state.get("guided_sessions", 0)) + 1
    if count > MAX_GUIDED_SESSIONS:
        return None
    state["guided_sessions"] = count
    save_state(state)
    if count == 1:
        return (
            "This is the member's FIRST session since installing the GOAT Academy content "
            "machine plugin. Before anything else, greet them warmly in Mongolian (2-3 "
            "sentences: it researches viral formats, creates their posts and schedules them on "
            "Instagram and TikTok; setup takes about 15 minutes) and offer to start setup now "
            "with the goat-setup skill. If they agree, invoke goat-setup."
        )
    return (
        f"This is session {count} of {MAX_GUIDED_SESSIONS} since the member installed the GOAT "
        "Academy plugin, and setup is not finished. In your first reply add ONE short Mongolian "
        "line saying setup is unfinished and /goat-setup continues it. Then help with what they "
        "asked. Do not push if they decline."
    )


def after_setup(state):
    notes = []
    mode = state.get("mode", "learning")
    since_week = days_since(state.get("last_week_run"))
    since_start = days_since(state.get("start_date"))

    if mode == "learning" and not state.get("autonomy_asked") and since_start is not None \
            and since_start >= LEARNING_DAYS:
        notes.append(
            f"The member's {LEARNING_DAYS}-day learning period is over. When the next goat-week "
            "run starts (or now, if they have no other request), show what was learned and ask "
            "once whether the machine may run on its own, as goat-week step 4 describes."
        )

    report = STATE_DIR / "autopilot" / "last-run.md"
    try:
        seen = state.get("autopilot_report_seen")
        mtime = date.fromtimestamp(report.stat().st_mtime).isoformat()
        if report.exists() and seen != mtime:
            notes.append(
                "The GOAT autopilot ran while the member was away. In your first reply, summarize "
                f"{report} in 2-4 Mongolian lines (what was made, uploaded, what needs them), then "
                f"set autopilot_report_seen to \"{mtime}\" in state.json."
            )
    except Exception:
        pass

    if not state.get("autopilot") and state.get("mode") == "autonomous":
        today = date.today().isoformat()
        if (state.get("upload_log") or {}).get(today) is None:
            notes.append(
                "Autopilot is not installed, so posts are only uploaded when the member opens "
                "Claude. If any post in ~/.goat-academy/weeks is marked ready, offer in one line "
                "to upload today's (max 2) now with goat-schedule."
            )

    if since_week is None or since_week >= WEEK_DUE_DAYS:
        if mode == "autonomous":
            notes.append(
                "A new content week is due and the member granted autonomous mode. Unless they "
                "asked for something else, tell them in one Mongolian line that you are "
                "preparing next week's content, then run the goat-week skill."
            )
        else:
            notes.append(
                "A new content week is due. In your first reply, offer in one Mongolian line to "
                "prepare and schedule next week's content now (goat-week skill). Then help with "
                "what they asked."
            )
    return " ".join(notes) or None


def main():
    state = load_state()
    msg = after_setup(state) if state.get("setup_done") else before_setup(state)
    if not msg:
        return 0
    context = (
        "[GOAT Academy plugin] " + msg + " The member can stop these reminders by saying so; "
        "then set setup_done true (before setup) or note it in state.json."
    )
    print(json.dumps({
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
