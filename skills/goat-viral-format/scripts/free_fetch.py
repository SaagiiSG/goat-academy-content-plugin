#!/usr/bin/env python3
"""Free outlier fetcher for GOAT Academy (no paid API).

TikTok    -> yt-dlp      (https://github.com/yt-dlp/yt-dlp)
Instagram -> Instaloader (https://github.com/instaloader/instaloader)

Pulls each account's recent public posts, computes
    outlier = post views / median views of that account's recent videos
and writes JSON plus a short summary of the outliers.

Install once:
    python3 -m pip install --user -U yt-dlp instaloader

Usage:
    python3 free_fetch.py tiktok    user1 user2 --limit 25 --out tiktok.json
    python3 free_fetch.py instagram user1 user2 --limit 25 --out ig.json
    python3 free_fetch.py instagram user1 --session MY_IG_USERNAME   # optional, see below

Instagram limits anonymous access hard. If you get "login required" / 401 / 429,
create a session ONCE in your own terminal with:  instaloader --login MY_IG_USERNAME
(it asks for the password itself, so it never goes into chat or this script),
then pass --session MY_IG_USERNAME. A secondary account is safer than your main one.

Only public post stats are collected. No follower lists, no personal data.
"""
import argparse
import itertools
import json
import statistics
import sys
import time
from datetime import datetime, timezone

YOUNG_DAYS = 7  # posts younger than this haven't settled; flagged, not counted as outliers


def now():
    return datetime.now(timezone.utc)


def age_days(dt):
    if dt is None:
        return None
    return (now() - dt).total_seconds() / 86400


# ---------------------------------------------------------------- TikTok
def fetch_tiktok(username, limit):
    try:
        import yt_dlp
    except ImportError:
        raise SystemExit("yt-dlp алга. Суулгах: python3 -m pip install --user -U yt-dlp")

    username = username.lstrip("@")
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ignoreerrors": True,
        "playlistend": limit,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"https://www.tiktok.com/@{username}", download=False)
    if not info:
        raise RuntimeError("yt-dlp returned nothing (account private, blocked, or yt-dlp needs updating)")

    followers = info.get("channel_follower_count")
    posts = []
    for e in (info.get("entries") or [])[:limit]:
        if not e:
            continue
        ts = e.get("timestamp")
        dt = datetime.fromtimestamp(ts, timezone.utc) if ts else None
        posts.append({
            "platform": "tiktok",
            "account": username,
            "url": e.get("webpage_url") or e.get("url"),
            "views": e.get("view_count"),
            "likes": e.get("like_count"),
            "comments": e.get("comment_count"),
            "shares": e.get("repost_count"),
            "date": dt.isoformat() if dt else None,
            "_dt": dt,
            "duration_s": e.get("duration"),
            "caption": (e.get("description") or e.get("title") or "")[:300],
            "is_video": True,
        })
        followers = followers or e.get("channel_follower_count")
    return followers, posts


# ---------------------------------------------------------------- Instagram
def fetch_instagram(username, limit, session=None):
    try:
        import instaloader
    except ImportError:
        raise SystemExit("instaloader алга. Суулгах: python3 -m pip install --user -U instaloader")

    username = username.lstrip("@")
    L = instaloader.Instaloader(
        download_pictures=False, download_videos=False, download_video_thumbnails=False,
        download_geotags=False, download_comments=False, save_metadata=False,
        compress_json=False, quiet=True,
    )
    if session:
        L.load_session_from_file(session)

    profile = instaloader.Profile.from_username(L.context, username)
    posts = []
    for post in itertools.islice(profile.get_posts(), limit):
        dt = post.date_utc.replace(tzinfo=timezone.utc) if post.date_utc else None
        views = None
        if post.is_video:
            views = getattr(post, "video_play_count", None) or post.video_view_count
        posts.append({
            "platform": "instagram",
            "account": username,
            "url": f"https://www.instagram.com/p/{post.shortcode}/",
            "views": views,
            "likes": post.likes,
            "comments": post.comments,
            "shares": None,
            "date": dt.isoformat() if dt else None,
            "_dt": dt,
            "duration_s": getattr(post, "video_duration", None),
            "caption": (post.caption or "")[:300],
            "is_video": post.is_video,
        })
        time.sleep(1.5)  # be gentle; Instagram rate-limits fast
    return profile.followers, posts


# ---------------------------------------------------------------- scoring
def score(followers, posts):
    settled = [p["views"] for p in posts
               if p["is_video"] and p["views"] and (age_days(p["_dt"]) or 99) >= YOUNG_DAYS]
    med = statistics.median(settled) if len(settled) >= 5 else None
    for p in posts:
        a = age_days(p["_dt"])
        p["young"] = a is not None and a < YOUNG_DAYS
        p["outlier"] = round(p["views"] / med, 1) if (med and p["views"]) else None
        p["views_per_follower"] = round(p["views"] / followers, 1) if (followers and p["views"]) else None
        p.pop("_dt", None)
    return med


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("platform", choices=["tiktok", "instagram"])
    ap.add_argument("accounts", nargs="+")
    ap.add_argument("--limit", type=int, default=25, help="recent posts per account (default 25)")
    ap.add_argument("--threshold", type=float, default=3.0, help="outlier threshold (default 3x)")
    ap.add_argument("--session", help="Instagram username whose instaloader session to load")
    ap.add_argument("--out", default="outliers.json")
    args = ap.parse_args()

    result = {"platform": args.platform, "fetched_at": now().isoformat(), "accounts": [], "errors": []}
    for acc in args.accounts:
        try:
            if args.platform == "tiktok":
                followers, posts = fetch_tiktok(acc, args.limit)
            else:
                followers, posts = fetch_instagram(acc, args.limit, args.session)
            med = score(followers, posts)
            result["accounts"].append({
                "account": acc.lstrip("@"), "followers": followers,
                "median_views": med, "posts_fetched": len(posts), "posts": posts,
            })
            print(f"✓ {acc}: {len(posts)} пост, median {med}", file=sys.stderr)
        except SystemExit:
            raise
        except Exception as e:  # keep going with the other accounts
            result["errors"].append({"account": acc, "error": f"{type(e).__name__}: {e}"[:300]})
            print(f"✗ {acc}: {type(e).__name__}: {e}", file=sys.stderr)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    outliers = sorted(
        (p for a in result["accounts"] for p in a["posts"]
         if p["outlier"] and p["outlier"] >= args.threshold and not p["young"]),
        key=lambda p: p["outlier"], reverse=True,
    )
    print(f"\n{len(outliers)} outlier (≥{args.threshold}x) · JSON: {args.out}")
    for p in outliers[:30]:
        print(f"{p['outlier']:>6}x  {p['views']:>10,}  @{p['account']:<20} {p['url']}")
    if result["errors"]:
        print(f"\n{len(result['errors'])} аккаунт амжилтгүй — JSON-ийн 'errors' хэсгийг хар.")


if __name__ == "__main__":
    main()
