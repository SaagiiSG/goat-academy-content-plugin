---
name: goat-audit
description: >
  GOAT профайл аудит. Гишүүний Instagram (ба TikTok) профайлыг Claude-ийн browser-оор уншиж,
  Jun Yuh-ийн контентын аргачлалаар 8 өнцгөөс (мессеж ба багана, хэнд зориулсан, funnel,
  highlights ба нотолгоо, нүүр ба итгэл, давтамж, 3-1-2-1 холимог, ялагч постууд) үнэлж,
  bio-н хувилбар, эхлээд хийх 3 зүйлтэй монгол аудитын хуудас (artifact) гаргана. Долоо хоног
  бүр дахин ажиллаж, ижил хуудсаа шинэчилж, өөрчлөлтийг түүхэнд нэмнэ. Use when the user
  types /goat-audit, /аудит, or says "профайлаа шалга", "аудит хий", "миний профайл яаж
  байна", "audit my profile", "audit this account", or when goat-autopilot runs the weekly
  audit.
---

# GOAT Audit — долоо хоног бүрийн профайл аудит

Read `WORKSPACE.md` (plugin root). The page is built from `assets/audit-template.html`
(next to this file). The template draws everything from one JSON block, so each run only
writes data; the design stays the same for every member.

## 1. Which profile

Default: the member's own `instagram_handle` from `state.json` (plus `tiktok_handle` when
present: add TikTok as a second section of lenses only if it has data). If the member gives
another URL or handle ("audit this account"), audit that one but don't change their weekly
audit; give it its own data folder `~/.goat-academy/audit/<handle>/`.

## 2. Collect (Claude's built-in browser, logged in)

Open `https://www.instagram.com/<handle>/` and read with snapshots:
- name, bio (exact text), link, followers, following, post count, category, highlights
  (names, in order);
- the latest 12–30 posts: type (reel / carousel / photo), cover text, caption first line,
  date, and for reels the view count shown on the grid (`/<handle>/reels/`); likes and
  comments by opening a few posts if the grid doesn't show them;
- pinned posts.
Compute the usual views (median of reels older than 7 days) and winners (≥ 2x usual) with
`skills/goat-viral-format/scripts/score.js` (put the member's own account through it).

Go slowly (WORKSPACE.md browser rules). If logged out or blocked: use what the public page
shows, and mark the lenses that need post data as `none` with a clear note. Never invent a
number.

## 3. Score with the Jun Yuh brain

Read `skills/goat-ideas/brain/_hot.md`, then frameworks 1, 2, 7, 18, 22 and positions
"Niche", "Personal brand versus a business page", "Posting cadence", "Showing your face",
"Selling inside content". Score these 8 lenses, each with `status` (`good` / `warn` /
`weak` / `none`), `score` 1–5 (null when not measured), a `finding` (what you saw, concrete,
quoting the profile), a `fix` (what to do, concrete, in their niche) and `sources` (framework
number and S-ids):

| Lens (name in Mongolian) | Question | Brain |
|---|---|---|
| Мессеж ба багана | One message, 3–4 pillars? | Framework 1 |
| Хэнд зориулсан бэ | Would the right person know in 3 s it's for them? | Framework 2 (WHO) |
| Профайл → санал (funnel) | Does the profile send traffic to an offer? | Positions: personal brand vs business |
| Нотолгоо ба түүх (highlights) | Do highlights show proof, origin, offer? | Framework 22 |
| Нүүр ба итгэл | Can people see and trust the person? | Positions: showing your face |
| Нийтлэх давтамж | Steady cadence (≥3/week)? | Positions: posting cadence |
| Зорилгын холимог (3-1-2-1) | Attract / nurture / position / convert balance (last 12 posts) | Framework 18 |
| Ялагч постууд | Which formats beat their usual views by 2x+? | Framework 7 |

Then write: a 3–4 sentence `summary` (strongest point, biggest gap, what to do this week),
3 `actions` (title with time estimate + detail), and 2 `bio_options` (label, text, why).
Plain spoken Mongolian. Never shame; Jun Yuh "never shames a flop".

## 4. Build and publish

Data lives in `~/.goat-academy/audit/<handle>/data.json`. Load the previous one if it exists:
keep its `history` and append today's row (`date`, `followers`, `posts`, `following`,
`median_views`, `note`: one line on what changed since last week, e.g. "+312 дагагч, bio
шинэчилсэн"). Mention last week's actions that were done in the summary.

Fill the template: replace the text between `/*AUDIT_DATA_START*/` and `/*AUDIT_DATA_END*/`
with the JSON (escape `</` as `<\/`), and set `<title>` to `@<handle> Profile Audit`. Save
as `~/.goat-academy/audit/<handle>/audit.html`.

**Publish to the same place every week:**
- If an Artifact tool is available: first time, publish the file (icon "chart") and save the
  returned URL as `audit_artifact_url` in `state.json` (for another handle, in that handle's
  `data.json` as `artifact_url`). Later runs: read the artifact once with that URL, then
  publish the new file with `url` set to it, so the link never changes. If a publish is
  refused because the page changed, merge onto the version it returns and publish again.
- No Artifact tool (or it fails): open `audit.html` in the helper browser (`goat-browser`;
  the built-in browser can't open local files) and tell the member where the file is. The weekly file is overwritten in place.

Set `last_audit: <today>` in `state.json`. When run by the member, end with the link and the
3 actions in chat. When run by goat-autopilot, put the link in the run report.
