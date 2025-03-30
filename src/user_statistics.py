import flet as ft
import math

def get_category_icon(category):
    icon_mapping = {
        'food': ft.icons.RESTAURANT,
        'transport': ft.icons.DIRECTIONS_BUS,
        'housing': ft.icons.HOME,
        'salary': ft.icons.ATTACH_MONEY,
        'entertainment': ft.icons.MOVIE,
        'utilities': ft.icons.LIGHTBULB,
    }
    return icon_mapping.get(category.lower(), ft.icons.RECEIPT)


class Statistics(ft.Column):
    def __init__(self, page, sidebar):
        super().__init__()
        self.page = page
        self.p = 0
        self.sidebar = sidebar
        # Main content column (holds welcome text and charts)
        self.main_column = ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Row([
                    ft.Text("My Statistics!",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREEN_400
                            ),
                    ft.ElevatedButton(
                        "Print Report",
                        icon=ft.icons.PRINT,
                        on_click=self.print_report
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("Insights on your expenses, incomes, savings and transactions",
                        size=14,
                        color=ft.colors.GREY_600,
                        ),
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.START,
        )
        # Body structure: Row(sidebar, main content)
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

        # Initialize the statistics page
        self.construct_charts()

    def print_report(self, e):
        # Handle print report action
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Generating PDF report..."),
            action="Done"
        )
        self.page.snack_bar.open = True
        self.page.update()

    def construct_charts(self):
        # Create a scrollable container for all charts
        charts_container = ft.Container(
            content=ft.Column([
                # Income vs Expenses Overview
                self.create_income_expense_overview(),
                ft.Container(height=20),

                # Top section with two charts side by side
                ft.Row([
                    self.create_expense_pie_chart(),
                    self.create_monthly_trend_chart()
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=20),

                # Middle section with two charts side by side
                ft.Row([
                    self.create_category_comparison_chart()
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=20),


                # Full width chart at the bottom
                #self.create_transaction_history_chart()
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )

        # Add the charts container to the main column
        self.main_column.controls.append(charts_container)
        self.page.update()

    def create_income_expense_overview(self):
        # Create a container for income vs expense overview chart
        datas = self.page.db.get_user_metrics_sum(self.page.userId)
        print("Datas:",datas)
        maximum= 0
        for num in datas:

            num_float =float(num['amt'].split(' FCFA')[0])
            if num_float>maximum:
                maximum = num_float

        print(maximum)


        return ft.Container(
            content=ft.Column([
                ft.Text("Income vs Expenses Overview", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column([
                        # Income bar
                        ft.Text("Income", size=14),
                        ft.Row([

                            ft.Container(
                                content=ft.Container(
                                    bgcolor=ft.colors.GREEN_400,
                                    border_radius=5,
                                    height=30,
                                    width=0 if maximum==0 else (float(datas[0]['amt'].split(' FCFA')[0]) / maximum)* 600,  # Represents FCFA4,250
                                ),

                                height=30,
                                border_radius=5,
                                bgcolor=ft.colors.GREEN_100
                            ),
                            ft.Text(datas[0]["amt"], size=14, weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=15),
                        # Expenses bar
                        ft.Text("Expenses", size=14),
                        ft.Row([

                            ft.Container(
                                content=ft.Container(
                                    bgcolor=ft.colors.RED_400,
                                    border_radius=5,
                                    height=30,
                                    width=0 if maximum==0 else (float(datas[1]['amt'].split(' FCFA')[0]) / maximum)* 600,  # Represents FCFA2,830
                                ),

                                height=30,
                                border_radius=5,
                                bgcolor=ft.colors.RED_100
                            ),
                            ft.Text(datas[1]["amt"], size=14, weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=15),
                        # Savings bar
                        ft.Text("Net Savings", size=14),
                        ft.Row([

                            ft.Container(
                                content=ft.Container(
                                    bgcolor=ft.colors.BLUE_400,
                                    border_radius=5,
                                    height=30,
                                    width=0 if maximum==0 else (float(datas[2]['amt'].split(' FCFA')[0]) / maximum)* 600,
                                ),

                                height=30,
                                border_radius=5,
                                bgcolor=ft.colors.BLUE_100
                            ),ft.Text(datas[2]["amt"], size=14, weight=ft.FontWeight.BOLD)

                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ]),
                    padding=20
                )
            ]),
            width=self.page.window.width * 0.7,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            )
        )

    def create_expense_pie_chart(self):
        # Mock data for expense distribution
        categories = ['Food','Housing','Transport','Entertainment','Insurance','Health','Debt','Personal Care','Others']
        percentages = self.page.db.get_categories_percentage(categories,self.page.userId)
        sum = 0
        for value in percentages:
            sum += value
        colors = [
            ft.colors.AMBER_500,
            ft.colors.CYAN_500,
            ft.colors.INDIGO_500,
            ft.colors.LIME_500,
            ft.colors.BROWN_500,
            ft.colors.LIGHT_GREEN_500,
            ft.colors.DEEP_ORANGE_500,
            ft.colors.PINK_ACCENT_200,
            ft.colors.BLUE_GREY_500
        ]
        sections = []
        percents = []
        index = 0
        for percentage in percentages:
            percent = 0 if sum==0 else round((percentage/sum) * 100)
            percents.append(percent)
            pie = ft.PieChartSection(
                percentage,
                title=categories[index],
                title_style=ft.TextStyle(
                    size=7, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
                ),
                color=colors[index],
                radius=50,
            )
            sections.append(pie)
            index += 1
        chart = ft.PieChart(
            sections= sections,
            sections_space=0,
            center_space_radius=40,
            expand=True,
        )
        # Create chart container with legend
        return ft.Container(
            content=ft.Column([
                ft.Text("Expense Distribution", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.Row([
                    # Mock pie chart segments using overlapping containers with rotation
                    chart,
                    # Legend
                    ft.Column([
                        *[ft.Row([
                            ft.Container(width=12, height=12, bgcolor=colors[i], border_radius=3),
                            ft.Text(f"{categories[i]}: {percents[i]}%", size=12)
                        ], spacing=5) for i in range(len(categories))]
                    ], spacing=8)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            width=self.page.window.width * 0.33,
            height=400,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            )
        )

    def bar_chart(self):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        income_heights = self.page.db.get_heights(self.page.userId, "income")

        expense_heights = self.page.db.get_heights(self.page.userId, "expense")

        maximum = 0
        for income in income_heights:
            if income > maximum:
                maximum = income

        for income in expense_heights:
            if income > maximum:
                maximum = income

        barchart = []

        for idx, t in enumerate(income_heights):
            barchart.append(
                ft.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=0 if maximum==0 else (income_heights[idx]/maximum)*110,
                            width=20,
                            color=ft.Colors.GREEN_400,
                            tooltip=income_heights[idx],
                            border_radius=0,
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=0 if maximum==0 else (expense_heights[idx]/maximum)*110,
                            width=20,
                            color=ft.Colors.RED_400,
                            tooltip=expense_heights[idx],
                            border_radius=0,
                        )
                    ],
                )
            )
        chart = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Monthly income and expenses", size=20, color=ft.Colors.GREEN_400,
                            weight=ft.FontWeight.BOLD),
                    # Example of a bar chart (You can replace with actual chart library)
                    ft.BarChart(
                        bar_groups=barchart,
                        border=ft.border.all(1, ft.Colors.GREY_400),
                        left_axis=ft.ChartAxis(
                            labels_size=40, title=ft.Text("Amount"), title_size=40
                        ),
                        bottom_axis=ft.ChartAxis(
                            labels=months,
                            labels_size=40,
                        ),
                        horizontal_grid_lines=ft.ChartGridLines(
                            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
                        ),
                        tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
                        max_y=110,
                        interactive=True,
                        expand=True,
                    ),
                ]
            ),
            width=500,
        )
        return chart

    def create_monthly_trend_chart(self):
        # Mock data for monthly trends
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        income_heights = self.page.db.get_heights(self.page.userId,"income")

        expense_heights = self.page.db.get_heights(self.page.userId,"expense")

        maximum = 0
        for income in income_heights:
            if income>maximum:
                maximum=income

        for income in expense_heights:
            if income>maximum:
                maximum=income


        # Create chart container
        return ft.Container(
            content=ft.Column([
                ft.Text("This year Monthly Income & Expenses", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column([
                        # Create a bar chart with side-by-side bars
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        # Income bar
                                        ft.Container(
                                            height=0 if maximum==0 else (income_heights[i]/maximum)*200,
                                            width=15,
                                            bgcolor=ft.colors.GREEN_400,
                                            border_radius=ft.border_radius.only(top_left=5, top_right=5),
                                        ),
                                        # Expense bar
                                        ft.Container(
                                            height=0 if maximum==0 else (expense_heights[i]/maximum)*200,
                                            width=15,
                                            bgcolor=ft.colors.RED_400,
                                            border_radius=ft.border_radius.only(top_left=5, top_right=5),
                                        )
                                    ], spacing=4,alignment=ft.MainAxisAlignment.END),
                                    ft.Container(height=5),
                                    ft.Text(month, size=10)
                                ], alignment=ft.MainAxisAlignment.END),
                                width=40,
                                height=250,
                                alignment=ft.alignment.bottom_center
                            ) for i, month in enumerate(months)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=10, height=10, bgcolor=ft.colors.GREEN_400, border_radius=5),
                                    ft.Text("Income", size=10)
                                ], spacing=5),
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=10, height=10, bgcolor=ft.colors.RED_400, border_radius=5),
                                    ft.Text("Expenses", size=10)
                                ], spacing=5),
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                    ]),
                    padding=10,
                )
            ]),
            width=self.page.window.width * 0.33,
            height=400,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            )
        )

    def create_category_comparison_chart(self):
        # Mock data for year-over-year category comparison
        categories = ['Food','Housing','Transport','Entertainment','Insurance','Health','Debt','Personal Care','Others']
        last_year = self.page.db.get_last_month(categories,self.page.userId)
        this_year = self.page.db.get_this_month(categories,self.page.userId)


        # Create chart container
        return ft.Container(
            content=ft.Column([
                ft.Text("Month-over-Month Comparison", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=15),
                ft.Column([
                    *[ft.Row([
                        ft.Column([
                            ft.Text(categories[i], size=12, weight=ft.FontWeight.BOLD),
                            ft.Container(height=5),
                            ft.Text("Last Month (FCFA)", size=10, color=ft.colors.GREY_600),
                            ft.Row([
                                ft.Container(
                                    content=ft.Container(
                                        width=0 if this_year[i] == 0 and last_year[i] == 0 else (last_year[i] / max(this_year[i], last_year[i])) * 350,
                                        # Scale for visual representation
                                        height=16,
                                        bgcolor=ft.colors.GREY_200 if last_year[i] == 0 else ft.colors.BLUE_300,
                                        border_radius=4
                                    ),
                                    width=350 if last_year[i] == 0 else (last_year[i] / max(this_year[i],last_year[i ])) * 350,
                                    height=16,
                                    bgcolor=ft.colors.GREY_200,
                                    border_radius=4
                                ),
                                ft.Text(f"{last_year[i]}", size=10)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=5),
                            ft.Text("This Month (FCFA)", size=10, color=ft.colors.GREY_600),
                            ft.Row([
                                ft.Container(
                                    content=ft.Container(
                                        width=0 if this_year[i] == 0 and last_year[i] == 0 else (this_year[i] / max(this_year[i], last_year[i])) * 350,
                                        # Scale for visual representation
                                        height=16,
                                        bgcolor=ft.colors.GREY_200 if this_year[i] == 0 else ft.colors.BLUE_300,
                                        border_radius=4
                                    ),
                                    width=350 if this_year[i] == 0 else (this_year[i] / max(this_year[i],last_year[i])) * 350,
                                    height=16,
                                    bgcolor=ft.colors.GREY_200,
                                    border_radius=4
                                ),
                                ft.Text(f"{this_year[i]}", size=10)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=10)
                        ] , width=400),
                        ft.Column([
                            ft.Text(categories[i+1], size=12, weight=ft.FontWeight.BOLD),
                            ft.Container(height=5),
                            ft.Text("Last Month (FCFA)", size=10, color=ft.colors.GREY_600),
                            ft.Row([
                                ft.Container(
                                    content=ft.Container(
                                        width=0 if this_year[i+1]==0 and last_year[i+1]==0  else(last_year[i+1]/max(this_year[i+1],last_year[i+1]))*350,  # Scale for visual representation
                                        height=16,
                                        bgcolor=ft.colors.GREY_200 if last_year[i+1]==0 else ft.colors.BLUE_300,
                                        border_radius=4
                                    ),
                                    width=350 if last_year[i+1]==0 else(last_year[i+1]/max(this_year[i+1],last_year[i+1]))*350,
                                    height=16,
                                    bgcolor=ft.colors.GREY_200,
                                    border_radius=4
                                ),
                                ft.Text(f"{last_year[i+1]}", size=10)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=5),
                            ft.Text("This Month (FCFA)", size=10, color=ft.colors.GREY_600,text_align=ft.TextAlign.START),
                            ft.Row([
                                ft.Container(
                                    content=ft.Container(
                                        width=0 if this_year[i + 1] == 0 and last_year[i + 1] == 0 else (this_year[i + 1] / max(this_year[i + 1], last_year[i + 1])) * 350,
                                        # Scale for visual representation
                                        height=16,
                                        bgcolor=ft.colors.GREY_200 if this_year[i + 1] == 0 else ft.colors.BLUE_300,
                                        border_radius=4
                                    ),
                                    width=350 if this_year[i + 1] == 0 else (this_year[i + 1] / max(this_year[i + 1],                                                             last_year[i + 1])) * 350,
                                    height=16,
                                    bgcolor=ft.colors.GREY_200,
                                    border_radius=4
                                ),
                                ft.Text(f"{this_year[i+1]}", size=10)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=10)
                        ])

                    ]) for i in range(0,len(categories)-1,2)]
                ])
            ]),
            width=self.page.window.width * 0.7,
            height=800,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            )
        )

