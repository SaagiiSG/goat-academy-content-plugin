---
name: goat-week
description: >
  GOAT Content Machine — долоо хоногийн контентыг эхнээс нь дуустал хийдэг гол skill.
  Вирал формат шинэчлэх → санаа сонгох → скрипт, caption бичих → видео (AI дуу хоолой,
  анимэйшн) ба carousel бүтээх → гишүүнд үзүүлж батлуулах (эхний 2 долоо хоног) →
  TikTok Studio, Meta Business Suite-д товлож тавих → тайлан. Use when the user types
  /goat-week, /долоо-хоног, /контент-машин, or says "энэ долоо хоногийн контентоо хий",
  "машинаа ажиллуул", "дараагийн долоо хоногийн пост", "контент бэлд", "run my content
  machine", or when the GOAT session hook says a new week is due.
---

# GOAT Week — долоо хоногийн контент машин

Read `WORKSPACE.md` (plugin root) first: folders, `state.json`, modes, browser rules.

Before starting, check `state.json`. If `setup_done` is not true, run `goat-setup` instead.
Create this week's folder `~/.goat-academy/weeks/<YYYY>-W<NN>/` (ISO week of the first
posting day; if today is Fri–Sun, plan next week).

Tell the member in one line what you're about to do and roughly how long it takes.

## 1. Refresh research (only when needed)

- `formats.md` older than 14 days or missing → run `goat-viral-format` in machine mode (it
  saves to `formats.md`, no long chat report).
- Run `goat-review` first if any posts from previous weeks have no 48h/7d numbers yet: last
  week's results should shape this week.

## 2. Plan the week

1. Read `profile.md` (capacity, pillars, goal), `taste.md`, `results.md`.
2. Make sure `idea-bank.md` has ≥15 `new` ideas; if not, run `goat-ideas`.
3. Pick ideas for the week's capacity (default 4 posts: 2 video, 2 carousel):
   - Mission mix 3-1-2-1 scaled (mostly attract; max one convert post).
   - 80% proven formats (best outliers in `formats.md` and best rows in `results.md`), 20%
     experiments (Jun Yuh, positions.md "Studying formats").
   - Different pillars across the week; nothing that `taste.md` rules out.
   - Ideas marked `needs-member-input`: ask the member for the true story now (one question
     per idea). If they don't answer, swap the idea.
4. Pick posting times: if `results.md` shows best times use them; else TikTok 19:00–21:00 and
   Instagram 12:00–13:00 or 20:00–21:00 local time. Obey WORKSPACE.md → Pace limits: **at
   most 2 posts per day across all platforms** (a cross-posted video counts twice), ≥ 4 h
   apart. So the week holds at most 14 posts; cut the plan to fit before creating anything.
5. Write `plan.md`: table of posts (no., day/time, platform(s), media type, idea id, hook,
   mission). Mark ideas `planned` in `idea-bank.md`.

## 3. Create each post

For each post make `post-NN/` with:
- `script.md` — for video: the spoken script in Mongolian, second by second, with on-screen
  text and visual notes. For carousel: slide-by-slide text.
- `caption.md` — caption (hook line first, value, CTA matching the traffic goal), 3–5
  hashtags (mix of niche + Mongolian), and the platform-specific variants if needed.
- the media file(s).

Write in the member's voice (`profile.md`, `taste.md`). Plain spoken Mongolian, short
sentences. If the `unslop-mn` skill is installed, pass hooks and captions through it.

**Media by type**:
- `carousel` → follow `references/carousel.md` (HTML slides rendered to PNG in the
  goat-browser).
- `video-ai` → follow `references/video-production.md` (GOAT video skills + ElevenLabs).
- `video-member` → use a clip from `~/.goat-academy/inbox/`. If none is there, write a
  filming card (what to film, where, which lines, 30–60 s) and ask the member to drop the clip
  in `inbox/`; meanwhile replace this slot with a carousel so the week isn't blocked. When a
  clip exists, edit it with the video skills (cuts, captions, motion graphics).

Check every post before review: hook is in the first 1–2 seconds / first slide, readable on
mute, no spelling mistakes, correct aspect ratio (9:16 video, 4:5 carousel), file sizes
acceptable (video < 500 MB, ≤ 10 min), caption under platform limits (Instagram 2,200
chars, TikTok 4,000).

## 4. Review with the member (depends on mode)

**learning mode** (first 14 days): show each post one by one: the hook, a preview (send the
image / video file to the member if a file-sending tool exists, else give the path), caption.
Ask:
1. "Нийтлэх үү?" (yes / change / skip)
2. "Юу нь таалагдсан, юу нь таалагдаагүй вэ?" — keep it to one quick question.
Apply changes, then write the lesson to `taste.md` as a short rule with the date. Learn
fast: after 2–3 similar answers, turn them into a firm rule and stop asking about it.

**After day 14** (`today - start_date ≥ 14` and `autonomy_asked` is false): before reviewing,
show what you learned (top rules from `taste.md`, best and worst posts from `results.md`)
and ask once: "Одоо би өөрөө бүрэн ажиллаад, товлосон постуудаа танд тайлан болгож илгээх
үү? Хүссэн үедээ буцааж болно." Save the answer (WORKSPACE.md → Modes). If they say yes, offer the daily autopilot right away
(the `goat-autopilot` skill, part A): without it the machine only works when they open Claude.

**autonomous mode**: skip per-post review, except the cases WORKSPACE.md lists as "stop and
ask". Run your own quality check strictly against `taste.md`.

## 5. Schedule

Mark each approved post `ready` in its `status.txt`. Then run `goat-schedule`: it uploads
**today's quota only** (max 2, WORKSPACE.md → Pace limits), each scheduled for its planned
time. The rest go up on the following days: goat-autopilot does that daily; without
autopilot, the session hook reminds the member to open Claude so the next uploads happen.
Plan publish times so every post can be uploaded at least a day before it goes live.

## 6. Report

Short Mongolian summary in chat:
- What's scheduled (day, time, platform, hook), and anything that failed and why.
- What the member needs to do, if anything (film a clip, answer a story question).
- Next run: "Дараагийн долоо хоногийн контентыг [date]-нд бэлдэнэ."

Update `state.json`: `last_week_run: <today>`. Mark ideas `posted` once scheduled.
