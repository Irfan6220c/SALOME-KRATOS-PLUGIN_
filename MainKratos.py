# Making KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Import Kratos core and apps
from KratosMultiphysics import *
from KratosMultiphysics.StructuralMechanicsApplication import *
import structural_mechanics_analysis

# Read parameters
with open("ProjectParameters.json",'r') as parameter_file:
    parameters = Parameters(parameter_file.read())

model = Model()
analysis = structural_mechanics_analysis.StructuralMechanicsAnalysis(model, parameters)
analysis.Run()

