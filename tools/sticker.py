#!/usr/bin/env python3
"""tsundere-stickers 取图小工具。只用标准库，不用 pip install 任何东西。

    python tools/sticker.py list
    python tools/sticker.py list -e 傲娇
    python tools/sticker.py search 赌气
    python tools/sticker.py get "#10" -o 图.png
    python tools/sticker.py fetch-all --license open -o images
    python tools/sticker.py check

索引就是仓库根目录的 stickers.json，一条一个表情。
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "stickers.json"
UA = "tsundere-stickers/1.0 (+https://github.com/NotFatJustRound/tsundere-stickers)"
SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
CTYPE_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


def load_index(path=INDEX):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def norm_no(value):
    s = str(value).strip()
    if s.startswith("#"):
        s = s[1:]
    return "#" + s.zfill(2) if s.isdigit() else "#" + s


def pick_ext(url, content_type=""):
    suffix = Path(url.split("?")[0]).suffix.lower()
    if suffix in SUFFIXES:
        return suffix
    return CTYPE_EXT.get(content_type.split(";")[0].strip().lower(), ".png")


def download(url, dest_base, timeout=25):
    """下载 url 到 dest_base + 推断出来的后缀，返回 (路径, 字节数)。"""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        ext = pick_ext(url, resp.headers.get("Content-Type", ""))
    if not data:
        raise RuntimeError("空响应")
    dest = Path(dest_base).with_suffix(ext)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest, len(data)


def one_line(item):
    return "{no:<4} {emotion:<4} [{license:<4}] {content}".format(
        no=item.get("no", "?"),
        emotion=(item.get("emotion", "?") + " ")[:4],
        license=item.get("license", "-"),
        content=(item.get("content", "") or "")[:48],
    )


def select(stickers, emotion=None, license_=None, keyword=None):
    out = []
    for item in stickers:
        if emotion and emotion not in (item.get("emotion") or ""):
            continue
        if license_ and item.get("license") != license_:
            continue
        if keyword:
            blob = " ".join(
                [
                    item.get("content") or "",
                    item.get("usage") or "",
                    " ".join(item.get("keywords") or []),
                ]
            )
            if keyword not in blob:
                continue
        out.append(item)
    return out


def cmd_list(args):
    data = load_index()
    rows = select(data.get("stickers", []), args.emotion, args.license)
    if not rows:
        print("没挑到，换个情绪或关键词试试。")
        return 1
    for item in rows:
        print(one_line(item))
    print("\n共 %d 张。" % len(rows))
    return 0


def cmd_search(args):
    data = load_index()
    rows = select(data.get("stickers", []), args.emotion, args.license, args.keyword)
    if not rows:
        print("没有匹配到「%s」。" % args.keyword)
        return 1
    for item in rows:
        print(one_line(item))
        if args.verbose and item.get("usage"):
            print("     用法：%s" % item["usage"])
    return 0


def cmd_get(args):
    data = load_index()
    target = norm_no(args.no)
    item = next((x for x in data.get("stickers", []) if norm_no(x.get("no")) == target), None)
    if not item:
        print("索引里没有 %s。" % target, file=sys.stderr)
        return 1
    if not item.get("url"):
        print("%s 没有直链，只有页址：%s" % (target, item.get("page") or "-"), file=sys.stderr)
        return 1
    dest = Path(args.out or (target.lstrip("#")))
    try:
        path, size = download(item["url"], dest)
    except (urllib.error.URLError, RuntimeError, OSError) as exc:
        print("下载失败：%s" % exc, file=sys.stderr)
        return 2
    print("%s -> %s (%.1f KB, %s 授权)" % (target, path, size / 1024, item.get("license", "-")))
    return 0


def cmd_fetch_all(args):
    data = load_index()
    rows = select(data.get("stickers", []), args.emotion, args.license)
    rows = [x for x in rows if x.get("url")]
    if not rows:
        print("没有带直链的条目可下。")
        return 1
    ok = fail = 0
    outdir = Path(args.out or "images")
    for item in rows:
        name = norm_no(item.get("no")).lstrip("#")
        try:
            path, size = download(item["url"], outdir / name)
        except (urllib.error.URLError, RuntimeError, OSError) as exc:
            print("FAIL %s %s (%s)" % (item.get("no"), item["url"], exc), file=sys.stderr)
            fail += 1
            continue
        print("OK   %s -> %s (%.1f KB)" % (item.get("no"), path, size / 1024))
        ok += 1
    print("\n成功 %d，失败 %d。" % (ok, fail))
    return 0 if fail == 0 else 3


def cmd_check(args):
    data = load_index()
    rows = [x for x in data.get("stickers", []) if x.get("url")]
    bad = 0
    for item in rows:
        url = item["url"]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
        except urllib.error.HTTPError as exc:
            status = exc.code
        except (urllib.error.URLError, OSError) as exc:
            status = "ERR:%s" % exc
        flag = "OK  " if status == 200 else "DEAD"
        if status != 200:
            bad += 1
        print("%s %s %s %s" % (flag, item.get("no"), status, url))
    print("\n共 %d 条，异常 %d 条。" % (len(rows), bad))
    return 0 if bad == 0 else 4


def build_parser():
    p = argparse.ArgumentParser(
        prog="sticker.py",
        description="tsundere-stickers 表情索引工具（只用标准库）",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_filters(sp):
        sp.add_argument("-e", "--emotion", help="按情绪过滤，如 傲娇 / 无语 / 摆烂")
        sp.add_argument("--license", help="只取某种授权：open / net / own")

    sp = sub.add_parser("list", help="列出表情")
    add_filters(sp)
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("search", help="按关键词/内容/用法搜")
    sp.add_argument("keyword")
    add_filters(sp)
    sp.add_argument("-v", "--verbose", action="store_true", help="带上用法说明")
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("get", help="下载单张")
    sp.add_argument("no", help="编号，如 #10 或 10")
    sp.add_argument("-o", "--out", help="保存路径（后缀会自动按图类型修正）")
    sp.set_defaults(func=cmd_get)

    sp = sub.add_parser("fetch-all", help="批量下载")
    add_filters(sp)
    sp.add_argument("-o", "--out", default="images", help="输出目录，默认 images/")
    sp.set_defaults(func=cmd_fetch_all)

    sp = sub.add_parser("check", help="逐个验链接是否还活着")
    sp.set_defaults(func=cmd_check)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
