from user_dialog import events


def mainloop():
    events.help()
    while True:
        user_input = input("input: ")
        match user_input.lower():

            case "automatic":
                events.automatic()

            case "i":
                events.interactive()

            case "number_size":
                events.modify_number_size()

            case "quit":
                break

            case _:
                events.help()
