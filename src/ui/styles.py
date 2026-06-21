import flet as ft  # Фреймворк Flet для создания пользовательского интерфейса


class AppStyles:
    """
    Централизованное хранение стилей приложения.

    [MOBILE] Стили адаптированы под мобильные экраны: жёсткие ширины (400/920 px),
    рассчитанные на десктоп, заменены на резиновые (expand), чтобы элементы
    не выходили за границы узкого экрана телефона.
    """

    PAGE_SETTINGS = {
        "title": "AI Chat",
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
        "padding": 20,
        "bgcolor": ft.Colors.GREY_900,
        "theme_mode": ft.ThemeMode.DARK,
    }

    CHAT_HISTORY = {
        "expand": True,
        "spacing": 10,
        "auto_scroll": True,
        "padding": 20,
        # [MOBILE] убрана фиксированная "height": 400 — область чата тянется по expand.
    }

    MESSAGE_INPUT = {
        # [MOBILE] вместо "width": 400 делаем поле резиновым
        "expand": True,
        "height": 50,
        "multiline": False,
        "text_size": 16,
        "color": ft.Colors.WHITE,
        "bgcolor": ft.Colors.GREY_800,
        "border_color": ft.Colors.BLUE_400,
        "cursor_color": ft.Colors.WHITE,
        "content_padding": 10,
        "border_radius": 8,
        "hint_text": "Введите сообщение здесь...",
        "shift_enter": True,
    }

    SEND_BUTTON = {
        "text": "Отправка",
        "icon": ft.Icons.SEND,
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_700,
            padding=10,
        ),
        "tooltip": "Отправить сообщение",
        "height": 40,
        "width": 130,
    }

    SAVE_BUTTON = {
        "text": "Сохранить",
        "icon": ft.Icons.SAVE,
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_700,
            padding=10,
        ),
        "tooltip": "Сохранить диалог в файл",
        "width": 130,
        "height": 40,
    }

    CLEAR_BUTTON = {
        "text": "Очистить",
        "icon": ft.Icons.DELETE,
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_700,
            padding=10,
        ),
        "tooltip": "Очистить историю чата",
        "width": 130,
        "height": 40,
    }

    ANALYTICS_BUTTON = {
        "text": "Аналитика",
        "icon": ft.Icons.ANALYTICS,
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_700,
            padding=10,
        ),
        "tooltip": "Показать аналитику",
        "width": 130,
        "height": 40,
    }

    INPUT_ROW = {
        "spacing": 10,
        "alignment": ft.MainAxisAlignment.SPACE_BETWEEN,
        # [MOBILE] убрана "width": 920 — строка ввода занимает доступную ширину.
    }

    CONTROL_BUTTONS_ROW = {
        "spacing": 20,
        "alignment": ft.MainAxisAlignment.CENTER,
        # [MOBILE] перенос кнопок на узком экране
        "wrap": True,
    }

    CONTROLS_COLUMN = {
        "spacing": 20,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }

    MAIN_COLUMN = {
        "expand": True,
        "spacing": 20,
        "alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }

    MODEL_SEARCH_FIELD = {
        # [MOBILE] убрана "width": 400 — поле поиска резиновое
        "border_radius": 8,
        "bgcolor": ft.Colors.GREY_900,
        "border_color": ft.Colors.GREY_700,
        "color": ft.Colors.WHITE,
        "content_padding": 10,
        "cursor_color": ft.Colors.WHITE,
        "focused_border_color": ft.Colors.BLUE_400,
        "focused_bgcolor": ft.Colors.GREY_800,
        "hint_style": ft.TextStyle(color=ft.Colors.GREY_400, size=14),
        "prefix_icon": ft.Icons.SEARCH,
        "height": 45,
    }

    MODEL_DROPDOWN = {
        # [MOBILE] убрана "width": 400 — выпадающий список резиновый
        "height": 45,
        "border_radius": 8,
        "bgcolor": ft.Colors.GREY_900,
        "border_color": ft.Colors.GREY_700,
        "color": ft.Colors.WHITE,
        "content_padding": 10,
        "focused_border_color": ft.Colors.BLUE_400,
        "focused_bgcolor": ft.Colors.GREY_800,
    }

    MODEL_SELECTION_COLUMN = {
        "spacing": 10,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
        # [MOBILE] убрана "width": 400 — колонка выбора модели по ширине родителя
    }

    BALANCE_TEXT = {
        "size": 16,
        "color": ft.Colors.GREEN_400,
        "weight": ft.FontWeight.BOLD,
    }

    BALANCE_CONTAINER = {
        "padding": 10,
        "bgcolor": ft.Colors.GREY_900,
        "border_radius": 8,
        "border": ft.border.all(1, ft.Colors.GREY_700),
    }

    @staticmethod
    def set_window_size(page: ft.Page):
        """
        Установка фиксированного размера окна (ТОЛЬКО десктоп).

        [MOBILE] На Android/iOS объект page.window нерелевантен, поэтому вызов этого
        метода обёрнут проверкой платформы (см. main.py) и try/except.
        """
        try:
            page.window.width = 600
            page.window.height = 800
            page.window.resizable = False
        except Exception:
            pass
