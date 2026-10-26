#!/usr/bin/env python3
"""从分镜脚本生成后期与 Blender 所需的文件。

读取 docs/AChR-MG_分子动画分镜脚本_5min.md 中的分镜表格，输出：
  production/post/subtitles_zh.srt   字幕（剪映、Premiere、DaVinci Resolve 均可导入）
  production/post/narration_zh.txt   逐镜配音稿（可粘贴到配音 / TTS 工具）
  production/post/shots.json         镜头时间表（含帧范围，供 Blender 脚本读取）

分镜时间改动后重新运行即可：
  python production/tools/storyboard_to_post.py
  python production/tools/storyboard_to_post.py --fps 25
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_STORYBOARD = REPO / "docs" / "AChR-MG_分子动画分镜脚本_5min.md"
DEFAULT_OUT = REPO / "production" / "post"

ROW = re.compile(r"^\| (S\d\d) \|")
DURATION = re.compile(r"(\d+) s<br>(\d\d):(\d\d)–(\d\d):(\d\d)")


def clean(cell):
    cell = re.sub(r"\*\*(.+?)\*\*", r"\1", cell)
    return cell.strip()


def is_empty(cell):
    return cell.startswith("（无")


def parse(storyboard):
    shots, act, part = [], "", ""
    for line in storyboard.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            act, part = line[4:].strip(), ""
        elif line.startswith("#### "):
            part = line[5:].strip()
        elif ROW.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 6:
                sys.exit(f"{cells[0]}：应为 6 列，实际 {len(cells)} 列")
            sid, duration, visual, narration, subtitle, _ = cells
            m = DURATION.match(duration)
            if not m:
                sys.exit(f"{sid}：无法解析时长 {duration!r}")
            seconds = int(m.group(1))
            start = int(m.group(2)) * 60 + int(m.group(3))
            end = int(m.group(4)) * 60 + int(m.group(5))
            shots.append({
                "id": sid,
                "act": act,
                "part": part,
                "start": start,
                "end": end,
                "seconds": seconds,
                "narration": "" if is_empty(narration) else clean(narration),
                "subtitle": [] if is_empty(subtitle) else [clean(s) for s in subtitle.split("<br>")],
                "visual": [clean(v) for v in visual.split("<br>")],
            })
    return shots


def validate(shots):
    if not shots:
        sys.exit("没有找到分镜行")
    t = 0
    for s in shots:
        if s["start"] != t or s["end"] - s["start"] != s["seconds"]:
            sys.exit(f"{s['id']}：时间码不连续或与时长不符（应从 {t} s 开始）")
        t = s["end"]
    return t


def srt_time(seconds):
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d},000"


def mmss(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def write_srt(shots, path):
    blocks = []
    for s in shots:
        if s["subtitle"]:
            blocks.append(f"{len(blocks) + 1}\n{srt_time(s['start'])} --> {srt_time(s['end'])}\n"
                          + "\n".join(s["subtitle"]) + "\n")
    # 带 BOM 的 UTF-8，避免部分 Windows 软件把中文识别成乱码
    path.write_text("\n".join(blocks), encoding="utf-8-sig")
    return len(blocks)


def write_narration(shots, path, total):
    chars = 0
    lines = [
        "AChR-MG 分子动画 · 逐镜配音稿",
        f"总时长 {mmss(total)}；建议语速约 3–3.8 字/秒，镜头之间留 0.3–0.5 s 停顿。",
        "读音：重症肌无力的“重”读 zhòng；IgG 读 I-G-G；C1q 读 C-1-Q；α 读“阿尔法”；MuSK 全片统一读法。",
        "",
    ]
    for s in shots:
        if not s["narration"]:
            continue
        n = len(re.findall(r"[一-鿿]", s["narration"]))
        chars += n
        lines.append(f"【{s['id']}  {mmss(s['start'])}–{mmss(s['end'])}  {s['seconds']} s】")
        lines.append(s["narration"])
        lines.append("")
    lines.append(f"（旁白汉字合计 {chars} 字）")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return chars


def write_shots(shots, path, fps, total):
    data = {
        "fps": fps,
        "total_seconds": total,
        "frame_start": 1,
        "frame_end": total * fps,
        "shots": [
            {
                "id": s["id"],
                "act": s["act"],
                "part": s["part"],
                "start_seconds": s["start"],
                "end_seconds": s["end"],
                # Blender 帧号从 1 开始，帧范围首尾都包含
                "frame_start": s["start"] * fps + 1,
                "frame_end": s["end"] * fps,
                "narration": s["narration"],
                "subtitle": s["subtitle"],
            }
            for s in shots
        ],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--storyboard", type=Path, default=DEFAULT_STORYBOARD)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()

    shots = parse(args.storyboard)
    total = validate(shots)
    args.out.mkdir(parents=True, exist_ok=True)
    n_srt = write_srt(shots, args.out / "subtitles_zh.srt")
    n_chars = write_narration(shots, args.out / "narration_zh.txt", total)
    write_shots(shots, args.out / "shots.json", args.fps, total)
    print(f"{len(shots)} 个镜头，总长 {mmss(total)}，{args.fps} fps 共 {total * args.fps} 帧")
    print(f"字幕 {n_srt} 条，旁白 {n_chars} 字 → {args.out}")


if __name__ == "__main__":
    main()
