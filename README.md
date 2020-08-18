# Salome-Kratos-Plugin

                                    

[![alt text](logo.png "Salome-Kratos Plugin")](https://www.youtube.com/watch?v=Itn004yjfhU&feature=youtu.be)

Click on the picture to watch a demo on how to use the plug-in

This project is about creating a plugin for Kratos Mutiphysics in Salome.

## Requirements:
 - Salome 8.2 or higher.
 

## Objectives:
- * [x] Export meshes from Salome in Kratos format
- * [x] Apply boundary conditions and loads
- * [ ] Save the status and reload it


## Setting it up:
- register the directory of the plugin via the SALOME_PLUGINS_PATH system variable or,
- put everything inside the following salome-directory:
- (e.g Salome 8.2 on win64): \SALOME-8.2.0-WIN64\MODULES\GUI\RELEASE\GUI_INSTALL\share\salome\plugins\gui\
- (e.g Salome 8.3.0 on Ubuntu 16.04): ~/Desktop/SALOME-8.3.0-UB16.04/BINARIES-UB16.04/GUI/share/salome/plugins/gui

## Usage:
- You can open your hdf file in Salome or create a new mesh.
- Inside the 'Mesh'-module of Salome, the plugin is accessable via the 'Tools'-menu.

## Reference to check out:
- https://github.com/physici/ElmerSalomeModule

## Tests can be run with (in the top-directory)

`python3 -m pytest`