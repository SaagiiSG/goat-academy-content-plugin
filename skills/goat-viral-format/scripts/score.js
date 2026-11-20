#!/usr/bin/env node
// GOAT Academy outlier scorer: no installs needed (Node only).
// Scores view counts collected in the browser with the small-account rule:
//   viral = followers <= maxFollowers AND views >= threshold x median(views of the account's OTHER videos)
//
// Usage: node score.js input.json [--max-followers 100000] [--threshold 3] [--min-posts 8] [--out scored.json]
// input.json:
// [ { "platform": "tiktok", "account": "name", "followers": "6,953" | 6953,
//     "posts": [ { "url": "...", "views": "12.3K" | 12300, "young": false, "pinned": false } ] } ]
//  - views/followers may be strings as shown on the page ("1.2M", "85.8K", "12,345", "1,2 млн").
//  - mark posts younger than 7 days as young:true (or leave out); pinned posts are scored but flagged.
const fs = require("fs");

function num(v) {
  if (v === null || v === undefined || v === "") return null;
  if (typeof v === "number") return v;
  let s = String(v).trim().toLowerCase().replace(/\s/g, "");
  let mult = 1;
  if (/(k|к|мян|тыс)/.test(s)) mult = 1e3;
  if (/(m|м|сая|млн)$|(m|млн|сая)[^a-z]*$/.test(s) && !/мян/.test(s)) mult = 1e6;
  if (/(b|тэрбум|млрд)$/.test(s)) mult = 1e9;
  s = s.replace(/[^\d.,]/g, "");
  if (mult > 1) s = s.replace(",", "."); // "1,2" -> 1.2 when abbreviated
  else s = s.replace(/[.,](?=\d{3}\b)/g, ""); // "12,345" -> 12345
  const n = parseFloat(s);
  return isNaN(n) ? null : Math.round(n * mult);
}

function median(a) {
  if (!a.length) return null;
  const s = [...a].sort((x, y) => x - y), m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const input = args.find(a => !a.startsWith("--") && !/^\d/.test(a));
if (!input) { console.error("usage: node score.js input.json [--max-followers 100000] [--threshold 3] [--min-posts 8] [--out scored.json]"); process.exit(1); }
const MAX = +opt("--max-followers", 100000), TH = +opt("--threshold", 3), MIN = +opt("--min-posts", 8);
const out = opt("--out", input.replace(/\.json$/, "") + ".scored.json");

const accounts = JSON.parse(fs.readFileSync(input, "utf8"));
const viral = [];
for (const a of accounts) {
  a.followers = num(a.followers);
  a.small_account = a.followers !== null && a.followers <= MAX;
  for (const p of a.posts || []) p.views = num(p.views);
  const settled = (a.posts || []).filter(p => p.views && !p.young);
  a.usual_views = median(settled.map(p => p.views));
  a.note = settled.length < MIN ? `only ${settled.length} settled videos (< ${MIN}); not scored` : null;
  for (const p of a.posts || []) {
    p.outlier = null;
    if (!a.note && p.views && !p.young) {
      const others = settled.filter(q => q !== p).map(q => q.views);
      const med = median(others);
      if (med) p.outlier = Math.round((p.views / med) * 10) / 10;
    }
    p.views_per_follower = a.followers && p.views ? Math.round((p.views / a.followers) * 10) / 10 : null;
    p.viral = !!(a.small_account && p.outlier && p.outlier >= TH);
    if (p.viral) viral.push({ ...p, account: a.account, platform: a.platform, followers: a.followers, usual_views: a.usual_views });
  }
}
fs.writeFileSync(out, JSON.stringify({ rules: { max_followers: MAX, threshold: TH, min_posts: MIN, baseline: "median of the account's other settled videos" }, accounts }, null, 2));
viral.sort((x, y) => y.outlier - x.outlier);
console.log(`${viral.length} viral posts (small account, >= ${TH}x usual) -> ${out}`);
for (const p of viral.slice(0, 40))
  console.log(`${String(p.outlier).padStart(6)}x ${String(p.views.toLocaleString("en")).padStart(11)} views (usual ${Math.round(p.usual_views).toLocaleString("en")}) ${p.platform} @${p.account} [${p.followers.toLocaleString("en")}] ${p.pinned ? "(pinned) " : ""}${p.url}`);
const big = accounts.filter(a => a.followers !== null && !a.small_account).map(a => a.account);
if (big.length) console.log(`skipped big accounts: ${big.join(", ")}`);
const unknown = accounts.filter(a => a.followers === null).map(a => a.account);
if (unknown.length) console.log(`follower count missing (not counted as small): ${unknown.join(", ")}`);
