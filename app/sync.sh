#!/usr/bin/env bash
# 將 kana-dojo 網站同步入 Android app 的 www/，然後同步到原生專案
set -euo pipefail
SRC=/home/admin/kana-dojo
DST=/home/admin/kana-android/www
mkdir -p "$DST"
rsync -a --delete \
  --exclude '.git' --exclude 'tools' --exclude 'sw.js' --exclude '.DS_Store' \
  "$SRC"/ "$DST"/
cd /home/admin/kana-android
npx cap sync android
echo "synced $(du -sh "$DST" | cut -f1) into www/"
