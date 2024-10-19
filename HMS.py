from HmsApp import HmsApp


def main():
    app = HmsApp()
    while app.is_running:
        app.choose_action()
        app.check_app_status()
    app.HmsDb.close_db_connection()


if __name__ == "__main__":
    main()
