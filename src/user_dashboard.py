import flet as ft

def get_type_icon(category):
    icon_mapping = {
        'income': ft.Icon(
                            name=ft.Icons.TRENDING_UP,  # Create this helper function
                            color=ft.Colors.GREEN_600
                        ),
        'expense': ft.Icon(
                            name=ft.Icons.TRENDING_DOWN,  # Create this helper function
                            color=ft.Colors.RED_600
                        ),
        'saving': ft.Icon(
                            name=ft.Icons.SAVINGS,  # Create this helper function
                            color=ft.Colors.YELLOW_600
                        ),

    }
    return icon_mapping.get(category.lower())
class Dashboard(ft.Column):
    def __init__(self, page, sidebar):

        super().__init__()
        self.page = page
        self.p=0
        self.sidebar = sidebar

        # Main content column (holds welcome text and cards)
        self.main_column = ft.Column(
            controls=[
                ft.Container(height=50),
                ft.Text("Welcome Back!",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.GREEN_400
                        ),
                ft.Text("Let’s help you manage your expenses",
                        size=14,
                        color=ft.colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                        ),
            ],
            spacing=6,  # Better spacing between texts
            alignment=ft.MainAxisAlignment.START,

        )

        # Body structure: Row(sidebar, main content)
        self.controls = [ft.Container(
            content=ft.Row(
                controls=[sidebar, self.main_column],
                spacing=20  # Remove default spacing
            ),
            height=self.page.window.height,
            padding=ft.padding.symmetric(horizontal=0, vertical=0)
        )]

    def construct_cards(self):
        datas = self.page.db.get_user_metrics_sum(self.page.userId)

        # Simulating a list of recent transactions
        transactions = self.page.db.get_transactions_by_user(self.page.userId,"limit")

        cards = []
        for data in datas:
            cards.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.ATTACH_MONEY, color=ft.colors.GREEN_400, size=30),
                                    title=ft.Text(data["title"] + " (FCFA)", size=10, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(data["amt"].split('FCFA')[0], size=15, weight=ft.FontWeight.BOLD,
                                                     color=ft.colors.BLACK),
                                )
                            ],
                            spacing=10,
                        ),
                        width=240,
                        padding=15,
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,  # Rounded corners
                        shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.colors.GREY_400),  # Soft shadow
                        border=ft.border.all(1, ft.colors.GREY_300),
                    )
                )
            )

        # Add cards to the main column
        self.main_column.controls.append(ft.Row(cards, wrap=True))

        # Transaction cards wrapped in a scrollable ListView
        transaction_cards = [
            ft.Card(
                elevation=5,
                color=ft.Colors.WHITE,
                surface_tint_color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
                content=ft.Container(
                    content=ft.ListTile(
                        leading=get_type_icon(t['type']),
                        title=ft.Text(
                            t['title'],
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.GREY_800
                        ),
                        subtitle=ft.Text(
                            f"{t['date']} • {t['description']}",
                            color=ft.Colors.GREY_500,
                            size=12
                        ),
                        trailing=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Text(
                                    f"{t['amount']} FCFA",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREEN_600 if t['type'] == 'income' else ft.Colors.RED_600 if t['type'] == 'expense' else ft.Colors.YELLOW_600
                                ),
                                ft.Text(
                                    t['type'].upper(),
                                    size=12,
                                    color=ft.Colors.GREY_500,
                                    weight=ft.FontWeight.W_500
                                )
                            ]
                        ),
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    border=ft.border.only(
                        left=ft.border.BorderSide(
                            width=3,
                            color=ft.Colors.GREEN_600 if t['type'] == 'income' else ft.Colors.RED_600 if t['type'] == 'expense' else ft.Colors.YELLOW_600
                        )
                    ),
                    bgcolor=ft.Colors.WHITE,
                )
            ) for idx, t in enumerate(transactions[:5])
        ]

        # Create a scrollable ListView for the transactions
        transactions_list = ft.ListView(
            expand=True,
            controls=transaction_cards,
            height=350,  # You can adjust the height based on your design needs
            padding=10
        )
        maxim = 0
        expenses_data = self.page.db.get_last_7_days_expenses(self.page.userId)
        for data in expenses_data:
            if data['amount'] > maxim:
                maxim = data['amount']

        barchart = []
        labels = []
        for idx, t in enumerate(expenses_data):
            labels.append(
                ft.ChartAxisLabel(
                    value=idx, label=ft.Container(ft.Text(t["date"]), padding=10)
                )
            )
            barchart.append(
                ft.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=t["amount"],
                            width=40,
                            color=ft.Colors.GREEN_400,
                            tooltip=t["amount"],
                            border_radius=0,
                        ),
                    ],
                )
            )

        bottom = ft.Row(
            controls=[
                # Chart on the left side (Spending Habits in the last 7 days)
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Spending Habits (Last 7 Days)", size=20, color=ft.Colors.GREEN_400,
                                    weight=ft.FontWeight.BOLD),
                            # Example of a bar chart (You can replace with actual chart library)
                            ft.BarChart(
                                bar_groups=barchart,
                                border=ft.border.all(1, ft.Colors.GREY_400),
                                left_axis=ft.ChartAxis(
                                    labels_size=40, title=ft.Text("Amount Spent"), title_size=40
                                ),
                                bottom_axis=ft.ChartAxis(
                                    labels=labels,
                                    labels_size=40,
                                ),
                                horizontal_grid_lines=ft.ChartGridLines(
                                    color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
                                ),
                                tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
                                max_y= maxim,
                                interactive=True,
                                expand=True,
                            ),
                        ]
                    ),
                    width=500,
                ),
                # Transaction cards on the right side
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(width=400, height=30),
                            ft.Text("Recent Transactions", size=20, color=ft.Colors.GREEN_400,
                                    weight=ft.FontWeight.BOLD),
                            transactions_list if len(transactions) >0 else ft.Text("No Transactions", size=15,
                                    weight=ft.FontWeight.BOLD),  # Insert the scrollable transaction list here

                        ]
                    ),
                    width=400,
                ),
            ],
            spacing=10,
        )

        self.main_column.controls.append(bottom)
        self.page.update()
