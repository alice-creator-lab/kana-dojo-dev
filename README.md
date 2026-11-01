# 五十音 Kana Dojo

日文五十音練習，三種模式：

1. **睇字 → 寫拼音** — 見假名打羅馬字（接受 shi/si、tsu/tu、wo/o 等寫法）
2. **聽聲 → 寫假名** — 聽發音揀返正確假名
3. **聽聲 → 手寫** — 聽發音喺格上面寫，本地筆順比對自動認字，認唔到可以自己對答案

語音：Google（預設）／Nanami 神經語音／系統 TTS，可切換慢讀。
可選「拼音」提示：開咗之後喇叭下面會顯示羅馬字。

## 網頁版（PWA，可加落主畫面）

<https://sunhsieh.github.io/kana-dojo/>

已經係 PWA：第二次開會用 service worker cache，斷網都用得。iPhone/Android 用瀏覽器「加入主畫面」就同 app 差不多。

## Android app（APK）

下載： <https://sunhsieh.github.io/kana-dojo/apk/kana-dojo-1.0.0.apk> （約 4.3 MB，Android 5.1+）

安裝步驟：

1. 用 Android 手機開上面條 link 下載
2. 開檔案，如果彈「未知來源」→ 去 設定 → 應用程式 → 允許來自此來源
3. 安裝完成，圖示係藍底白色「あ」

特點：所有檔案（音檔、筆順模板）都內建，**完全離線**，唔需要網絡。

> 簽名：用自己 keystore（`CN=Kana Dojo`）。日後出新版要同一個 keystore 簽名才可以直接覆蓋安裝；keystore 保存喺 server `~/kana-android/keys/kana-release.jks`（唔會 commit）。

## 專案結構

```
index.html              # 全部 app 邏輯（單頁 vanilla JS）
kana-templates.json     # KanjiVG 筆順模板（46 平假名 + 46 片假名）
audio/g/*.mp3           # Google 日語語音
audio/n/*.mp3           # Nanami 神經語音
icons/                  # PWA / favicon 圖示
manifest.webmanifest    # PWA manifest
sw.js                   # service worker（離線 cache）
apk/                    # 打包好嘅 Android APK
app/                    # Capacitor + Android 原生專案（重建 APK 用）
tools/make_icons.py     # 生成網頁圖示
```

## 重建 APK

需要 JDK 17 + Android SDK 34。

```bash
# 1. 同步網頁檔案入 www/
cd app && bash sync.sh

# 2. 準備簽名（第一次先要）
#    喺 app/ 放 keystore.properties：
#    storeFile=../keys/kana-release.jks
#    storePassword=***
#    keyAlias=kana
#    keyPassword=***

# 3. 編譯
cd android && ./gradlew assembleRelease
# 出廠檔：android/app/build/outputs/apk/release/app-release.apk
```

低記憶體機器（<2GB RAM）注意：`android/gradle.properties` 已調低 heap，並且要加
`-x :capacitor-android:verifyReleaseResources` 跳過資源驗證任務，否則 Gradle 會被 OOM 殺。

## 授權

筆順模板來自 [KanjiVG](https://kanjivg.tagaini.net/)（CC BY-SA 3.0）。
