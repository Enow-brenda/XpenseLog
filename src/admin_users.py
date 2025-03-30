import flet as ft
import datetime


class AUsersPage(ft.Column):
    def __init__(self, page, sidebar):
        super().__init__()
        self.page = page
        self.sidebar = sidebar

        # Mock user data
        self.users = self.page.db.get_all_users()

        # Main content column
        self.main_column = ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Row([
                    ft.Text("Users",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREEN_400
                            ),
                    ft.ElevatedButton(
                        "Add User",
                        icon=ft.icons.ADD,
                        on_click=self.open_add_user_modal


                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("View all users information",
                        size=14,
                        color=ft.colors.GREY_600,
                        ),
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.START,
        )

        # Body structure
        self.controls = [ft.Container(
            content=ft.Row(
                controls=[sidebar, ft.Container(
                    content=self.main_column,
                    expand=True,
                    padding=20
                )],
                spacing=0
            ),
            height=self.page.window.height,
            padding=ft.padding.only(left=0)
        )]


        self.create_user_table()

        # Add user modal
        self.user_modal = None
        self.setup_user_modal()

    def create_user_table(self):
        # Create table headers
        self.user_table_headers = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("#", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Email", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Username", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Date joined", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
            ]
        )

        # Create table
        self.user_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("#")),
                ft.DataColumn(label=ft.Text("Email")),
                ft.DataColumn(label=ft.Text("Username")),
                ft.DataColumn(label=ft.Text("Date joined")),
                ft.DataColumn(label=ft.Text("Actions")),
            ],
            rows=[],
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            sort_column_index=0,
            sort_ascending=False,
        )

        # Populate table with users
        self.update_user_table()

        # Add table to main column
        self.main_column.controls.append(ft.Container(
            content=self.user_table,
            margin=ft.margin.only(top=20),
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            ),
            height=self.page.window.height * 0.65,
        ))

    def update_user_table(self):
        # Clear existing rows
        self.user_table.rows.clear()

        # Add rows to table
        for index,user in enumerate(self.users):

            # Format date
            date_parts = user["date"].split(" ")
            formatted_date = f"{date_parts[0]} {date_parts[1]}"

            # Create actions column
            actions = ft.Row([
                ft.IconButton(
                    icon=ft.icons.INFO,
                    icon_color=ft.colors.GREEN_400,
                    tooltip="View",
                    on_click=self.view_user , data=user['id']


                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color=ft.colors.BLUE_500,
                    tooltip="Edit",
                    on_click=self.open_edit_modal, data=user['id']

                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.RED_500,
                    tooltip="Delete",
                    on_click=self.delete_user, data=user['id']

                )
            ])

            # Add row to table
            self.user_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(index+1)),
                        ft.DataCell(ft.Text(user["email"])),
                        ft.DataCell(ft.Text(user["name"])),
                        ft.DataCell(ft.Text(formatted_date)),
                        ft.DataCell(actions),
                    ]
                )
            )

        # Update the page
        self.page.update()

    def show_error_box(self, title: str):
        self.error_box = ft.Container(
            content=ft.Text(title, color=ft.colors.RED_300),
            bgcolor=ft.colors.RED_100,
            border_radius=5,
            padding=10,
            width=500
        )
        self.user_modal.content.controls.insert(0, self.error_box)
        self.user_modal.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.users = self.page.db.get_all_users()
        self.update_user_table()
        self.page.update()
    def setup_user_modal(self):
        # user title field
        self.user_username_field = ft.TextField(
            label="Username",
            hint_text="Enter Username",
            expand=True,
        )
        self.user_email_field = ft.TextField(
            label="Email",
            hint_text="Enter user's Email",
            expand=True,
        )
        self.user_password_field = ft.TextField(
            label="Password",
            hint_text="Enter User's Password",
            password=True,
            expand=True,
        )
        # Create modal dialog
        self.user_modal = ft.AlertDialog(
            title=ft.Text("Add user"),
            content=ft.Column([
                self.user_username_field,
                self.user_email_field,
                self.user_password_field
            ], spacing=20, width=500, height=300),
            actions=[
                ft.TextButton("Cancel",on_click=lambda e:self.close_user_modal()),
                ft.ElevatedButton("Save",on_click=lambda e:self.save_user()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def setup_edit_modal(self,userId):
        user = self.page.db.get_user_by_id(userId)
        print(f"user id is {userId}")
        # user title field
        self.user_username_field = ft.TextField(
            label="Username",
            hint_text="Enter Username",
            value=user[0][2],
            expand=True,
        )
        self.user_email_field = ft.TextField(
            label="Email",
            hint_text="Enter user's Email",
            value=user[0][1],
            expand=True,
        )

        # Create modal dialog
        self.user_modal = ft.AlertDialog(
            title=ft.Text("Edit user"),
            content=ft.Column([
                self.user_username_field,
                self.user_email_field,
            ], spacing=20, width=500, height=300),
            actions=[
                ft.TextButton("Cancel",on_click=lambda e:self.close_user_modal()),
                ft.ElevatedButton("Save",on_click=self.update_user , data=userId),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def open_add_user_modal(self,e=None):
        self.setup_user_modal()
        self.page.dialog = self.user_modal
        self.page.dialog.open = True
        self.controls.append(self.page.dialog)
        self.page.add(self.controls)



    def close_user_modal(self, e=None):
        self.user_modal.open = False
        self.page.update()

    def update_user(self, e):
        user_id = e.control.data
        username = self.user_username_field.value
        email = self.user_email_field.value

        if not username or not email :
            self.show_error_box("All fields must be filled.")
            return

        if self.page.db.update_user_info(user_id, username, email):
            self.show_dialog_new("Success", "User Updated Successively.", False)

    def view_user(self,e):
        userId = e.control.data
        route =f"/view_users?member_id={userId}"
        self.page.go(route)
        self.page.update()

    def delete_user(self,e):
        userId = e.control.data
        if self.page.db.delete_user(userId):
            self.show_dialog_new("Success", "User Deleted Successively.", False)

    def open_edit_modal(self, e):
        param = e.control.data
        self.setup_edit_modal(param)
        self.page.dialog = self.user_modal
        self.page.dialog.open = True
        self.controls.append(self.page.dialog)
        self.page.add(self.controls)

    def save_user(self):
        username = self.user_username_field.value
        email = self.user_email_field.value
        password = self.user_password_field.value

        if not username or not email or not password:
            self.show_error_box("All fields must be filled.")
            return

        if self.page.db.add_user(username, email,password):
            self.show_dialog_new("Success", "User Added Successively.", False)

    def show_dialog_new(self, title: str, description: str, is_error: bool = False):
        if self.page.dialog:
            self.page.dialog.open = False
        color = ft.Colors.GREEN_400
        if is_error:
            color = ft.Colors.RED_400

        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=color),
            content=ft.Text(description),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog(e))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog.open = True
        self.controls.append(self.page.dialog)
        self.page.update()
