from assets import *
import PySimpleGUI as sg


#local variables rewrite test
FILE_NAME = "TEST"
WINDOW_NAME = 'TEST'
BUTTONS_NAME = ["Bezárás", "Üzemel", "Szünet", "Takarítás", "Karbantartás", "Nincs használatban", "Műszakváltás", "Nullázó"] # list for insert buttons list number start 0 to endnumber, the  "close" is basic zeronumber
USER = login()
MACHINE = "TEST"
DATE = date()
TIME =time()
DATETIME = dt()


sg.theme('TealMono') 

# create login and data window
def main_window():
    global LAST_STATE, DATETIME, MACHINE, USER
    main_window_layout = [[sg.Text(DATETIME, key="datetime", justification="left", pad=((0,100),(0,0))), sg.Text("Előző állapot:", justification="right"), sg.Text(last_state(FILE_NAME), key="last_state",justification="rigth")], 
                [sg.Text("Felhasználó:", justification="left", pad=((0,0),(0,0))), sg.Text(USER, pad=((0,100),(0,0))), sg.Text("Jelenlegi Állapot:"), sg.Text(key='state')],
                [sg.Button(BUTTONS_NAME[1]), sg.Button(BUTTONS_NAME[2]), sg.Button(BUTTONS_NAME[3]), sg.Button(BUTTONS_NAME[4]), sg.Button(BUTTONS_NAME[5])],
                [sg.Button(BUTTONS_NAME[6]), sg.Button(BUTTONS_NAME[7]), sg.Exit(BUTTONS_NAME[0])]]

    main_window = sg.Window(WINDOW_NAME, main_window_layout, 
                            finalize=True,
                            text_justification='center',
                            auto_size_text=True,
                            auto_size_buttons=False,
                            default_button_element_size=(20, 1))

    for key, state in {f'{BUTTONS_NAME[1]}': False, f'{BUTTONS_NAME[2]}': False, f'{BUTTONS_NAME[3]}': False, f'{BUTTONS_NAME[4]}': False, f'{BUTTONS_NAME[5]}': False}.items():
        main_window[key].update(disabled=state)


    while True:

        event, values = main_window.read(timeout=1000)
        

        main_window["datetime"].Update(dt())
        main_window["last_state"].Update(last_state1(FILE_NAME))
        main_window["state"].Update(last_state(FILE_NAME))

        if last_state(FILE_NAME) != "Takarítás" and last_state(FILE_NAME) != "Karbantartás" and last_state(FILE_NAME) != "Nincs használatban":       
            if time() == "21:44:10" or time() == "19:12:30" or time() == "19:12:50":
                event = BUTTONS_NAME[2]
                main_window[key].update(disabled=state)
                main_window["state"].Update(event)
                
                
            elif time() == "21:44:20" or time() == "19:12:40":    
                event = BUTTONS_NAME[1]
                main_window[key].update(disabled=state)
                main_window["state"].update(event)


        if event == BUTTONS_NAME[1]:
            for key, state in {f'{BUTTONS_NAME[1]}': True, f'{BUTTONS_NAME[2]}': False, f'{BUTTONS_NAME[3]}': False, f'{BUTTONS_NAME[4]}': False, f'{BUTTONS_NAME[5]}': False}.items():
                main_window[key].update(disabled=state)
            main_window['state'].update(event)
            working(FILE_NAME, MACHINE, USER, BUTTONS_NAME[1], dt(), dt() - last_time(FILE_NAME))
            

        elif event == BUTTONS_NAME[2]:
            for key, state in {f'{BUTTONS_NAME[1]}': False, f'{BUTTONS_NAME[2]}': True, f'{BUTTONS_NAME[3]}': False, f'{BUTTONS_NAME[4]}': False, f'{BUTTONS_NAME[5]}': False}.items():
                main_window[key].update(disabled=state)
            main_window['state'].update(event)
            pause(FILE_NAME, MACHINE, USER, BUTTONS_NAME[2], dt(), dt() - last_time(FILE_NAME))
            

        elif event == BUTTONS_NAME[3]:
            for key, state in {f'{BUTTONS_NAME[1]}': False, f'{BUTTONS_NAME[2]}': False, f'{BUTTONS_NAME[3]}': True, f'{BUTTONS_NAME[4]}': False, f'{BUTTONS_NAME[5]}': False}.items():
                main_window[key].update(disabled=state)
            main_window['state'].update(event)
            cleaning(FILE_NAME, MACHINE, USER, BUTTONS_NAME[3], dt(), dt() - last_time(FILE_NAME))
            

        elif event == BUTTONS_NAME[4]:
            for key, state in {f'{BUTTONS_NAME[1]}': False, f'{BUTTONS_NAME[2]}': False, f'{BUTTONS_NAME[3]}': False, f'{BUTTONS_NAME[4]}': True, f'{BUTTONS_NAME[5]}': False}.items():
                main_window[key].update(disabled=state)
            main_window['state'].update(event)
            maintenance(FILE_NAME, MACHINE, USER, BUTTONS_NAME[4], dt(), dt() - last_time(FILE_NAME))


        elif event == BUTTONS_NAME[5]:
            for key, state in {f'{BUTTONS_NAME[1]}': False, f'{BUTTONS_NAME[2]}': False, f'{BUTTONS_NAME[3]}': False, f'{BUTTONS_NAME[4]}': False, f'{BUTTONS_NAME[5]}': True}.items():
                main_window[key].update(disabled=state)
            main_window['state'].update(event)
            not_using(FILE_NAME, MACHINE, USER, BUTTONS_NAME[5], dt(), dt() - last_time(FILE_NAME))

        elif event == BUTTONS_NAME[6]:
            shift_change_window()
            main_window['state'].update(event)
            main_window.close()
        
            
        elif event == BUTTONS_NAME[7]:
            main_window['state'].update(event)
            zero_window()
            
        if event == sg.WIN_CLOSED or event == BUTTONS_NAME[0]:
            break
        # print(last_state(FILE_NAME))
        


def zero_window():
    zero_layout = [
        [sg.Text("Utolsó adat nullázása")],
        [sg.Text("Kérem a kódot:"), sg.Input(password_char="*")],
        [sg.Button("Nullázás"), sg.Exit("Mégse")]
    ]

    zero_window = sg.Window(WINDOW_NAME, zero_layout)

    while True:
        name, zero_password = zero_window.read()

        if name == sg.WIN_CLOSED or name == "Mégse":
            break

        else:
            if zero_password[0] != "12356":
                sg.popup("Nem adtál meg jelszót", auto_close=True)

            else:
                set_zero_default_value(FILE_NAME, MACHINE, USER, dt())
                zero_window.close()


def shift_change_window():
    shift_change_layout = [[sg.Text('Műszak vége:'), sg.Text(USER)],        
            [sg.Text("Számláló előző állása"), sg.Text(last_value(FILE_NAME), key="last_value")],
            [sg.Text("Számláló állása"), sg.Input()],      
            [sg.Button('Bevitel'), sg.Exit("Bezárás")]]      

    shift_change_window = sg.Window(WINDOW_NAME, shift_change_layout)      

 

    while True:                             # The Event Loop
        event, values = shift_change_window.read()

        if event == sg.WIN_CLOSED or event == "Bezárás":
            break        

        if event == "Bevitel":

            if event == "Bevitel" and values[0] == "" or int(values[0]) < int(last_value(FILE_NAME)) or int(values[0]) > 10000 + int(last_value(FILE_NAME)):
                sg.popup("Nem megfelelő érték")

            else:
                shift_change(FILE_NAME, MACHINE, USER, BUTTONS_NAME[6], values[0], dt(), dt() - last_time(FILE_NAME))
                shift_change_window.close()
                
                

if __name__ == '__main__':
    main_window()