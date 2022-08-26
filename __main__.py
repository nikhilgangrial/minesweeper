#removing right click dots
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from random import randint
from kivy.uix.boxlayout import BoxLayout
from math import ceil
from kivy.uix.popup import Popup
from kivy.uix.actionbar import ActionBar, ActionView, ActionOverflow, ActionButton, ActionPrevious
from threading import Thread
from time import sleep
import sys, os


#function for exe error
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



bombs = set()  #stores location of bombs
buttons_dictionary = {}
prestart = 0   #stores the time before resuming game


# function to calculate elasped time in game
def timer():
    while 1:
        global prestart
        sleep(1)
        time.text = str(prestart)
        # breaks the loop and stops timer when paused
        if buttons_dictionary[(1, 1)].paused:
            break
        prestart += 1


# handle play/pause button commands 
def pause_button_command(*args):
    del args

    # freezes the buttons ie pauses game and ends timer thread
    if not buttons_dictionary[(1, 1)].paused:
        but1.text = "Play"
        for p in range(1, 11):
            for q in range(1, 11):
                buttons_dictionary[(p, q)].paused = True

    # resumes the game
    else:
        but1.text = "Pause"
        for p in range(1, 11):
            for q in range(1, 11):
                buttons_dictionary[(p, q)].paused = False

        # starts the timer thread 
        Thread(target=timer).start()


# handles mouseclick commands command
def mouse_cilick_handler(touch):
    x = ceil(touch.spos[0] * 10)  #calculates button no in row direction
    y = 10 - ceil((touch.spos[1] - 0.1) * 100 / 9)  #calculates button column in y direction

    # skips if not clicked on button  or game is paused
    if not (1 <= x <= 10 and 1 <= y <= 10) or buttons_dictionary[(1, 1)].paused:
        return

    # gets button from the storing list
    self_ = buttons_dictionary[(y, x)]

    #handles right mouse click and marks bombs
    if touch.button == "right" and not self_.destroyed and not self_.marked:
        self_.mark()
    # demarks as bomb when right clicked again
    elif touch.button == "right" and not self_.destroyed:
        self_.demark()
        
    #left mose buuton destroy's button
    else:
        BUTTONS.destroy(y, x)


#creates game enviroonment
def create_new():
    global bombs, prestart
    prestart = 0
    bombs = set()
    # decides bomb location
    while len(bombs) < 10:
        bombs.update({(randint(1, 10), randint(1, 10))})

    #creates buttons and adds them to layout
    for i in range(1, 11):
        for j in range(1, 11):
            address = BUTTONS(i, j)
            Layout.add_widget(address.button)
    #chevks the neighbouring buttons an sets the button value
    for i in range(1, 11):
        for j in range(1, 11):
            buttons_dictionary[(i, j)].check_nighbour()
    #runs timer in thread
    Thread(target=timer).start()
            


# ressets the game environment and delets all butttons and then passes to create function
def reset(instance=None):
    del instance
    #pauses the timer by using the break loop condition
    buttons_dictionary[(1, 1)].paused = True

    #removes all buttons from layout
    for y in range(1, 11):
        for u in range(1, 11):
            Layout.remove_widget(buttons_dictionary[(y, u)].button)
            del buttons_dictionary[(y, u)]
    #creates new environment
    create_new()


# action bar
action = ActionBar()
action.pos_hint = {'top': 1, 'x': 0}
action.size_hint_max_y = 0.1

view = ActionView()
view.use_separator = True

prev = ActionPrevious()
prev.app_icon = resource_path("ico.png")
prev.title = 'Minesweeper'
prev.add_widget(ActionOverflow())
prev.add_widget(ActionButton(text='Time'))
time = ActionButton()
prev.add_widget(time)

view.add_widget(ActionButton(text="Reset", on_release=reset))
but1 = ActionButton(text="Pause", on_release=pause_button_command)
view.add_widget(prev)
view.add_widget(but1)
action.add_widget(view)

# main layout includes all wigets
box = BoxLayout()
box.orientation = 'vertical'
box.add_widget(action) # adding action bar

# grid layout for all buttons
Layout = GridLayout()
box.add_widget(Layout)
Layout.cols = 10
Layout.on_touch_down = mouse_cilick_handler


# closes popup and clears environment
def popup_handler(instance):
    del instance
    pop_up.dismiss()
    reset()


#shows loose message if bomb is triggred
def loose():
    global pop_up
    # disabling buttons to stop from further playing
    for q in range(1, 11):
        for w in range(1, 11):
            buttons_dictionary[(q, w)].destroyed = True
    # displays messaage
    pop_up = Popup()
    pop_up.size_hint = (0.5, 0.5)
    pop_up.add_widget(Button(text=" You loose!!\nclick to retry", on_release=popup_handler))
    buttons_dictionary[(1,1)].paused = True #used to stop the timer
    pop_up.open()


# checks if player has won
def check_win():
    des = 0
    for i in range(1, 11):
        for j in range(1, 11):
            if buttons_dictionary[(i, j)].destroyed:
                des += 1
    if des == 90:
        return True
    else:
        return False


# displays win message
def win():
    global pop_up
    #disabling buttons
    for q in range(1, 11):
        for w in range(1, 11):
            buttons_dictionary[(q, w)].destroyed = True
    #displaying message
    pop_up = Popup()
    pop_up.size_hint = (0.5, 0.5)
    pop_up.add_widget(Button(text="   You Win!!\nclick to Play Again", on_release=popup_handler))
    buttons_dictionary[(1,1)].paused = True # terminates the timer
    pop_up.open()


# class for making buttons and managing them
class BUTTONS:
    global buttons_dictionary, bombs
    while len(bombs) < 10:
        bombs.update({(randint(1, 10), randint(1, 10))})

    def __init__(self, x, y):

        buttons_dictionary[(x, y)] = self
        if (x, y) in bombs:
            self.value = -1
        else:
            self.value = 0

        button_temp = Button(text='')
        self.button = button_temp
        if (x + y) % 2 == 1:
                self.button.background_normal = resource_path("normal.png")
        else:
            self.button.background_normal = resource_path("normal2.png")
        self.button.background_down = resource_path("click.png")

        self.count = 0
        self.x = x
        self.y = y
        self.cords = (x, y)
        self.destroyed = False
        self.marked = False
        self.paused = False


    def check_nighbour(self):

        if self.value != -1:
            count = 0
            for k in range(self.x - 1, self.x + 2):
                for l in range(self.y - 1, self.y + 2):
                    # noinspection PyBroadException
                    try:
                        if buttons_dictionary[(k, l)].value == -1:
                            count += 1
                    except:
                        pass
            self.value = count

    def mark(self):

        self.marked = True
        if (self.x + self.y) % 2 == 1:
            self.button.background_normal =resource_path("mark.png")
            self.button.background_down = resource_path("mark.png")
        else:
            self.button.background_normal = resource_path("mark2.png")
            self.button.background_down = resource_path("mark2.png")

    def demark(self):

        self.marked = False
        if (self.x + self.y) % 2 == 1:
            self.button.background_normal = resource_path("normal.png")
        else:
            self.button.background_normal = resource_path("normal2.png")
        self.button.background_down = resource_path("click.png")


    @staticmethod    
    def destroy(x, y):

        address = buttons_dictionary[(x, y)]
        if not (address.destroyed or address.paused or address.marked):
            address.destroyed = True
            if (x, y) in bombs:
                loose()

            elif address.value == 0:

                address.button.background_normal = resource_path("clickclick.png")
                address.button.background_down = resource_path("clickclick.png")

                for x_ in range(x - 1, x + 2):
                    for y_ in range(y - 1, y + 2):
                            try:
                                BUTTONS.destroy(x_, y_)
                            except:
                                pass

            else:
                colors = ((0, 0, 1, 1),(1, 0.8, 0.5, 1), (1, 0.6, 0.4, 1), (1, 0, 0, 1), (1, 0, 1, 1))

                address.button.color = colors[4] if address.value > 5 else colors[address.value-1]
                address.button.font_size = 25
                address.button.text = str(address.value)
                address.button.background_normal = resource_path("clickclick.png")
                address.button.background_down = resource_path("clickclick.png")
        if check_win():
            win()


#creates game env
create_new()


class Game(App):
    def build(self):
        return box
        

# run the game
if __name__ == "__main__":
    Game().run()
    App.get_running_app().stop()
    
