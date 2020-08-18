try:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
except ImportError:
    from PyQt5 import QtWidgets as QtGui
    from PyQt5 import QtCore
    
from global_utilities import DEBUG


from distutils import spawn
import os

def InMeshModule(context):
    active_module = context.sg.getActiveComponent()
    if active_module != "SMESH":
        QtGui.QMessageBox.about(None, str(active_module),
                                "Functionality is only provided in mesh module.")
        return False
    return True

# %% mesh creation
def SaveFilesPath():
    title = 'Select file'
    fname = QtGui.QFileDialog.getSaveFileName(parent=None, caption=title,
                                                    filter='Calculation files')
    # Salome 8.2 behavior
    if isinstance(fname, tuple):
        fname = fname[0]

    # pdb.set_trace()
    # call to Kratos for converting the mesh into dat file
    if fname:
        fname = os.path.normpath(str(fname))
        path = os.path.dirname(fname)
        name_file = os.path.basename(fname)
    if os.path.exists(fname):
        os.remove(fname)
        
    return {"mdpa_name" : name_file, "path" : path}

def ExportMesh(mesh_dict, path_dict):
    global sp, smesh, salome, subprocess, QtGui, pdb, spawn, myMesh
    
    if mesh_dict["exporting_submesh"]:
        mesh_dict["myMesh"].ExportDAT(path_dict["path"] + os.sep + mesh_dict["name"] + '.dat', mesh_dict["myMesh"].GetSubMesh(mesh_dict["sub_mesh_shape"], mesh_dict["name"]))
    else:
        
        mesh_dict["myMesh"].ExportDAT(path_dict["path"] + os.sep + mesh_dict["name"] + '.dat')
        if (DEBUG):
            print("Export Successful!")  
