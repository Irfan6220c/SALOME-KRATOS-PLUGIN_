import kratos_window_manager as kwm
import ProjectParameters_json as pp
import StructuralMaterials_json as sm
import os
import shutil
from global_utilities import DEBUG


def AssembleProjectParametersJson(KratosWindowManager,root_path):
    """Assemble the projectparameters dictionary from user input
    
    Args:
    -----
    ->KratosWindowManager:  presumably main_window in salome_plugins 

    Output:
    -----
    ->ProjectParameters dictionary

    The output of this function should then be used as the input of 
    WriteProjectToJson function of ProjectParameters_json.py
    """

    ##Create the dict.
    projectparameters_dict = {}

    projectparameters_dict["problem_data"] = pp.problem_data_dict
    if KratosWindowManager.is2D:
        projectparameters_dict["problem_data"]["domain_size"]=2
    
    for key in KratosWindowManager.SSsave:
        pp.solver_settings[key] = KratosWindowManager.SSsave[key]    

    projectparameters_dict["solver_settings"] = pp.solver_settings
    
    projectparameters_dict["solver_settings"]["model_import_settings"]["input_filename"]=root_path["mdpa_name"]





    projectparameters_dict["output_configuration"] = pp.output_configuration_value

    projectparameters_dict["list_other_processes"] = []
    projectparameters_dict["contact_process_list"] = []


    projectparameters_dict["loads_process_list"]=[]
    projectparameters_dict["constraints_process_list"]=[]
    for boundarycondition in KratosWindowManager.boundaryConditionEditor:
        if boundarycondition.load_process_list:
            projectparameters_dict["solver_settings"]["processes_sub_model_part_list"][1]=boundarycondition.name
            projectparameters_dict["loads_process_list"].append(boundarycondition.load_process_list)
        
        if boundarycondition.constrain_process_list:
            projectparameters_dict["solver_settings"]["processes_sub_model_part_list"][0]=boundarycondition.name
            projectparameters_dict["constraints_process_list"].append(boundarycondition.constrain_process_list)
        if boundarycondition.entityType=='Element':## if element, it is the domain and get its name
            projectparameters_dict["solver_settings"]["problem_domain_sub_model_part_list"][0]=boundarycondition.name
    if(DEBUG):        
        print(projectparameters_dict)
    return pp.WriteProjectToJson(projectparameters_dict)

def AssembleStructuralMaterialsJson(KratosWindowManager):
    """Assemble the structuralmaterials dictionary from user input
    
    Args:
    -----
    ->KratosWindowManager:  presumably main_window in salome_plugins 

    Output:
    -----
    ->StructuralMaterials dictionary

    The output of this function should then be used as the input of 
    WriteMaterialToJson function of StructuralMaterials_json.py
    """
    for key in KratosWindowManager.MatSave.keys():
        if(DEBUG):
            print(key)
            print(type(KratosWindowManager.MatSave[key]))
        sm.structuralmaterials_dict["properties"][0]["Material"]["Variables"][key]=KratosWindowManager.MatSave[key]
    for bclistobject in KratosWindowManager.boundaryConditionEditor:
        if(DEBUG):
            print(bclistobject.name)
        if bclistobject.entityType=='Element':
            sm.structuralmaterials_dict["properties"][0]["model_part_name"]=bclistobject.name


    if KratosWindowManager.is2D:
        sm.structuralmaterials_dict["properties"][0]["Material"]["constitutive_law"]["name"]="KratosMultiphysics.StructuralMechanicsApplication.LinearElasticPlaneStrain2DLaw"
    else:
        sm.structuralmaterials_dict["properties"][0]["Material"]["constitutive_law"]["name"]="KratosMultiphysics.StructuralMechanicsApplication.LinearElastic3DLaw"
        

    if(DEBUG):
        print(sm.structuralmaterials_dict)
    return sm.WriteMaterialToJson(sm.structuralmaterials_dict)
def WriteProjectParametersjson(save_path,dic_in_json_format):
    """Writes the ProjectParameters.json file in a given save_path
     Args:
     -----
     ->dic_in_json_format: ideally the output of AssembleProjectParametersJson function.

     """
     
    complete_name=os.path.join(save_path,"ProjectParameters.json")  
    with open(complete_name, "w") as save_file:
        save_file.write(dic_in_json_format)
    if(DEBUG):
        print("ProjectParameters.json written")

def WriteStructuralMaterialsjson(save_path,dic_in_json_format):
    """Writes the StructuralMaterials.json file in a given save_path
     Args:
     -----
     ->dic_in_json_format: ideally the output of AssembleStructuralMaterialsJson function.

    """
    complete_name=os.path.join(save_path,"StructuralMaterials.json")  
    with open(complete_name, "w") as save_file:
        save_file.write(dic_in_json_format)
    if(DEBUG):
        print("StructuralMaterials.json written")


def WriteMainKratosFromDefaults(path):
    ''' This has to be changed for every user, could be improved '''
    default_path_to_main_kratos="/home/oguz/Downloads/SALOME-8.3.0-UB16.04/BINARIES-UB16.04/GUI/share/salome/plugins/gui/salome-kratos-plugin"
    MainIn=os.path.join(default_path_to_main_kratos,"MainKratos.py")
    MainOut=os.path.join(path,"MainKratos.py")
    shutil.copyfile(MainIn, MainOut)
    if(DEBUG):
        print("MainKratos.py copied") 
       
if __name__ == '__main__':
    """Can be used as a standalone script to check
    """
    a_window_manager=kwm.KratosWindowManager()
    path="/home/oguz/Desktop"
    WriteProjectParametersjson(path,AssembleProjectParametersJson(a_window_manager))
    WriteStructuralMaterialsjson(path,AssembleStructuralMaterialsJson(a_window_manager))

