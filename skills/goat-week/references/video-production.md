# Videos: production with the GOAT video plugins

Videos are made by separate GOAT plugins that `goat-setup` installs. This machine never
edits video itself: it prepares the inputs, invokes the right skill, and checks the result.
Each video skill has its own full instructions; follow them once invoked.

Glass Ribbon (`goat-glass-ribbon`) is left out on purpose while it is being reworked. Don't use
it even if the member has it installed, until this file lists it.

| Plugin (marketplace) | Skill | Input | Cost |
|---|---|---|---|
| `goat-doodle-notes@goat-doodle-notes` | `goat-doodle-notes` | member's clips or photos | free (runs locally) |
| `goat-word-behind@goat-word-behind` | `goat-word-behind` | talking-head clip | free |
| `goat-grid-explainer@goat-grid-explainer` | `goat-grid-explainer` | talking-head clip | free |
| `goat-scrapbook@goat-scrapbook` | `goat-scrapbook` | clips + photos | free |
| `goat-product-void@goat-product-void` | `goat-product-void` | product photos | free |
| `goat-proof-frame@goat-proof-frame` | `goat-proof-frame` | before + after clip/photo | free |
| `animation-engine@goat-academy` | `animate` (+ `mn-voice`, `reel-edit`) | script only | kie.ai ~150–300 credits ($0.75–1.50) per 15–35 s piece + ElevenLabs |
| `avatar-maker@goat-academy` | `make-avatar` | one photo of the member | ~17 credits ($0.09), once |

Check what's installed with `claude plugin list`. If a needed plugin is missing, offer to run
the `goat-setup` video step; meanwhile fall back (below).

## Choosing the video type for a post

1. **`video-ai` (no filming)** → `animate`. Use when the member doesn't show their face, has
   no fitting clip, or the format is a skit, story or animated explainer. If `profile.md` has
   an avatar (`~/.goat-academy/avatar/`), use it as the main character's reference image so
   every animation features the same "cartoon member". Voice lines in Mongolian via
   `mn-voice` (ElevenLabs v4; the voice set in `profile.md`).
2. **`video-member` (member's footage)** → pick a look by the post's format and the member's
   business, then `taste.md` preferences:

| Post format / content | Best look | Also good |
|---|---|---|
| Talking-head opinion, myth vs truth, hot take | Word Behind Head | Doodle Notes |
| Step-by-step, how to book, app or process demo | Grid Explainer | Doodle Notes (paper page) |
| Tips list, pointing at things, features, "look here" | Doodle Notes | Word Behind (chips) |
| Before / after, transformation, result proof | Proof Frame | Scrapbook |
| Product showcase, new arrivals, price | Product Void | Scrapbook, Doodle Notes |
| Lifestyle, journal, behind the scenes, salon/boutique | Scrapbook | Doodle Notes |
| Premium beauty, skincare, wellness talking head | Word Behind Head | Scrapbook |

Rotate looks across the week so the feed doesn't repeat; in learning mode, try at least 3
different looks over the 2 weeks and record which the member likes in `taste.md`.

## Running a video skill from the machine

The look skills work in "the current folder": they create `raw/` and `output/` there and
expect clips in `raw/`. So for post `post-NN/`:
1. `mkdir -p post-NN/raw post-NN/output`; copy the chosen clips from `~/.goat-academy/inbox/`
   (and photos) into `post-NN/raw/`. Move used clips from `inbox/` to `inbox/used/`.
2. Invoke the look skill and treat `post-NN/` as the project folder (`cd` there in every
   command). Give it what it would otherwise ask the member for: the script/notes from
   `script.md`, what to point at, prices or offers only if the member gave them (never
   invent a price, phone number or date), brand colors from `profile.md`.
3. The skills may want to self-update first and ask for `/reload-plugins`. In autonomous mode
   skip the update step if it would need the member.
4. Long steps (first speech-model download ~1.6 GB, renders) take minutes: run them in the
   background or with a 10-minute timeout, and never restart an interrupted download.
5. Copy the result (`output/<look>.mp4`) to `post-NN/video.mp4`.

For `animate`: run it inside `post-NN/` too. **Before spending:** check the price with the
skill's `KIE price` / `KIE credits` commands, and stay within the member's monthly video
budget in `profile.md` (track spend in `~/.goat-academy/spend.md`: date, post, credits). In
learning mode always show the animatic (free still-frame cut) and get a yes before paying for
video generation. In autonomous mode, go ahead within budget; if the budget would be
exceeded, make that post a carousel and tell the member.

## Keys and tools

The video skills read `KIE_API_KEY` and `ELEVENLABS_API_KEY` from the environment of the
shell Claude Code started from. `goat-setup` stores them in `~/.goat-academy/keys.env` (the
member types them in themselves) and adds a line to the shell profile that loads that file,
so every new Claude Code session has them. If a skill says a key is missing: check
`grep -c '^KIE_API_KEY=.' ~/.goat-academy/keys.env` (never print the file) and ask the member
to restart Claude Code; if the key is absent, run the goat-setup key step.

Tools the looks need: Node 22+, ffmpeg, whisper-cpp (captions). Animation needs Python 3
with Pillow, and ffmpeg. `goat-setup` installs them with the member's OK.

## Fallbacks

- Look plugin missing or a render fails twice → make the post a carousel this week, keep the
  clip in `inbox/` for next time, and tell the member.
- No clip for a `video-member` post → filming card (what to film: phone upright, chest up,
  hold still 2–3 s on anything that gets a drawing, quiet room) and swap in a carousel.
- No kie.ai key or budget → don't plan `video-ai` posts.

## Check after rendering

Extract 3 frames (start, middle, end) with ffmpeg and read them: hook text visible in the
first second, captions readable and not covering the face, nothing cut off, 1080×1920.
Confirm the audio is Mongolian and matches the script. AI-generated videos get the platform
AI label when scheduled (goat-schedule).
