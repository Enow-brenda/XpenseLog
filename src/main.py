import flet as ft
from login import LoginForm
from signup import SignupForm
from user_sidebar import Sidebar
from user_dashboard import Dashboard
from admin_sidebar import ASidebar
from admin_users import AUsersPage
from admin_userinfo import UserInfoPage
from admin_transactions import ATransactionsPage
from admin_dashboard import ADashboard
from user_statistics import Statistics
from user_transactions import TransactionsPage
from db_helper import DatabaseHelper


def main(page: ft.Page):

    # App configuration
    page.db = DatabaseHelper()
    page.title = "XpenseLog"
    page.theme_mode = ft.ThemeMode.LIGHT
    #page.horizontal_alignment = "center"
    #page.scroll = "adaptive"

    #route management
    def route_change(route):
        page.views.clear()

        if page.route == "/login" or page.route=="/":
            page.views.append(ft.View("/login", [LoginForm(page)]))
        if page.route == "/signup":
            page.views.append(ft.View("/signup", [SignupForm(page)]))
        if page.route.startswith("/dashboard"):
            # 1. Create sidebar FIRST
            user_id = None
            if "?userId=" in page.route:
                user_id = page.route.split("?userId=")[1]
                page.userId = user_id

            sidebar = Sidebar(page)
            sidebar.construct(0)
            dashboard = Dashboard(page,sidebar)
            dashboard.construct_cards()
            page.views.append(ft.View("/dashboard", [dashboard]))
        if page.route == "/statistics" :
            sidebar = Sidebar(page)
            sidebar.construct(1)
            statistics = Statistics(page, sidebar)
            #statistics.construct_cards()
            page.views.append(ft.View("/statistics", [statistics]))
        if page.route == "/transactions" :
            sidebar = Sidebar(page)
            sidebar.construct(2)
            transactions = TransactionsPage(page, sidebar)
            #statistics.construct_cards()
            page.views.append(ft.View("/transactions", [transactions]))
        if page.route.startswith("/control") or page.route == "/admin_dashboard":

            user_id = None
            if "?userId=" in page.route:
                user_id = page.route.split("?userId=")[1]
                page.userId = user_id

            # 1. Create sidebar FIRST
            sidebar = ASidebar(page)
            sidebar.construct(0)
            dashboard = ADashboard(page,sidebar)
            dashboard.construct_cards()
            page.views.append(ft.View("/control", [dashboard]))
        if page.route == "/admin_users":
            # 1. Create sidebar FIRST
            sidebar = ASidebar(page)
            sidebar.construct(1)
            dashboard = AUsersPage(page, sidebar)
            page.views.append(ft.View("/admin_users", [dashboard]))
        if page.route == "/admin_userinfo":
            # 1. Create sidebar FIRST
            sidebar = ASidebar(page)
            sidebar.construct(1)
            dashboard = UserInfoPage(page, sidebar)

            page.views.append(ft.View("/control", [dashboard]))
        if page.route == "/admin_transactions":
            # 1. Create sidebar FIRST
            sidebar = ASidebar(page)
            sidebar.construct(2)
            dashboard = ATransactionsPage(page,sidebar)

            page.views.append(ft.View("/control", [dashboard]))
        if page.route.startswith("/view_users"):
            user_id = None
            if "?member_id=" in page.route:
                member_id = page.route.split("?member_id=")[1]
                page.member_id = member_id
                print("member id",member_id)

            # 1. Create sidebar FIRST
            sidebar = ASidebar(page)
            sidebar.construct(0)
            dashboard = UserInfoPage(page, sidebar)

            page.views.append(ft.View("/view_users", [dashboard]))
        if page.route == "/exit" or page.route == "/admin_exit" :
            page.userId = None
            page.go('/login')


        page.update()



    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER)