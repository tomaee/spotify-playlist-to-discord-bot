import PySimpleGUI as sg


def open_interface():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Enter playlist link:')],
            [sg.InputText()],
            [sg.OK()]
            ]
    window = sg.Window(title='Playlist Player', layout=layout, margins=(100, 50))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'OK':
            break
    window.close()
    return values[0]



open_interface()

