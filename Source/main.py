from genericpath import exists
import reader
import tkinter as tk
import shutil
import os, sys
from tkinter import CENTER, filedialog as fd


collection = []
"""collection of the filepaths selected dependencies"""

button_color = '#363f6e'

root = tk.Tk()
root.iconbitmap("Icon.ico")
root.title("Godot packager")
root.geometry("400x250")
root.config(bg='#4e5782')

label_text = tk.StringVar()
label = tk.Label(root, textvariable=label_text, fg="#33e869", bg=button_color)

collection_var = tk.StringVar(value=collection)
collection_label = tk.Listbox(root, listvariable=collection_var, bg='#7f90b3', height=5, width=380)

project_text = tk.StringVar()

def find_root_folder(f):
    """searches the given path for the folder with a project.godot file"""
    root_path = ""
    #reader.REPLACEMENT_PATH = f + "/"
    #print(reader.REPLACEMENT_PATH)
    split_path = os.path.split(f)[0]
    while not exists(split_path+"/project.godot"):
        split_path = os.path.split(split_path)[0]
        print(split_path)
        if split_path == "D:/":
            break
    
    if exists(split_path+"/project.godot"):
        root_path = split_path
        print("root path: ", root_path)
    else:
        print("root path can't be found")
    return root_path
    

def import_scene():
    print("do import stuff")
    scene = fd.askopenfilename()
    print(scene)
    global collection
    
    if scene is None:
        return

    root_path = find_root_folder(scene)
    if root_path == "":
        return

    reader.REPLACEMENT_PATH = root_path + "/"

    collection += reader.collect_dependencies(scene)
    collection_var.set(collection)
    label_text.set("Collection was imported")
    export_button.config(state="normal")

    print("dependencies added to collection")

def transfer_files(target):
    
    #removes duplicate filepaths
    global collection
    collection = list(dict.fromkeys(collection))

    for File in collection:
        if exists(File):
            shutil.copy(File, target)
    
    
    label_text.set("Files were copied successfully")
    print("all files transferred successfully")
    clear_collection()

def export_scene():
    print("do export stuff")
    print(collection)

    target = fd.askdirectory()
    transfer_files(target)

def print_collection():
    print(collection)
    pass

def set_project_folder():
    f = fd.askdirectory()
    reader.REPLACEMENT_PATH = f + "/"
    print(reader.REPLACEMENT_PATH)

    if exists(reader.REPLACEMENT_PATH+"project.godot"):
        print(reader.REPLACEMENT_PATH)
        project_text.set(("folder: "+ f))
        import_button.config(state="active")
    else:
        label_text.set("Project.godot could not be found")
        import_button.config(state="disabled")

def clear_collection():
    collection.clear()
    collection_var.set(collection)
    label_text.set("Collection was cleared")
    export_button.config(state="disabled")

clear_button = tk.Button(root, text="Clear Collection", command=clear_collection, bg=button_color, fg='white')
#project_folder = tk.Button(root, text="root Folder", command=find_root_folder, bg=button_color, fg='white')
#project_label = tk.Label(root, textvariable=project_text, bg=button_color, fg='white')
import_button = tk.Button(root,anchor=CENTER, text="Import", command = import_scene, state="normal", bg=button_color, fg='white')
import_button.place(x=0, y=75)
export_button = tk.Button(root,anchor=CENTER, text="Export", command = export_scene, bg=button_color, fg='white', state="disabled", height=2, width=20)


# print_button = tk.Button(root, text="Export", command = print_collection)


clear_button.pack()
#project_folder.pack()
#project_label.pack()
import_button.pack()
collection_label.pack()
export_button.pack()
label.pack()
# print_button.pack()

root.mainloop()
root.quit()
