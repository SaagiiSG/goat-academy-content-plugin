---
name: goat-setup
description: >
  GOAT Academy plugin-ийн тохируулах заавар (монголоор). Plugin суулгасны дараах эхний
  чатуудад автоматаар санал болгогдоно. Гишүүнд алхам алхмаар туслана: plugin юу хийдгийг
  тайлбарлах, үнэгүй scraper (yt-dlp, Instaloader) эсвэл Apify-г холбох, туршилт хийх,
  дууссаныг тэмдэглэх. Use when the user types /goat-setup, /тохиргоо, or says "тохируулъя",
  "setup хийе", "яаж эхлэх вэ", "plugin ажиллахгүй байна", "Apify холбох", "scraper суулгах",
  "how do I set up goat academy", or when the GOAT Academy session hook asks to start setup.
---

# GOAT Academy — Тохируулах заавар

Гишүүд ихэвчлэн программист биш. Тиймээс:
- **Нэг удаад нэг алхам.** Алхам бүрийн дараа "болсон уу?" гэж асуугаад хүлээ.
- Терминалын командыг гишүүнд хуулахаар өгөхийн оронд **өөрөө ажиллуул** (Bash tool),
  гишүүн зөвшөөрөл өгөхөд л хангалттай. Зөвхөн нууц үг, нэвтрэлт шаардсан алхмыг гишүүн
  өөрөө хийнэ.
- Нууц үг, token-ыг **хэзээ ч чатад бичүүлэхгүй**.
- Монголоор, энгийн үгээр. Техникийн нэр томьёог нэг удаа товч тайлбарла.

## Алхам 0 — Төлөв шалгах

```bash
cat ~/.goat-academy/state.json 2>/dev/null; claude mcp list 2>/dev/null | grep -i -E "apify|brightdata|vidiq"; python3 -c "import yt_dlp, instaloader; print('free-ok')" 2>&1 | tail -1
```

Үр дүнгээс аль хэсэг нь аль хэдийн бэлэн болохыг тодорхойлж, бэлэн хэсгийг алгас.
`setup_done: true` бол "Тохиргоо аль хэдийн дууссан" гээд Алхам 4-ийн туршилтыг санал болго.

## Алхам 1 — Танилцуулга (2–4 өгүүлбэр)

Энэ plugin юу хийдгийг хэл:
- `/goat-viral-format`: таны niche-д Instagram Reels, TikTok дээр яг одоо вирал болж буй
  форматыг олж, танд 10 бэлэн пост санаа, 2 долоо хоногийн төлөвлөгөө гаргана.
- Жинхэнэ тоон дата (бичлэг бүрийн үзэлт) авахын тулд нэг "дата tool" холбох хэрэгтэй.
  Үүнд 5 минут орно.

## Алхам 2 — Дата tool сонгох

AskUserQuestion (байвал) эсвэл энгийн асуултаар сонгуул:

| Сонголт | Үнэ | Давуу тал | Сул тал |
|---|---|---|---|
| **A. Үнэгүй (yt-dlp + Instaloader)** | 0₮ | Бүрэн үнэгүй, open-source | TikTok заримдаа эвдэрдэг, Instagram нэвтрэлт шаардаж магадгүй |
| **B. Apify (санал болгох)** | Сар бүр үнэгүй credit, дараа нь хэрэглээгээр | Хамгийн найдвартай, Instagram + TikTok бүрэн | Бүртгэл хэрэгтэй, их хэрэглэвэл төлбөртэй |
| **C. Одоохондоо алгасах** | 0₮ | Шууд эхэлнэ | Зөвхөн вэб хайлт, тоо сул |

A ба B хоёуланг нь хийж болно: Apify үндсэн, үнэгүй нь нөөц.

## Алхам 3A — Үнэгүй scraper суулгах

1. Python байгаа эсэх: `python3 --version` (байхгүй бол python.org-оос суулгах заавар өг).
2. Суулгах (гишүүнээс зөвшөөрөл аваад өөрөө ажиллуул):
   ```bash
   python3 -m pip install --user -U yt-dlp instaloader
   ```
3. TikTok туршилт (жижиг, 5 пост):
   ```bash
   python3 "<goat-viral-format skill folder>/scripts/free_fetch.py" tiktok khaby.lame --limit 5 --out /tmp/goat-test.json
   ```
   Скриптийн зам: энэ skill-ийн хажууд байгаа `goat-viral-format/scripts/free_fetch.py`.
   Олдохгүй бол `find ~/.claude -name free_fetch.py` гэж хай.
4. Instagram: эхлээд нэвтрэлтгүй туршина. "login required" / 401 / 429 гарвал гишүүнд:
   - Өөрийн терминалд **өөрөө** `instaloader --login ТАНЫ_IG_НЭР` гэж бичээд нууц үгээ
     тэнд оруулна (Claude-д хэзээ ч бүү өг). Үндсэн биш, нэмэлт аккаунт ашиглахыг зөвлө.
   - Дараа нь skill нь `--session ТАНЫ_IG_НЭР`-ээр ажиллана.
5. Ажиллахгүй бол: `python3 -m pip install --user -U yt-dlp` (yt-dlp-г шинэчлэх нь
   TikTok-ийн ихэнх алдааг засдаг). Дахин бүтэлгүйтвэл B сонголтыг санал болго.

## Алхам 3B — Apify холбох

1. Гишүүн apify.com дээр үнэгүй бүртгүүлнэ (Google-ээр нэвтэрч болно).
2. Терминалд (Claude Code-ийн гадна, ердийн терминал):
   ```bash
   claude mcp add apify "https://mcp.apify.com" -t http
   ```
3. Claude Code-ийг хаагаад дахин нээ. Эхний удаа Apify ашиглахад нэвтрэх хуудас нээгдэнэ,
   зөвшөөр.
4. Дахин нээсний дараа энэ skill-ийг (`/goat-setup`) ажиллуулбал Алхам 0 Apify-г харна.

Команд ажиллахгүй бол docs.apify.com/platform/integrations/mcp-ийн хамгийн сүүлийн
зааврыг шалга.

## Алхам 4 — Туршилт

"Таны niche юу вэ?" гэж асуугаад `goat-viral-format` skill-ийг **жижиг хэмжээгээр**
ажиллуул (3 аккаунт, аккаунт бүрээс 10 пост), тоон дата ирж байгааг харуул.

## Алхам 5 — Дууссаныг тэмдэглэх ("mark done")

```bash
mkdir -p ~/.goat-academy && python3 - <<'EOF'
import json, pathlib
p = pathlib.Path.home()/".goat-academy"/"state.json"
s = json.loads(p.read_text()) if p.exists() else {}
s["setup_done"] = True
p.write_text(json.dumps(s, ensure_ascii=False, indent=2))
print("ok")
EOF
```

Дараа нь богино хураангуй өг:
- Юу холбогдсон (A / B / C)
- Өдөр тутам ашиглах: `/goat-viral-format` (эсвэл "юу пост хийх вэ?" гэж асуухад л болно)
- 2 долоо хоног тутам дахин ажиллуулахыг зөвлө, trend өөрчлөгддөг.
- Тохиргоог дахин хийх бол `/goat-setup`.

Гишүүн C сонгосон эсвэл "дараа хийнэ" гэвэл ч Алхам 5-ыг хийж, сануулга зогсоо. Дараа нь
хүссэн үедээ `/goat-setup` бичиж болно гэдгийг хэл.
