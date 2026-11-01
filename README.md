# 五十音 Kana Dojo

日文五十音練習，三種模式：

1. **睇字 → 寫拼音** — 見假名打羅馬字（接受 shi/si、tsu/tu、wo/o 等寫法）
2. **聽聲 → 寫假名** — 聽發音揀返正確假名
3. **聽聲 → 手寫** — 聽發音喺格上面寫，本地筆順比對自動認字，認唔到可以自己對答案

題庫選擇：**平假名／片假名／隨機混合／錯題簿**

- **隨機混合**：平假名同片假名一齊出，每題上面會標明係「ひらがな」定「カタカナ」
- **錯題簿**：答錯嘅字自動記低（同一個字唔會重覆），喺錯題簿答啱就會自動移走。
  撳「管理」可以睇晒成個 list：逐個 tick 要唔要練、✕ 刪走、手動加字、全選／全不選、清空，
  再「開始練習」就只會出你有 tick 嘅字。

語音：Google（預設）／Nanami 神經語音，可切換慢讀。
可選「拼音」提示：開咗之後喇叭下面會顯示羅馬字。

**字類（可選加練）**：`濁音`（が ざ だ ば）、`半濁音`（ぱ ぴ ぷ ぺ ぽ）、`拗音`（きゃ しゃ ちゃ …）
逐個開關，預設全部關（即係只練 46 清音）。開咗之後練習題庫、鍵盤同讀音都會包括嗰類字，
平假名／片假名同步。手寫模式對加練字暫時冇筆順模板，會提示你撳「睇答案」自己對。

## 網頁版（PWA，可加落主畫面）

<https://alice-creator-lab.github.io/kana-dojo-dev/>

已經係 PWA：第二次開會用 service worker cache，斷網都用得。iPhone/Android 用瀏覽器「加入主畫面」就同 app 差不多。

## 平台

只做網頁版（PWA）。Android APK 同 Capacitor 原生專案已經移出呢個 repo；要重出 APK 請參考上游 `sunhsieh/kana-dojo` 嘅歷史版本。

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
