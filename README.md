# AI Chat — мобильная сборка

Кроссплатформенный клиент OpenRouter на Flet, адаптированный для сборки под Android (APK)
и iOS (IPA) помимо десктопа.

> **Важно.** Сам файл APK/IPA собирается только на вашей машине — для этого нужны
> Flutter SDK, Android SDK + JDK (для APK) и macOS + Xcode (для IPA). В этом архиве —
> полностью готовый к сборке исходный код + конфигурация.

## 1. Структура проекта

```
aichat_mobile/
├─ src/
│  ├─ main.py            # главное приложение (адаптировано под mobile)
│  ├─ main_simple.py     # упрощённая версия
│  ├─ api/openrouter.py  # клиент OpenRouter API
│  ├─ ui/                # компоненты и стили (резиновые/responsive)
│  └─ utils/             # storage, logger, cache (SQLite), analytics, monitor
├─ assets/               # иконка приложения (icon.png)
├─ android/manifest.template.xml  # референс разрешений Android
├─ ios/Info.plist        # референс ключей iOS
├─ pyproject.toml        # конфигурация flet build (разрешения, идентификаторы)
├─ requirements.txt
└─ .env.example          # скопируйте в .env и впишите ключ
```

## 2. Что было адаптировано под мобильные (помечено `[MOBILE]` / `[FIX]` в коде)

1. **Хранилище файлов** (`utils/storage.py`) — БД, логи и экспорт пишутся в `FLET_APP_STORAGE_DATA`
   (писабельный каталог приложения), а не в текущую папку — на Android/iOS CWD только для чтения.
2. **Резиновый UI** (`ui/styles.py`) — убраны жёсткие ширины 400/920 px, заменены на `expand`,
   кнопки переносятся (`wrap`) на узком экране.
3. **Размер окна** — `set_window_size()` вызывается только на десктопе (`is_mobile()`),
   на телефоне окно управляется ОС.
4. **`os.startfile`** (кнопка «Открыть папку») — только на десктопе; кроссплатформенно
   (Windows/macOS/Linux). На мобильном показывается только путь.
5. **psutil опционален** (`utils/monitor.py`) — на Android/iOS не собирается, мониторинг
   деградирует до uptime без ошибок.
6. **Разрешения** — INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE (Android),
   NSAppTransportSecurity / NSNetworkUsageDescription (iOS) заданы в `pyproject.toml`.
7. **Исправлены баги**: вложенные кавычки в f-строке (`models_data['data']`),
   присвоение `model_dropdown.value` (берём `id`), дублирование лог-обработчиков.

## 3. Подготовка

```bash
# 1. Ключ API
cp .env.example .env
# откройте .env и впишите свой OPENROUTER_API_KEY

# 2. Иконка (нужен PNG для mobile)
# положите assets/icon.png (512x512). При наличии .ico:
#   magick assets/icon.ico assets/icon.png

# 3. Установите Flet CLI
pip install "flet[all]==0.25.2"
```

Проверка на десктопе перед сборкой:

```bash
pip install -r requirements.txt
flet run src/main.py
```

## 4. Сборка Android (APK)

Требования: Flutter SDK, Android SDK, JDK 17. Из корня проекта:

```bash
flet build apk -v
```

Готовый файл: `build/apk/app-release.apk`.
Можно задать имя/пакет явно:

```bash
flet build apk --project AIChat --org com.example -v
# package-name => com.example.aichat
```

## 5. Сборка iOS (IPA)

Требования: macOS + Xcode, Flutter SDK, CocoaPods. Из корня проекта:

```bash
flet build ipa -v
```

Для установки на устройство/публикации нужна подпись (Apple Developer Account).

## 6. Разрешения

| Платформа | Разрешение | Зачем |
|----------|------------|-------|
| Android  | INTERNET | запросы к OpenRouter |
| Android  | ACCESS_NETWORK_STATE | проверка сети |
| Android  | WRITE_EXTERNAL_STORAGE | экспорт истории (Android ≤ 9) |
| iOS      | NSAppTransportSecurity | сетевые запросы |
| iOS      | NSNetworkUsageDescription | описание использования сети |

## 7. Частые проблемы

- **Пустой экран / нет ответа** — проверьте OPENROUTER_API_KEY в .env и интернет.
- **Ошибка сборки про psutil** — убедитесь, что в requirements.txt у psutil стоит маркер
  платформы (уже задан).
- **Нет иконки** — добавьте assets/icon.png.
