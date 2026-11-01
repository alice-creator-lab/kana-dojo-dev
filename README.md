# 五十音 Kana Dojo

日文五十音練習，三種模式：

1. **睇字 → 寫拼音** — 見假名打羅馬字（接受 shi/si、tsu/tu、wo/o 等寫法）
2. **聽聲 → 寫假名** — 聽發音揀返正確假名
3. **聽聲 → 手寫** — 聽發音喺格上面寫，本地筆順比對自動認字，認唔到可以自己對答案

語音：Google（預設）／Nanami 神經語音／系統 TTS，可切換慢讀。
可選「拼音」提示：開咗之後喇叭下面會顯示羅馬字。

## 網頁版（PWA，可加落主畫面）

<https://alice-creator-lab.github.io/kana-dojo-dev/>

已經係 PWA：第二次開會用 service worker cache，斷網都用得。iPhone/Android 用瀏覽器「加入主畫面」就同 app 差不多。

## 平台

只做網頁版（PWA）。原本嘅 Android APK 同 Capacitor 原生專案已移除，想重出 APK 請參考上游 repo 歷史版本。

## 專案結構

```
index.html              # 全部 app 邏輯（單頁 vanilla JS）
kana-templates.json     # KanjiVG 筆順模板（46 平假名 + 46 片假名）
audio/g/*.mp3           # Google 日語語音
audio/n/*.mp3           # Nanami 神經語音
icons/                  # PWA / favicon 圖示
manifest.webmanifest    # PWA manifest
sw.js                   # service worker（離線 cache）
tools/make_icons.py     # 生成網頁圖示
```

## 授權

筆順模板來自 [KanjiVG](https://kanjivg.tagaini.net/)（CC BY-SA 3.0）。
