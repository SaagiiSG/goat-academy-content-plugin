#!/usr/bin/env python3
"""GOAT Academy free outlier finder: small accounts, outsized views.

A VIRAL FORMAT SIGNAL = a post from a SMALL account (default <= 100K followers)
whose views are far above that account's usual video (default >= 3x).
A small account can't lean on its audience, so a big spike means the FORMAT
carried it. That's what members can copy.

Tools (free, open-source):
    TikTok    -> yt-dlp      https://github.com/yt-dlp/yt-dlp
    Instagram -> Instaloader https://github.com/instaloader/instaloader
Install once:
    python3 -m pip install --user -U yt-dlp instaloader

Commands
  1) discover : find candidate accounts from a hashtag
       python3 free_fetch.py discover tiktok    homeworkout --limit 40
       python3 free_fetch.py discover instagram homeworkout --limit 40 --session MY_IG
  2) scan     : pull each account's recent posts and score outliers
       python3 free_fetch.py scan tiktok    user1 user2 ... --out tt.json
       python3 free_fetch.py scan instagram user1 user2 ... --out ig.json [--session MY_IG]
     Options: --limit 30 (posts per account), --max-followers 100000,
              --threshold 3 (x above usual), --min-posts 8

Scoring (per post, video posts only, posts younger than 7 days excluded):
    usual_views  = MEDIAN views of the account's OTHER recent videos
                   (median, not mean, so one earlier hit doesn't hide the next)
    outlier      = views / usual_views
    vs_average   = views / mean views of the other videos (shown for reference)
    views_per_follower = views / followers
  A post is flagged VIRAL when: account is small AND outlier >= threshold.

Instagram requires a login (tested Nov 2026: logged-out scans are redirected to login).
Easiest, no password: be logged into Instagram in Chrome/Firefox, then run ONCE in your own
terminal:   instaloader --load-cookies chrome      (or firefox, edge, safari)
Alternative: instaloader --login MY_IG   (asks for the password itself; never paste it in chat)
Then add --session MY_IG.
Use a spare account, not your main one. Hashtag discovery on Instagram needs a session.

Only public post stats + captions are read. No follower lists, no personal data.
"""
import argparse
import itertools
import json
import statistics
import sys
import time
from datetime import datetime, timezone

YOUNG_DAYS = 7


def now():
    return datetime.now(timezone.utc)


def age_days(dt):
    return None if dt is None else (now() - dt).total_seconds() / 86400


def log(msg):
    print(msg, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ loaders
def need_ytdlp():
    try:
        import yt_dlp
        return yt_dlp
    except ImportError:
        raise SystemExit("yt-dlp алга. Суулгах: python3 -m pip install --user -U yt-dlp")


def need_instaloader(session):
    try:
        import instaloader
    except ImportError:
        raise SystemExit("instaloader алга. Суулгах: python3 -m pip install --user -U instaloader")
    L = instaloader.Instaloader(
        download_pictures=False, download_videos=False, download_video_thumbnails=False,
        download_geotags=False, download_comments=False, save_metadata=False,
        compress_json=False, quiet=True,
    )
    if session:
        L.load_session_from_file(session)
    return instaloader, L


YTDLP_OPTS = {"quiet": True, "no_warnings": True, "skip_download": True, "ignoreerrors": True}


# ------------------------------------------------------------------ discover
def discover_tiktok(tag, limit):
    yt_dlp = need_ytdlp()
    with yt_dlp.YoutubeDL({**YTDLP_OPTS, "playlistend": limit}) as ydl:
        info = ydl.extract_info(f"https://www.tiktok.com/tag/{tag.lstrip('#')}", download=False)
    if not info:
        raise RuntimeError("TikTok hashtag хуудсыг yt-dlp уншиж чадсангүй. Энэ нь түгээмэл: "
                           "аккаунтын handle-ыг вэб хайлтаар олоод шууд 'scan'-д өг")
    accounts = {}
    for e in (info.get("entries") or [])[:limit]:
        if not e:
            continue
        u = e.get("uploader") or e.get("channel") or e.get("uploader_id")
        if not u:
            continue
        a = accounts.setdefault(u, {"account": u, "followers": e.get("channel_follower_count"),
                                    "seen_posts": 0, "max_views": 0})
        a["seen_posts"] += 1
        a["max_views"] = max(a["max_views"], e.get("view_count") or 0)
    return list(accounts.values())


def discover_instagram(tag, limit, session):
    instaloader, L = need_instaloader(session)
    if not session:
        log("⚠ Instagram hashtag хайлт ихэвчлэн нэвтрэлт шаарддаг (--session).")
    h = instaloader.Hashtag.from_name(L.context, tag.lstrip("#"))
    accounts = {}
    for post in itertools.islice(h.get_top_posts(), limit):
        u = post.owner_username
        a = accounts.setdefault(u, {"account": u, "followers": None, "seen_posts": 0, "max_views": 0})
        a["seen_posts"] += 1
        if post.is_video:
            v = getattr(post, "video_play_count", None) or post.video_view_count or 0
            a["max_views"] = max(a["max_views"], v)
        time.sleep(1)
    return list(accounts.values())


# ------------------------------------------------------------------ scan
def tiktok_followers_from_page(username):
    """yt-dlp often omits follower counts; the public profile page embeds them."""
    import re
    import urllib.request
    req = urllib.request.Request(
        f"https://www.tiktok.com/@{username}",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/131.0 Safari/537.36",
                 "Accept-Language": "en-US,en;q=0.9"},
    )
    try:
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception:
        return None
    m = re.search(r'"followerCount":(\d+)', html)
    return int(m.group(1)) if m else None


def scan_tiktok(username, limit):
    yt_dlp = need_ytdlp()
    username = username.lstrip("@")
    with yt_dlp.YoutubeDL({**YTDLP_OPTS, "playlistend": limit}) as ydl:
        info = ydl.extract_info(f"https://www.tiktok.com/@{username}", download=False)
    if not info:
        raise RuntimeError("yt-dlp юу ч буцаасангүй (хаалттай аккаунт, хаалт, эсвэл yt-dlp-г шинэчлэх хэрэгтэй)")
    followers = info.get("channel_follower_count")
    posts = []
    for e in (info.get("entries") or [])[:limit]:
        if not e:
            continue
        ts = e.get("timestamp")
        followers = followers or e.get("channel_follower_count")
        posts.append({
            "url": e.get("webpage_url") or e.get("url"),
            "views": e.get("view_count"), "likes": e.get("like_count"),
            "comments": e.get("comment_count"), "shares": e.get("repost_count"),
            "_dt": datetime.fromtimestamp(ts, timezone.utc) if ts else None,
            "duration_s": e.get("duration"),
            "caption": (e.get("description") or e.get("title") or "")[:300],
            "is_video": True,
        })
    if followers is None:
        followers = tiktok_followers_from_page(username)
    return followers, posts


def scan_instagram(username, limit, session):
    instaloader, L = need_instaloader(session)
    profile = instaloader.Profile.from_username(L.context, username.lstrip("@"))
    posts = []
    for post in itertools.islice(profile.get_posts(), limit):
        views = (getattr(post, "video_play_count", None) or post.video_view_count) if post.is_video else None
        posts.append({
            "url": f"https://www.instagram.com/p/{post.shortcode}/",
            "views": views, "likes": post.likes, "comments": post.comments, "shares": None,
            "_dt": post.date_utc.replace(tzinfo=timezone.utc) if post.date_utc else None,
            "duration_s": getattr(post, "video_duration", None),
            "caption": (post.caption or "")[:300],
            "is_video": post.is_video,
        })
        time.sleep(1.5)  # Instagram rate-limits fast
    return profile.followers, posts


def score(account, followers, posts, args):
    small = followers is not None and followers <= args.max_followers
    settled = [p for p in posts if p["is_video"] and p["views"] and (age_days(p["_dt"]) or 99) >= YOUNG_DAYS]
    enough = len(settled) >= args.min_posts
    for p in posts:
        a = age_days(p["_dt"])
        p["date"] = p["_dt"].isoformat() if p["_dt"] else None
        p["young"] = a is not None and a < YOUNG_DAYS
        p["outlier"] = p["vs_average"] = None
        p["views_per_follower"] = round(p["views"] / followers, 1) if (followers and p["views"]) else None
        if enough and p in settled:
            others = [q["views"] for q in settled if q is not p]
            med, mean = statistics.median(others), statistics.mean(others)
            if med:
                p["outlier"] = round(p["views"] / med, 1)
            if mean:
                p["vs_average"] = round(p["views"] / mean, 1)
        p["viral"] = bool(small and p["outlier"] and p["outlier"] >= args.threshold)
        p.pop("_dt", None)
    usual = statistics.median([q["views"] for q in settled]) if settled else None
    return {
        "account": account.lstrip("@"), "followers": followers, "small_account": small,
        "usual_views": usual, "videos_scored": len(settled) if enough else 0,
        "note": None if enough else f"Хангалттай видео алга ({len(settled)} < {args.min_posts}), оноо тооцоогүй",
        "posts": posts,
    }


# ------------------------------------------------------------------ main
def cmd_discover(args):
    fn = discover_tiktok if args.platform == "tiktok" else (lambda t, l: discover_instagram(t, l, args.session))
    try:
        accounts = fn(args.hashtag, args.limit)
    except SystemExit:
        raise
    except Exception as e:
        print(f"✗ Hashtag хайлт амжилтгүй: {type(e).__name__}: {str(e)[:200]}")
        print("Instagram бол --session шаардлагатай. Эсвэл вэб хайлтаар handle олоод шууд 'scan' ажиллуул.")
        return
    accounts.sort(key=lambda a: a["max_views"], reverse=True)
    json.dump({"platform": args.platform, "hashtag": args.hashtag, "accounts": accounts},
              open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(accounts)} аккаунт олдлоо (#{args.hashtag}) · JSON: {args.out}")
    if not accounts:
        print("Hashtag-аас аккаунт гарсангүй (платформ хаасан байж магадгүй). "
              "Вэб хайлтаар handle олоод шууд 'scan' ажиллуул.")
    for a in accounts:
        f = f"{a['followers']:,}" if a["followers"] else "?"
        print(f"  @{a['account']:<24} дагагч {f:>10}  хамгийн их үзэлт {a['max_views']:>10,}")
    print("\nДараагийн алхам: жижиг (≤100K) аккаунтуудыг 'scan'-д өг.")


def cmd_scan(args):
    result = {"platform": args.platform, "fetched_at": now().isoformat(),
              "rules": {"max_followers": args.max_followers, "threshold": args.threshold,
                        "young_days_excluded": YOUNG_DAYS, "baseline": "median of the account's other recent videos"},
              "accounts": [], "skipped_big": [], "errors": []}
    for acc in args.accounts:
        try:
            if args.platform == "tiktok":
                followers, posts = scan_tiktok(acc, args.limit)
            else:
                followers, posts = scan_instagram(acc, args.limit, args.session)
            if followers is not None and followers > args.max_followers:
                result["skipped_big"].append({"account": acc.lstrip("@"), "followers": followers})
                log(f"– @{acc}: {followers:,} дагагч > {args.max_followers:,}, том аккаунт тул алгаслаа")
                continue
            a = score(acc, followers, posts, args)
            result["accounts"].append(a)
            log(f"✓ @{acc}: {len(posts)} пост, ердийн үзэлт {a['usual_views']}, дагагч {followers}")
        except SystemExit:
            raise
        except Exception as e:
            result["errors"].append({"account": acc, "error": f"{type(e).__name__}: {e}"[:300]})
            log(f"✗ @{acc}: {type(e).__name__}: {e}")

    json.dump(result, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    viral = sorted(({**p, "account": a["account"], "followers": a["followers"], "usual_views": a["usual_views"]}
                    for a in result["accounts"] for p in a["posts"] if p["viral"]),
                   key=lambda p: p["outlier"], reverse=True)
    print(f"\n{len(viral)} вирал бичлэг (жижиг аккаунт, ердийнхөөсөө ≥{args.threshold}x) · JSON: {args.out}")
    for p in viral[:40]:
        print(f"{p['outlier']:>6}x  {p['views']:>11,} үзэлт (ердийн {int(p['usual_views'] or 0):,})  "
              f"@{p['account']} [{p['followers']:,}]  {p['url']}")
    if result["skipped_big"]:
        print(f"\n{len(result['skipped_big'])} том аккаунт алгассан (--max-followers-оос их).")
    if result["errors"]:
        print(f"{len(result['errors'])} аккаунт амжилтгүй. JSON-ийн 'errors' хэсгийг хар.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover", help="find candidate accounts from a hashtag")
    d.add_argument("platform", choices=["tiktok", "instagram"])
    d.add_argument("hashtag")
    d.add_argument("--limit", type=int, default=40)
    d.add_argument("--session")
    d.add_argument("--out", default="discover.json")

    s = sub.add_parser("scan", help="score recent posts of accounts")
    s.add_argument("platform", choices=["tiktok", "instagram"])
    s.add_argument("accounts", nargs="+")
    s.add_argument("--limit", type=int, default=30)
    s.add_argument("--max-followers", type=int, default=100_000)
    s.add_argument("--threshold", type=float, default=3.0)
    s.add_argument("--min-posts", type=int, default=8)
    s.add_argument("--session")
    s.add_argument("--out", default="outliers.json")

    args = ap.parse_args()
    cmd_discover(args) if args.cmd == "discover" else cmd_scan(args)


if __name__ == "__main__":
    main()
