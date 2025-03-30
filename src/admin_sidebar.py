import flet as ft

class ASidebar(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.user = self.page.db.get_user_by_id(self.page.userId)
        self.sidebar_content = ft.Column(
            controls=[
                ft.Column(
                    [
                        ft.Text("XpenseLog!", size=40, color=ft.Colors.GREEN_400, weight=ft.FontWeight.BOLD),
                        ft.Image(src="./assets/icon.png", width=50, height=50, fit=ft.ImageFit.CONTAIN),
                        ft.Text(self.user[0][2], size=20, text_align=ft.TextAlign.CENTER),
                        ft.Text(self.user[0][1], size=15, text_align=ft.TextAlign.CENTER),
                        ft.Container(
                            content=ft.Row([

                                ft.Text("Admin",color=ft.colors.WHITE,text_align=ft.TextAlign.CENTER)
                            ], spacing=5),
                            padding=ft.padding.all(5),
                            width=50,
                            border_radius=15,
                            bgcolor=ft.colors.GREEN_300
                        )
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(),  # Adds a separator before the buttons
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.controls = [ft.Container(
            content=self.sidebar_content,
            width=300,  # Fixed width
            height=self.page.window.height,  # Sidebar takes full height
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),  # Optional border
        )]


    def construct(self, active_index):
        sides = ["Dashboard","Users", "Transactions", "Exit"]

        buttons = []
        for index, side in enumerate(sides):
            if index == active_index:
                buttons.append(ft.ElevatedButton(
                    text=side,
                    height=40,
                    bgcolor=ft.Colors.GREEN_100,
                    color=ft.Colors.GREEN_400,
                    width=200,
                    on_click=lambda e, s=side: self.navigate_to(s),
                ))
            else:
                buttons.append(ft.TextButton(
                    text=side,
                    height=40,
                    width=200,
                    style=ft.ButtonStyle(color=ft.Colors.BLACK),
                    on_click=lambda e, s=side: self.navigate_to(s),
                ))

        # Update the sidebar content with the buttons dynamically
        self.sidebar_content.controls = self.sidebar_content.controls[
                                        :2] + buttons  # Add the buttons after the profile section
        self.page.update()  # Update the page with new controls



    def navigate_to(self, section):
        print(f"Navigating to: {section}")  # Replace with actual navigation logic
        self.page.go(f"/admin_{section.lower()}")