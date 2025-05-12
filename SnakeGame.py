from tkinter import *
from tkinter import messagebox
import random
import sqlite3

#Color Theme
BG_COLOR = "#1e1e1e" 
FG_COLOR = "#ffffff"
COLOR = "#4CAF50"
SECONDARY_COLOR = "#2d2d2d"
HIGHLIGHT_COLOR = "#3e3e3e"

#DataBase Setup
user_alias_db = sqlite3.connect("User DataBase.db")
cr = user_alias_db.cursor()

def create_tables():
  #Users Table
  cr.execute('''
    CREATE TABLE IF NOT EXISTS Users
    (ID INTEGER PRIMARY KEY,
    Name NVARCHAR(20) NOT NULL UNIQUE)
    ''')
  #All User Scores
  cr.execute('''
    CREATE TABLE IF NOT EXISTS Scores
    (Name NVARCHAR(20),
    Score INTEGER,
    FOREIGN KEY (Name) REFERENCES Users(Name))
    ''')

create_tables()

#Default Game Settings Values
game_settings = {
    'border': True,
    'speed': 'Medium'  #Can Be 'Slow', 'Medium', 'Fast'
}

def refresh_alias_lists():
  global alias_id_list, alias_name_list
  alias_id_list = []
  alias_name_list = []
  cr.execute("SELECT * FROM Users")
  results = cr.fetchall()
  for row in results:
    alias_id_list.append(row[0])
    alias_name_list.append(row[1])

refresh_alias_lists()

def add_alias_menu():
  add_alias_window = Toplevel()
  add_alias_window.geometry("300x200")
  add_alias_window.title("Add New Alias Menu")
  add_alias_window.config(bg=BG_COLOR)
  add_alias_window.resizable(False, False)

  def add():
    new_name = name_entry.get().strip()
    if not new_name:
      messagebox.showerror(title= "Error", message= "Alias cannot be empty")
      return
    try:
      #Insert New User Into DataBase
      cr.execute("SELECT MAX(ID) FROM Users")
      last_id = cr.fetchone()[0]
      new_id = 1 if last_id is None else last_id + 1
      cr.execute("INSERT INTO Users VALUES(?, ?)",(new_id, new_name))
      user_alias_db.commit()
      refresh_alias_lists()
      messagebox.showinfo(title= "Success", message= "Alias Added Successfully")
      add_alias_window.destroy()
    except sqlite3.IntegrityError:
      messagebox.showerror(title="Error", message= "Alias Already Exists")

  input_frame = Frame(add_alias_window, bg=BG_COLOR, padx=20, pady=20)
  input_frame.pack(expand=True, fill=BOTH)

  enter_alias_label = Label(input_frame, text="Enter New Alias:",
                            font=('Arial', 12), bg=BG_COLOR, fg=FG_COLOR)
  enter_alias_label.pack(pady=(0, 10))

  name_entry = Entry(input_frame, font=('Arial', 12),
                    bg=SECONDARY_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR,
                    highlightcolor=COLOR,
                    highlightbackground=HIGHLIGHT_COLOR,
                    relief=FLAT, highlightthickness=1) 
  name_entry.pack(ipady=5, fill=X)

  alm_button_frame = Frame(input_frame, bg=BG_COLOR)
  alm_button_frame.pack(pady=(20, 0))

  add_button= Button(alm_button_frame, text="Add", command=add,
                    font=('Arial', 10, 'bold'), padx=20, pady=5, borderwidth=0,
                    bg=COLOR, fg=FG_COLOR, activebackground=COLOR)
  add_button.pack(side=LEFT, padx=5)

  alm_close_button = Button(alm_button_frame, text="Close", command=add_alias_window.destroy,
                            font=('Arial', 10, 'bold'), padx=20, pady=5, borderwidth=0,
                            bg=SECONDARY_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR)
  alm_close_button.pack(side=LEFT, padx=5)

def load_alias_menu():
  #Hide Main Menu Buttons
  buttons_frame.pack_forget()

  alias_listbox.delete(0, END)
  if not alias_name_list:
    alias_listbox.insert(END, "No Alias Yet!")
  else:
    for name in alias_name_list:
      alias_listbox.insert(END, name)

  #Show Load Alias Menu Widgets
  alias_listbox.pack(pady=(20, 10), padx=10, fill=BOTH, expand=True)

  loadalias_button_frame.pack(pady=(20, 0))

  load_button.pack(side=LEFT, padx=5)
  delete_button.pack(side=LEFT, padx=5)
  llm_back_button.pack(side=LEFT, padx=5)

def delete_alias():
  selected = alias_listbox.curselection()
  if not selected:
    messagebox.showerror(title= "Error",message= "No Alias Selected")
    return

  selected_name = alias_listbox.get(selected[0])
  if selected_name == "No Alias Yet!":
    messagebox.showerror(title="Error", message="No Alias To Delete")
    return
  else:
    try:
      cr.execute("DELETE FROM Users WHERE Name=?", (selected_name,))
      user_alias_db.commit()
      refresh_alias_lists()
      load_alias_menu()  #Refresh The List
      messagebox.showinfo(title= "Success",message= "Alias Deleted Successfully")
    except Exception as e:
      messagebox.showerror(title= "Error",message= f"Failed To Delete Alias: {str(e)}")

def play_menu():
  selected = alias_listbox.curselection()
  if not selected:
    messagebox.showerror(title= "Error",message= "No Alias Selected")
    return
  selected_name = alias_listbox.get(selected[0])
  if selected_name == "No Alias Yet!":
    messagebox.showerror(title="Error", message="Please Create An Alias First")
    return
  else:
    #Hide Load Alias Menu Widgets
    loadalias_button_frame.pack_forget()

    #Show Play Menu Widgets
    playmenu_button_frame.pack(pady=10)

    play_button.pack(pady=5)
    settings_button.pack(pady=5)
    scores_button.pack(pady=5)

def return_to_main_menu():
  # Hide load menu widgets
  loadalias_button_frame.pack_forget()

  # Show main menu buttons
  buttons_frame.pack()

def speed_choice(speed):
    game_settings['speed'] = speed

def border_choice(has_border):
    game_settings['border'] = has_border

def settings_menu():
  settings_window = Toplevel()
  settings_window.geometry("400x350")
  settings_window.title("Settings")
  settings_window.config(bg=BG_COLOR)
  settings_window.resizable(False, False)

  main_frame = Frame(settings_window, bg=BG_COLOR, padx=20, pady=20)
  main_frame.pack(expand=True, fill=BOTH)

  #Snake Speed Settings
  snakespeed_labelframe = LabelFrame(main_frame, text="Snake Speed",font=('Arial', 10, 'bold'),
                          padx=10, pady=10, bg=BG_COLOR, fg=COLOR)
  snakespeed_labelframe.pack(fill=X, pady=(0, 20))

  speeds_list = ["Slow", "Medium", "Fast"]
  speed_var = StringVar(value=game_settings['speed'])

  for speed in speeds_list:
    snakespeeds_radiobuttons = Radiobutton(snakespeed_labelframe, text=speed, variable=speed_var, value=speed,
                                          command=lambda: speed_choice(speed_var.get()), font=('Arial', 10),
                                          bg=BG_COLOR, fg=FG_COLOR, selectcolor=SECONDARY_COLOR,
                                          activebackground=BG_COLOR, activeforeground=FG_COLOR)
    snakespeeds_radiobuttons.pack(anchor=W, pady=2)

  #Border Settings
  borders_labelframe = LabelFrame(main_frame, text="Borders",font=('Arial', 10, 'bold'),
                        padx=10, pady=10, bg=BG_COLOR, fg=COLOR)
  borders_labelframe.pack(fill=X)

  border_var = StringVar(value="Yes" if game_settings['border'] else "No")

  enable_radionbuton = Radiobutton(borders_labelframe, text="Enabled", variable=border_var, 
                                  value="Yes", command=lambda: border_choice(True), font=('Arial', 10),
                                  bg=BG_COLOR, fg=FG_COLOR, selectcolor=SECONDARY_COLOR,
                                  activebackground=BG_COLOR, activeforeground=FG_COLOR)
  enable_radionbuton.pack(anchor=W, pady=2)
  no_radionbuton = Radiobutton(borders_labelframe, text="Disableed", variable=border_var, 
                              value="No", command=lambda: border_choice(False), font=('Arial', 10),
                              bg=BG_COLOR, fg=FG_COLOR, selectcolor=SECONDARY_COLOR,
                              activebackground=BG_COLOR, activeforeground=FG_COLOR)
  no_radionbuton.pack(anchor=W, pady=2)

  close_button = Button(main_frame, text="Close", command=settings_window.destroy,
                        font=('Arial', 10, 'bold'), padx=20, pady=5, borderwidth=0,
                        bg=COLOR, fg=FG_COLOR, activebackground=COLOR)
  close_button.pack(pady=(20, 0))

def high_scores_menu():
  scores_window = Toplevel()
  scores_window.geometry("400x350")
  scores_window.title("High Scores")
  scores_window.config(bg=BG_COLOR)
  scores_window.resizable(False, False)

  frame = Frame(scores_window, bg=BG_COLOR, padx=20, pady=20)
  frame.pack(fill=BOTH, expand=True)

  title_label = Label(frame, text="High Scores", font=('Arial', 14, 'bold'),
                      bg=BG_COLOR, fg=COLOR )
  title_label.pack(pady=(0, 10))

  list_frame = Frame(frame, bg=BG_COLOR)
  list_frame.pack(fill=BOTH, expand=True)

  scrollbar = Scrollbar(list_frame)
  scrollbar.pack(side=RIGHT, fill=Y)

  scores_list = Listbox(list_frame, yscrollcommand=scrollbar.set,
                        font=('Arial', 11),
                        borderwidth=0, highlightthickness=0,
                        bg=SECONDARY_COLOR, fg=FG_COLOR,
                        selectbackground=HIGHLIGHT_COLOR,
                        selectforeground=FG_COLOR)
  scores_list.pack(fill=BOTH, expand=True)

  scrollbar.config(command=scores_list.yview)

  #Choosing The Highest Score For Every Player
  cr.execute("""
        SELECT Name, MAX(Score) as HighScore 
        FROM Scores 
        GROUP BY Name 
        ORDER BY HighScore DESC
    """)
  high_scores = cr.fetchall()

  if not high_scores:
    scores_list.insert(END, "No Scores Yet!")
  else:
    for i, (name, score) in enumerate(high_scores, 1):
      scores_list.insert(END, f"{i}. {name}: {score}")

  button_frame = Frame(frame, bg=BG_COLOR)
  button_frame.pack(pady=(20, 0))

  close_button = Button(button_frame, text="Close", command=scores_window.destroy,
                        font=('Arial', 10, 'bold'), padx=20, pady=5, borderwidth=0,
                        bg=COLOR, fg=FG_COLOR, activebackground=COLOR)
  close_button.pack(side=LEFT, padx=5)

  def delete_all_scores():
    if not high_scores:
      messagebox.showerror(title="Error", message="No Scores To Delete")
    else:
      cr.execute("DELETE FROM Scores")
      user_alias_db.commit()
      scores_window.destroy()
      messagebox.showinfo(title="Succesfull", message="All Scores Deleted Succesfully")

  delete_all_button = Button(button_frame, text="Delete All", command=delete_all_scores,
                            font=('Arial', 10, 'bold'), padx=20, pady=5, borderwidth=0,
                            bg='red', fg=FG_COLOR, activebackground='red')
  delete_all_button.pack(side=LEFT, padx=5)

def start_game():
  GAME_WIDTH = 1000
  GAME_HEIGHT = 700
  speed_settings = {
    'Slow': 150,
    'Medium': 100,
    'Fast': 50
  }
  SPEED = speed_settings[game_settings['speed']]
  SPACE_SIZE = 30
  BODY_PARTS = 3
  SNAKE_COLOR = "#00FF00"
  FOOD_COLOR = 'red'
  BACKGROUND_COLOR = 'black'

  window=Toplevel()
  window.title("Snake Game By Ziad")
  window.config(bg=BACKGROUND_COLOR)
  window.resizable(False, False)

  #Force Focus On Game Window
  window.focus_force()
  window.grab_set()  #Prevent Other Windows From Receiving Input

  score = 0
  direction = 'down'

  score_frame = Frame(window, bg=BACKGROUND_COLOR)
  score_frame.pack(fill=X, padx=20, pady=10)

  label = Label(score_frame, text=f'Score : {score}', font=('Arial', 16, 'bold'),
                bg=BACKGROUND_COLOR, fg=FG_COLOR)
  label.pack(side=LEFT)

  #Player Name Display
  selected = alias_listbox.curselection()
  if selected:
    player_name = alias_listbox.get(selected[0])
    player_label = Label(score_frame, text=f"Player : {player_name}", 
                        font=('Arial', 12), bg=BACKGROUND_COLOR, fg=FG_COLOR)
    player_label.pack(side=RIGHT)

  canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT,
                  highlightthickness=0)
  canvas.pack()
  #Make Sure Canvas Can Receive Focus
  canvas.focus_set()

  class Snake:
    def __init__(self):
      self.body_size = BODY_PARTS
      self.coordinates = []
      self.squares = []

      for i in range(0, BODY_PARTS):
        self.coordinates.append([0, 0])

      for x, y in self.coordinates:
        square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE,
                                        fill=SNAKE_COLOR, tag='Snake')
        self.squares.append(square)

  class Food:
    def __init__(self):
      x = random.randint(0,int((GAME_WIDTH/SPACE_SIZE)-1)) * SPACE_SIZE
      # 700/50 =14, like chess , convert into pixels by *space_size
      y = random.randint(0,int((GAME_HEIGHT/SPACE_SIZE)-1)) * SPACE_SIZE
      self.coordinates = [x, y]
      canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE,
                        fill=FOOD_COLOR, tag='food')

  def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    #Handle Borderless Wrapping Before Collision Detection
    if not game_settings['border']:
        if x < 0:
            x = GAME_WIDTH - SPACE_SIZE
        elif x >= GAME_WIDTH:
            x = 0
        if y < 0:
            y = GAME_HEIGHT - SPACE_SIZE
        elif y >= GAME_HEIGHT:
            y = 0

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    food_x, food_y = food.coordinates
    #Modified Food Collision Detection To Account For Wrapping
    if ((food_x <= x < food_x + SPACE_SIZE and food_y <= y < food_y + SPACE_SIZE) or
        (not game_settings['border'] and 
        ((x < 0 and GAME_WIDTH - SPACE_SIZE <= x + SPACE_SIZE < GAME_WIDTH and food_y <= y < food_y + SPACE_SIZE) or
          (x >= GAME_WIDTH - SPACE_SIZE and 0 <= x - GAME_WIDTH < SPACE_SIZE and food_y <= y < food_y + SPACE_SIZE) or
          (y < 0 and GAME_HEIGHT - SPACE_SIZE <= y + SPACE_SIZE < GAME_HEIGHT and food_x <= x < food_x + SPACE_SIZE) or
          (y >= GAME_HEIGHT - SPACE_SIZE and 0 <= y - GAME_HEIGHT < SPACE_SIZE and food_x <= x < food_x + SPACE_SIZE)))):
        nonlocal score
        score += 1
        label.config(text=f"Score : {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisios(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

  def change_direction(new_direction):
    nonlocal direction
    if new_direction == 'left':
      if direction != 'right':
        direction = new_direction
    elif new_direction == 'right':
      if direction != 'left':
        direction = new_direction
    if new_direction == 'up':
      if direction != 'down':
        direction = new_direction
    elif new_direction == 'down':
      if direction != 'up':
        direction = new_direction

  def check_collisios(snake):
    x, y = snake.coordinates[0]

    #Check Wall Collisions Based On Border Settings
    if game_settings['border']:
      if x < 0 or x >= GAME_WIDTH:
        return True
      elif y < 0 or y >= GAME_HEIGHT:
        return True
    else:
      if x < 0:
        x = GAME_WIDTH - SPACE_SIZE
      elif x >= GAME_WIDTH:
        x = 0
      if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE
      elif y >= GAME_HEIGHT:
        y = 0

      snake.coordinates[0] = [x, y]

    #Check Snake Collisions
    for body_part in snake.coordinates[1:]:
      if x == body_part[0] and y == body_part[1]:
        return True

    return False

  def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                      font=('Arial', 50, 'bold'), text='Game Over!', fill='red', tag='gameover')
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 60,
                      font=('Arial', 24), text=f'Final Score: {score}',
                      fill=FG_COLOR)

    #Save Player Score
    selected = alias_listbox.curselection()
    if selected:
      player_name = alias_listbox.get(selected[0])
      cr.execute("INSERT INTO Scores VALUES(?, ?)", (player_name, score))
      user_alias_db.commit()

    window.grab_release()

  #Key Binding For Window And Canvas
  window.bind("<Up>", lambda event: change_direction('up'))
  window.bind("<Down>", lambda event: change_direction('down'))
  window.bind("<Left>", lambda event: change_direction('left'))
  window.bind("<Right>", lambda event: change_direction('right'))

  canvas.bind('<Up>', lambda event: change_direction('up'))
  canvas.bind('<Down>', lambda event: change_direction('down'))
  canvas.bind('<Left>', lambda event: change_direction('left'))
  canvas.bind('<Right>', lambda event: change_direction('right'))

  snake = Snake()
  food = Food()

  canvas.focus_set()
  next_turn(snake, food)

  #Adjust the window to middle of screen
  window.update()
  window_width = window.winfo_width()
  window_height = window.winfo_height()
  screen_width = window.winfo_screenwidth()
  screen_height = window.winfo_screenheight()

  x = int((screen_width/2) - (window_width/2))
  y = int((screen_height/2) - (window_height/2))

  window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Main Window Setup
main_window = Tk()
main_window.title("Snake Game By Ziad")
main_window.geometry("400x400")
main_window.config(bg=BG_COLOR)
main_window.resizable(False, False)


#Game Title
title_frame = Frame(main_window, bg=BG_COLOR, pady=20)
title_frame.pack(fill=X)

title_label = Label(title_frame, text="Snake Game By Ziad", font=('Arial', 20, 'bold'),
                    bg=BG_COLOR, fg=COLOR)
title_label.pack()

#Main Menu Widgets
buttons_frame = Frame(main_window, bg=BG_COLOR, padx=40, pady=20)
buttons_frame.pack(expand=True, fill=BOTH)

new_alias_button = Button(buttons_frame, text="New Alias", command=add_alias_menu,
                          font=('Arial', 12, 'bold'), padx=20, pady=10, borderwidth=0,
                          bg=COLOR, fg=FG_COLOR, activebackground=COLOR)
new_alias_button.pack(pady=5, fill=X)

load_alias_button = Button(buttons_frame, text="Load Alias", command=load_alias_menu,
                          font=('Arial', 12, 'bold'), padx=20, pady=10, borderwidth=0,
                          bg=SECONDARY_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR)
load_alias_button.pack(pady=5, fill=X)

#Load Alias Menu Widgets
loadalias_button_frame = Frame(main_window, bg=BG_COLOR)

alias_listbox = Listbox(loadalias_button_frame,font=('Arial', 11), borderwidth=0,
                        bg=SECONDARY_COLOR, fg=FG_COLOR, highlightthickness=0,
                        selectbackground=HIGHLIGHT_COLOR, selectforeground=FG_COLOR)

load_button = Button(loadalias_button_frame, text="Load", command=play_menu,
                    font=('Arial', 10, 'bold'), padx=20, pady=10, borderwidth=0,
                    bg=COLOR, fg=FG_COLOR, activebackground=COLOR)

delete_button = Button(loadalias_button_frame, text="Delete", command=delete_alias,
                      font=('Arial', 10, 'bold'), padx=20, pady=10, borderwidth=0,
                      bg=SECONDARY_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR)

llm_back_button = Button(loadalias_button_frame, text="Back", command=return_to_main_menu,
                        font=('Arial', 10, 'bold'), padx=20, pady=10, borderwidth=0,
                        bg=SECONDARY_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR)

#Play Menu Widgets
playmenu_button_frame = Frame(main_window, bg=BG_COLOR)

play_button = Button(main_window, text="Play", command=start_game, width=15,
                    font=('Arial', 10), padx=15, pady=5, borderwidth=0,
                    bg=COLOR, fg=FG_COLOR, activebackground=COLOR)

settings_button = Button(main_window, text="Settings", command=settings_menu, width=15,
                        font=('Arial', 10), padx=15, pady=5, borderwidth=0,
                        bg=SECONDARY_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR)

scores_button = Button(main_window, text="High Scores", command=high_scores_menu, width=15,
                      font=('Arial', 10), padx=15, pady=5, borderwidth=0,
                        bg=SECONDARY_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR)

#Adjust Window In Middle of The Screen
main_window.update()
window_width = main_window.winfo_width()
window_height = main_window.winfo_height()
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

main_window.mainloop()