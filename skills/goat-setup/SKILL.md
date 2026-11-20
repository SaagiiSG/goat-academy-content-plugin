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

Total time: about 15 minutes. Tell the member that at the start.

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

## Step 4 — Mongolian voice (ElevenLabs)

Video skills use ElevenLabs for the Mongolian voice-over.

1. Ask if they have an ElevenLabs account. If not: elevenlabs.io → sign up. The free plan has
   a small monthly allowance; more videos need a paid plan. Tell them this honestly.
2. They copy their API key (Profile → API Keys) and save it **themselves**. Create the file
   for them with a placeholder and open it in their editor:
   ```bash
   [ -f ~/.goat-academy/keys.env ] || printf 'ELEVENLABS_API_KEY=энд_түлхүүрээ_тавина\n' > ~/.goat-academy/keys.env; chmod 600 ~/.goat-academy/keys.env
   ```
   Tell them: open `~/.goat-academy/keys.env`, replace the placeholder, save. Never paste it
   in chat.
3. Check it exists without printing it:
   ```bash
   grep -q '^ELEVENLABS_API_KEY=sk' ~/.goat-academy/keys.env && echo key-ok || echo key-missing
   ```
   (ElevenLabs keys start with `sk_`. If not, ask them to recheck.)
4. Voice choice: ask whether they want their own cloned voice (ElevenLabs Voice Lab, needs a
   1-minute recording) or a stock voice. Note the choice and voice name in `profile.md`.

Skipping is fine: videos will then use the member's own recorded voice or text-only.

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
