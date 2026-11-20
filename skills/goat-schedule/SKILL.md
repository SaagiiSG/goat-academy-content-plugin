---
name: goat-schedule
description: >
  GOAT Content Machine-ийн нийтлэх хэсэг. Бэлэн болсон постуудыг (видео, carousel, caption)
  Claude-ийн browser-оор TikTok Studio болон Meta Business Suite (Instagram)-д байршуулж,
  төлөвлөсөн цагт нь товлож тавина. Платформын өөрийн товлогчийг ашигладаг тул компьютер
  унтарсан ч цагтаа нийтлэгдэнэ. Use when goat-week reaches the scheduling step, or when the
  user types /goat-schedule, /товлох, or says "постуудаа товло", "нийтэл", "schedule my
  posts", "энэ видеог TikTok-д тавь", "Instagram-д товлоод тавь".
---

# GOAT Schedule — товлож нийтлэх

Read `WORKSPACE.md` (plugin root): browser rules, modes. Input: a week folder
`~/.goat-academy/weeks/<week>/` with `plan.md` and `post-NN/` folders.

**Only schedule posts that are ready and allowed**: in learning mode, only posts the member
approved in this session; in autonomous mode, posts that passed goat-week's quality check.
Never upload anything from outside the week folder, never to an account other than the
member's (`state.json` handles).

## Daily quota (anti-ban rule)

Before anything, read WORKSPACE.md → Pace limits and `state.json` → `upload_log`,
`cooldown_until`. Upload **at most 2 posts today in total** (each platform upload counts as
one), never more, even if many posts are `ready` and even if the member asks to "do them
all". Explain once that it protects their account. Pick the `ready` posts with the earliest
publish times first. Wait 2–5 minutes between the two uploads. Log each successful upload in
`upload_log` immediately. Skip any platform under cooldown.

## Why native schedulers

TikTok Studio schedules up to ~10 days ahead; Meta Business Suite schedules Instagram (and
Facebook) posts weeks ahead. Once scheduled, posts go out on time even when Claude and the
computer are off. So the machine only needs to run once a week.

## General method (both platforms)

The upload pages change their layout often. Don't rely on remembered button positions:
1. Navigate, then `browser_snapshot` to read the page.
2. Find the file input / upload area; use `browser_file_upload` with the absolute file
   path(s). For carousels, upload all slide PNGs in order.
3. Wait for processing to finish (snapshot until the progress indicator is gone).
4. Paste the caption from `caption.md` with `browser_type` into the caption field.
5. Switch on "Schedule" and set the date and time from `plan.md` (check the time zone the
   page shows).
6. Before the final click, snapshot and verify: right account, right file, caption, date,
   time. Then click Schedule.
7. Confirm success (a success message or the post listed under scheduled/drafts), and take
   one screenshot as proof into the post folder.
8. Write `status.txt`: `scheduled <platform> <datetime>` or `failed <platform>: <reason>`.

If a login page, captcha or security check appears: stop, ask the member to handle it in
the browser window, then continue. If an upload fails twice, mark it failed and move on.

## TikTok

- URL: `https://www.tiktok.com/tiktokstudio/upload` (or "Upload" from tiktok.com).
- Video: upload `video.mp4`. Carousel: TikTok web supports photo posts on many accounts; if
  the upload area only accepts video, mark the carousel `skipped tiktok: photo upload not
  available on web` and tell the member.
- Settings to set when present: who can watch = Everyone; allow comments on; mark
  "AI-generated content" ON for `video-ai` posts (TikTok requires labelling realistic AI
  content); for a paid promotion / brand post, switch on the content disclosure toggle.
- Scheduling: "When to post" → Schedule → date/time (TikTok allows roughly 15 minutes to
  10 days ahead). If a planned time is more than 10 days out, schedule it in next week's run.

## Instagram (via Meta Business Suite)

Requires `instagram_scheduler: business_suite` in `state.json`.
- URL: `https://business.facebook.com/latest/home` → "Create post" (feed / carousel) or
  "Create reel" (video).
- Placement: select the Instagram account only (unless the member asked to also post on the
  Facebook Page).
- Upload media, paste caption, then "Schedule" → set date/time → Schedule.
- Reels: add the caption; leave "Also share to feed" on.
- For `video-ai` reels, turn on the AI label if the form offers it.

If `instagram_scheduler` is `none`: Instagram can't be scheduled. Options, in order:
1. If Claude is running at the planned time (e.g. the member keeps the session open), post
   directly on `https://www.instagram.com/` (Create → Post/Reel) at that time.
2. Otherwise put the files and caption in `post-NN/` and tell the member to post them, or
   offer again to connect Business Suite (`goat-setup` step 2.3).

## After scheduling

Update `plan.md` with each post's status, and report to goat-week (or to the member when
called directly): scheduled count, failures with reasons, anything the member must do.
