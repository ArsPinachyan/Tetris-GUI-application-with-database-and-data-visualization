import numpy as np
import pygame, sys
from tkinter import *
from pygame import mixer
from button_ver1 import Buttons
import matplotlib.pyplot as plt
from mysql.connector import connect, Error
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tetris_v1 import main, s_width, s_height, exp_sound,poch_sound,game_sound

pygame.init()
# s_width = 800 and s_height = 700
SCREEN = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Main menu: Welcome to TETRIS!")

icon = pygame.image.load('assets/teticon.png').convert_alpha()
icon = pygame.transform.scale(icon, (52, 52)) 

pygame.display.set_icon(icon)

BG = pygame.image.load("assets/Background.png")

volume = 0.4

musicList = ['assets/original-tetris-theme.mp3','assets/quiet-resource.mp3','assets/loginska.mp3','assets/starry-night-piano.mp3']

currentIndex = 0
initMusic = musicList[currentIndex]

ind = musicList[currentIndex].rindex('/')
songName = musicList[currentIndex][ind + 1:]

mixer.music.load(initMusic)
mixer.music.set_volume(volume)
mixer.music.play(-1)

if_play = 1

paused = False
clicked = True
expPlay = True
losePlay = True
changePlay = True

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def player_name(play,vol,filename,explay,loseplay,poch_play):
    root = Tk()
    root.title('ALMOST PLAYING: SELECT YOUR NAME!')
    root.iconbitmap('assets/teticon.ico')
    root.geometry('450x450')

    red = PhotoImage(file="assets/redCross.png")
    redCross = red.subsample(48,48)

    names = []

    try:
        connection = connect(host = 'localhost',user = 'root', password = '', database = 'testing', port = '3306')
        conn = connection.cursor()
        conn.execute("SELECT * FROM players")
        for row in conn:
            names.append(row[1])
    except Error as e:
        messagebox.showerror('',f'Connection not working. {e}')
        print(e)

    def delete_name():
        try:
            selected = combo.get()
            delete_sql = f"DELETE FROM players WHERE name LIKE '{selected}'"
            conn.execute(delete_sql)
            connection.commit()
            messagebox.showinfo('',f'The name {selected} is successfully deleted!')
        except Error as e:
            messagebox.showerror('',f'There is error! {e}')
        except:
            messagebox.showerror('','There is error! Something went wrong')
        else:
            names.remove(selected)
            combo.config(values=names)
            last = len(names) - 1
            combo.current(last)

    def main_game():

        id = 0
        try:
            selected = combo.get()
            delete_sql = f"SELECT * FROM players WHERE name LIKE '{selected}'"
            conn.execute(delete_sql)
            for row in conn:
                id = row[0]
            connection.commit()
        except Error as e:
            messagebox.showerror('',f'There is error! {e}')
        except:
            messagebox.showerror('','There is error! Something went wrong')
        else:
            root.destroy()
            main(play,vol,filename,explay,loseplay,poch_play,id)
    
    def command_name():

        def remove_new_frame():
            for widget in new_frame.winfo_children():
                widget.destroy()
            new_frame.pack_forget()
            addName.config(state = 'normal')
            addName.config(text = 'Add a name in list')
        
        def add_name():
            try:
                new_name = entry_name.get()
                add_sql = f"INSERT INTO `players`(`name`) VALUES ('{new_name}')"
                conn.execute(add_sql)
                connection.commit()
                messagebox.showinfo('',f'The name {new_name} is successfully added!')
            except Error as e:
                messagebox.showerror('',f'There is error! {e}')
            except:
                messagebox.showerror('','There is error! Something went wrong')
            else:
                names.append(new_name)
                combo.config(values=names)
                last = len(names) - 1
                combo.current(last)
                remove_new_frame()

        new_frame = Frame(root,bg = "#3c0424")

        lab_name = Label(new_frame, text = 'Add a name',font = ('Press Start 2P',11,'normal'),bg = "#3c0424",fg = 'white')
        lab_name.grid(row = 0,column = 0, pady = 5)

        entry_name = Entry(new_frame, font = ('Press Start 2P',14,'normal'), bg = 'white',fg = 'black', width = 15)
        entry_name.grid(row = 1,column = 0, pady = 5)

        redButton = Button(new_frame,image = redCross,command = remove_new_frame,bg = "#3c0424",borderwidth = 0)
        redButton.grid(row = 1, column = 1, padx = 5)

        add_button = Button(new_frame, text = 'Add',font = ('Press Start 2P',10,'bold'),command = add_name,bg = "gray",fg = 'white',activebackground = 'white',  
        activeforeground = 'black')

        add_button.grid(row = 2, column = 0, pady = 3)

        new_frame.pack()
        addName.config(text = 'click red Cross')
        addName.config(state = 'disabled')
        

    background = PhotoImage(file = 'assets/background_opt.png')

    # Show image using label
    label1 = Label(root, image = background)
    label1.place(x = 0,y = 0)

    last = len(names) - 1

    mainFrame = Frame(root,bg = "#3c0424")
    mainFrame.pack(pady = 5)

    label_name = Label(mainFrame, text = 'Select a player name',font = ('Press Start 2P',12,'normal'),bg = "#3c0424",fg = 'white')
    label_name.grid(row = 0,column = 0)
    combo = ttk.Combobox(mainFrame,values = names,font = ('Press Start 2P',14,'normal'),width = 9,height = 6)
    combo.grid(row = 1, column = 0, pady = 10)
    combo.current(last)

    delete_Frame = Frame(root,bg = "#3c0424")
    delete_Frame.pack(pady = 10)

    dele_name = Label(delete_Frame, text = 'Delete a name from list',font = ('Press Start 2P',9,'normal'),bg = "#3c0424",fg = 'white')
    dele_name.grid(row = 0,column = 0, pady = 2)

    del_name = Button(delete_Frame, text = 'Delete name',font = ('Press Start 2P',11,'normal'),command = delete_name,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')
    del_name.grid(row = 1, column = 0, pady = 3)

    ifFrame = Frame(root,bg = "#3c0424")
    ifFrame.pack(pady = 23)

    label1_name = Label(ifFrame, text = 'If there is no your name',font = ('Press Start 2P',9,'normal'),bg = "#3c0424",fg = 'white')
    label1_name.grid(row = 0,column = 0)

    addName = Button(ifFrame, text = 'Add a name in list',font = ('Press Start 2P',12,'normal'),command = command_name,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')

    play_button = Button(root, text = 'PLAY',font = ('Press Start 2P',15,'bold'),command = main_game,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')
    play_button.place(x = 310, y = 360)

    addName.grid(row = 1,column = 0,pady = 5)

    mainloop()

def history():
    root = Tk()
    root.title('Game histroy: FIND YOUR SCORES!')
    root.iconbitmap('assets/teticon.ico')
    root.geometry('750x700')

    background = PhotoImage(file = 'assets/background_opt.png')

    # Show image using label
    label1 = Label(root, image = background)
    label1.place(x = 0,y = 0)

    current_id = 0
    info_selected = []

    def update_selected():
        global current_id
        try:
            id = entry_id.get()
            player_name = entry_name.get()
            select_query = f'SELECT * FROM `players` WHERE name LIKE "{player_name}"'
            conn.execute(select_query)
            r = 0
            id_player = 0
            for row in conn:    
                id_player = int(row[0])
                r += 1
            if r > 0:
                update_query = f'''UPDATE info SET id = {id},player_id = {id_player} WHERE id = {current_id}'''
                print(update_query)
                conn.execute(update_query)
                messagebox.showinfo('','Successfully updated!')
                connection.commit()
            else:
                insert_query = f"INSERT INTO `players`(`name`) VALUES ('{player_name}')"
                conn.execute(insert_query)
                connection.commit()

                select_player_query = f'SELECT * FROM `players` WHERE name LIKE "{player_name}"'
                conn.execute(select_player_query)

                for row in conn:
                    id_player = row[0]
                connection.commit()

                update_query = f'''UPDATE info SET id = {id},player_id= {id_player} WHERE id = {current_id}'''
                print(update_query)
                conn.execute(update_query)
                connection.commit()
                messagebox.showinfo('','Successfully updated! New name added!')
        except Error as e:
            messagebox.showerror('',f'The row is not modfied. {e}')
        except:
            messagebox.showerror('',f'The row is not modfied. Connection not working.')
        else:
            selected = tree.focus()
            tree.item(selected, text = '', values=(entry_id.get(),entry_name.get(),info_selected[0],info_selected[1],info_selected[2]))

    def select_record():
        global current_id
        try:

            entry_name.delete(0,END)
            entry_id.delete(0,END)

            selected = tree.focus()

            values = tree.item(selected, 'values')

            entry_id.insert(0,values[0])
            current_id = int(values[0])
            entry_name.insert(0,values[1])

            for i in range(2,5):
                info_selected.append(values[i])
        except:
            messagebox.showerror('',f'Something is wrong and not working.')


    def remove_one():
        try:
            record = tree.selection()[0]
            index = tree.item(record)['values'][0]
            delete_sql = f'DELETE FROM `info` WHERE `id` = {index}'
            conn.execute(delete_sql)
            connection.commit()
            tree.delete(record)
            messagebox.showinfo('',f'Your row with the index {index} is removed from database.')
            print(index)
        except:
            messagebox.showerror('','Your row is not removed! Something went wrong.')

    def remove_selected():
        try:
            lst = tree.selection()
            indexes = []
            for record in lst:
                index = tree.item(record)['values'][0]
                delete_sql = f'DELETE FROM `info` WHERE `id` = {index}'
                conn.execute(delete_sql)
                connection.commit()
                tree.delete(record)
                indexes.append(index)
            messagebox.showinfo('',f'Your row or rows with the index {indexes} is or are removed from database.')
        except:
            messagebox.showerror('',f'a row/rows is/are not removed. Something went wrong.')

    def remove_all():
        try:
            for record in tree.get_children():
                tree.delete(record)
            delete_sql = 'DELETE FROM `info`'
            conn.execute(delete_sql)
            connection.commit()
            messagebox.showinfo('',f'All the rows are removed from database.')

            alter_table_query = 'ALTER TABLE info AUTO_INCREMENT = 1'
            conn.execute(alter_table_query)
            connection.commit()
        except:
            messagebox.showerror('','rows are not removed. Something went wrong.')

    label_frame = Frame(root,bg = "#3c0424")
    label_frame.pack(pady = 15)

    label_name = Label(label_frame, text = 'History',font = ('Press Start 2P',22,'normal'),bg = "#3c0424",fg = 'white')
    label_name.grid(row = 0,column = 0)

    tree_frame = Frame(root)
    tree_frame.pack(pady = 40)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side = RIGHT, fill = Y)

    bottom_scroll = Scrollbar(tree_frame, orient = 'horizontal')
    bottom_scroll.pack(side = BOTTOM, fill = X)

    tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, xscrollcommand = bottom_scroll.set)

    try:
        connection = connect(host = 'localhost',user = 'root', password = '', database = 'testing', port = '3306')
        conn = connection.cursor()
        conn.execute("SELECT info.id, players.name,score,date,duration  FROM info inner join players on player_id = players.id")
        i = 0
        for row in conn:
            if i % 2 == 0:
                tree.insert('',i, text = '', values = (row[0],row[1],row[2],row[3],row[4]), tags = ('oddrow'))
            else:
                tree.insert('',i, text = '', values = (row[0],row[1],row[2],row[3],row[4]), tags = ('evenrow'))
            i += 1
    except Error as e:
        messagebox.showerror('',f'Connection not working. {e}')
        print(e)

    tree_scroll.config(command = tree.yview)
    bottom_scroll.config(command = tree.xview)

    tree['show'] = 'headings'

    s = ttk.Style(root)
    s.theme_use('clam')

    s.configure('Treeview',background = '#D3D3D3',foreground = 'black',rowheight = 35, fieldbackground = '#D3D3D3')
    s.configure('.',font = ('Press Start 2P',11,'normal'))
    s.configure('Treeview.Heading',foreground = 'green',font = ('Press Start 2P',11,'bold'))
    s.map('Treeview',background = [('selected','green')])

    tree['columns'] = ('ID','Name','Score','Date','Duration')

    tree.column('ID',width = 200,minwidth = 200,anchor = CENTER)
    tree.column('Name',width = 200,minwidth = 200,anchor = CENTER)
    tree.column('Score',width = 200,minwidth = 200,anchor = CENTER)
    tree.column('Date',width = 330,minwidth = 330,anchor = CENTER)
    tree.column('Duration',width = 270,minwidth = 270,anchor = CENTER)


    tree.heading('ID',text = 'Player ID',anchor = CENTER)
    tree.heading('Name',text = 'Player Name',anchor = CENTER)
    tree.heading('Score',text = 'Player Score',anchor = CENTER)
    tree.heading('Date',text = 'Playing date',anchor = CENTER)
    tree.heading('Duration',text = 'Playing Duration',anchor = CENTER)

    tree.tag_configure('oddrow',background = 'silver')
    tree.tag_configure('evenrow',background = '#D3D3D3')

    tree.pack()

    mainFrame = Frame(root,bg = "#3c0424")
    mainFrame.pack()

    label_id = Label(mainFrame, text = 'ID',font = ('Press Start 2P',13,'normal'),bg = "#3c0424",fg = 'white')
    label_id.grid(row = 0,column = 0)

    label_name = Label(mainFrame, text = 'Name',font = ('Press Start 2P',13,'normal'),bg = "#3c0424",fg = 'white')
    label_name.grid(row = 0,column = 1)

    entry_id = Entry(mainFrame, font = ('Press Start 2P',13,'normal'), bg = 'white',fg = 'black', width = 15)
    entry_id.grid(row = 1,column = 0, pady = 5, padx = 15)

    entry_name = Entry(mainFrame, font = ('Press Start 2P',13,'normal'), bg = 'white',fg = 'black', width = 15)
    entry_name.grid(row = 1,column = 1, pady = 5)

    button_frame = Frame(root,bg = "#3c0424")
    button_frame.pack(pady = 10)

    remove_button = Button(button_frame, text = 'Delete one',font = ('Press Start 2P',13,'bold'),command = remove_one,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')
    remove_button.grid(row = 0,column = 0, padx = 20)

    remove_all_button = Button(button_frame, text = 'Delete All',font = ('Press Start 2P',13,'bold'),command = remove_all,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')
    remove_all_button.grid(row = 0,column = 1)

    remove_many_button = Button(button_frame, text = 'Delete Many',font = ('Press Start 2P',13,'bold'),command = remove_selected,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')
    remove_many_button.grid(row = 0,column = 2, padx = 20)

    update_frame = Frame(root,bg = "#3c0424")
    update_frame.pack(pady = 10)

    update_button = Button(update_frame, text = 'Update Record',font = ('Press Start 2P',13,'bold'),command = update_selected,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')
    update_button.grid(row = 0,column = 0,padx = 10)

    select_button = Button(update_frame, text = 'Select Record',font = ('Press Start 2P',13,'bold'),command = select_record,bg = "gray",fg = 'white',activebackground = 'white',  
    activeforeground = 'black')
    select_button.grid(row = 0,column = 1)

    mainloop()
    
def options():

    root = Tk()
    root.title('Music Player: CHANGE MUSIC WHATEVER YOU WANT!')
    root.iconbitmap('assets/teticon.ico')
    root.geometry('700x700')

    background = PhotoImage(file = 'assets/background_opt.png')

    label1 = Label(root, image = background)
    label1.place(x = 0,y = 0)

    volumeOn = PhotoImage(file = r"assets\volumeOn.png")
    volumeOff = PhotoImage(file = r"assets\volumeOff.png")
    volume_on = volumeOn.subsample(7, 7)
    volume_off  = volumeOff.subsample(7, 7)

    def loseMusic():
        global losePlay

        if losePlay == True:
            losePlay = False
            loseCheck.config(image = volume_off)
        else:
            losePlay = True
            loseCheck.config(image = volume_on)
            game_sound.play()

    def expMusic():
        global expPlay

        if expPlay == True:
            expPlay = False
            expCheck.config(image = volume_off)
        else:
            expPlay = True
            expCheck.config(image = volume_on)
            exp_sound.play()

    def changePMusic():
        global changePlay

        if changePlay == True:
            changePlay = False
            changeCheck.config(image = volume_off)
        else:
            changePlay = True
            changeCheck.config(image = volume_on)
            poch_sound.play()

    def changing_name():

        global musicList
        global currentIndex
        global songName

        ind = musicList[currentIndex].rindex('/')
        songN = musicList[currentIndex][ind + 1:]

        song_name.config(text = songN)
        songName = songN

    def add_song():

        global musicList
        global currentIndex
        global volume

        song = filedialog.askopenfilename(initialdir = 'audio/', title = 'Choose a song', filetypes=(('mp3 Files',"*.mp3"),))
        
        if song != '':
            musicList.append(song)
            currentIndex = len(musicList) - 1

            mixer.music.stop()

            mixer.music.load(musicList[currentIndex])
            mixer.music.set_volume(volume)
            mixer.music.play(-1)

            changing_name()


    def volume_control(x):
        global volume
            
        vol = volume_slider.get()/100
        volume = vol
        mixer.music.set_volume(volume)

    def play_music():

        global musicList
        global currentIndex
        global volume
        global if_play

        mixer.music.load(musicList[currentIndex])
        mixer.music.set_volume(volume)
        mixer.music.play(-1)
        if_play = 1

    def stop_music():
        global if_play

        mixer.music.stop()
        if_play = 0

    def back_music():

        global musicList
        global currentIndex
        global volume
        global if_play

        currentIndex -= 1

        if currentIndex < 0:
            currentIndex = len(musicList) - 1

        if if_play == 1:
            mixer.music.load(musicList[currentIndex])
            mixer.music.set_volume(volume)
            mixer.music.play(-1)

        changing_name()

    def forward_music():

        global musicList
        global currentIndex
        global volume

        currentIndex += 1

        if currentIndex == len(musicList):
            currentIndex = 0


        if if_play == 1:
            mixer.music.load(musicList[currentIndex])
            mixer.music.set_volume(volume)
            mixer.music.play(-1)

        changing_name()

    play_btnImgg = PhotoImage(file="assets/play_button.png")
    play_btnImg = play_btnImgg.subsample(6, 6)

    stop_btnImgg = PhotoImage(file="assets/stop_button.png")
    stop_btnImg = stop_btnImgg.subsample(6, 6)

    main_frame = Frame(root, bg = '#3c0424')
    main_frame.pack(fill = BOTH, expand = 1)

    my_canvas = Canvas(main_frame, bg = '#3c0424')
    my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command = my_canvas.yview)
    my_scrollbar.pack(side = RIGHT, fill = Y)

    my_canvas.configure(yscrollcommand = my_scrollbar.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion = my_canvas.bbox('all')))


    playFrame = Frame(my_canvas,bg = "#3c0424")
    playFrame.pack(pady = 10)

    playlabel = Label(playFrame,text = "Music on: ",font = ('Press Start 2P',18,'bold'),bg = '#3c0424',fg = 'white')
    playlabel.grid(row = 0, column = 0, pady = 20, padx = 5)

    play_btn = Button(playFrame,image = play_btnImg,command = play_music,bg = '#3c0424',borderwidth = 0,activebackground = '#3c0424')
    play_btn.grid(row = 0, column = 1, pady = 20)

    stoplabel = Label(playFrame,text = "Music off: ",font = ('Press Start 2P',18,'bold'),bg = '#3c0424',fg = 'white')
    stoplabel.grid(row = 1, column = 0, pady = 20, padx = 5)

    stop_btn = Button(playFrame,image = stop_btnImg,command = stop_music,bg = '#3c0424',borderwidth = 0,activebackground = '#3c0424')
    stop_btn.grid(row = 1, column = 1, pady = 20)




    volume_frame = Frame(my_canvas,bg = "#3c0424")
    volume_frame.pack(pady = 14)

    vol_label = Label(volume_frame,text = "Music volume",font = ('Press Start 2P',14,'bold'),bg = '#3c0424',fg = 'white')
    vol_label.grid(row = 0, column = 0, pady = 20, padx = 20)

    volume_slider = Scale(volume_frame,from_ = 0,to = 100,activebackground = 'gray',bg = '#3c0424',fg = "white",cursor = 'cross',font = ('Press Start 2P',14,'bold'),orient = "horizontal",command = volume_control,length = 300,resolution = 1)
    volume_slider.set(volume*100)
    volume_slider.grid(row = 1, column = 0, pady = 20, padx = 20)



    name_frame = Frame(my_canvas,bg = '#3c0424')
    name_frame.pack(pady = 14)

    song_name = Label(name_frame,text = f"{songName}",font = ('Press Start 2P',16,'bold'),bg = '#3c0424',fg = 'green')
    song_name.grid(row = 0, column = 0, pady = 20, padx = 50)
    

    adds_frame = Frame(my_canvas,bg = '#3c0424')
    adds_frame.pack(pady = 14)

    add_songB = Button(adds_frame,text = "Add a song",font = ('Press Start 2P',18,'bold'),command = add_song,bg = 'gray',fg = "white",activebackground = 'gray')
    add_songB.grid(row = 0, column = 0,pady = 20, padx = 50)


    control_frame = Frame(my_canvas,bg = '#3c0424')
    control_frame.pack(pady = 8)

    back_btnImgg = PhotoImage(file="assets/back_button.png")
    back_btnImg = back_btnImgg.subsample(6, 6)

    forward_btnImgg = PhotoImage(file="assets/forward_button.png")
    forward_btnImg = forward_btnImgg.subsample(6, 6)

    back_btn = Button(control_frame,image = back_btnImg,command = back_music,bg = '#3c0424',borderwidth = 0,activebackground = '#3c0424')
    back_btn.grid(row = 1, column = 1, padx = 10)

    forward_btn = Button(control_frame,image = forward_btnImg,command = forward_music,bg = '#3c0424',borderwidth = 0,activebackground = '#3c0424')
    forward_btn.grid(row = 1, column = 2, padx = 10)



    expFrame = Frame(my_canvas,bg = "#3c0424")
    expFrame.pack(pady = 10)

    if expPlay == True:
        pic = volume_on
    else:
        pic = volume_off

    expCheck = Button(expFrame,image = pic,command = expMusic,bg = '#3c0424',borderwidth = 0,activebackground = '#3c0424')
    expCheck.grid(row = 0, column = 2,pady = 20, padx = 20)

    exp_btnImgg = PhotoImage(file="assets/explosion_png.png")
    exp_btnImg = exp_btnImgg.subsample(21, 21)

    explabel = Label(expFrame,text = "Explosion sound on or off",font = ('Press Start 2P',12,'bold'),bg = '#3c0424',fg = 'white')
    explabel.grid(row = 0, column = 0, pady = 20)

    exp_label = Label(expFrame,image = exp_btnImg,bg = '#3c0424')
    exp_label.grid(row = 0, column = 1, pady = 20)


    loseFrame = Frame(my_canvas,bg = "#3c0424")
    loseFrame.pack(pady = 10)

    lose_btnImgg = PhotoImage(file="assets/lose.png")
    lose_btnImg = lose_btnImgg.subsample(11, 11)

    if losePlay == True:
        pic1 = volume_on
    else:
        pic1 = volume_off

    loseCheck = Button(loseFrame,image = pic1,command = loseMusic,bg = '#3c0424',borderwidth = 0,activebackground = '#3c0424')
    loseCheck.grid(row = 0, column = 2,pady = 20, padx = 20)

    loselabel = Label(loseFrame,text = "Game Lost sound on or off",font = ('Press Start 2P',12,'bold'),bg = '#3c0424',fg = 'white')
    loselabel.grid(row = 0, column = 0, pady = 20)

    lose_label = Label(loseFrame,image = lose_btnImg,bg = '#3c0424')
    lose_label.grid(row = 0, column = 1, pady = 20)

    changeFrame = Frame(my_canvas,bg = "#3c0424")
    changeFrame.pack(pady = 10)

    change_btnImgg = PhotoImage(file="assets/settings.png")
    change_btnImg = change_btnImgg.subsample(30, 30)

    if changePlay == True:
        pic2 = volume_on
    else:
        pic2 = volume_off

    changeCheck = Button(changeFrame,image = pic2,command = changePMusic,bg = '#3c0424',borderwidth = 0,activebackground = '#3c0424')
    changeCheck.grid(row = 0, column = 2,pady = 20)

    changelabel = Label(changeFrame,text = "Position Change sound on off",font = ('Press Start 2P',12,'bold'),bg = '#3c0424',fg = 'white')
    changelabel.grid(row = 0, column = 0, pady = 20)

    change_label = Label(changeFrame,image = change_btnImg,bg = '#3c0424')
    change_label.grid(row = 0, column = 1, pady = 20)

    my_canvas.create_window((350,0), window = playFrame)
    my_canvas.create_window((350,200), window = volume_frame)
    my_canvas.create_window((350,350), window = name_frame)
    my_canvas.create_window((350,420), window = adds_frame)
    my_canvas.create_window((350,510), window = control_frame)
    my_canvas.create_window((350,610), window = expFrame)
    my_canvas.create_window((350,710), window = loseFrame)
    my_canvas.create_window((350,810), window = changeFrame)


    root.mainloop()

def stats():
    root = Tk()
    root.title('Stats Page: SEE WHETHER YOUR SCORE IS THE HIGHEST!')
    root.iconbitmap('assets/teticon.ico')
    root.geometry('950x600')

    background = PhotoImage(file = 'assets/background_opt.png')

    # Show image using label
    label1 = Label(root, image = background)
    label1.place(x = 0,y = 0)

    main_frame = Frame(root, bg = '#3c0424')
    main_frame.pack(fill = BOTH, expand = 1)

    my_canvas = Canvas(main_frame, bg = '#3c0424')
    my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command = my_canvas.yview)
    my_scrollbar.pack(side = RIGHT, fill = Y)

    my_canvas.configure(yscrollcommand = my_scrollbar.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion = my_canvas.bbox('all')))

    def _clear():
        for canvas in canvases:
            for item in canvas.get_tk_widget().find_all():
                canvas.get_tk_widget().delete(item)

    def destroy():
        root.quit()
        mixer.music.stop()
        pygame.quit()
        sys.exit()


    def line(n):
        s = []

        try:
            conn.execute(f'''SELECT `score` FROM `info` inner join `players` on info.player_id = players.id WHERE `name` like '{n}' ''')
            for row in conn:
                    s.append(row[0])
            connection.commit()
        except Error as e:
            messagebox.showerror('',f'Could not get scores. {e}')
        t = range(1,len(s) + 1)
        ax6.plot(t,s,marker = "o",ms = 10)
    
    ids = []
    scores = []

    try:
        connection = connect(host = 'localhost',user = 'root', password = '', database = 'testing', port = '3306')
        conn = connection.cursor()
        conn.execute("SELECT id, score, duration FROM info")
        for row in conn:
            scores.append(row[1])
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Connection not working. {e}')
        print(e)

    for i in range(1,len(scores) + 1):
        ids.append(i)

    canvases = []

    capital_frame = Frame(my_canvas,bg = '#3c0424')
    capital_frame.pack()

    stat_frame = Frame(my_canvas,bg = '#3c0424')
    stat_frame.pack()

    graph_frame = Frame(my_canvas,bg = '#3c0424')
    graph_frame.pack()

    lower_frame = Frame(my_canvas,bg = '#3c0424')
    lower_frame.pack(pady=5000)

    end_frame = Frame(my_canvas,bg = '#3c0424')
    end_frame.pack()

    capital = Label(capital_frame, text = 'STATISTICS',font = ('Press Start 2P',28,'bold'),bg = "#3c0424",fg = 'white')
    capital.grid(pady = 35)

    total_played = 0
    total_score = 0
    total_time = 0

    try:
        conn.execute("SELECT count(id),SUM(score),SUM(`duration`) FROM `info`")
        for row in conn:
            total_played = row[0]
            total_score = row[1]
            total_time = row[2]
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Could not get scores. {e}')
        print(e)

    max_score = 0
    max_time = 0
    min_score = 0
    min_time = 0
    try:
        conn.execute("SELECT max(score),max(duration), min(score),min(duration) player_id FROM `info`")
        for row in conn:
            max_score = row[0]
            min_score = row[2]
            max_time = row[1]
            min_time = row[3]
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Could not get scores. {e}')
        print(e)

    hours = total_time // 3600
    mins = (total_time - hours*3600) // 60
    seconds = (total_time - hours*3600) - mins*60

    mean_score = total_score / total_played
    mean_score = round(mean_score,2)

    mean_time = total_time // total_played
    mean_hours = mean_time // 3600
    mean_mins = (mean_time - mean_hours*3600) // 60
    mean_secs = (mean_time - mean_hours*3600)  - mean_mins*60

    played_total = Label(stat_frame, text = f'Total played: {total_played}                              ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    played_total.grid(row = 0,column = 0, pady = 20)


    score_total = Label(stat_frame, text = f'Total score of game: {total_score}                     ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    score_total.grid(row = 1,column = 0)

    time_total = Label(stat_frame, text = f'Total time: {hours} hours {mins} mins {seconds} secs ({total_time} secs)',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    time_total.grid(row = 2,column = 0,pady = 20)

    mean_score_lab = Label(stat_frame, text = f'Mean score per game: {mean_score}                    ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    mean_score_lab.grid(row = 3,column = 0, pady = 20)

    mean_time_lab = Label(stat_frame, text = f'Mean time: {mean_hours} hours {mean_mins} mins {mean_secs} secs ({mean_time} secs)   ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    mean_time_lab.grid(row = 4,column = 0)

    max_score_lab = Label(stat_frame, text = f'Max score ever: {max_score}                           ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    max_score_lab.grid(row = 5,column = 0,pady = 30)

    min_score_lab = Label(stat_frame, text = f'Min score ever: {min_score}                           ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    min_score_lab.grid(row = 6,column = 0)

    max_time_lab = Label(stat_frame, text = f'Max time ever: {max_time}                        ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    max_time_lab.grid(row = 7,column = 0,pady = 30)

    min_time_lab = Label(stat_frame, text = f'Min time ever: {min_time}                       ',font = ('Press Start 2P',13,'bold'),bg = "#3c0424",fg = 'white')
    min_time_lab.grid(row = 8,column = 0)

    close_button = Button(end_frame, text = 'Close window',font = ('Press Start 2P',13,'bold'),command = destroy,bg = "gray",fg = 'white',activebackground = 'white', activeforeground = 'black')
    close_button.grid(pady = 40)

    font1 = {"family":"Microsoft Tai Le","color":"blue","size":21}
    font2 = {"family":"Georgia","color":"green","size":17}
    font3 = {"family":"Microsoft Tai Le","color":"purple","size":21}
    font4 = {"family":"Georgia","color":"blue","size":17}
    font5 = {"family":"Georgia","color":"black","size":15}
    font6 = {"family":"Microsoft Tai Le","color":"green","size":21}

    xpoints = np.array(ids)
    ypoints = np.array(scores)

    fig1, ax1 = plt.subplots()

    ax1.set_title('Scores per game',fontdict=font1)
    ax1.set_xlabel("Playing Times", fontdict=font2)
    ax1.set_ylabel("Players' Scores", fontdict=font2)
    ax1.grid()
    ax1.plot(xpoints,ypoints,c="#2ACE70",marker = "o",ms = 10)

    canvas1 = FigureCanvasTkAgg(fig1,graph_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack()
    canvases.append(canvas1)

    players = []
    sum_scores = []

    try:
        conn.execute('''SELECT SUM(`score`), name FROM `info` inner join `players` on info.player_id = players.id GROUP By player_id''')
        for row in conn:
            sum_scores.append(row[0])
            players.append(row[1])
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Could not get scores. {e}')
        print(e)

    players = np.array(players)
    sum_scores = np.array(sum_scores)

    fig2, ax2 = plt.subplots()
    ax2.set_title('Total scores per player',fontdict=font3)
    ax2.set_xlabel("Players' Names", fontdict=font4)
    ax2.set_ylabel("Players' Total Scores", fontdict=font4)
    ax2.bar(players,sum_scores,color = '#fac002')
    ax2.grid(axis='y',color='b')

    canvas2 = FigureCanvasTkAgg(fig2,graph_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(pady = 50)
    canvases.append(canvas2)

    time_players = []
    time_durations = []
    percents = []

    try:
        conn.execute('''SELECT SUM(`duration`), name FROM `info` inner join `players` on info.player_id = players.id GROUP By player_id''')
        for row in conn:
            time_durations.append(row[0])
            time_players.append(row[1])
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Could not get scores. {e}')
        print(e)

    def your_autopct_format(prct_value):
        return '{:.1f}%\n{:.0f}'.format(prct_value,float(total_time)*prct_value/100)

    fig3, ax3 = plt.subplots()

    y = np.array(time_durations)

    colors = np.array(["#4CAF50","hotpink","blue","#f5ce42","#fa1b1b","#fa3cf4","#5258fa","#43f0d6"])
    mylabels = np.array(time_players)

    ax3.set_title('Players total time played in seconds',fontdict=font6)

    ax3.pie(y,labels = mylabels,startangle = 90,shadow = True,colors = colors,autopct=your_autopct_format,textprops=font5)
    ax3.legend(title = "Players:",loc = 4)

    canvas3 = FigureCanvasTkAgg(fig3,graph_frame)
    canvas3.draw()
    canvas3.get_tk_widget().pack(pady = 30)
    canvases.append(canvas3)

    names = []
    times = []

    try:
        conn.execute('''SELECT name, count(player_id) FROM `info` inner join players on info.player_id = players.id group by player_id''')
        for row in conn:
            names.append(row[0])
            times.append(row[1])
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Could not get scores. {e}')
        print(e)

    names = np.array(names)
    times = np.array(times)

    fig4, ax4 = plt.subplots()
    ax4.set_title('Played times for each player',fontdict=font6)
    ax4.set_xlabel('Times',fontdict=font5)
    ax4.barh(names,times,color = '#088026',height=0.4)

    canvas4 = FigureCanvasTkAgg(fig4,graph_frame)
    canvas4.draw()
    canvas4.get_tk_widget().pack(pady = 10)
    canvases.append(canvas4)

    score_names = []
    max_scores = []
    min_scores = []

    try:
        conn.execute('''SELECT name, max(score),min(score) FROM `info` inner join players on info.player_id = players.id group by player_id''')
        for row in conn:
            score_names.append(row[0])
            max_scores.append(row[1])
            min_scores.append(row[2])
        connection.commit()
    except Error as e:
        messagebox.showerror('',f'Could not get scores. {e}')
        print(e)

    fig5, ax5 = plt.subplots()

    ax5.set_title('Max, min scored points in one game',fontdict=font6)
    ax5.set_xlabel("Players' Names", fontdict=font4)
    ax5.set_ylabel('Scores',fontdict=font4)
    ax5.grid(axis='y')
    ax5.scatter(score_names,max_scores,color = "#1105b3",s=60)
    ax5.scatter(score_names,min_scores,color = "#f50599",s = 60)
    ax5.legend(title = 'States',labels = ['max','min'],loc = 9)

    canvas5 = FigureCanvasTkAgg(fig5,graph_frame)
    canvas5.draw()
    canvas5.get_tk_widget().pack(pady = 30)
    canvases.append(canvas5)

    fig6, ax6 = plt.subplots()

    ax6.set_title('Players progress',fontdict=font6)
    ax6.set_xlabel('Times', fontdict=font4)
    ax6.set_ylabel("Players' points",fontdict=font4)
    ax6.grid()
    for name in players:
        line(name)
    ax6.legend(title = 'Players by colors',labels = players,loc = 5)

    canvas6 = FigureCanvasTkAgg(fig6,graph_frame)
    canvas6.draw()
    canvas6.get_tk_widget().pack(pady = 10)
    canvases.append(canvas6)

    my_canvas.create_window((300,400), window = capital_frame)
    my_canvas.create_window((200,700), window = stat_frame)
    my_canvas.create_window((300,2550), window = graph_frame)
    my_canvas.create_window((300,4200), window = end_frame)

    mainloop()

def main_menu():
    global musicList
    global currentIndex
    global volume
    global if_play
    
    while True:
        SCREEN.blit(BG, (0, 0))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("TETRIS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(s_width // 2, 100))
        
        button_rect = pygame.image.load("assets/Play Rect.png")
        button_rect = pygame.transform.scale(button_rect,(250,80))

        PLAY_BUTTON = Buttons(image=button_rect, pos=(s_width // 2, s_height // 2 - 130), text_input="PLAY", font=get_font(24), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Buttons(image=button_rect, pos=(s_width // 2, (s_height // 2) - 30), text_input="OPTIONS", font=get_font(24), base_color="#d7fcd4", hovering_color="White")
        HIS_BUTTON = Buttons(image=button_rect, pos=(s_width // 2, (s_height // 2) + 70), text_input="HISTORY", font=get_font(24), base_color="#d7fcd4", hovering_color="White")
        STATS_BUTTON = Buttons(image=button_rect, pos=(s_width // 2, (s_height // 2) + 170), text_input="STATS", font=get_font(24), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Buttons(image=button_rect, pos=(s_width // 2, (s_height // 2) + 270), text_input="QUIT", font=get_font(24), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON,HIS_BUTTON,STATS_BUTTON,QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_name(if_play,volume,musicList[currentIndex],expPlay,losePlay,changePlay)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if HIS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    history()
                if  STATS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    stats()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()

main_menu()