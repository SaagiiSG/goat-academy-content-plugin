# 🐐 GOAT Academy: Content Machine (Claude Code plugin)

<p align="center"><img src="assets/poster.png" alt="GOAT Academy: вирал формат ологч"></p>

GOAT Academy-ийн гишүүдэд зориулсан контент машин. Claude өөрийн browser-ийг нээгээд:

1. Таны niche-д Instagram Reels, TikTok дээр **жижиг аккаунтуудын вирал болсон форматыг**
   олно (ердийн үзэлтээсээ 3x+ авсан бичлэг).
2. **Jun Yuh-ийн санааны аргачлал** дээр тулгуурлан таны 3 контент баганад санаа гаргана.
3. Скрипт, caption бичиж, **видео** (монгол AI дуу хоолой) болон **carousel** бүтээнэ.
4. **TikTok Studio, Meta Business Suite**-д товлоод тавина. Компьютер унтарсан ч цагтаа
   нийтлэгдэнэ.
5. Үр дүнгээс суралцаж, дараагийн долоо хоногт сайжруулна.

Эхний 2 долоо хоног пост бүрийг танд үзүүлж таны амтыг сурна. Дараа нь зөвшөөрвөл бүрэн
өөрөө ажиллана.

## Суулгах

Шаардлага: Claude Code, [Node.js](https://nodejs.org) 22+, Google Chrome. Видеоны хэрэгслүүдийг (ffmpeg, whisper-cpp, GOAT видео plugin-ууд) тохиргооны үеэр Claude өөрөө суулгана.

```
/plugin marketplace add SaagiiSG/goat-academy-content-plugin
```

```
/plugin install goat-content-machine@goat-content-machine
```

Claude Code-ийг дахин нээгээрэй. Эхний чатад Claude өөрөө тохируулах заавраар (15 минут)
дагуулна: browser нээгдэж, Instagram, TikTok-доо нэг удаа нэвтэрнэ.

## Командууд

| Команд | Юу хийх |
|---|---|
| `/goat-setup` | Тохиргоо: browser, нэвтрэлт, брэнд профайл, дуу хоолой |
| `/goat-week` | Долоо хоногийн контентыг бүтээж товлох (гол команд) |
| `/goat-viral-format` | Вирал формат судлах |
| `/goat-ideas` | Санааны сан дүүргэх |
| `/goat-schedule` | Бэлэн постуудыг товлох |
| `/goat-review` | Үр дүн уншиж суралцах |

## Вирал формат гэж юу вэ

**Жижиг аккаунт (≤100K дагагч) өөрийн ердийн видеоноосоо 3 дахин буюу түүнээс их үзэлт
авсан бичлэг.** Том аккаунт дагагчдынхаа хүчээр үзэлт авдаг. Жижиг аккаунтын огцом өсөлт
бол *формат* ажилласны баталгаа, үүнийг та давтаж чадна.

## Видео

Видеог GOAT-ийн видео plugin-ууд хийнэ. Тохиргооны үеэр Claude таны бизнест тохирохыг нь
суулгана:

| Plugin | Юунд |
|---|---|
| [Doodle Notes](https://github.com/SaagiiSG/goat-doodle-notes), [Word Behind](https://github.com/SaagiiSG/goat-word-behind), [Glass Ribbon](https://github.com/SaagiiSG/goat-glass-ribbon), [Grid Explainer](https://github.com/SaagiiSG/goat-grid-explainer), [Scrapbook](https://github.com/SaagiiSG/goat-scrapbook), [Product Void](https://github.com/SaagiiSG/goat-product-void), [Proof Frame](https://github.com/SaagiiSG/goat-proof-frame) | Таны өөрийн бичлэг, зургийг эдитлэнэ |
| [Animation Engine, Avatar Maker](https://github.com/SaagiiSG/goat-academy-plugins) | Нүүр харуулахгүй AI анимэйшн, монгол дуу хоолойтой; таны cartoon аватар |

## Үнэ

| Хэсэг | Үнэ |
|---|---|
| Plugin, browser, судалгаа, carousel, товлолт | 0₮ |
| Өөрийн бичлэгийг эдитлэх (video look-ууд) | 0₮ (таны компьютер дээр ажиллана) |
| AI анимэйшн ([kie.ai](https://kie.ai)) | ~$0.75–1.50 нэг видео |
| Аватар (kie.ai) | ~$0.09, нэг удаа |
| Монгол дуу хоолой ([ElevenLabs](https://elevenlabs.io)) | Үнэгүй багц бага; олон видеонд төлбөртэй багц |

Сарын төсвөө тохиргооны үеэр хэлнэ; машин түүнээс хэтрүүлэхгүй.

## Нууцлал

- Зөвхөн нийтэд нээлттэй бичлэгийн тоон үзүүлэлт (views, likes, comments) ба caption-ийг
  уншина. Дагагчдын жагсаалт, хувь хүний мэдээлэл цуглуулахгүй.
- Бүх тохиргоо, профайл, контент зөвхөн таны компьютерт (`~/.goat-academy/`) хадгалагдана.
- Claude нууц үг хэзээ ч бичихгүй: та browser цонхонд өөрөө нэвтэрнэ. ElevenLabs түлхүүрээ
  `~/.goat-academy/keys.env` файлд өөрөө бичнэ.
- Зөвхөн таны өөрийн аккаунтад, таны долоо хоногийн хавтас дахь файлыг нийтэлнэ.
- Нууц үг, token-оо хэзээ ч чатад бүү бич.

## Бүтэц

```
.claude-plugin/        plugin.json, marketplace.json
.mcp.json              Claude-ийн browser (Playwright MCP)
WORKSPACE.md           ~/.goat-academy/ хавтасны бүтэц, горимууд, browser-ийн дүрэм
hooks/                 Тохиргоо, долоо хоногийн сануулга, бие даах горимын асуулт
skills/
  goat-setup/          Тохиргоо
  goat-week/           Долоо хоногийн контент машин (гол)
  goat-viral-format/   Вирал формат судалгаа (+ score.js, free_fetch.py)
  goat-ideas/          Санааны хөдөлгүүр (brain/: Jun Yuh-ийн контент санааны аргачлал)
  goat-schedule/       TikTok Studio, Meta Business Suite-д товлох
  goat-review/         Үр дүнгээс суралцах
```

---

**English:** A content machine plugin for GOAT Academy members. Claude drives its own browser to research viral formats, generates ideas with a Jun Yuh-based idea engine, creates videos and carousels, schedules them in TikTok Studio and Meta Business Suite, and learns from results. Viral research finds viral Instagram Reels
and TikTok formats in a member's niche: posts from small accounts (≤100K followers) that got
3x+ the account's usual views (median of its other recent videos), fetched free with yt-dlp
and Instaloader, then turns them into 10 ready-to-shoot post ideas and a 2-week traffic plan,
in Mongolian. For a member's first 3 sessions, a SessionStart hook offers a guided setup.

License: MIT
