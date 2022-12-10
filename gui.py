import PySimpleGUI as sg
from gui_screens import welcome_screen, new_screen, edit_screen, run_screen
from minitroll import MiniTroll

sg.theme('Topanga')

window = welcome_screen()

def main():
    
    while True:
    
        event, values = window.read()
        
        
        if event == sg.WIN_CLOSED:
            return
    
        elif event == 'New':
            new_screen()
        
        elif event == 'Edit':
            edit_screen()
            
        elif event == 'Run':
            run_screen()
            
        elif event == 'About':
            sg.popup('Credits','Made By:\n\nAbdelrahman Wael\nFady Amr\nEslam Mohammed\nAhmed Elsayed\n','Supervisied by:\nDr.Khaled Bahnasy', icon='Troll.ico')
main()    