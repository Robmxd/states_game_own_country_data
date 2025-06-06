import pandas
import turtle
from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import pandas as pd


"""
    - marcar e desmarcar posicao com m1/m2
    - exibir lista de estados ja cadastrado
    - color picker par texto
    - tamanho de fonte
    - manual como usar

"""

MY_COUNTRY_MAP = ''
DF_PATH = ''
ALIGNMENT = "right"
FONT = ('Arial', 14, 'normal')

WHITE = '#FFF5E4'
ORANGE = '#FFA725'
LIGHT_GREEN = '#C1D8C3'
GREEN = '#6A9C89'
STATES_LIST = []
STATES_FIELD = ''
CHECKED_STATES = []
STATES_COORD = []
CURRENT_IDX = 0
STATES_FONT = None
STATES_FONT_COLOR = '#000000'
DF = None


def set_states_list():
    global STATES_LIST, DF
    DF = pd.read_csv(DF_PATH)
    STATES_LIST = DF[STATES_FIELD].to_list()

def unpin_click(event):
    #undo last pin
    global CHECKED_STATES, STATES_COORD, CURRENT_IDX
    if len(CHECKED_STATES): CHECKED_STATES[-1][1].destroy()
    CHECKED_STATES = CHECKED_STATES[:-1]
    STATES_COORD = STATES_COORD[:-1]
    CURRENT_IDX = len(CHECKED_STATES)
    list_box.delete(0, END)
    for s in CHECKED_STATES:
        insert_lb(s[0])
    current_label.config(text=f'Current State ({CURRENT_IDX+1}/{len(STATES_LIST)})')
    current_state.set(STATES_LIST[CURRENT_IDX])



def pin_click(event):
    
    def convert_to_turtle_coordinats():
        return (x/ratio - og_width//2 - (max_width-resize_to[0])//2, -y/ratio + og_height//2 -(max_height-resize_to[1])//2)

    global CURRENT_IDX, STATES_COORD, CHECKED_STATES
    x, y = event.x, event.y
    if CURRENT_IDX < len(STATES_LIST):
        print(f"Mouse clicked at ({x}, {y})")
        STATES_COORD.append(convert_to_turtle_coordinats())

        checked_state = custom_state_label(STATES_LIST[CURRENT_IDX], x, y)

        CHECKED_STATES.append((STATES_LIST[CURRENT_IDX], checked_state))
        list_box.delete(0, END)
        for s in CHECKED_STATES:
            insert_lb(s[0])

        # Optional: draw a dot where clicked
        #img_canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
        CURRENT_IDX += 1
        if CURRENT_IDX < len(STATES_LIST):
            current_state.set(STATES_LIST[CURRENT_IDX])
            current_label.config(text=f'Current State ({CURRENT_IDX+1}/{len(STATES_LIST)})')
    if CURRENT_IDX >= len(STATES_LIST):
        finish_button()
def font_selected():
   pass 

def insert_lb(txt):
    list_box.insert(END, txt.rjust(15 + len(txt)//2, ' '))

def custom_state_label(name, x, y):
    checked_state = Label(img_canvas, text=name, font=STATES_FONT, fg=STATES_FONT_COLOR)
    checked_state.place(x=x, y=y, anchor='center')
    return checked_state

def select_font(event):
    new_font = fonts_selector.get()
    STATES_FONT.configure(size=new_font)

def finish_button():
    finish = Button(img_canvas, text='save to csv', command=save_to_csv, bg=ORANGE, font=('arial', 15, 'normal'))
    finish.place(x=100, y=int(img_canvas.winfo_height()*0.9))

def save_to_csv():
    DF['x'] = [c[0] for c in STATES_COORD]
    DF['y'] = [c[1] for c in STATES_COORD]
    DF['font_size'] = STATES_FONT['size']
    DF['font_color'] = STATES_FONT_COLOR
    print(DF)
    DF.to_csv(DF_PATH, index=False)



if __name__ == "__main__":

    width = 2000
    height = 1500
    x = 200
    y = 200

    # set data variables
    MY_COUNTRY_MAP = input('Path to country map: ')
    DF_PATH = input('Path to csv file that contains state names: ')
    STATES_FIELD = input('Name of the column with state names')
    set_states_list()

    window = Tk()
    window.title("Building Country Data")
    window.config(padx=50, pady=50, bg=WHITE)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    STATES_FONT = tkfont.Font(family='Arial', size=14, weight='normal')

    #background canvas
    canvas = Canvas(window, bg=LIGHT_GREEN, highlightthickness=1)
    canvas.place(relx=0, rely=0, width=1900, height=1400)

    #inner grid of content
    img_canvas = Canvas(bg=GREEN, highlightthickness=0, width=1480, height=1360)
    img_canvas.grid(column=1, row=0, columnspan=4, rowspan=9, sticky='nw', pady=(20, 20))

    window.update()
    max_width, max_height = 1480, 1360
    og_img = Image.open(MY_COUNTRY_MAP)
    og_width, og_height = og_img.size
    ratio = min(max_width / og_width, max_height / og_height)
    resize_to = (int(og_width * ratio), int(og_height * ratio))
    resized_img = og_img.resize(resize_to, Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(resized_img)
    #country_map = PhotoImage(file="day_25_us_states_game_start/country_game_data_maker/brasil_topografico_gabarito.gif")
    img_canvas.create_image(img_canvas.winfo_width()//2, img_canvas.winfo_height()//2, image=tk_img, anchor='center')

    canvas.update_idletasks()

    img_canvas_x = img_canvas.winfo_rootx()
    img_canvas_y = img_canvas.winfo_rooty()

    # mouse pin and unpin interaction for pin current state
    img_canvas.bind("<Button-1>", pin_click)
    img_canvas.bind("<Button-3>", unpin_click)

    #how to use widget
    how_to_use_canvas = Canvas(bg=ORANGE, width=360, height=300)
    how_to_use_canvas.grid(column=0, row=0, padx=(20, 20), pady=(20, 20))

    label_mouse_1 = Label(how_to_use_canvas, text="M1 - pin")
    how_to_use_canvas.create_window(100, 100, window=label_mouse_1, anchor='nw')

    label_mouse_2 = Label(how_to_use_canvas, text="M2 - undo pin")
    how_to_use_canvas.create_window(100, 150, window=label_mouse_2, anchor='nw')

    def color_picker():
        global STATES_FONT_COLOR
        color = colorchooser.askcolor(title='Names color')
        STATES_FONT_COLOR = color[1]
        for l in CHECKED_STATES:
            l[1].config(fg=color[1])

    choose_color = Button(text='text color', command=color_picker)
    choose_color.grid(column=0, row=1, pady=(10, 20))

    #font_size
    size_opts = [i for i in range(10, 26)]
    fonts_selector = ttk.Combobox(values=size_opts, width=8, state='readonly')
    fonts_selector.set("font size")
    fonts_selector.grid(column=0, row=2, pady=(0, 20))
    fonts_selector.bind("<<ComboboxSelected>>", select_font)

    # current state highlight
    current_label = Label(bg=LIGHT_GREEN, text=f'Current State ({CURRENT_IDX+1}/{len(STATES_LIST)})')
    current_label.grid(column=0, row=3, sticky='w', padx=(50, 0), pady=(0, 10))

    current_state = StringVar()
    current = Entry(width=20, state='readonly', textvariable=current_state)
    current.grid(column=0, row=4, pady=(0, 40))
    current_state.set(STATES_LIST[CURRENT_IDX])

    #states list
    list_box = Listbox(width=20, height=22, bg=WHITE)
    list_box.grid(column=0, row=5)

    







    window.mainloop()
