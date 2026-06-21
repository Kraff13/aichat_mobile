Поместите сюда иконку приложения icon.png (рекомендуется 512x512, формат PNG).

Исходная иконка проекта была assets/icon.ico (Windows). Для мобильной сборки
нужен PNG. Конвертация из .ico в .png:

  # ImageMagick
  magick assets/icon.ico assets/icon.png

Flet автоматически использует assets/icon.png при сборке (flet build apk/ipa),
либо укажите путь явно флагом --icon assets/icon.png.
