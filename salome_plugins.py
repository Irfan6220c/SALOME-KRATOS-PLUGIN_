# -*- coding: utf-8 -*-
"""
Plugin for KratosMultiphysics in Salome
author: Philipp Bucher
May 2018
"""

import salome_pluginsmanager
import logging
import sys, os



try:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
    logging.info("Using PyQt4")
    print("Using PyQt4")
except ImportError:
    from PyQt5 import QtWidgets as QtGui
    from PyQt5 import QtCore
    logging.info("Using PyQt5")
    print("Using PyQt5")

# %% setup
plugin_path = ""
# add SALOME_PLUGIN_PATH to Python environment for easier module import
if (os.environ.get("SALOME_PLUGINS_PATH") is not None):
    plugin_path = os.environ.get("SALOME_PLUGINS_PATH") +\
                  os.sep + "plugin"
if not (os.path.exists(plugin_path + os.sep + "kratos_window_manager.py")):
    import inspect
    plugin_path = os.path.dirname(inspect.getfile(inspect.currentframe())) +\
                  os.sep + "plugin"

sys.path.append(plugin_path)

if not (os.path.exists(plugin_path + os.sep + "kratos_window_manager.py")):
    sys.exit("No Kratos Plugin module found")

# import window handler
import kratos_window_manager as kratos_manager
import convert_to_kratos 
import assemble_json_files as ajf
from global_utilities import DEBUG

# global variable that will contain the Kratos-class and its memory-location
global main_window

# the environement variable is required to prevent the re-initialization
# of the Kratos-class each time the menu is opened, otherwise everything will
# be lost again,
# see http://www.salome-platform.org/forum/forum_12/575675631/639739196
if os.getenv("kratos_already_initialized", "0") != "1":
    main_window = kratos_manager.KratosWindowManager()

# ======================================================================================================
# this line enables interactive changing with salome
os.environ["kratos_already_initialized"] = "0" # TODO reenable this, but testing is easier this way!!!
#=======================================================================================================

widget = None

def KratosPlugin(context):
    """Creates a floating window in the foreground that allows access to the
    Kratos functionality the same way the Tools-menu does.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """
    global DEBUG
    
    if(DEBUG):
        print("KratosPlugin START")

    global QtGui, QtCore
    global widget

    global InGeometryModule, InMeshModule
    global ShowBoundaryConditions, ShowMaterials,About, SaveCase, LoadCase, WriteCalcFiles, ShowSolverSettings, export_mesh, convert_to_kratos

    convert_to_kratos.print_logo()
    
    # QWidget
    widget = QtGui.QWidget()
    widget.setWindowTitle('Kratos MultiPhysics')
    widget.setWindowFlags(widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

    # QPushButtons
    button_bcs = QtGui.QPushButton('Boundary Conditions', widget)
    button_materials = QtGui.QPushButton('Materials', widget)
    button_sol_settings = QtGui.QPushButton('Solver Settings', widget)
    button_write_calc_file = QtGui.QPushButton('Write Calculation Files', widget)
    button_save_case = QtGui.QPushButton('Save Case', widget)
    button_load_case = QtGui.QPushButton('Load Case', widget)
    button_about = QtGui.QPushButton('About', widget)

    # QPushButton-Events
    button_bcs.clicked.connect(lambda: ShowBoundaryConditions(context))
    button_about.clicked.connect(lambda: About(context))
    button_sol_settings.clicked.connect(lambda: ShowSolverSettings(context))
    button_write_calc_file.clicked.connect(lambda: WriteCalcFiles(context))
    button_save_case.clicked.connect(lambda: SaveCase(context))
    button_load_case.clicked.connect(lambda: LoadCase(context))
    button_materials.clicked.connect(lambda: ShowMaterials(context))


    layout = QtGui.QVBoxLayout()
    layout.addWidget(button_bcs)
    layout.addWidget(button_materials)
    layout.addWidget(button_sol_settings)
    layout.addWidget(button_write_calc_file)
    layout.addWidget(button_save_case)
    layout.addWidget(button_load_case)
    layout.addWidget(button_about)

    widget.setLayout(layout)

    widget.show()

    if(DEBUG):
        print("End\n\n")

def InGeometryModule(context):
    active_module = context.sg.getActiveComponent()
    if active_module != "GEOM":
        QtGui.QMessageBox.about(None, str(active_module),
                                "Functionality is only provided in geometry module.")
        return False
    return True

def InMeshModule(context):
    active_module = context.sg.getActiveComponent()
    if active_module != "SMESH":
        QtGui.QMessageBox.about(None, str(active_module),
                                "Functionality is only provided in mesh module.")
        return False
    return True

def ShowSolverSettings(context):
    """Shows the window for the solver settings.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """
    global main_window, QtGui
    # get active module and check if SMESH
    active_module = context.sg.getActiveComponent()
    if not InMeshModule(context):
        return

    main_window.showSolverSettings()

#%% define show boundary conditions Function
def ShowBoundaryConditions(context):
    """Defines Boundary Conidtions of the problem

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """

    global main_window, QtGui
    
    main_window.ShowBoundaryConditions(context)

def ShowMaterials(context):

    global main_window, QtGui

    main_window.showAddMaterial(context)

# %% define about Function
def About(context):
    """Shows an info dialog for the plugin. May contain additional information
    in the future.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """

    global main_window, QtGui

    if not InMeshModule(context):
        return

    title = "Kratos Multiphysics plugin for SALOME editor"
    msg = "Interface that allows setup of a Kratos simulation with the help of the Salome Mesh editor and generation of necessary sif-file.\n"
    msg1 = "The mesh is exported as *.unv and converted with ElmerGrid. ElmerSolver can be started in a single process or using multiprocessing.\n\n"
    msg2 = "by Philipp Bucher, 2018."
    QtGui.QMessageBox.about(None, title, msg + msg1 + msg2)
    return

# %% define about Function
def WriteCalcFiles(context):
    """Write the calculation files for Kratos

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """

    global main_window, QtGui,ajf,DEBUG

    if not InMeshModule(context):
        return
    root_path = main_window.exportDat()
    p_parameters_dict = ajf.AssembleProjectParametersJson(main_window,root_path)
    materials_dict = ajf.AssembleStructuralMaterialsJson(main_window)
    
    ajf.WriteMainKratosFromDefaults(root_path["path"])
    ajf.WriteProjectParametersjson(root_path["path"],p_parameters_dict)
    ajf.WriteStructuralMaterialsjson(root_path["path"],materials_dict)
    convert_to_kratos.write_mdpa_file( root_path["mdpa_name"], root_path["path"], main_window.boundaryConditionEditor)
    if(DEBUG):
        print("name of mdpa file : ", root_path["mdpa_name"])
        print("files path : ", root_path["path"])
    return


# %% define about Function
def SaveCase(context):
    """Saves the entire configuration (Salome and Kratos files)

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """

    global main_window, QtGui

    title = "Kratos Multiphysics plugin for SALOME editor"
    msg = "This functionality is not yet implemented"
    QtGui.QMessageBox.about(None, title, msg)
    return



# %% define about Function
def LoadCase(context):
    """Loads the entire configuration (Salome and Kratos files)
    in the future.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """

    global main_window, QtGui

    title = "Kratos Multiphysics plugin for SALOME editor"
    msg = "This functionality is not yet implemented"
    QtGui.QMessageBox.about(None, title, msg)
    return


salome_pluginsmanager.AddFunction('Kratos Multiphysics',
                                  'Starts the Kratos plugin',
                                  KratosPlugin)
