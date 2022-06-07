from dataclasses import replace
from os.path import exists
import re
from tokenize import String

# f = open("debuging\World.tscn", "r")

# txt = f.read()
# f.close()

replacement_path = 'D:\Gravity Falls Game\\'


#returns the dependencies with their full path
def get_dependencies_path(txt_file):
    """searches for dependencies in tscn and tres files. DOESN'T Work in Gd files, for that use get_dependencies_path_gd"""
    ext_block = re.findall("ext_resource.*]", txt_file)
    ext_block = "\n".join(ext_block)
    expression_tscn = 'res:.*tscn'                  #(ext_resource.*)(tscn|gd|png)
    expression_gd = 'res:.*gd'
    expression_png = 'res:.*png'
    expression_mp4 = 'res:.*mp4'
    expression_shader = 'res:.*shader'
    dependencies = re.findall(expression_tscn, ext_block)
    dependencies += re.findall(expression_gd, ext_block)
    dependencies += re.findall(expression_png, ext_block)
    dependencies += re.findall(expression_mp4, ext_block)
    dependencies += re.findall(expression_shader, ext_block)

    actual_path = []

    #need to replace the godot file path with actual windows filepath
    for i in dependencies:
        actual_path.append(i.replace("res://", replacement_path))


    return actual_path

def get_dependencies_path_gd(txt_file):
    """searches for dependencies in gd files"""

    expression_tscn = 'res:.*tscn'                  #(ext_resource.*)(tscn|gd|png)
    expression_gd = 'res:.*gd'
    expression_png = 'res:.*png'
    expression_mp4 = 'res:.*mp4'
    expression_shader = 'res:.*shader'
    dependencies = re.findall(expression_tscn, txt_file)
    dependencies += re.findall(expression_gd, txt_file)
    dependencies += re.findall(expression_png, txt_file)
    dependencies += re.findall(expression_mp4, txt_file)
    dependencies += re.findall(expression_shader, txt_file)

    actual_path = []

    #need to replace the godot file path with actual windows filepath
    for i in dependencies:
        actual_path.append(i.replace("res://", replacement_path))


    return actual_path

    pass

def collect_dependencies(scene_path):
    """reads a tscn or gd file for external dependencies and then returns a list with all dependencies filepaths"""
    

    #print("read ", scene_path)
    if not exists(scene_path) or "png" in scene_path or "shader" in scene_path or "mp4" in scene_path:
        return
        
    sub_dependencies = []
    all_paths = []
    #first read the scene path to extract required dependencies
    f = open(scene_path, "r")
    txt = f.read()
    f.close()
    
    if ".gd" in scene_path:
        dependencies = get_dependencies_path_gd(txt)
    else:
        dependencies = get_dependencies_path(txt)
    for i in dependencies:
        if collect_dependencies(i) is not None:

            if i not in sub_dependencies:
                sub_dependencies += collect_dependencies(i)

    all_paths.append(scene_path)
    all_paths += dependencies
    all_paths += sub_dependencies

    all_paths = list(dict.fromkeys(all_paths))
    return all_paths