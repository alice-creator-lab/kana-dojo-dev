#!/usr/bin/env python3
"""Generate audio for 濁音 / 半濁音 / 拗音 (the 58 extra romaji keys).

Base 46 kana audio ships in audio/g (Google Translate TTS) and audio/n
(Nanami neural voice, silence-trimmed). The extra kana reuse the same naming
scheme: audio/<voice>/<romaji>.mp3, so the app needs no code change to play
them — only the files.

Usage:  python3 tools/make_extra_audio.py [--only g|n] [--force]
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# romaji -> kana text to speak (hiragana; katakana sounds identical)
TEXT = {
    # 濁音
    "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
    "za": "ざ", "ji": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
    "da": "だ", "di": "ぢ", "du": "づ", "de": "で", "do": "ど",
    "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",
    # 半濁音
    "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",
    # 拗音
    "kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",
    "sha": "しゃ", "shu": "しゅ", "sho": "しょ",
    "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
    "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
    "hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",
    "mya": "みゃ", "myu": "みゅ", "myo": "みょ",
    "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",
    "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
    "ja": "じゃ", "ju": "じゅ", "jo": "じょ",
    "bya": "びゃ", "byu": "びゅ", "byo": "びょ",
    "pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",
}

TRIM = (
    "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,"
    "areverse,"
    "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.06,"
    "areverse"
)


def google_tts(text, dest):
    q = urllib.parse.quote(text)
    url = (
        "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=ja&q=" + q
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    if not data.startswith(b"ID3") and data[:1] != b"\xff":
        raise RuntimeError("Google TTS returned non-mp3 payload")
    with open(dest, "wb") as f:
        f.write(data)


def nanami_tts(text, dest):
    raw = dest + ".raw.mp3"
    subprocess.run(
        ["edge-tts", "--voice", "ja-JP-NanamiNeural", "--text", text,
         "--write-media", raw],
        check=True, capture_output=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", TRIM, dest],
        check=True,
    )
    os.remove(raw)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["g", "n"], help="generate one voice only")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args()

    voices = [args.only] if args.only else ["g", "n"]
    made, skipped, bad = 0, 0, []
    for voice in voices:
        outdir = os.path.join(ROOT, "audio", voice)
        os.makedirs(outdir, exist_ok=True)
        for rom, text in TEXT.items():
            dest = os.path.join(outdir, rom + ".mp3")
            if os.path.exists(dest) and not args.force:
                skipped += 1
                continue
            try:
                if voice == "g":
                    google_tts(text, dest)
                else:
                    nanami_tts(text, dest)
                d = duration(dest)
                if not (0.15 <= d <= 1.4):
                    bad.append((voice, rom, round(d, 2)))
                else:
                    made += 1
            except Exception as e:  # noqa: BLE001 - report per file
                bad.append((voice, rom, str(e)))
            time.sleep(0.08)
    print(json.dumps({"made": made, "skipped": skipped, "bad": bad}, ensure_ascii=False))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
