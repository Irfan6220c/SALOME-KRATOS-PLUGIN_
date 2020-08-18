try:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
except ImportError:
    from PyQt5 import QtWidgets as QtGui
    from PyQt5 import QtCore


from distutils import spawn

import salome_pluginsmanager as sp
import smesh
import salome
import sys
import os
import subprocess
import pdb
from global_utilities import DEBUG


def InMeshModule(context):
    active_module = context.sg.getActiveComponent()
    if active_module != "SMESH":
        QtGui.QMessageBox.about(None, str(active_module),
                                "Functionality is only provided in mesh module.")
        return False
    return True

# %% mesh creation
    
def TakeMesh(context):
    
    global sp, smesh, salome, subprocess, QtGui, pdb, spawn, myMesh

    # get active module and check if SMESH
    if InMeshModule(context):
        active_module = context.sg.getActiveComponent()

        exporting_submesh = False
        sub_mesh_shape = None

        # get selection
        selCount = sp.sg.SelectedCount()
        if selCount == 0:
            QtGui.QMessageBox.warning(None, str(active_module),
                                    "Nothing selected. Please select a mesh.")
            return
        # check if selection == mesh
        elif selCount > 1:
            QtGui.QMessageBox.warning(None, str(active_module),
                                    "More than one mesh selected. Please select only one mesh.")
            return
        else:
            objID = sp.sg.getSelected(0)
            salomeObj = sp.salome.myStudy.FindObjectID(objID)
            
            ref = salome.IDToObject(objID)
            if (DEBUG):
                print(ref)
            name = salomeObj.GetName()
    
            # With this you can see which methods are available
            # WARNING: It prints quite some output!
            #for method_name in dir(ref):
            #    print(method_name)

            try:
                myMesh = smesh.Mesh(ref)
            except AttributeError as e:
                try:
                    if (DEBUG):
                        print("it is a submesh:", e)
                    sub_mesh_shape = ref.GetSubShape()
                    exporting_submesh = True
                except AttributeError:
                    QtGui.QMessageBox.warning(None, str(active_module),
                                        "Selection is not a mesh.")
                    return

        
    return {"name": name,"myMesh": myMesh, "exporting_submesh": exporting_submesh, "sub_mesh_shape": sub_mesh_shape}
    
