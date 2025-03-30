import flet as ft
import settings


class SignupForm(ft.Column):  # Changed from UserControl to Column
    def __init__(self, page):
        super().__init__()
        self.page = page

        # Configure page alignment in the main function, not here
        self.spacing = 10
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Add this
        self.expand = True  # Important for vertical centering

        # Form fields
        self.username = ft.TextField(
            label="Username",
            width=300,
            border_color=settings.color
        )
        self.email = ft.TextField(
            label="Email Address",
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

        self.error_box= ft.Container(
            content = ft.Text ("",color=ft.colors.RED_300),
            bgcolor= ft.colors.RED_100,
            border_radius=5,
            padding=10,
            width=300
        )


        # Login button with click handler
        self.login_btn = ft.ElevatedButton(
            "Create Account",
            width=300,
            style=ft.ButtonStyle(
                bgcolor=settings.color,  # Background color
                color=ft.colors.WHITE,  # Text color
                padding=20,
                overlay_color=ft.colors.TRANSPARENT,
            ),
            on_click=self.signup_clicked
        )


        # Create controls list
        self.controls = [
            ft.Text("XpenseLog!", size=24, color=settings.color),
            ft.Text("Join us Today and start!", size=15),
            self.username,
            self.email,
            self.password,

            self.login_btn,
            ft.Row(
                [
                    ft.Text("Already have an account?"),
                    ft.TextButton(
                        "Login now",
                        on_click=self.navigate_to_login,
                        style=ft.ButtonStyle(color=ft.colors.GREEN))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            )
        ]

    def signup_clicked(self, e):
        # Add your login validation logic here
        if not self.username.value:
            self.error_box.content.value = "Please Enter Username"
            self.controls.insert(2,self.error_box)
            self.update()
            return
        if not self.email.value:
            self.error_box.content.value = "Please Enter Your Email"
            self.controls.insert(2, self.error_box)
            self.update()
            return
        if not self.password.value:
            self.error_box.content.value = "Please Enter Password"
            self.controls.insert(2, self.error_box)
            self.update()
            return

        # Clear errors
        pusers = self.page.db.get_user_by_email(self.email.value)
        print("pusers:" , pusers)
        if(len(pusers) != 0):
            self.error_box.content.value = "User with this email already exist"
            self.controls.insert(2, self.error_box)
            self.update()
        else:
            self.page.db.add_user(self.email.value,self.username.value,self.password.value)
            self.error_box.content.value = ""
            self.controls.pop(2)
            self.show_dialog()


    def show_dialog(self):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Account Created!"),
            content=ft.Text("You will be redirected to the login page"),
            actions=[ft.TextButton("OK", on_click=self.close_dialog)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.dialog.open = True
        self.controls.append(self.dialog)
        self.page.add(self.controls)

    def close_dialog(self,e):
        print("it has closed")
        self.dialog.open = False
        self.page.go("/login")
        self.page.update()

    def navigate_to_login(self, e):
        self.page.go("/login")
        self.page.update()