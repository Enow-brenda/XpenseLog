import flet as ft
import datetime


class ATransactionsPage(ft.Column):
    def __init__(self, page, sidebar):
        super().__init__()
        self.page = page
        self.sidebar = sidebar
        self.current_filter = "all"

        # Mock transaction data
        self.transactions = self.page.db.get_all_transactions()

        # Main content column
        self.main_column = ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Row([
                    ft.Text("Transactions",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREEN_500
                            )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("View all user transactions",
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


    def create_filter_controls(self):
        self.filter_controls = ft.Row([
            ft.Text("Filter by: ", size=14),
            ft.ElevatedButton(
                "All",
                icon=ft.icons.LIST_ALT,
                on_click=lambda e: self.filter_transactions("all"),
                bgcolor=ft.colors.BLUE_500 if self.current_filter == "all" else ft.colors.BLUE_100,
                color=ft.colors.WHITE if self.current_filter == "all" else ft.colors.BLUE_900,
            ),
            ft.ElevatedButton(
                "Income",
                icon=ft.icons.TRENDING_UP,
                on_click=lambda e: self.filter_transactions("income"),
                bgcolor=ft.colors.GREEN_500 if self.current_filter == "income" else ft.colors.GREEN_100,
                color=ft.colors.WHITE if self.current_filter == "income" else ft.colors.GREEN_900,
            ),
            ft.ElevatedButton(
                "Expense",
                icon=ft.icons.TRENDING_DOWN,
                on_click=lambda e: self.filter_transactions("expense"),
                bgcolor=ft.colors.RED_500 if self.current_filter == "expense" else ft.colors.RED_100,
                color=ft.colors.WHITE if self.current_filter == "expense" else ft.colors.RED_900,
            ),
            ft.ElevatedButton(
                "Saving",
                icon=ft.icons.SAVINGS,
                on_click=lambda e: self.filter_transactions("saving"),
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
                ft.DataCell(ft.Text("User", weight=ft.FontWeight.BOLD)),
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
                ft.DataColumn(label=ft.Text("User")),
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
            #date_parts = transaction["date"].split("-")
            formatted_date = transaction["date"]


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
                        ft.DataCell(ft.Text(transaction["username"])),
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
                button.bgcolor = ft.colors.PURPLE_500 if filter_type == "saving" else ft.colors.YELLOW_100
                button.color = ft.colors.WHITE if filter_type == "saving" else ft.colors.PURPLE_900

        # Update table
        self.update_transaction_table()

