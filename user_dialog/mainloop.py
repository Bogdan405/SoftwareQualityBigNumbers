from user_dialog import events


def mainloop():
    events.help()
    while True:
        user_input = input("input: ")
        match user_input.lower():

            case "automatic":
                events.automatic()

            case "interactive":
                events.interactive()

            case "number_size":
                events.modify_number_size()

            case "verbosity":
                events.modify_verbosity()

            case "quit":
                break

            case _:
                events.help()
