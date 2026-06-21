# Импорт необходимых библиотек
import flet as ft
from api import OpenRouterClient
from ui import MessageBubble
import asyncio


class SimpleChatApp:
    def __init__(self):
        self.api_client = OpenRouterClient()

    def main(self, page: ft.Page):
        page.title = "Simple AI Chat"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = 20
        page.bgcolor = ft.Colors.GREY_900
        page.theme_mode = ft.ThemeMode.DARK

        self.chat_history = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10,
            auto_scroll=True
        )
        self.message_input = ft.TextField(
            expand=True,
            height=50,
            multiline=False,
            text_size=16,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREY_800,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.WHITE,
            content_padding=10,
            border_radius=8,
            hint_text="Введите сообщение здесь..."
        )

        async def send_message(e):
            if not self.message_input.value:
                return
            user_message = self.message_input.value
            self.message_input.value = ""
            page.update()
            self.chat_history.controls.append(
                MessageBubble(message=user_message, is_user=True)
            )
            loading = ft.ProgressRing()
            self.chat_history.controls.append(loading)
            page.update()
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.api_client.send_message(user_message, "openai/gpt-3.5-turbo")
            )
            self.chat_history.controls.remove(loading)
            if "error" in response:
                response_text = f"Ошибка: {response['error']}"
            else:
                response_text = response["choices"][0]["message"]["content"]
            self.chat_history.controls.append(
                MessageBubble(message=response_text, is_user=False)
            )
            page.update()

        send_button = ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            icon_color=ft.Colors.BLUE_400,
            on_click=send_message
        )
        page.add(
            ft.Container(
                content=ft.Column([
                    self.chat_history,
                    ft.Row([
                        self.message_input,
                        send_button
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ]),
                expand=True,
                padding=10,
                bgcolor=ft.Colors.GREY_800
            )
        )


if __name__ == "__main__":
    app = SimpleChatApp()
    ft.app(target=app.main)
