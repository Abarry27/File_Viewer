"""
User must use Python 3.9.12 or lower as some imported modules aren't compatable with newer Python versions.
"""
from cgitb import text
from distutils import text_file
from select import select
from textwrap import fill
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from turtle import bgcolor
import PyPDF2
import os, sys
import win32print
import win32api


global open_status
open_status = False


root = Tk()
root.title("PDF Editor")
root.geometry("1200x650")

tool_bar_frame = Frame(root)
tool_bar_frame.pack(fill=X)

#Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)



#Scroll Bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

new_font = ['Biome', 14, 'normal']

#Text Box
my_text = Text(my_frame, height = 50, width=140, font=(new_font), selectbackground="grey", bd=5, relief=GROOVE, undo = True, yscrollcommand=text_scroll.set, wrap = None)
my_text.pack()

#Scroll Bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)


#Horizontal Bar(May need a little fixing up)
horizontal_bar = Scrollbar(my_frame, orient='horizontal')
horizontal_bar.pack(side=BOTTOM, fill = X)

#Configure Scroll Bar
text_scroll.config(command=my_text.yview)


#Canvas
#canvas = Canvas(root, bg='red')
#canvas.pack(fill=BOTH, anchor=NW)


#New File Function
def new_file():
    my_text.delete(1.0, END)
    root.title('New File')
    global open_status
    open_status = False

# Open File Function
def open_file():
    my_text.delete("1.0", END)
    
    text_file = filedialog.askopenfilename(initialdir="C:/Desktop/", 
    title="Open File", 
    filetypes=( 
    ("Text Files", "*.txt"),
    ("All Files", "*.*")))
    
    
    
    """
    PDF file open code. Text files are used for testing reasons to test different functionallty.
    """
    
    #if text_file:
        #pdf_file = PyPDF2.PdfFileReader(text_file)
        #page = pdf_file.getPage(0)
        #page_content = page.extractText()
        #my_text.insert(1.0, page_content)
        #global open_status
        #open_status = text_file

    #Open File
    text_file = open(text_file, 'r')
    file_text = text_file.read()
    my_text.insert(END, file_text)
    text_file.close()

# Save File Function
def save_file():
    global open_status
    if open_status:
        text_file = open(open_status, 'w')
        text.file.write(my_text.get(1.0, END))
        #Close File
        text_file.close()
    else:
        save_file_as()    


# Save File As Function
def save_file_as():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Desktop/", title = "Save File", filetypes=(("Text Files ", "*.txt")))
    if text_file:
        name = text_file
        name = name.replace("C:/Desktop/", "")
        #Save File
        text_file = open(text_file, 'w')
        text.file.write(my_text.get(1.0, END))
        #Close File
        text_file.close()


#Cut Function
def cut_text(e):
    global selected
    #Check to see if shortcut keys were used.
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)



def copy_text(e):
    global selected
    #Check to see if shortcut keys were used.
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)



#Paste Function
def paste_text(e):
    global selected
    #Check to see if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)

#Bold Text Function
def bold_it():
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")


    #Configure Tag
    my_text.tag_configure("bold", font=bold_font)
    current_tags = my_text.tag_names("sel.first")

    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")    


#Italic Font Function
def italic_it():
    italic_font = font.Font(my_text, my_text.cget("font"))
    italic_font.configure(slant="italic")


    #Configure Tag
    my_text.tag_configure("italic", font=italic_font)
    current_tags = my_text.tag_names("sel.first")

    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")    
    
#Change Text Color Font Function
def text_color():
    color_font = font.Font(my_text, my_text.cget("font")) 
    my_color = colorchooser.askcolor()[1]
    


    #Configure Tag
    my_text.tag_configure("colored", font=color_font, foreground=my_color)
    current_tags = my_text.tag_names("sel.first")

    if "colored" in current_tags:
        my_text.tag_remove("colored", "sel.first", "sel.last")
    else:
        my_text.tag_add("colored", "sel.first", "sel.last")
    

def print_file():
    printer_name = win32print.GetDefaultPrinter()
    
    file_to_print = filedialog.askopenfilename(defaultextension=".*", initialdir="C:/Desktop/", title = "Save File", filetypes=(("PDF Files", "*.pdf"), ("Text Files ", "*.txt")))

    if file_to_print:
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)


#Zoom In And Out Function
def zoom_in_and_out(str1):
    if str1 == "plus":
        new_font[1] = new_font[1] + 1
    else:
        new_font[1] = new_font[1] - 1
    my_text.config(font=new_font)
        

"""
When drawing lines a canvas is needed to draw. A text box doesn't allow you to draw.
"""

#Draw Lines on Canvas(TODO)
#def x_and_y(event):
    #global lastx, lasty
    #lastx, lasty = event.x, event.y



#def draw_lines(event):
    #global lastx, lasty
    #canvas.create_line(lastx, lasty, event.x, event.y, fill='blue')
    #lastx, lasty = event.x, event.y


#canvas.bind("<Button-1>", x_and_y)
#canvas.bind("<B1-Motion>", draw_lines)  


#Menu
my_menu = Menu(root)
root.config(menu=my_menu)


#Bold Button

bold_button = Button(tool_bar_frame, text='BOLD', bd=1, bg='dark grey', font='Arial', command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=30)


#Italic Button
italic_button = Button(tool_bar_frame, text='ITALIC', bd=1, bg='dark grey', font='Arial', command=italic_it)
italic_button.grid(row=0, column=1, padx= 30 )

#Undo Button
undo_button = Button(tool_bar_frame, text='UNDO', bd=1, bg='dark grey', font='Arial', command=my_text.edit_undo)
undo_button.grid(row=0, column=2, sticky=W, padx=30)

#Redo Button
redo_button = Button(tool_bar_frame, text='REDO', bd=1, bg='dark grey', font='Arial', command=my_text.edit_redo)
redo_button.grid(row=0, column=3, sticky=W, padx=30)

#Text Color Button
color_text_button = Button(tool_bar_frame, text="TEXT COLOR", bd=1, bg='dark grey', font='Arial', command = text_color)
color_text_button.grid(row=0, column=4, sticky=W, padx = 30)

#Zoom In Button
zoom_in_button = Button(tool_bar_frame, text="ZOOM IN +", bd=1, bg='dark grey', font='Arial', command = lambda: zoom_in_and_out("plus"))
zoom_in_button.grid(row = 0, column=5, sticky=W, padx=30)

#Zoom Out Button
zoom_out_button = Button(tool_bar_frame, text="ZOOM OUT -", bd=1, bg='dark grey', font='Arial', command = lambda: zoom_in_and_out("minus"))
zoom_out_button.grid(row = 0, column=6, sticky=W, padx=30)




#Add File Menu
file_menu = Menu(my_menu, tearoff=False, bd=10)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_separator()
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save", command = save_file)
file_menu.add_separator()
file_menu.add_command(label="Save As", command = save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Print", command = print_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)



#Edit Menu
edit_menu =Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut | Ctrl+x", command=lambda: cut_text(False))
edit_menu.add_command(label="Copy | Ctrl+c",command=lambda: copy_text(False))
edit_menu.add_command(label="Paste | Ctrl+v",command=lambda: paste_text(False))
edit_menu.add_separator()
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")


#Edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)







#Main Loop
root.mainloop()