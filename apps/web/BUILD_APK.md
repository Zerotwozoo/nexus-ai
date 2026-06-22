# Membangun APK Nexus AI

## Prasyarat

1. **Node.js 20+** — `node --version`
2. **pnpm** — `npm install -g pnpm`
3. **Java JDK 17+** — Download dari https://adoptium.net/
4. **Android Studio** — Download dari https://developer.android.com/studio
   - Install **Android SDK** (API 34+)
   - Set environment variable `ANDROID_HOME`

## Langkah-langkah

```bash
# 1. Install dependencies (dari root project)
cd nexus-ai
pnpm install

# 2. Build Next.js untuk static export
cd apps/web
pnpm build

# 3. Sync web build ke project Android
npx cap sync

# 4. Build APK Debug
cd android
./gradlew assembleDebug

# atau (Windows)
gradlew.bat assembleDebug
```

APK akan ada di:
```
apps/web/android/app/build/outputs/apk/debug/app-debug.apk
```

## Build APK Release (untuk Play Store)

1. Generate keystore:
```bash
keytool -genkey -v -keystore nexus-release.keystore -alias nexus -keyalg RSA -keysize 2048 -validity 10000
```

2. Copy keystore ke `apps/web/android/app/`

3. Buat file `android/app/key.properties`:
```
storePassword=passwordmu
keyPassword=passwordmu
keyAlias=nexus
storeFile=nexus-release.keystore
```

4. Build release APK:
```bash
cd apps/web/android
./gradlew assembleRelease
```

Release APK akan ada di:
```
apps/web/android/app/build/outputs/apk/release/app-release.apk
```

## Catatan Penting

- Aplikasi ini adalah **client** yang terhubung ke backend FastAPI.
- Untuk mode offline penuh, deploy backend di server atau gunakan PWA mode.
- Pastikan `NEXT_PUBLIC_API_URL` di `.env` mengarah ke backend yang aktif.

## Troubleshooting

| Error | Solusi |
|-------|--------|
| `Command not found: gradlew` | Pastikan Java JDK terinstal |
| `SDK location not found` | Set `ANDROID_HOME` environment variable |
| `FAILURE: Build failed with an exception` | Buka project di Android Studio, sync Gradle, lalu build dari sana |
