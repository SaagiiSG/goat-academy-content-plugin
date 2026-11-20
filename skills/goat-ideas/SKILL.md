---
name: goat-ideas
description: >
  GOAT Content Machine-ийн санааны хөдөлгүүр. Jun Yuh-ийн контент санааны аргачлал
  (34 видеоноос бүрдсэн "brain": санааны эх сурвалж, бөглөх загвар, дэгээний загвар, 3P түүх,
  4 зорилго) + гишүүний профайл + вирал форматын тайланг нийлүүлж, гишүүний санааны санг
  (idea bank) дүүргэнэ. Санаа бүр дэгээ, формат, Problem/Pursuit/Payoff, зорилготой.
  Use when goat-week needs ideas, or when the user types /goat-ideas, /санаа, or says
  "санаа өг", "санаа дууссан", "юу пост хийх вэ", "нийтлэх зүйл алга", "hook санаа",
  "контент санаа гарга", "what should I post", "I have nothing to post".
---

# GOAT Ideas — санааны хөдөлгүүр

Read `WORKSPACE.md` (plugin root) for the folder layout. Inputs:
- `~/.goat-academy/profile.md` (message, pillars, audience, goal) — required. If missing, run
  the profile part of `goat-setup` first.
- `~/.goat-academy/formats.md` — the latest viral formats. If missing or older than 14 days
  and you have time, run `goat-viral-format` first; otherwise use the format menu in
  `brain/frameworks.md` (framework 13) and say the formats aren't freshly researched.
- `~/.goat-academy/taste.md`, `results.md`, `idea-bank.md` — what the member likes, what
  performed, what's already in the bank (avoid duplicates).

## The brain

`brain/` holds a compiled knowledge base of Jun Yuh's public teaching on content ideas (34
YouTube sources, ids in `brain/sources.md`). Read in this order:
1. `brain/_hot.md` — always.
2. `brain/idea-engine.md` — always: idea sources, 30 fill-in-the-blank prompts, hook
   templates, the one-hour weekly plan, the "nothing to post today" checklist.
3. At most two more when needed: `frameworks.md` (3P story, four missions 3-1-2-1, hook
   mechanics, repurposing ladder, format menu), `principles.md`, `positions.md` (his newer
   view wins when they conflict), `voice.md`, `stories.md`.

This is a simulation of his methods built from public videos, not Jun Yuh. Never say the
ideas come from him personally or invent quotes; when you cite a method, give its source id
(e.g. "3P, S004") in the internal notes, not in the member's post.

## How ideas are made

Every idea = **message pillar × proven viral format × Jun Yuh prompt or idea source**.

1. **Mine** (idea-engine §1): use what the member gave you this week (moments, customer
   questions, DMs) if any; if a DM inbox or comments were read by goat-review, use those
   questions. Otherwise use the transformation list, mistakes list, younger-customer pains.
2. **Shape** each into a fill-in-the-blank prompt (idea-engine §2), translated to the member's
   niche and to natural Mongolian.
3. **Fit a format** from `formats.md` (prefer formats with strong small-account outliers) or
   the format menu. Note the format's example link.
4. **Assign a mission** (framework 18): attract, nurture, position, convert. Weekly mix
   follows 3-1-2-1 scaled to the member's capacity: mostly attract, an offer post at most
   once a week.
5. **Write the 3P**: Problem, Pursuit, Payoff, one line each (framework 3).
6. **Hook**: 2 options, built from the hook templates and hook mechanics (framework 20).
   Check: does the first second make sense on mute?
7. **Media type**: `video-ai` (made by the video skills with ElevenLabs voice), `video-member`
   (member films; needs a clip in `inbox/`), or `carousel`. Respect the member's choice about
   showing their face and `taste.md`.

Personal stories: never invent the member's life events. For story posts write the prompt
("Таны бизнесийн хамгийн хэцүү өдөр…?") and mark the idea `needs-member-input`; the
machine asks the member for the true story before producing it.

## Idea bank format

Append to `~/.goat-academy/idea-bank.md` (create with a header if missing):

```markdown
## I-0042 · new · pillar: [..] · mission: attract · media: carousel
- Hook A: "..."  Hook B: "..."
- Format: [name] (example: URL)
- 3P: Problem: ... / Pursuit: ... / Payoff: ...
- CTA: ...
- Source: prompt #7 (S015) + format F2
```

Keep at least 15 `new` ideas in the bank. When called directly by the member (not by
goat-week), also show the top 5 in chat, in Mongolian, and offer to turn one into a post now.
