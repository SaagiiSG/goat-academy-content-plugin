---
name: goat-setup
description: >
  GOAT Content Machine-ийн тохируулах заавар (монголоор). Plugin суулгасны дараах эхний
  чатуудад автоматаар санал болгогдоно. Claude өөрийн browser-ийг нээж, гишүүн Instagram,
  TikTok, Meta Business Suite-д нэг удаа нэвтэрнэ; дараа нь гишүүний брэнд профайлыг
  (niche, мессеж, 3 контент багана, үзэгч, зорилго, долоо хоногт хэдэн пост) ярилцлагаар
  бүрдүүлж, ElevenLabs дуу хоолой холбож, анхны 7 хоногийн контентыг эхлүүлнэ. Use when the
  user types /goat-setup, /тохиргоо, or says "тохируулъя", "setup хийе", "яаж эхлэх вэ",
  "plugin ажиллахгүй байна", "browser нээгдэхгүй байна", "дахин нэвтрэх", "профайлаа засах",
  "how do I set up goat academy", or when the GOAT Academy session hook asks to start setup.
---

# GOAT Content Machine — Тохируулах заавар

Read `WORKSPACE.md` at the plugin root first (folder layout, state.json, browser rules).

Members are not programmers. So:
- **One step at a time.** After each step, confirm it worked before moving on.
- Run commands yourself (Bash); the member only approves. The member does only what needs
  their hands: logging in, and writing their API key into a file.
- Never ask for a password or API key in chat. Never print `keys.env`.
- Mongolian, plain words. Explain a technical term once, briefly.

Total time: about 20–30 minutes (most of it waiting for installs). Tell the member that at the start.

## Step 0 — Where are we

```bash
mkdir -p ~/.goat-academy/inbox ~/.goat-academy/weeks && cat ~/.goat-academy/state.json 2>/dev/null; ls ~/.goat-academy; node --version 2>&1 | head -1
```

Skip any step whose result already exists (`profile.md` present → skip Step 3, and so on).
If `setup_done` is true, ask what they want to change (re-login, edit profile, voice) and do
only that.

## Step 1 — Open Claude's browser

The plugin brings its own browser (the `goat-browser` tools). Test it: navigate to
`https://www.tiktok.com` and take a snapshot.

- **Works** → a browser window opens on the member's screen. Tell them: "Энэ бол миний
  ажилладаг browser. Үүнийг хааж болохгүй, ажил дууссаны дараа би өөрөө хаана."
- **Tools missing or `npx` / Node error** → Node.js is not installed. Tell the member to
  install the LTS version from nodejs.org (one installer, next-next-finish), then fully quit
  and reopen Claude Code, then type `/goat-setup` again. On Mac with Homebrew you may run
  `brew install node` yourself with their OK.
- **"Browser not installed" / Chrome not found** → the browser runs on Google Chrome. Ask the
  member to install Chrome from google.com/chrome (normal installer), then try again. They
  don't have to use Chrome themselves; Claude just needs it on the computer.

## Step 2 — Log in once (the member does this)

Open each site in the goat-browser and ask the member to log in **in that window** (not their
usual browser). Wait for "болсон" after each.

1. `https://www.instagram.com/` — their own account.
2. `https://www.tiktok.com/login` — their own account.
3. `https://business.facebook.com/latest/home` — Meta Business Suite. This is what lets us
   **schedule** Instagram posts. It needs the Instagram account to be a *Professional*
   (Creator or Business) account connected to a Facebook Page.
   - If they don't have that: offer to walk them through it (Instagram app → Settings →
     Account type and tools → Switch to professional account; then in Business Suite →
     Settings → Instagram account → Connect). It's free and takes 5 minutes.
   - If they decline: set `instagram_scheduler` to `none`. The machine will then post Instagram
     items at the planned time only while Claude is running, or hand them to the member.
4. Verify each login with a snapshot (profile icon visible, not a login form). Read and save
   their handles. Record in `state.json`: `platforms`, `instagram_handle`, `tiktok_handle`,
   `instagram_scheduler` (`business_suite` if step 3 works).

Mention once: use the browser normally; if a platform asks for a security code, the member
types it in the window.

## Step 3 — Brand profile (interview, ~5 minutes)

Ask in 2–3 short rounds (AskUserQuestion when available). Base it on the Jun Yuh "message
plus pillars" method (`skills/goat-ideas/brain/frameworks.md`, framework 1 and 2):

1. Юуны тухай контент хийдэг вэ? Юу зардаг вэ (сургалт, үйлчилгээ, бүтээгдэхүүн)?
2. Хэнд зориулсан бэ? (нас, хүйс, асуудал нь)
3. Нэг өгүүлбэрт: үзэгчиддээ юу өгөхийг хүсдэг вэ? → this becomes the **message**.
4. 3 сэдэв (багана) + хувийн түүх: suggest 3 pillars from their answers and let them edit.
5. Traffic хаашаа: дагагч / bio линк / DM / дэлгүүр?
6. Долоо хоногт хэдэн пост хүсэх вэ? (default: 4 = 2 video + 2 carousel). Видеонд
   нүүрээ харуулах уу, эсвэл AI дуу хоолой + анимэйшн уу?
7. Брэндийн өнгө, фонт байгаа юу? (If not, pick 2 colors + 1 font for them.)

Also open their own profiles in the browser and read their last 12 posts (views, topics):
it tells you their current level and what already works.

Write `~/.goat-academy/profile.md` with clear headings. Show a 5-line summary and ask
"зөв үү?".

## Step 4 — Video tools (about 5–10 minutes, mostly waiting)

Videos come from the GOAT video plugins (`skills/goat-week/references/video-production.md`
has the full list). Ask two things first:
- Нүүрээ харуулж бичлэг хийх үү? (yes → video looks; no → animation)
- Сард видеонд хэдэн төгрөг/доллар зарцуулж болох вэ? Animation costs about $0.75–1.50 per
  video on kie.ai, plus ElevenLabs. Looks for their own footage are free. Save the monthly
  budget in `profile.md`.

### 4a. Install the plugins (Claude runs these, member approves)

Pick 3–4 looks that fit their business (table in video-production.md), plus animation if
they want faceless videos. For each look:
```bash
claude plugin marketplace add SaagiiSG/goat-doodle-notes && claude plugin install goat-doodle-notes@goat-doodle-notes
```
(same pattern for goat-word-behind, goat-grid-explainer, goat-scrapbook, goat-product-void,
goat-proof-frame). Animation and avatar:
```bash
claude plugin marketplace add SaagiiSG/goat-academy-plugins && claude plugin install animation-engine@goat-academy && claude plugin install avatar-maker@goat-academy
```
Afterwards the member types `/reload-plugins` (or restarts Claude Code) so the new skills
load. Record the installed looks in `profile.md`.

### 4b. Install the tools they need

Check: `node --version` (22+), `ffmpeg -version`, `whisper-cli --help` (whisper-cpp),
`python3 -c "import PIL"`. Install only what's missing, after asking:
- Mac (Homebrew): `brew install node ffmpeg whisper-cpp`; `python3 -m pip install --user pillow`.
  No Homebrew? Offer to install it (brew.sh one-liner) or point to the nodejs.org /
  ffmpeg installers.
- Windows: `winget install OpenJS.NodeJS.LTS` and `winget install Gyan.FFmpeg`, reopen the
  terminal; for captions follow the whisper step in the goat-doodle-notes skill;
  `py -m pip install pillow`.
Tell them: the first talking video downloads a ~1.6 GB speech model once; after that it's
fast. Everything in the looks runs on their computer, nothing is uploaded.

### 4c. Keys (the member types them, never in chat)

- **ElevenLabs** (Mongolian voice): elevenlabs.io → Profile → API Keys. Free plan is small;
  regular videos need a paid plan.
- **kie.ai** (animation and avatar, only if they want those): kie.ai/api-key, then top up
  credits (1 credit = $0.005).

Create the key file with placeholders and open it for them:
```bash
mkdir -p ~/.goat-academy; [ -f ~/.goat-academy/keys.env ] || printf 'ELEVENLABS_API_KEY=\nKIE_API_KEY=\n' > ~/.goat-academy/keys.env; chmod 600 ~/.goat-academy/keys.env
```
Tell them: open `~/.goat-academy/keys.env` (on Mac: `open -e ~/.goat-academy/keys.env`),
paste each key after its `=`, save. Then make every new Claude Code session load it. Mac /
Linux, add once to the shell profile (`~/.zshrc` on Mac, else `~/.bashrc`):
```bash
grep -q goat-academy/keys.env ~/.zshrc 2>/dev/null || printf '\n# GOAT Academy keys\n[ -f ~/.goat-academy/keys.env ] && set -a && . ~/.goat-academy/keys.env && set +a\n' >> ~/.zshrc
```
Windows (PowerShell; the file is `%USERPROFILE%\.goat-academy\keys.env`), run once after
they fill it. It copies the keys into their user environment without showing them:
```powershell
Get-Content "$HOME\.goat-academy\keys.env" | ForEach-Object { if ($_ -match '^(\w+)=(.+)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'User') } }
```
(Run it again whenever they change a key.)

Check without printing values:
```bash
for k in ELEVENLABS_API_KEY KIE_API_KEY; do grep -q "^$k=." ~/.goat-academy/keys.env && echo "$k ok" || echo "$k missing"; done
```
Then they restart Claude Code once so the keys are loaded.

### 4d. Voice and avatar (optional, 2 minutes)

- Voice: their own cloned voice (ElevenLabs Voice Lab, a 1-minute recording) or a stock
  voice. Note the choice in `profile.md`.
- Avatar: if they'll use animation, offer the `make-avatar` skill with one clear photo of
  them (~$0.09). Save the set to `~/.goat-academy/avatar/`: the animations then star a
  cartoon version of the member every time.

Skipping is fine: without keys the machine makes carousels and edits their own clips with
the free looks.

## Step 5 — Start the machine

1. Set in `state.json`: `setup_done: true`, `start_date: <today>`, `mode: "learning"`,
   `autonomy_asked: false`.
2. Explain in 4 lines how it works:
   - Долоо хоног бүр би: вирал формат судална → санаа гаргана → видео, carousel хийнэ →
     танд үзүүлнэ → TikTok Studio, Meta Business Suite-д товлоод тавина.
   - Эхний 2 долоо хоног пост бүрийг танд үзүүлж, юу таалагдсаныг сурна.
   - Дараа нь хүсвэл би бүрэн өөрөө ажиллана.
   - Хэзээ ч `/goat-week` гэж бичээд эхлүүлж болно.
3. Offer to run the first week now: invoke the `goat-week` skill.
