from user_dialog.user_dialog import UserDialog


def mainloop():
    UserDialog.welcome()
    UserDialog.main_help()
    while True:
        print()
        user_input = input("input: ")
        match user_input.lower():

            case "automatic":
                UserDialog.automatic_menu()

            case "interactive":
                UserDialog.interactive_menu()

            case "number_size":
                UserDialog.modify_number_size()

            case "verbosity":
                UserDialog.modify_verbosity()

            case "current_expression":
                UserDialog.show_current_expression()

            case "solve":
                UserDialog.solve_current_expression()

            case "quit":
                break

            case _:
                UserDialog.main_help()
