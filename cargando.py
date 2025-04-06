import flet as ft

def main(page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.CupertinoActivityIndicator(
            radius=50,
            color=ft.colors.RED,
            animating=True,
        )
    )

ft.app(main)