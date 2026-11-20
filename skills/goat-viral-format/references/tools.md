# Дата tool-ууд: ашиглах ба суулгах

## Агуулга
0. Үнэгүй скрипт (browser ажиллахгүй үеийн нөөц)
1. Apify (нөөц)
2. Bright Data
3. vidIQ
4. Вэб хайлт (fallback)
5. Гишүүнд зориулсан суулгах заавар

---

## 0. Үнэгүй скрипт: browser ажиллахгүй үеийн нөөц

`scripts/free_fetch.py`: TikTok-ийг yt-dlp, Instagram-ийг Instaloader-оор уншина.
`discover` (hashtag → аккаунт) ба `scan` (аккаунт → вирал бичлэг) гэсэн 2 команд.
Дүрэм, командуудыг SKILL.md-ийн Алхам 3-аас, бүх сонголтыг `--help`-ээс хар.

Түгээмэл алдаа:
- TikTok "Unable to extract" → `python3 -m pip install --user -U yt-dlp` (TikTok өөрчлөгдөх
  бүрт yt-dlp шинэчлэгддэг).
- Instagram 401 / 429 / "login required" → `--session` (goat-setup), эсвэл 10–30 минут хүлээ.
- Дагагчийн тоо `null` → аккаунтын хуудас бүрэн уншигдаагүй. Жижиг эсэхийг вэб хайлтаар
  шалга, эсвэл тэр аккаунтыг алгас.

---

## 1. Apify MCP: нөөц

Instagram, TikTok-ийн бүрэн нээлттэй дата (views, likes, comments, дагагч, огноо, caption).
Нэвтрэлт нь OAuth тул token хуулах шаардлагагүй. Үнэгүй багцад сар бүр бага хэмжээний
credit ордог (одоогийн хэмжээг apify.com/pricing-оос шалга). Энэ skill-ийн нэг ажиллуулалт
ихэвчлэн үнэгүй эрхэд багтдаг.

**Ажиллах арга:** Apify MCP нь "Actor" (бэлэн scraper) хайж, ажиллуулдаг. Tool-ийн нэр
хувилбараас хамаарч өөрчлөгддөг тул эхлээд ToolSearch-аар `apify` гэж хайж жинхэнэ нэрийг
нь ол. Ихэвчлэн: Actor хайх (`search-actors`), Actor-ын input schema харах
(`fetch-actor-details`), ажиллуулах (`call-actor`), үр дүн авах (`get-actor-output`).

**Ашиглах Actor-ууд** (нэрийг `search-actors`-оор баталгаажуул, input-ыг
`fetch-actor-details`-ээс уншина. Input талбарын нэрийг таамаглаж болохгүй):

| Зорилго | Actor (жишээ) |
|---|---|
| IG hashtag-ийн топ бичлэг | `apify/instagram-hashtag-scraper` |
| IG профайлын reels | `apify/instagram-reel-scraper` эсвэл `apify/instagram-scraper` |
| TikTok hashtag / хайлт | `clockworks/tiktok-scraper` |
| TikTok профайлын бичлэгүүд | `clockworks/tiktok-scraper` эсвэл `clockworks/tiktok-profile-scraper` |

**Зардал хэмнэх:** `resultsLimit` / ижил төстэй талбарыг аккаунт бүрт 20–30 болгож тохируул.
Аккаунтуудыг нэг run-д массиваар өг (олон жижиг run-аас хямд).

**Үр дүнгийн талбарууд:** IG: `videoViewCount` / `videoPlayCount`, `likesCount`,
`commentsCount`, `timestamp`, `url`, `caption`, `ownerUsername`. TikTok: `playCount`,
`diggCount`, `shareCount`, `commentCount`, `createTimeISO`, `webVideoUrl`, `text`,
`authorMeta.fans`. Талбарын нэр Actor-оос хамаарч ялгаатай байж болно, тиймээс эхний мөрийг
харж баталгаажуул.

---

## 2. Bright Data

Anthropic-ийн plugin directory-д байдаг ("Bright Data" plugin). Сар бүр 5,000 хүсэлт үнэгүй.
Гэхдээ Instagram/TikTok-ийн бүтэцтэй дата tool-ууд (`web_data_instagram_reels`,
`web_data_instagram_profiles`, `web_data_tiktok_posts`, `web_data_tiktok_profiles` гэх
мэт) нь ихэвчлэн "Pro" горимд байдаг бөгөөд нэмэлт төлбөртэй байж болно. Tool жагсаалтад
эдгээр харагдахгүй бол Pro горим асаагүй байна гэсэн үг.

- Профайлын URL өгөөд reels/posts татна. Hashtag хайлт сул бол вэб хайлтаар
  (`site:instagram.com/reel <түлхүүр үг>`, `site:tiktok.com <түлхүүр үг>`) URL олоод,
  түүнийгээ Bright Data-д өг.
- Үр дүнгийн бүтэц Apify-тай төстэй (views, likes, comments, огноо, URL).

---

## 3. vidIQ MCP

Гишүүн vidIQ холбосон бол хамгийн хурдан зам:
- `vidiq_instagram_tiktok_outlier_search`: niche/түлхүүр үгээр шууд outlier бичлэг олно.
  Outlier оноог өөрөө тооцдог тул Алхам 3b-г богиносгоно.
- `vidiq_ig_profile_reels`, `vidiq_tiktok_profile_videos`: аккаунт бүрийн бичлэгүүд.
- `vidiq_tiktok_trending_sound_search`: trend дуу (формат 13-д хэрэгтэй).

Tool-ийн schema-г ToolSearch-аар ачаалж, параметрийг тэндээс уншина.

---

## 4. Вэб хайлт (fallback)

Scraping tool байхгүй үед:
- `"[niche] viral reels 2026"`, `"[niche] tiktok trend"`, `"trending reels formats [сар]"`
- `site:instagram.com/reel [түлхүүр үг]`, `site:tiktok.com/@ [түлхүүр үг]`
- Монгол: `"[монгол түлхүүр үг]" reels`, `[niche] монгол tiktok`
- Creator-уудын "what's working" нийтлэл, Later / Hootsuite / TikTok Creative Center-ийн
  trend тайлан.

Вэб хуудсаар Instagram/TikTok-ийн үзэлтийн тоо ихэвчлэн харагддаггүй. Иймээс энэ горимд
форматын *давтамж* (олон эх сурвалжид гарсан эсэх) гол нотолгоо болно. Итгэлцлийг
"Бага" гэж тэмдэглэ.

---

## 5. Гишүүнд зориулсан суулгах заавар

Гишүүн "яаж холбох вэ" гэж асуувал эсвэл tool байхгүй үед энэ зааврыг монголоор өг:

**Apify (санал болгох, 2 минут):**
1. apify.com дээр үнэгүй бүртгүүл.
2. Claude Code-ийн терминалд:
   ```bash
   claude mcp add apify "https://mcp.apify.com" -t http
   ```
3. Claude Code-ийг дахин нээгээд эхний удаа ашиглахад Apify-ийн нэвтрэх хуудас нээгдэнэ.
   Зөвшөөр.
4. `/goat-viral-format`-ийг дахин ажиллуул.

**Bright Data (өөр сонголт):**
1. brightdata.com дээр бүртгүүлээд Account settings-оос API token ав.
2. Claude Code-д `/plugin` бичээд "Bright Data" plugin суулга, эсвэл терминалд:
   ```bash
   claude mcp add --transport http brightdata "https://mcp.brightdata.com/mcp?token=ТАНЫ_TOKEN"
   ```
3. Instagram/TikTok tool-ууд харагдахгүй бол Bright Data-ийн заавраар Pro горимыг асаа
   (нэмэлт төлбөртэй байж болно).

Token-оо хэзээ ч чатад хуулж бүү бич, бусадтай бүү хуваалц. Суулгах командууд
хувилбараас хамаарч өөрчлөгдөж болох тул ажиллахгүй бол docs.apify.com/platform/integrations/mcp
эсвэл docs.brightdata.com-ийн Claude Code хэсгийг шалга.
