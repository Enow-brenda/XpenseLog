import flet as ft
import settings


class LoginForm(ft.Column):  # Changed from UserControl to Column
    def __init__(self, page):
        super().__init__()
        self.page = page

        # Configure page alignment in the main function, not here
        self.spacing = 10
        self.bgcolor = settings.color
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Add this
        self.expand = True  # Important for vertical centering

        # Form fields
        self.email = ft.TextField(
            label="Email",
            width=300,
            border_color=settings.color
        )
        self.password = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=settings.color,

        )
        self.error = ft.Text("", color="red")

        # Login button with click handler
        self.login_btn = ft.ElevatedButton(
            "Login",
            width=300,
            style=ft.ButtonStyle(
                bgcolor=settings.color,  # Background color
                color=ft.colors.WHITE,  # Text color
                padding=20,
                overlay_color=ft.colors.TRANSPARENT,
            ),
            on_click=self.login_clicked
        )

        # Create controls list
        self.controls = [
            ft.Text("XpenseLog!", size=24,color=settings.color),
            ft.Text("Welcome Back!", size=15),
            self.email,
            self.password,
            self.error,
            self.login_btn,
            ft.Row(
                [
                    ft.Text("Don't have an account?"),
                    ft.TextButton(
                        "Create new account",
                        on_click=lambda e: self.page.go("/signup"),
                        style=ft.ButtonStyle(color=ft.colors.GREEN))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            )
        ]

    def login_clicked(self, e):
        # Add your login validation logic here
        if not self.email.value:
            self.error.value = "Please enter email"
            self.update()
        elif not self.password.value:
            self.error.value = "Please enter password"
            self.update()
        else:
            # Implement actual login logic
            user = self.page.db.login(self.email.value,self.password.value)
            print(user)
            if(len(user)>0):
                self.error.value = ""
                if (user[0][1] == 'Member'):
                    self.page.go(f"/dashboard?userId={user[0][0]}")
                elif (user[0][1] == 'Admin'):
                    self.page.go(f"/control?userId={user[0][0]}")
                self.update()
            else:
                self.error.value = "Invalid Credentials"
                self.update()



    def navigate_to_signup(self, e):
        self.page.go("/signup")
        self.update()
