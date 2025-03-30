import flet as ft
import datetime


class TransactionsPage(ft.Column):
    def __init__(self, page, sidebar):
        super().__init__()
        self.page = page
        self.sidebar = sidebar
        self.current_filter = "all"



        # Mock transaction data
        self.transactions = self.page.db.get_transactions_by_user(self.page.userId)

        # Main content column
        self.main_column = ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Row([
                    ft.Text("Transactions",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREEN_500
                            ),
                    ft.ElevatedButton(
                        "Add Transaction",
                        icon=ft.icons.ADD,
                        on_click= lambda e:self.open_transaction_modal()

                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("View, add, edit, and manage all your transactions",
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

        # Create filter controls and transaction table
        self.create_filter_controls()
        self.create_transaction_table()

        # Add transaction modal
        self.transaction_modal = None
        #self.setup_transaction_modal()

    def create_filter_controls(self):
        self.filter_controls = ft.Row([
            ft.Text("Filter by: ", size=14),
            ft.ElevatedButton(
                "All",
                icon=ft.icons.LIST_ALT,
                on_click= lambda e: self.filter_transactions("all"),
                bgcolor=ft.colors.BLUE_500 if self.current_filter == "all" else ft.colors.BLUE_100,
                color=ft.colors.WHITE if self.current_filter == "all" else ft.colors.BLUE_900,
            ),
            ft.ElevatedButton(
                "Income",
                icon=ft.icons.TRENDING_UP,
                on_click= lambda e: self.filter_transactions("income"),
                bgcolor=ft.colors.GREEN_500 if self.current_filter == "income" else ft.colors.GREEN_100,
                color=ft.colors.WHITE if self.current_filter == "income" else ft.colors.GREEN_900,
            ),
            ft.ElevatedButton(
                "Expense",
                icon=ft.icons.TRENDING_DOWN,
                on_click= lambda e: self.filter_transactions("expense"),
                bgcolor=ft.colors.RED_500 if self.current_filter == "expense" else ft.colors.RED_100,
                color=ft.colors.WHITE if self.current_filter == "expense" else ft.colors.RED_900,
            ),
            ft.ElevatedButton(
                "Saving",
                icon=ft.icons.SAVINGS,
                on_click= lambda e: self.filter_transactions("saving"),
                bgcolor=ft.colors.PURPLE_500 if self.current_filter == "saving" else ft.colors.PURPLE_100,
                color=ft.colors.WHITE if self.current_filter == "saving" else ft.colors.PURPLE_900,
            ),
        ], spacing=10)

        self.main_column.controls.append(ft.Container(
            content=self.filter_controls,
            margin=ft.margin.only(top=20)
        ))

    def create_transaction_table(self):
        # Create table headers
        self.transaction_table_headers = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("Date", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Title", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Type", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Amount", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Description", weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
            ]
        )

        # Create table
        self.transaction_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Date")),
                ft.DataColumn(label=ft.Text("Title")),
                ft.DataColumn(label=ft.Text("Type")),
                ft.DataColumn(label=ft.Text("Amount")),
                ft.DataColumn(label=ft.Text("Description")),
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

        # Populate table with transactions
        self.update_transaction_table()

        # Add table to main column
        self.main_column.controls.append(ft.Container(
            content=self.transaction_table,
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

    def update_transaction_table(self):
        # Clear existing rows
        self.transaction_table.rows.clear()

        # Filter transactions based on current filter
        filtered_transactions = self.transactions

        if self.current_filter != "all":
            filtered_transactions = [t for t in self.transactions if t["type"] == self.current_filter]

        # Sort transactions by date (most recent first)
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["date"], reverse=True)

        # Add rows to table
        for transaction in filtered_transactions:
            # Format amount based on transaction type
            if transaction["type"] == "income":
                amount_text = f"+FCFA{transaction['amount']}"
                amount_color = ft.colors.GREEN_500
                type_color = ft.colors.GREEN_100
                icon = ft.icons.TRENDING_UP
            elif transaction["type"] == "expense":
                amount_text = f"-FCFA{transaction['amount']}"
                amount_color = ft.colors.RED_500
                type_color = ft.colors.RED_100
                icon = ft.icons.TRENDING_DOWN
            else:  # saving
                amount_text = f"FCFA{transaction['amount']}"
                amount_color = ft.colors.PURPLE_500
                type_color = ft.colors.PURPLE_100
                icon = ft.icons.SAVINGS

            # Format date
            date_parts = transaction["date"].split("-")
            formatted_date = transaction["date"]

            # Create actions column
            actions = ft.Row([
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color=ft.colors.BLUE_500,
                    tooltip="Edit",
                    on_click= self.open_update_transaction,
                    data = transaction['id']

                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.RED_500,
                    tooltip="Delete",
                    on_click= self.delete_transaction,
                    data=transaction['id']


                )
            ])

            # Add row to table
            self.transaction_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(formatted_date)),
                        ft.DataCell(ft.Text(transaction["title"])),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(icon, size=16, color=amount_color),
                                    ft.Text(transaction["type"].capitalize())
                                ], spacing=5),
                                padding=ft.padding.all(5),
                                border_radius=15,
                                bgcolor=type_color
                            )
                        ),
                        ft.DataCell(ft.Text(amount_text, color=amount_color)),
                        ft.DataCell(ft.Text(transaction["description"])),
                        ft.DataCell(actions),
                    ]
                )
            )

        # Update the page
        self.page.update()

    def filter_transactions(self, filter_type):
        # Update current filter
        self.current_filter = filter_type

        # Update button colors
        for i, button_type in enumerate(["all", "income", "expense", "saving"]):
            button = self.filter_controls.controls[i + 1]  # +1 to skip the "Filter by:" text

            if button_type == "all":
                button.bgcolor = ft.colors.BLUE_500 if filter_type == "all" else ft.colors.BLUE_100
                button.color = ft.colors.WHITE if filter_type == "all" else ft.colors.BLUE_900
            elif button_type == "income":
                button.bgcolor = ft.colors.GREEN_500 if filter_type == "income" else ft.colors.GREEN_100
                button.color = ft.colors.WHITE if filter_type == "income" else ft.colors.GREEN_900
            elif button_type == "expense":
                button.bgcolor = ft.colors.RED_500 if filter_type == "expense" else ft.colors.RED_100
                button.color = ft.colors.WHITE if filter_type == "expense" else ft.colors.RED_900
            elif button_type == "saving":
                button.bgcolor = ft.colors.PURPLE_500 if filter_type == "saving" else ft.colors.PURPLE_100
                button.color = ft.colors.WHITE if filter_type == "saving" else ft.colors.PURPLE_900

        # Update table
        self.update_transaction_table()

    def open_transaction_modal(self, e=None):
        self.setup_transaction_modal()
        self.page.dialog = self.transaction_modal
        self.page.dialog.open = True
        self.controls.append(self.page.dialog)
        self.page.add(self.controls)

        #self.page.update()

    def close_transaction_modal(self, e=None):
        self.transaction_modal.open = False
        self.page.update()

    def open_update_transaction(self,e):
        id = e.control.data
        self.update_transaction_modal(id)
        self.page.dialog = self.transaction_modal
        self.page.dialog.open = True
        self.controls.append(self.page.dialog)
        self.page.add(self.controls)


    def update_transaction_modal(self,id):
        # Transaction type dropdown
        expenses_type = ['Food', 'Housing', 'Transport', 'Entertainment', 'Insurance', 'Health', 'Debt',
                         'Personal Care', 'Others']
        dropdown = []
        transaction = self.page.db.get_transaction_by_id(id)

        for type in expenses_type:
            dropdown.append(ft.dropdown.Option(type, type))

        self.transaction_type_dropdown = ft.Dropdown(
            label="Transaction Type",
            hint_text="Select transaction type",
            value=transaction[0][2],
            options=[
                ft.dropdown.Option("income", "Income"),
                ft.dropdown.Option("expense", "Expense"),
                ft.dropdown.Option("saving", "Saving"),
            ],
            autofocus=True,
            width=250,
            expand=True,
        )

        self.transaction_expense_dropdown = ft.Dropdown(
            label="Expense Type",
            hint_text="Select Expense type (Only for expenses)",
            options=dropdown,
            value=transaction[0][3],
            width=250,
            autofocus=True,
            expand=True,
        )

        # Transaction title field
        self.transaction_title_field = ft.TextField(
            label="Title",
            hint_text="Enter transaction title",
            value=transaction[0][0],
            expand=True,
        )

        # Transaction amount field
        self.transaction_amount_field = ft.TextField(
            label="Amount",
            hint_text="Enter amount",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="FCFA",
            value=transaction[0][1],
            expand=True,
        )

        # Transaction date picker
        self.transaction_date_field = ft.TextField(
            label="Date",
            hint_text="MM/DD/YYYY",
            value=transaction[0][5],
            expand=True,
        )

        # Transaction description field
        self.transaction_description_field = ft.TextField(
            label="Description",
            hint_text="Enter transaction description",
            multiline=True,
            min_lines=3,
            max_lines=5,
            value=transaction[0][4],
            expand=True,
        )

        # Create modal dialog
        self.transaction_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Transaction"),
            content=ft.Column([
                ft.Row([
                    self.transaction_title_field
                ]),
                ft.Row([
                    self.transaction_type_dropdown,
                    self.transaction_expense_dropdown,
                ], spacing=20),
                ft.Row([
                    self.transaction_date_field,
                    self.transaction_amount_field,
                ], spacing=20),
                self.transaction_description_field,
            ], spacing=20, width=500, height=300),
            actions=[
                ft.TextButton("Cancel", on_click= lambda e:self.close_transaction_modal()),
                ft.ElevatedButton("Save", on_click= self.update_transaction ,data = id)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def setup_transaction_modal(self):
        # Transaction type dropdown
        expenses_type = ['Food','Housing','Transport','Entertainment','Insurance','Health','Debt','Personal Care','Others']
        dropdown = []
        for type in expenses_type:
            dropdown.append(ft.dropdown.Option(type, type))

        self.transaction_type_dropdown = ft.Dropdown(
            label="Transaction Type",
            hint_text="Select transaction type",
            options=[
                ft.dropdown.Option("income", "Income"),
                ft.dropdown.Option("expense", "Expense"),
                ft.dropdown.Option("saving", "Saving"),
            ],
            autofocus=True,
            expand=True,
            width=250
        )

        self.transaction_expense_dropdown = ft.Dropdown(
            label="Expense Type",
            hint_text="Select Expense type (Only for expenses)",
            options=dropdown,
            autofocus=True,
            expand=True,
            width= 250
        )

        # Transaction title field
        self.transaction_title_field = ft.TextField(
            label="Title",
            hint_text="Enter transaction title",
            expand=True,
        )

        # Transaction amount field
        self.transaction_amount_field = ft.TextField(
            label="Amount",
            hint_text="Enter amount",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="FCFA",
            expand=True,
        )

        # Transaction date picker
        self.transaction_date_field = ft.TextField(
            label="Date",
            hint_text="MM/DD/YYYY",
            value=datetime.date.today().strftime("%m/%d/%Y"),
            expand=True,
        )

        # Transaction description field
        self.transaction_description_field = ft.TextField(
            label="Description",
            hint_text="Enter transaction description",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True,
        )

        # Create modal dialog
        self.transaction_modal = ft.AlertDialog(
            title=ft.Text("Add Transaction"),
            content=ft.Column([
                ft.Row([
                    self.transaction_title_field
                ]),
                ft.Row([
                    self.transaction_type_dropdown,
                    self.transaction_expense_dropdown,
                ], spacing=20),
                ft.Row([
                    self.transaction_date_field,
                    self.transaction_amount_field,
                ], spacing=20),
                self.transaction_description_field,
            ], spacing=20, width=500, height=300),
            actions=[
                ft.TextButton("Cancel",on_click= lambda e:self.close_transaction_modal()),
                ft.ElevatedButton("Save",on_click= lambda e:self.save_transaction()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def show_dialog_new(self,title: str ,description:str ,is_error: bool = False):
        if self.page.dialog.open:
            self.page.dialog.open = False
        color = ft.Colors.GREEN_400
        if is_error:
            color = ft.Colors.RED_400

        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title,color=color),
            content=ft.Text(description),
            actions=[ft.TextButton("OK", on_click= lambda e:self.close_dialog(e))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog.open = True
        self.controls.append(self.page.dialog)
        self.page.update()

    def show_error_box(self, title: str):
        self.error_box = ft.Container(
            content=ft.Text(title, color=ft.colors.RED_300),
            bgcolor=ft.colors.RED_100,
            border_radius=5,
            padding=10,
            width=500
        )
        self.transaction_modal.content.controls.insert(0, self.error_box)
        self.transaction_modal.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.transactions = self.page.db.get_transactions_by_user(self.page.userId)
        self.update_transaction_table()
        self.page.update()
    def save_transaction(self):
        """Function to save transaction details"""
        transaction_type= self.transaction_type_dropdown.value
        expense_type= self.transaction_expense_dropdown.value if self.transaction_type_dropdown.value == "expense" else "None"
        title = self.transaction_title_field.value
        amount= self.transaction_amount_field.value
        date = self.transaction_date_field.value
        description = self.transaction_description_field.value

        if not transaction_type or not title or not amount or not date or not description:
            self.show_error_box( "All fields must be filled.")
            return

        try:
            amount = float(amount)  # Convert amount to float
        except ValueError:
            self.show_error_box("Amount must be a valid number.")

            return

            # Save to database

        if self.page.db.add_transaction(self.page.userId, title, expense_type, transaction_type, amount, description, date):
            self.show_dialog_new("Success", "Transaction Added Successively.",False)

    def update_transaction(self,e):
        trans_id = e.control.data
        transaction_type= self.transaction_type_dropdown.value
        expense_type= self.transaction_expense_dropdown.value if self.transaction_type_dropdown.value == "expense" else "None"
        title = self.transaction_title_field.value
        amount= self.transaction_amount_field.value
        date = self.transaction_date_field.value
        description = self.transaction_description_field.value


        if not transaction_type or not title or not amount or not date or not description:
            self.show_error_box( "All fields must be filled.")
            return

        try:
            amount = float(amount)  # Convert amount to float
        except ValueError:
            self.show_error_box("Amount must be a valid number.")
            return

            # Save to database
        if self.page.db.update_transaction(trans_id, title, expense_type, transaction_type, amount, description, date):
            self.show_dialog_new("Success", "Transaction Updated Successively.",False)

    def delete_transaction(self,e):
        transactionId = e.control.data
        # Save to database
        if self.page.db.delete_transaction(transactionId):
            self.show_dialog_new("Success", "Transaction Deleted Successively.",False)




