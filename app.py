import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from movie import Movie
from watchlist import Watchlist
import csv


app = customtkinter.CTk()
app.title('LettnorboxD')
app.geometry('1500x500')
app.config(bg='#161C25')
app.resizable(False, False)

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 12, 'bold')

def get_next_movie_id():
    movies = watchlist.view_movies()
    if not movies:
        return 1
    return max([movie.movie_id for movie in movies]) + 1

def newCtkLabel(text='CTK Label'):
    widget_Font = font1
    widget_TextColor = '#FFF'
    widget_BgColor = '#161C25'

    widget = customtkinter.CTkLabel(app,
                                  text=text,
                                  font=widget_Font,
                                  text_color=widget_TextColor,
                                  bg_color=widget_BgColor)
    return widget

def newCtkEntry(text='CTK Label'):
    widget_Font = font1
    widget_TextColor = '#000'
    widget_FgColor = '#FFF'
    widget_BorderColor = '#0C9295'
    widget_BorderWidth = 2
    widget_Width = 250

    widget = customtkinter.CTkEntry(app,
                                  font=widget_Font,
                                  text_color=widget_TextColor,
                                  fg_color=widget_FgColor,
                                  border_color=widget_BorderColor,
                                  border_width=widget_BorderWidth,
                                  width=widget_Width)
    return widget

def newCtkComboBox(options=['DEFAULT', 'OTHER'], entryVariable=None):
    widget_Font = font1
    widget_TextColor = '#000'
    widget_FgColor = '#FFF'
    widget_DropdownHoverColor = '#0C9295'
    widget_ButtonColor = '#0C9295'
    widget_ButtonHoverColor = '#0C9295'
    widget_BorderColor = '#0C9295'
    widget_BorderWidth = 2
    widget_Width = 250
    widget_Options = options

    widget = customtkinter.CTkComboBox(app,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    width=widget_Width,
                                    variable=entryVariable,
                                    values=options,
                                    state='readonly')
    
    widget.set(options[0])

    return widget

def newCtkButton(text='CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
    widget_Font = font1
    widget_TextColor = '#FFF'
    widget_FgColor = fgColor
    widget_HoverColor = hoverColor
    widget_BackgroundColor = bgColor
    widget_BorderColor = borderColor
    widget_BorderWidth = 2
    widget_Cursor = 'hand2'
    widget_CornerRadius = 15
    widget_Width = 260
    widget_Function = onClickHandler

    widget = customtkinter.CTkButton(app,
                                    text=text,
                                    command=widget_Function,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    hover_color=widget_HoverColor,
                                    bg_color=widget_BackgroundColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    cursor=widget_Cursor,
                                    corner_radius=widget_CornerRadius,
                                    width=widget_Width)
    return widget


def add_to_treeview():
    movies = watchlist.view_movies()
    tree.delete(*tree.get_children())
    for movie in movies:
        tree.insert('', END, values=(movie.movie_id, movie.title, movie.genre, movie.year, movie.rating, movie.comments))


def clear_form(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    title_entry.delete(0, END)
    genre_entry.delete(0, END)
    year_entry.delete(0, END)
    rating_entry.delete(0, END)
    comments_entry.delete(0, END)

def read_display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear_form()
        title_entry.insert(0, row[1])
        genre_entry.insert(0, row[2])
        year_entry.insert(0, row[3])
        rating_entry.insert(0, row[4])
        comments_entry.insert(0, row[5])
    else:
        pass
    
    return None    

def add_entry():
    title = title_entry.get()
    genre = genre_entry.get()
    year = year_entry.get()
    rating = rating_entry.get()
    comments = comments_entry.get()

    if not (title and genre and year and rating and comments):
        messagebox.showerror('Error', 'Enter all fields.')
    if not year.isdigit():
        return messagebox.showerror('Error', 'Year must be a number!')
    if not rating.replace('.', '', 1).isdigit() or float(rating) < 1 or float(rating) > 5:
        messagebox.showerror('Error', 'Rating must be a valid number between 1 and 5!')
        return
    else:
        movie_id = get_next_movie_id()
        movie = Movie(title, genre, int(year), rating, comments, movie_id)
        watchlist.add_movie(movie)
        add_to_treeview()
        clear_form()
        messagebox.showinfo('Success', 'Movie has been added.')


def delete_entry():
    selected_item = tree.focus()  
    if not selected_item:
        messagebox.showerror('Error', 'Choose a movie to delete') 
    else:
        movie_id = tree.item(selected_item)['values'][0]
    
        watchlist.delete_movie(movie_id)
        
        add_to_treeview()
        
        clear_form()
        messagebox.showinfo('Success', 'Movie has been deleted')

def update_entry():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a movie to update')
    else:
        row = tree.item(selected_item)['values']
        movie_id = row[0]
        
        title = title_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()
        rating = rating_entry.get()
        comments = comments_entry.get()

        if not (title and genre and year and rating and comments):
            messagebox.showerror('Error', 'Enter all fields.')
        if not year.isdigit():
            return messagebox.showerror('Error', 'Year must be a number!')
        if not rating.replace('.', '', 1).isdigit() or float(rating) < 1 or float(rating) > 5:
            messagebox.showerror('Error', 'Rating must be a valid number between 1 and 5!')
            return
        
        movie = Movie(title, genre, int(year), rating, comments, int(movie_id))
        
        watchlist.update_movie(movie)
        
        add_to_treeview()
        
        clear_form()
        messagebox.showinfo('Success', 'Movie has been updated')

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    movies = watchlist.view_movies()

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Title', 'Genre', 'Year', 'Rating', 'Comments'])

        for movie in movies:
            writer.writerow([movie.movie_id, movie.title, movie.genre, movie.year, movie.rating, movie.comments])

        print('Success', 'Movies have been exported successfully!')

def import_from_csv():

    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        for row in reader:
            if row: 
                movie_id, title, genre, year, rating, comments = row
                movie = Movie(title, genre, int(year), rating, comments, int(movie_id))
                watchlist.add_movie(movie)

    add_to_treeview()
    messagebox.showinfo('Success', 'Movies have been imported successfully!')

watchlist = Watchlist()

title_label = newCtkLabel('Title')
title_label.place(x=20, y=40)
title_entry = newCtkEntry()
title_entry.place(x=100, y=40)

genre_label = newCtkLabel('Genre')
genre_label.place(x=20, y=100)
genre_entry = newCtkEntry()
genre_entry.place(x=100, y=100)

year_label = newCtkLabel('Year')
year_label.place(x=20, y=160)
year_entry = newCtkEntry()
year_entry.place(x=100, y=160)

rating_label = newCtkLabel('Rating')
rating_label.place(x=20, y=220)
rating_entry = newCtkEntry()
rating_entry.place(x=100, y=220)

comments_label = newCtkLabel('Comments')
comments_label.place(x=20, y=280)
comments_entry = newCtkEntry()
comments_entry.place(x=130, y=280)

add_button = newCtkButton(text='Add Movie',
                          onClickHandler=add_entry,
                          fgColor='#05A312',
                          hoverColor='#00850B',
                          borderColor='#05A312')
add_button.place(x=50, y=331)

update_button = newCtkButton(text='Update Movie',
                             onClickHandler=update_entry)
update_button.place(x=50, y=400)

delete_button = newCtkButton(text='Delete Movie',
                            onClickHandler=delete_entry,
                            fgColor='#E40404',
                            hoverColor='#AE0000',
                            borderColor='#E40404')
delete_button.place(x=360, y=400)

export_button = newCtkButton(
    text='Export to CSV',
    onClickHandler=export_to_csv,
    fgColor='#0288D1',
    hoverColor='#0277BD',
    borderColor='#0288D1')
export_button.place(x=670, y=400)

import_button = newCtkButton(
    text='Import from CSV',
    onClickHandler=import_from_csv,
    fgColor='#0288D1',
    hoverColor='#0277BD',
    borderColor='#0288D1')
import_button.place(x=1000, y=400)

style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview',
                font=font2,
                foreground='#fff',
                background='#000',
                fieldlbackground='#313837')

style.map('Treeview', background=[('selected', '#1A8F2D')])

tree = ttk.Treeview(app, height=15)
tree['columns'] = ('ID', 'Title', 'Genre', 'Year', 'Rating', 'Comments')
tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', anchor=tk.CENTER, width=10)
tree.column('Title', anchor=tk.CENTER, width=150)
tree.column('Genre', anchor=tk.CENTER, width=150)
tree.column('Year', anchor=tk.CENTER, width=10)
tree.column('Rating', anchor=tk.CENTER, width=100)
tree.column('Comments', anchor=tk.CENTER, width=300)

tree.heading('ID', text='ID')
tree.heading('Title', text='Title')
tree.heading('Genre', text='Genre')
tree.heading('Year', text='Year')
tree.heading('Rating', text='Rating')
tree.heading('Comments', text='Comments')

tree.place(x=560, y=20, width=1200, height=400)

tree.bind('<ButtonRelease>', read_display_data)

add_to_treeview()


app.mainloop()
















