import flet as ft
import datetime


class UserInfoPage(ft.Column):
    def __init__(self, page, sidebar):
        super().__init__()
        self.page = page
        self.page.member_id = page.member_id
        self.sidebar = sidebar


        # Mock user data
        self.user_data = self.page.db.get_user_metrics_sum(self.page.member_id,is_admin=True)

        self.transactions = self.page.db.get_transactions_by_user(self.page.member_id)
        print(self.transactions)

        # User Information Section
        self.user_info_section = ft.Column([
            ft.ElevatedButton("Go Back",on_click= lambda e:self.back()),
            ft.Text("User Information", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_500),
            ft.Text(f"Name: {self.user_data['name']}", size=16),
            ft.Text(f"Email: {self.user_data['email']}", size=16),
            ft.Text(f"Member Since: {self.user_data['date']}", size=16),
            ft.Text(f"Wallet Balance: FCFA {self.user_data['wallet_balance']}", size=16, color=ft.colors.GREEN_500),
            ft.Text(f"Total Income: FCFA {self.user_data['total_income']}", size=16, color=ft.colors.BLUE_500),
            ft.Text(f"Total Expenditure: FCFA {self.user_data['total_expenditure']}", size=16, color=ft.colors.RED_500),
            ft.Text(f"Total Savings: FCFA {self.user_data['total_savings']}", size=16, color=ft.colors.PURPLE_500),
        ])

        # Transaction Table
        self.transaction_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Date")),
                ft.DataColumn(label=ft.Text("Title")),
                ft.DataColumn(label=ft.Text("Type")),
                ft.DataColumn(label=ft.Text("Amount")),
            ],
            rows=self.get_transaction_rows(),
        )

        # Main Content
        self.controls = [
            ft.Row([
                sidebar,
                ft.Container(
                    content=ft.Row([
                        self.user_info_section,
                        ft.ListView([
                            ft.Text("Transactions", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_500),
                            self.transaction_table,
                        ], spacing=10,width=700)
                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ,
                    bgcolor= ft.Colors.WHITE,
                    height= 600,
                    expand=True,
                    padding=20,
                )
            ])
        ]

    def get_transaction_rows(self):
        rows = []
        for transaction in self.transactions:
            amount_color = (
                ft.colors.GREEN_500 if transaction["type"] == "income" else
                ft.colors.RED_500 if transaction["type"] == "expense" else
                ft.colors.YELLOW_500
            )
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(transaction["date"])),
                    ft.DataCell(ft.Text(transaction["title"])),
                    ft.DataCell(ft.Text(transaction["type"].capitalize())),
                    ft.DataCell(ft.Text(f"FCFA {transaction['amount']}", color=amount_color)),
                ]
            ))
        return rows

    def back(self):
        self.page.go('/admin_users')
        self.page.update()
