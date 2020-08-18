# -*- coding: utf-8 -*-
"""
AFEM PROJECT: Salome-Kratos Plugin 2018 Summer Semester


Main class for Kratos plugin functionality
"""
qt4 = False
try:
    from PyQt4 import QtGui
    from PyQt4 import QtXml
    from PyQt4 import QtCore
    qt4 = True
except ImportError:
    from PyQt5 import QtWidgets as QtGui
    from PyQt5 import QtXml
    from PyQt5 import QtCore

import sys
from convert_to_kratos import TWO_D, THREE_D, creat_mesh_dict, find_element_type, write_mdpa_file
from global_utilities import LOAD_PROCESS_POINT_LOAD,LOAD_PROCESS_SURFACE_LOAD,LOAD_PROCESS_POSITIVE_FACE_PRESSURE, CONSTRAINT_PROCESS,DEBUG
global TWO_D, THREE_D, LOAD_PROCESS_POINT_LOAD,LOAD_PROCESS_SURFACE_LOAD,LOAD_PROCESS_POSITIVE_FACE_PRESSURE, CONSTRAINT_PROCESS
import take_mesh
import export_mesh_function as em

    
import os
import os.path
import sys
import glob
import tempfile

from xml.etree import ElementTree as et

import pdb

path = os.path.dirname(os.path.abspath(__file__))
path_forms = path + os.sep + "forms" + os.sep
path_edfs = path + os.sep + "edf" + os.sep

main = None


class KratosWindowManager(object):
    def __init__(self):
        """Constructor"""
        self.meshDirectory = ''
        self.smp_path_dict = {}
        self.boundaryConditionEditor = []  
        self.is2D = False 
        self.elementProperties = {}  
        self.MatSave = {"YOUNG_MODULUS":206900000000.0,"POISSON_RATIO":0.29,"I33":1.0,"DENSITY":7850.0,"CROSS_AREA":1.0}
        self.SSsave = {"solver_type":"Static","echo_level":1.0,"analysis_type":"linear", "max_iteration":1e+1,"residual_absolute_tolerance":1.0}
        self._ProcessesBcWindow=None
        self._solverSet = None
        self._matWindow = None
        self._bcWindow = None
        self._bc_count=0
        self._parent = self

        self.dynamicEditorReady = QtCore.pyqtSignal(int, 
                                           name="dynamicEditorReady")
   

    def showAddBoundaryCondition(self, visible=True):
        """Show Boundary conditions settings window
        
        Return:
        -------
        _bcWindow: QtWidget
            QtWidget with listview and boundary settings section
        """
        
        ## When the saving time arrived, the objects will be again checked and updated !

        if not self._bcWindow:
            # Boundary Conditions General Windows
            self._bcWindow = QtGui.QWidget()
            layout = QtGui.QHBoxLayout()
            
            if(DEBUG):
                print("Boundary Conditions Windows is on")
            self._bcWindow.setGeometry(100,100,600,280)
            self._bcWindow.setWindowTitle("Boundary Conditions")
            self._bcWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


            # Buttons:
            # New BC
            self.NewBcBtn = QtGui.QPushButton("&New", self._bcWindow)
            # Delete BC
            self.DeleteBcBtn = QtGui.QPushButton("&Delete", self._bcWindow)

            # Boundary Conditions List
            self.BCList = QtGui.QListWidget(self._bcWindow)           

            # Name Text Box
            self.NameLabel = QtGui.QLabel('Name',self._bcWindow)
            self.NameBox = QtGui.QLineEdit(self._bcWindow)

            # Select DimensionType
            self.SelectDimensionType = QtGui.QLabel('Dimension Type',self._bcWindow)      
            self.DimensionType = QtGui.QComboBox(self._bcWindow)
            self.DimensionType.addItem('2D')
            self.DimensionType.addItem('3D')           

            # Select Entity
            self.SelectLabel = QtGui.QLabel('Entity',self._bcWindow)  
            self.FaceBtn = QtGui.QPushButton("Select Entity", self._bcWindow)

            # Select Entity Type
            self.SelectEntType = QtGui.QLabel('Entity Type',self._bcWindow)      
            self.EntTypeCB = QtGui.QComboBox(self._bcWindow)
            self.EntTypeCB.addItem('Element')
            self.EntTypeCB.addItem('Condition')

            # Select BC Type 
            self.BctypeText = QtGui.QLabel('Name of Entity',self._bcWindow)    
            self.Bctype = QtGui.QComboBox(self._bcWindow)

            # Property ID
            self.ProperIDText = QtGui.QLabel('Property ID:',self._bcWindow)
            self.PropertyIDBox = QtGui.QLineEdit(self._bcWindow)
            self.PropertyIDBox.setReadOnly(True)

            # Save Button
            self.SaveExitBtn = QtGui.QPushButton("&Save", self._bcWindow)

            # Ok Button
            self.OkBtn = QtGui.QPushButton("&Ok", self._bcWindow)                 

            #Button Layout
            buttonLayout = QtGui.QHBoxLayout()
            buttonLayout.addWidget(self.NewBcBtn)
            buttonLayout.addWidget(self.DeleteBcBtn)            
            buttonLayout.addWidget(self.SaveExitBtn)
            buttonLayout.addWidget(self.OkBtn)            
            
            # Name Layout
            nameLayout = QtGui.QHBoxLayout()
            nameLayout.addWidget(self.NameLabel)
            nameLayout.addWidget(self.NameBox)
            
            # entityLayout Layout
            entityLayout = QtGui.QHBoxLayout()
            entityLayout.addWidget(self.SelectLabel)
            entityLayout.addWidget(self.FaceBtn)

            # entityType Layout Layout   
            entityTypeLayout = QtGui.QHBoxLayout()
            entityTypeLayout.addWidget(self.SelectEntType)
            entityTypeLayout.addWidget(self.EntTypeCB)
            # BcType LAyout
            bcTypeLayout = QtGui.QHBoxLayout()
            bcTypeLayout.addWidget(self.BctypeText)
            bcTypeLayout.addWidget(self.Bctype)

            # propertyLayout
            propertyLayout = QtGui.QHBoxLayout()
            propertyLayout.addWidget(self.ProperIDText, stretch = 5)
            propertyLayout.addWidget(self.PropertyIDBox)
            # sublayout
            sublayout = QtGui.QVBoxLayout()
            sublayout.addLayout(nameLayout)
            sublayout.addLayout(entityLayout)
            sublayout.addLayout(entityTypeLayout)
            sublayout.addLayout(bcTypeLayout)
            sublayout.addLayout(propertyLayout)
            sublayout.addLayout(buttonLayout)

            layout.addWidget(self.BCList)
            layout.addLayout(sublayout)       

            self._bcWindow.setLayout(layout)

            # signals
            self.BCList.currentItemChanged.connect(self.BCitemChanged)
            self.OkBtn.clicked.connect(self.okBC)
            self.NewBcBtn.clicked.connect(self.newBC)
            self.SaveExitBtn.clicked.connect(self.saveBC)
            self.DeleteBcBtn.clicked.connect(self.deleteBC)
            
            self.newBC()
         
            if visible:
                self._bcWindow.show()
        else:
            if visible:
                self._bcWindow.show()

        return self._bcWindow
    
    def showAddMaterial(self, visible=True):
        """Show Boundary conditions settings window
        
        Return:
        -------
        _matWindow: QtWidget
            QtWidget with listview and boundary settings section
        """
        
        ## When the saving time arrived, the objects will be again checked and updated !
        if(DEBUG):
            print('materials open')
        if not self._matWindow:
            # Boundary Conditions General Windows
            self._matWindow = QtGui.QWidget()
            layout = QtGui.QHBoxLayout()
            if(DEBUG):
                print("Materials Windows is on")
            self._matWindow.setGeometry(100,100,400,280)
            self._matWindow.setWindowTitle("Materials")
            self._matWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


            # Buttons:

            # Young Modulus Text Box
            self.YoungLabel = QtGui.QLabel('Young Modulus',self._matWindow)
            self.YoungBox = QtGui.QLineEdit(self._matWindow)

            # density  Text Box
            self.densityLabel = QtGui.QLabel('Density',self._matWindow)
            self.densityBox = QtGui.QLineEdit(self._matWindow)
            # poisson Text Box
            self.poissonLabel = QtGui.QLabel('Poisson',self._matWindow)
            self.poissonBox = QtGui.QLineEdit(self._matWindow)
            # Inertia Text Box
            self.InertiaLabel = QtGui.QLabel('Inertia',self._matWindow)
            self.InertiaBox = QtGui.QLineEdit(self._matWindow)
            # Cross Area Text Box
            self.CrossLabel = QtGui.QLabel('Cross Area',self._matWindow)
            self.CrossBox = QtGui.QLineEdit(self._matWindow)
            #Thickness
            self.ThicknessLabel = QtGui.QLabel('Thickness',self._matWindow)
            self.ThicknessBox = QtGui.QLineEdit(self._matWindow)

            # Save Button #isime dikkat et, bc ile cakismasin.
            self.SaveExitBtn = QtGui.QPushButton("&Save", self._matWindow)

            # Ok Button #isime dikkat et, bc ile cakismasin.
            self.OkBtn = QtGui.QPushButton("&Ok", self._matWindow)     

            #Button Layout
            buttonLayout = QtGui.QHBoxLayout()
            
            buttonLayout.addWidget(self.SaveExitBtn)
            buttonLayout.addWidget(self.OkBtn)            
            # Name Layout
            youngLayout = QtGui.QHBoxLayout()
            youngLayout.addWidget(self.YoungLabel)
            youngLayout.addWidget(self.YoungBox, stretch=5)
            # Name Layout
            densityLayout = QtGui.QHBoxLayout()
            densityLayout.addWidget(self.densityLabel)
            densityLayout.addWidget(self.densityBox)
            # Name Layout
            poissonLayout = QtGui.QHBoxLayout()
            poissonLayout.addWidget(self.poissonLabel)
            poissonLayout.addWidget(self.poissonBox)
            # Name Layout
            InertiaLayout = QtGui.QHBoxLayout()
            InertiaLayout.addWidget(self.InertiaLabel)
            InertiaLayout.addWidget(self.InertiaBox)
                        # Name Layout
            crossLayout = QtGui.QHBoxLayout()
            crossLayout.addWidget(self.CrossLabel)
            crossLayout.addWidget(self.CrossBox)

            #name layout
            thicknessLayout = QtGui.QHBoxLayout()
            thicknessLayout.addWidget(self.ThicknessLabel)
            thicknessLayout.addWidget(self.ThicknessBox, stretch=5)

            # sublayout
            sublayout = QtGui.QVBoxLayout()
            sublayout.addLayout(youngLayout)
            sublayout.addLayout(densityLayout)
            sublayout.addLayout(poissonLayout)
            sublayout.addLayout(InertiaLayout)
            sublayout.addLayout(crossLayout)
            sublayout.addLayout(thicknessLayout)
            sublayout.addLayout(buttonLayout)

            layout.addLayout(sublayout)       

            self._matWindow.setLayout(layout)

            # signals
            self.OkBtn.clicked.connect(self.okMat)
            self.SaveExitBtn.clicked.connect(self.saveMat)
            
         
            if visible:
                self._matWindow.show()
        else:
            if visible:
                self._matWindow.show()

        return self._matWindow

    def showSolverSettings(self, visible=True):
        """Show Boundary conditions settings window
        
        Return:
        -------
        _matWindow: QtWidget
            QtWidget with listview and boundary settings section
        """
        
        ## When the saving time arrived, the objects will be again checked and updated !
        if(DEBUG):
            print('Solver settings open')
        if not self._solverSet:
            # Boundary Conditions General Windows
            self._solverSet = QtGui.QWidget()
            layout = QtGui.QHBoxLayout()
            
            self._solverSet.setGeometry(100,100,400,280)
            self._solverSet.setWindowTitle("SolverSettings")
            self._solverSet.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
  
            # Buttons:

            # Solver Type Text Box
            self.SolverTypeLabel = QtGui.QLabel('Solver Type',self._solverSet)
            self.SolverCB = QtGui.QComboBox(self._solverSet)
            self.SolverCB.addItem('Static')
            # Add here
            self.SolverCB.addItem('Add here')
            self.SolverCB.addItem('Add here')
            self.SolverCB.addItem('Add here')

            #RotationDOFs
            self.RotationDOFsLabel = QtGui.QLabel('Rotation Dofs',self._solverSet)
            self.RotationDOFsCB = QtGui.QComboBox(self._solverSet)
            self.RotationDOFsCB.addItem('True')
            self.RotationDOFsCB.addItem('False')



            #ModelPartName
            self.ModelPartNameLabel = QtGui.QLabel('Model Part Name',self._solverSet)
            self.ModelPartNameCB = QtGui.QComboBox(self._solverSet)
            self.ModelPartNameCB.addItem('Structure')
            self.ModelPartNameCB.addItem('Add Here')


            # Analysis type Text Box
            self.AnalysisTypeLabel = QtGui.QLabel('Solver Type',self._solverSet)
            self.AnalysisCB = QtGui.QComboBox(self._solverSet)
            self.AnalysisCB.addItem('linear')
            self.AnalysisCB.addItem('non_linear')

            # max iter Text Box
            self.maxiterLabel = QtGui.QLabel('Max iter',self._solverSet)
            self.maxiterBox = QtGui.QLineEdit(self._solverSet)
            # Residual text Box
            self.ResidualLabel = QtGui.QLabel('Residual',self._solverSet)
            self.ResidualBox = QtGui.QLineEdit(self._solverSet)
            # Echo Level Text Box
            self.EchoLevelLabel = QtGui.QLabel('Echo Level',self._solverSet)
            self.EchoLevelBox = QtGui.QLineEdit(self._solverSet)

            # Save Button #isime dikkat et, bc ile cakismasin.
            self.SaveExitBtn = QtGui.QPushButton("&Save", self._solverSet)

            # Ok Button #isime dikkat et, bc ile cakismasin.
            self.OkBtn = QtGui.QPushButton("&Ok", self._solverSet)     

            #Button Layout
            buttonLayout = QtGui.QHBoxLayout()
            buttonLayout.addWidget(self.SaveExitBtn)
            buttonLayout.addWidget(self.OkBtn)            
            # Name Layout
            solverLayout = QtGui.QHBoxLayout()
            solverLayout.addWidget(self.SolverTypeLabel)
            solverLayout.addWidget(self.SolverCB, stretch=5)

            # RotationDOFsLayout
            RotationDOFsLayout = QtGui.QHBoxLayout()
            RotationDOFsLayout.addWidget(self.RotationDOFsLabel)
            RotationDOFsLayout.addWidget(self.RotationDOFsCB, stretch=5)



            # ModelPartNameLayout
            ModelPartNameLayout = QtGui.QHBoxLayout()
            ModelPartNameLayout.addWidget(self.ModelPartNameLabel)
            ModelPartNameLayout.addWidget(self.ModelPartNameCB, stretch=5)            

            # analysysyLayout Layout
            analysysyLayout = QtGui.QHBoxLayout()
            analysysyLayout.addWidget(self.AnalysisTypeLabel)
            analysysyLayout.addWidget(self.AnalysisCB)
            # EchoLevelLayout
            maxiterLayout = QtGui.QHBoxLayout()
            maxiterLayout.addWidget(self.maxiterLabel)
            maxiterLayout.addWidget(self.maxiterBox)
            # Name LayoutEchoLevelLayout
            ResidualLayout = QtGui.QHBoxLayout()
            ResidualLayout.addWidget(self.ResidualLabel)
            ResidualLayout.addWidget(self.ResidualBox)
            # EchoLevelLayout
            EchoLevelLayout = QtGui.QHBoxLayout()
            EchoLevelLayout.addWidget(self.EchoLevelLabel)
            EchoLevelLayout.addWidget(self.EchoLevelBox)
            # sublayout
   
            sublayout = QtGui.QVBoxLayout()
            sublayout.addLayout(solverLayout)
            sublayout.addLayout(RotationDOFsLayout)
            sublayout.addLayout(ModelPartNameLayout)
            sublayout.addLayout(analysysyLayout)
            sublayout.addLayout(maxiterLayout)
            sublayout.addLayout(ResidualLayout)
            sublayout.addLayout(EchoLevelLayout)
            sublayout.addLayout(buttonLayout)

            layout.addLayout(sublayout)       

            self._solverSet.setLayout(layout)

            # signals
            self.OkBtn.clicked.connect(self.okSS)
            
            self.SaveExitBtn.clicked.connect(self.saveSS)

         
            if visible:
                self._solverSet.show()
        else:
            self._solverSet.show()
            
    def ShowBoundaryConditions(self, context, visible=True):
        """Show Boundary conditions settings window

        Return:
        -------
        _bcWindow: QtWidget
            QtWidget with listview and boundary settings section
        """
        if not self._bcWindow:
            # Boundary Conditions General Windows
            self._bcWindow = QtGui.QWidget()
            layout = QtGui.QHBoxLayout()
            
            if(DEBUG):
                print("Boundary Conditions Windows is on")
            sys.stdout.flush()
            self._bcWindow.setGeometry(100,100,600,280)
            self._bcWindow.setWindowTitle("Boundary Conditions")
            self._bcWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

            # Buttons:
            # New BC
            self.NewBcBtn = QtGui.QPushButton("&New", self._bcWindow)
            
            # Delete BC
            self.DeleteBcBtn = QtGui.QPushButton("&Delete", self._bcWindow)

            #Processes button
            self.ProcessesBcBtn= QtGui.QPushButton("&Processes", self._bcWindow)

            # Boundary Conditions List
            self.BCList = QtGui.QListWidget(self._bcWindow)           

            # Name Text Box
            self.NameLabel = QtGui.QLabel('Name',self._bcWindow)
            self.NameBox = QtGui.QLineEdit(self._bcWindow)

            # Select Entity
            self.SelectLabel = QtGui.QLabel('Entity',self._bcWindow)  
            self.FaceBtn = QtGui.QPushButton("Select Entity", self._bcWindow)

            # Select Dimension Type
            self.SelectDimensionType = QtGui.QLabel('Dimension Type',self._bcWindow)
            self.DimensionType = QtGui.QComboBox(self._bcWindow)
            self.DimensionType.addItem('2D')
            self.DimensionType.addItem('3D')

            # Select Problem Type
            self.SelectProbType = QtGui.QLabel('Problem Type',self._bcWindow)      
            self.ProbType = QtGui.QComboBox(self._bcWindow)
            self.ProbType.addItem('0_Generic')
            self.ProbType.addItem('1_Fluid')
            self.ProbType.addItem('2_Structure')

            # Select Entity Type
            self.SelectEntType = QtGui.QLabel('Entity Type',self._bcWindow)      
            self.EntTypeCB = QtGui.QComboBox(self._bcWindow)
            self.EntTypeCB.addItem('Element')
            self.EntTypeCB.addItem('Condition')

            # Select BC Type 
            self.BctypeText = QtGui.QLabel('Name of Entity',self._bcWindow)    

            self.Bctype = QtGui.QComboBox(self._bcWindow)

            for value in THREE_D["ELEMENTS"]["0_Generic"].values():
                self.Bctype.addItems(value)
            for value in THREE_D["CONDITIONS"]["0_Generic"].values():
                self.Bctype.addItems(value)

            # Property ID
            self.ProperIDText = QtGui.QLabel('Property ID:',self._bcWindow)
            self.PropertyIDBox = QtGui.QLineEdit(self._bcWindow)
            #self.PropertyIDBox.setReadOnly(True)

            # Save Button
            self.SaveExitBtn = QtGui.QPushButton("&Save", self._bcWindow)

            # Ok Button
            self.OkBtn = QtGui.QPushButton("&Ok", self._bcWindow)

            #Button Layout
            buttonLayout = QtGui.QHBoxLayout()
            buttonLayout.addWidget(self.NewBcBtn)
            buttonLayout.addWidget(self.DeleteBcBtn)            
            buttonLayout.addWidget(self.SaveExitBtn)
            buttonLayout.addWidget(self.OkBtn)     
            buttonLayout.addWidget(self.ProcessesBcBtn)

            # Name Layout
            nameLayout = QtGui.QHBoxLayout()
            nameLayout.addWidget(self.NameLabel)
            nameLayout.addWidget(self.NameBox)

            # entityLayout Layout
            entityLayout = QtGui.QHBoxLayout()
            entityLayout.addWidget(self.SelectLabel)
            entityLayout.addWidget(self.FaceBtn)

            # DimensionType Layout
            DimensionTypeLayout = QtGui.QHBoxLayout()
            DimensionTypeLayout.addWidget(self.SelectDimensionType)
            DimensionTypeLayout.addWidget(self.DimensionType)

            # problemType Layout
            problemTypeLayout = QtGui.QHBoxLayout()
            problemTypeLayout.addWidget(self.SelectProbType)
            problemTypeLayout.addWidget(self.ProbType)

            # entityType Layout   
            entityTypeLayout = QtGui.QHBoxLayout()
            entityTypeLayout.addWidget(self.SelectEntType)
            entityTypeLayout.addWidget(self.EntTypeCB)
 
            # BcType Layout
            bcTypeLayout = QtGui.QHBoxLayout()
            bcTypeLayout.addWidget(self.BctypeText)
            bcTypeLayout.addWidget(self.Bctype)

            # propertyLayout
            propertyLayout = QtGui.QHBoxLayout()
            propertyLayout.addWidget(self.ProperIDText, stretch = 5)
            propertyLayout.addWidget(self.PropertyIDBox)

            # sublayout
            sublayout = QtGui.QVBoxLayout()
            sublayout.addLayout(nameLayout)
            sublayout.addLayout(entityLayout)
            sublayout.addLayout(DimensionTypeLayout)
            sublayout.addLayout(problemTypeLayout)
            sublayout.addLayout(entityTypeLayout)
            sublayout.addLayout(bcTypeLayout)
            sublayout.addLayout(propertyLayout)
            sublayout.addLayout(buttonLayout)

            layout.addWidget(self.BCList)
            layout.addLayout(sublayout)       

            self._bcWindow.setLayout(layout)

            # signals
            self.FaceBtn.clicked.connect(lambda: self.selectEntity(context))
            self.BCList.currentItemChanged.connect(self.BCitemChanged)
            self.DimensionType.currentIndexChanged.connect(self.updateBcType)
            self.ProbType.currentIndexChanged.connect(self.updateBcType)
            self.EntTypeCB.currentIndexChanged.connect(self.updateBcType)
            self.OkBtn.clicked.connect(self.okBC)
            self.NewBcBtn.clicked.connect(self.newBC)
            self.SaveExitBtn.clicked.connect(self.saveBC)
            self.DeleteBcBtn.clicked.connect(self.deleteBC)
            self.ProcessesBcBtn.clicked.connect(self.ProcessesBC)

            self.textNameBox = self.NameBox.text()
            self.newBC()
            if visible:
                self._bcWindow.show()
        else:
            if visible:
                self._bcWindow.show()

        return self._bcWindow

    def selectEntity(self, context):
        self.meshEntity = take_mesh.TakeMesh(context) 
        if(DEBUG):
            print ("Entity selected")
        self.NameBox.setText(self.meshEntity["name"])
        sys.stdout.flush()
    
    def updateBcType(self):
        if self.DimensionType.currentText() == "2D":
            if self.ProbType.currentText() == "0_Generic":
                self.ProcessesBcBtn.show()
                if self.EntTypeCB.currentText() == "Element":
                    if(DEBUG):
                        print ("Current Entity Type: Generic Element ")
                    self.Bctype.clear()
                    for value in TWO_D["ELEMENTS"]["0_Generic"].values():
                        self.Bctype.addItems(value)
                else:
                    if(DEBUG):
                        print ("Current Entity Type: Generic Condition ")
                    self.Bctype.clear()
                    for value in TWO_D["CONDITIONS"]["0_Generic"].values():
                        self.Bctype.addItems(value)
            elif self.ProbType.currentText() == "1_Fluid":
                self.ProcessesBcBtn.hide()
                if self.EntTypeCB.currentText() == "Element":
                    if(DEBUG):
                        print ("Current Entity Type: Fluid Element ")
                    self.Bctype.clear()
                    for value in TWO_D["ELEMENTS"]["1_Fluid"].values():
                        self.Bctype.addItems(value)
                else:
                    if(DEBUG):
                        print ("Current Entity Type: Fluid Condition ")
                    self.Bctype.clear()
                    for value in TWO_D["CONDITIONS"]["1_Fluid"].values():
                        self.Bctype.addItems(value)
            else:
                self.ProcessesBcBtn.show()
                print(self.ProbType.currentText())
                if self.EntTypeCB.currentText() == "Element":
                    if(DEBUG):
                        print ("Current Entity Type: Structure Element ")
                    self.Bctype.clear()
                    for value in TWO_D["ELEMENTS"]["2_Structure"].values():
                        self.Bctype.addItems(value)
                else:
                    if(DEBUG):
                        print ("Current Entity Type: Structure Condition ")
                    self.Bctype.clear()
                    for value in TWO_D["CONDITIONS"]["2_Structure"].values():
                        self.Bctype.addItems(value)
        else:
            if self.ProbType.currentText() == "0_Generic":
                self.ProcessesBcBtn.show()
                if self.EntTypeCB.currentText() == "Element":
                    if(DEBUG):
                        print ("Current Entity Type: Generic Element ")
                    self.Bctype.clear()
                    for value in THREE_D["ELEMENTS"]["0_Generic"].values():
                        self.Bctype.addItems(value)
                else:
                    if(DEBUG):
                        print ("Current Entity Type: Generic Condition ")
                    self.Bctype.clear()
                    for value in THREE_D["CONDITIONS"]["0_Generic"].values():
                        self.Bctype.addItems(value)
            elif self.ProbType.currentText() == "1_Fluid":
                self.ProcessesBcBtn.hide()
                if self.EntTypeCB.currentText() == "Element":
                    if(DEBUG):
                        print ("Current Entity Type: Fluid Element ")
                    self.Bctype.clear()
                    for value in THREE_D["ELEMENTS"]["1_Fluid"].values():
                        self.Bctype.addItems(value)
                else:
                    if(DEBUG):
                        print ("Current Entity Type: Fluid Condition ")
                    self.Bctype.clear()
                    for value in THREE_D["CONDITIONS"]["1_Fluid"].values():
                        self.Bctype.addItems(value)
            else:
                self.ProcessesBcBtn.show()
                print(self.ProbType.currentText())
                if self.EntTypeCB.currentText() == "Element":
                    if(DEBUG):
                        print ("Current Entity Type: Structure Element ")
                    self.Bctype.clear()
                    for value in THREE_D["ELEMENTS"]["2_Structure"].values():
                        self.Bctype.addItems(value)
                else:
                    if(DEBUG):
                        print ("Current Entity Type: Structure Condition ")
                    self.Bctype.clear()
                    for value in THREE_D["CONDITIONS"]["2_Structure"].values():
                        self.Bctype.addItems(value)

################################ SOLVER SETTINGS ITEMS ################################
    def okSS(self):
        self._solverSet.hide()

    def saveSS(self):
        ''' Save Solver Settings'''
        if self.SolverCB.currentIndex() == 0:
            self.SSsave["solver_type"] = "Static"
        else:
            self.SSsave["solver_type"] = "Non-Static"
            
            
        self.SSsave["echo_level"] =  float(self.EchoLevelBox.text()) if self.EchoLevelBox.text() else self.SSsave["echo_level"]
        
        
        if self.AnalysisCB.currentIndex()== 0:
            self.SSsave["analysis_type"] = "linear"
        else:
            self.SSsave["analysis_type"] = "non_linear"
        self.SSsave["max_iteration"] =  float(self.maxiterBox.text()) if self.maxiterBox.text() else self.SSsave["max_iteration"]
        self.SSsave["residual_absolute_tolerance"] =  float(self.ResidualBox.text()) if self.ResidualBox.text() else self.SSsave["residual_absolute_tolerance"]

        if self.RotationDOFsCB.currentIndex()==0:
            self.SSsave["rotation_dofs"] =  True
        elif self.RotationDOFsCB.currentIndex()==1:
            self.SSsave["rotation_dofs"] =  False 
        if self.ModelPartNameCB.currentIndex()==0:
            self.SSsave["model_part_name"] =  "Structure"
        elif self.ModelPartNameCB.currentIndex()==1:
            self.SSsave["model_part_name"] =  "Add Here1"
         
        
        if(DEBUG):
            print(self.SSsave)
################################ SOLVER SETTINGS ITEMS ################################

################################ MATERIALS ITEMS ################################
    def okMat(self):
        self._matWindow.hide()


    def saveMat(self):
        '''Save the Materials'''
        self.MatSave["YOUNG_MODULUS"] = float(self.YoungBox.text()) if self.YoungBox.text() else self.MatSave["YOUNG_MODULUS"]

        self.MatSave["POISSON_RATIO"] =float(self.poissonBox.text()) if self.poissonBox.text() else  self.MatSave["POISSON_RATIO"]
        
        self.MatSave["I33"] = float(self.InertiaBox.text()) if self.InertiaBox.text() else self.MatSave["I33"]

        self.MatSave["DENSITY"] = float(self.densityBox.text()) if self.densityBox.text() else self.MatSave["DENSITY"]

        self.MatSave["CROSS_AREA"] =float(self.CrossBox.text()) if self.CrossBox.text() else self.MatSave["CROSS_AREA"]
                
    def okProcess(self):
        self._ProcessesBcWindow.hide()

################################ MATERIALS ITEMS ################################

################################ BC ITEMS ################################
    def newBC(self):
        self._bc_count=self._bc_count+1
        de = myBcList()
        de.setText('Boundary Condition '+str( self._bc_count) )
        self.BCList.addItem(de)
        if (self._bc_count==1):
            self.ConstrainedXCheckBox=QtGui.QCheckBox()
            self.ConstrainedYCheckBox=QtGui.QCheckBox()
            self.ConstrainedZCheckBox=QtGui.QCheckBox()
            self.ValueXBox = QtGui.QLineEdit()
            self.ValueYBox = QtGui.QLineEdit()
            self.ValueZBox = QtGui.QLineEdit()
        self.boundaryConditionEditor.append(de)
        self.ConstrainedXCheckBox.setChecked(False)
        self.ConstrainedYCheckBox.setChecked(False)
        self.ConstrainedZCheckBox.setChecked(False)
        self.ValueXBox.clear()
        self.ValueYBox.clear()
        self.ValueZBox.clear()

    def ProcessesBC(self,context,visible=True):
        if not self._ProcessesBcWindow:
            # Boundary Conditions General Windows
            self._ProcessesBcWindow = QtGui.QWidget()
            layout = QtGui.QHBoxLayout()
            if(DEBUG):
                print("Processes Windows is on")
            sys.stdout.flush()
            self._ProcessesBcWindow.setGeometry(100,100,400,200)
            self._ProcessesBcWindow.setWindowTitle("Processes")
            self._ProcessesBcWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

                    
            self.LoadsName=QtGui.QLabel('Load Processes',self._ProcessesBcWindow)
            
            self.ConstrainName=QtGui.QLabel('Constrain Processes',self._ProcessesBcWindow)

            self.OkBtnProcess = QtGui.QPushButton("&Ok", self._ProcessesBcWindow)     

            #ConstrainedXCheckBox
    
            self.ConstrainedXCheckBox = QtGui.QCheckBox("X Constrained",self._ProcessesBcWindow)
            self.ConstrainedYCheckBox = QtGui.QCheckBox("Y Constrained",self._ProcessesBcWindow)
            self.ConstrainedZCheckBox = QtGui.QCheckBox("Z Constrained",self._ProcessesBcWindow)

            # Value X Text Box
            self.ValueXLabel = QtGui.QLabel('ValueX',self._ProcessesBcWindow)
            self.ValueXBox = QtGui.QLineEdit(self._ProcessesBcWindow)

            # Value Y Text Box
            self.ValueYLabel = QtGui.QLabel('ValueY',self._ProcessesBcWindow)
            self.ValueYBox = QtGui.QLineEdit(self._ProcessesBcWindow)

            # Value Z Text Box
            self.ValueZLabel = QtGui.QLabel('ValueZ',self._ProcessesBcWindow)
            self.ValueZBox = QtGui.QLineEdit(self._ProcessesBcWindow)

   
        
            # Constrained sub layout
            ConstrainLayout=QtGui.QVBoxLayout()
            ConstrainLayout.addWidget(self.ConstrainName)
            ConstrainLayout.addWidget(self.ConstrainedXCheckBox)
            ConstrainLayout.addWidget(self.ConstrainedYCheckBox)
            ConstrainLayout.addWidget(self.ConstrainedZCheckBox)

            ConstrainedValXLayout=QtGui.QHBoxLayout()
            ConstrainedValXLayout.addWidget(self.ValueXLabel)
            ConstrainedValXLayout.addWidget(self.ValueXBox)

            ConstrainedValYLayout=QtGui.QHBoxLayout()
            ConstrainedValYLayout.addWidget(self.ValueYLabel)
            ConstrainedValYLayout.addWidget(self.ValueYBox)

            ConstrainedValZLayout=QtGui.QHBoxLayout()
            ConstrainedValZLayout.addWidget(self.ValueZLabel)
            ConstrainedValZLayout.addWidget(self.ValueZBox)


            ConstrainLayout.addLayout(ConstrainedValXLayout)
            ConstrainLayout.addLayout(ConstrainedValYLayout)
            ConstrainLayout.addLayout(ConstrainedValZLayout)
            ConstrainLayout.addWidget(self.OkBtnProcess)



            self.VariableNameLabel = QtGui.QLabel('Variable Name',self._ProcessesBcWindow)
            self.VariableNameCB = QtGui.QComboBox(self._ProcessesBcWindow)
            self.VariableNameCB.addItem('POINT_LOAD')
            self.VariableNameCB.addItem('LINE_LOAD')
            self.VariableNameCB.addItem('SURFACE_LOAD')
            self.VariableNameCB.addItem('POSITIVE_FACE_PRESSURE')

            LoadLayout=QtGui.QVBoxLayout()
            LoadLayoutVarying=QtGui.QVBoxLayout()


            LoadLayout.addWidget(self.LoadsName)
            LoadLayoutVarName=QtGui.QHBoxLayout()
            LoadLayoutVarName.addWidget(self.VariableNameLabel)
            LoadLayoutVarName.addWidget(self.VariableNameCB)


            # Modulus Text Box
            self.ModulusLabel = QtGui.QLabel('Modulus',self._ProcessesBcWindow)
            self.ModulusBox = QtGui.QLineEdit(self._ProcessesBcWindow)

            # DirectionX Text Box
            self.DirectionXLabel = QtGui.QLabel('Direction X',self._ProcessesBcWindow)
            self.DirectionXBox = QtGui.QLineEdit(self._ProcessesBcWindow)

            # DirectionY Text Box
            self.DirectionYLabel = QtGui.QLabel('Direction Y',self._ProcessesBcWindow)
            self.DirectionYBox = QtGui.QLineEdit(self._ProcessesBcWindow)

            # DirectionXZ Text Box
            self.DirectionZLabel = QtGui.QLabel('Direction Z',self._ProcessesBcWindow)
            self.DirectionZBox = QtGui.QLineEdit(self._ProcessesBcWindow)

            DirectionXLayout=QtGui.QHBoxLayout()
            DirectionXLayout.addWidget(self.DirectionXLabel)
            DirectionXLayout.addWidget(self.DirectionXBox)

            DirectionYLayout=QtGui.QHBoxLayout()
            DirectionYLayout.addWidget(self.DirectionYLabel)
            DirectionYLayout.addWidget(self.DirectionYBox)

            DirectionZLayout=QtGui.QHBoxLayout()
            DirectionZLayout.addWidget(self.DirectionZLabel)
            DirectionZLayout.addWidget(self.DirectionZBox)

            ModulusLayout=QtGui.QHBoxLayout()
            ModulusLayout.addWidget(self.ModulusLabel)
            ModulusLayout.addWidget(self.ModulusBox)

            LoadLayoutVarying.addLayout(ModulusLayout)
            LoadLayoutVarying.addLayout(DirectionXLayout)
            LoadLayoutVarying.addLayout(DirectionYLayout)
            LoadLayoutVarying.addLayout(DirectionZLayout)

            LoadLayout.addLayout(LoadLayoutVarName)
            LoadLayout.addLayout(LoadLayoutVarying)

            layout.addLayout(LoadLayout)
            layout.addLayout(ConstrainLayout)

            self.OkBtnProcess.clicked.connect(self.okProcess)

    
            self._ProcessesBcWindow.setLayout(layout)
            if visible:
                self._ProcessesBcWindow.show()
        else:
            if visible:
                self._ProcessesBcWindow.show()

        return self._ProcessesBcWindow    

    def BCitemChanged(self): 
        if self.BCList.count() > 1 :
            bce = self.boundaryConditionEditor[0]
            for i in range(0, self.BCList.count()):
                if self.BCList.currentItem().text() == self.boundaryConditionEditor[i].name:
                    bce = self.boundaryConditionEditor[i]

            self._bcWindow.setWindowTitle(bce.name)
            self.SelectEntType = bce.entity
            self.PropertyIDBox.setText(bce.propertyId)
            self.NameBox.setText(bce.name)
            self.EntTypeCB.setCurrentIndex(self.EntTypeCB.findText(bce.entityType, QtCore.Qt.MatchFixedString))
            self.Bctype.setCurrentIndex(self.Bctype.findText(bce.nameOfEntity, QtCore.Qt.MatchFixedString))
            self._bcWindow.show()
    
    def okBC(self):
        self._bcWindow.hide()
        self.saveBC()

    def saveBC(self):
        de = self.BCList.currentItem()
        de.propertyId = self.PropertyIDBox.text() if self.PropertyIDBox.text() else "error"
        if(DEBUG):
            print(de.mesh_name)
        if self.Bctype.currentText() not in de.name:
            de.name =  str(self.Bctype.currentText() + '_' + self.NameBox.text()) 
        de.entityType = self.EntTypeCB.currentText()
        de.nameOfEntity = self.Bctype.currentText()
        
        if self.DimensionType.currentText() == '2D':
            self.is2D = True
            if de.entityType == 'Element':
                curr_dict = TWO_D["ELEMENTS"]
            if de.entityType == 'Condition':
                curr_dict = TWO_D["CONDITIONS"]
        else:
            if de.entityType == 'Element':
                curr_dict = THREE_D["ELEMENTS"]
            if de.entityType == 'Condition':
                curr_dict = THREE_D["CONDITIONS"]
        
        if self.ProbType.currentText() != "1_Fluid" and de.entityType=='Condition':
            loads_process_list_dict={}
            if self.VariableNameCB.currentText()=="POINT_LOAD" and self.ModulusBox.text():
                loads_process_list_dict=LOAD_PROCESS_POINT_LOAD
                loads_process_list_dict["Parameters"]["modulus"]=float(self.ModulusBox.text())
                loads_process_list_dict["Parameters"]["direction"][0]=float(self.DirectionXBox.text()) if self.DirectionXBox.text() else loads_process_list_dict
                loads_process_list_dict["Parameters"]["direction"][1]=float(self.DirectionYBox.text()) if self.DirectionYBox.text() else loads_process_list_dict
                loads_process_list_dict["Parameters"]["direction"][2]=float(self.DirectionZBox.text()) if self.DirectionZBox.text() else loads_process_list_dict

                loads_process_list_dict["Parameters"]["model_part_name"]=de.name
                de.load_process_list=loads_process_list_dict
                

            if self.VariableNameCB.currentText()=="LINE_LOAD" and self.ModulusBox.text():
                loads_process_list_dict=LOAD_PROCESS_SURFACE_LOAD
                loads_process_list_dict["Parameters"]["modulus"]=float(self.ModulusBox.text())
                loads_process_list_dict["Parameters"]["variable_name"]="LINE_LOAD"
                loads_process_list_dict["Parameters"]["direction"][0]=float(self.DirectionXBox.text()) if self.DirectionXBox.text() else loads_process_list_dict
                loads_process_list_dict["Parameters"]["direction"][1]=float(self.DirectionYBox.text()) if self.DirectionYBox.text() else loads_process_list_dict
                loads_process_list_dict["Parameters"]["direction"][2]=float(self.DirectionZBox.text()) if self.DirectionZBox.text() else loads_process_list_dict
                
                loads_process_list_dict["Parameters"]["model_part_name"]=de.name
                de.load_process_list=loads_process_list_dict

            if self.VariableNameCB.currentText()=="SURFACE_LOAD" and self.ModulusBox.text():
                loads_process_list_dict=LOAD_PROCESS_SURFACE_LOAD
                loads_process_list_dict["Parameters"]["modulus"]=float(self.ModulusBox.text())
                loads_process_list_dict["Parameters"]["direction"][0]=float(self.DirectionXBox.text()) if self.DirectionXBox.text() else loads_process_list_dict
                loads_process_list_dict["Parameters"]["direction"][1]=float(self.DirectionYBox.text()) if self.DirectionYBox.text() else loads_process_list_dict
                loads_process_list_dict["Parameters"]["direction"][2]=float(self.DirectionZBox.text()) if self.DirectionZBox.text() else loads_process_list_dict

                loads_process_list_dict["Parameters"]["model_part_name"]=de.name
                de.load_process_list=loads_process_list_dict
            
            if self.VariableNameCB.currentText()=="POSITIVE_FACE_PRESSURE" and self.ModulusBox.text():
                loads_process_list_dict=LOAD_PROCESS_POSITIVE_FACE_PRESSURE
                loads_process_list_dict["Parameters"]["value"]=float(self.ModulusBox.text())

                loads_process_list_dict["Parameters"]["model_part_name"]=de.name
                de.load_process_list=loads_process_list_dict
            
            if self.ConstrainedXCheckBox.isChecked() or self.ConstrainedYCheckBox.isChecked() or self.ConstrainedZCheckBox.isChecked():
                constrained_process_list_dict=CONSTRAINT_PROCESS
                if self.ConstrainedXCheckBox.isChecked():
                    constrained_process_list_dict["Parameters"]["constrained"][0]=True
                    constrained_process_list_dict["Parameters"]["value"][0]=float(self.ValueXBox.text()) if self.ValueXBox.text() else 0
                if self.ConstrainedYCheckBox.isChecked():
                    constrained_process_list_dict["Parameters"]["constrained"][1]=True
                    constrained_process_list_dict["Parameters"]["value"][1]=float(self.ValueYBox.text()) if self.ValueYBox.text() else 0
                if self.ConstrainedZCheckBox.isChecked():
                    constrained_process_list_dict["Parameters"]["constrained"][2]=True
                    constrained_process_list_dict["Parameters"]["value"][2]=float(self.ValueZBox.text()) if self.ValueZBox.text() else 0
                
                constrained_process_list_dict["Parameters"]["model_part_name"]=de.name
                de.constrain_process_list = constrained_process_list_dict
       
        de.elementType = find_element_type(self.ProbType.currentText(), curr_dict, de.nameOfEntity)
        de.setText(de.name)
        de.mesh_dict = creat_mesh_dict(True, de.elementType, de.entityType, de.nameOfEntity)
        de.meshDAT_dict = self.meshEntity
        de.mesh_name = de.meshDAT_dict["name"]
        self.NameBox.setText(de.name)
        if(DEBUG):
            print("The length of the dictionary is: " + str(len(self.boundaryConditionEditor)))
            print(self.boundaryConditionEditor[len(self.boundaryConditionEditor)-1].mesh_dict)

        sys.stdout.flush()

    def deleteBC(self):
        if self.BCList.count() > 0:
            # remove the current body force
            if self.BCList.count() > 1:

                de = self.BCList.currentItem()
                for i in range (len(self.boundaryConditionEditor)):
                    if de.myid == self.boundaryConditionEditor[i].myid:
                        del self.boundaryConditionEditor[i]
                        break

                self.BCList.takeItem(self.BCList.row(de))

            else:
                de = self.BCList.currentItem()
                self.BCList.takeItem(self.BCList.row(de))
                del self.boundaryConditionEditor[0]
                self._bcWindow.hide()
    
    def exportDat(self):
        if(DEBUG):
            print("Saving .dat and .mdpa files")
        path_dict = em.SaveFilesPath()      

        for i in range(len(self.boundaryConditionEditor)):
            instance = self.boundaryConditionEditor[i]
            mesh_dict = instance.meshDAT_dict
            if(DEBUG):
                print("Information of mesh : ", mesh_dict)
            em.ExportMesh(mesh_dict, path_dict)
        if(DEBUG):
            print("Succesfull export dat!")
        sys.stdout.flush()
        return path_dict
                
def StaticCounter():
    StaticCounter.counter += 1
    return StaticCounter.counter
StaticCounter.counter = 0

def Static2Counter():
    Static2Counter.counter += 1
    return Static2Counter.counter
Static2Counter.counter = 0

class myBcList(QtGui.QListWidgetItem):
    def __init__(self):
        super(myBcList, self).__init__()
        self.name ='Boundary Condition'
        self.entity = None
        self.entityType = 0
        self.nameOfEntity = 0
        self.elementType = 0
        self.mesh_name = 0
        self.mesh_dict = None
        self.propertyId=str(StaticCounter())
        self.meshDAT_dict = None
        self.myid = Static2Counter()
        self.load_process_list = {}
        self.constrain_process_list = {}
################################ BC ITEMS ################################    
