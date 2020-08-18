import kratos_io_utilities as kratos_utils
import global_utilities as global_utils
import os
import sys

dat_path = ""
# add SALOME_PLUGIN_PATH to Python environment for easier module import
import inspect
dat_path = os.path.dirname(inspect.getfile(inspect.currentframe())) +\
              os.sep + "testing_examples" + os.sep + "use_converter"


NODE_IDENTIFIER = 101 
TWO_D = {
    "GEOMETRY_IDENTIFIERS" : {
            NODE_IDENTIFIER : "Node",
            102 : "Line",
            203 : "Triangle",
            204 : "Quadrilateral",
            304 : "Tetrahedral",
            308 : "Hexahedral"
    },
    
    "ELEMENTS" : {
        "0_Generic" : {
            102 : [
                "Element2D2N",
            ],
            203 : [
                "Element2D3N",
            ],
            204 : [
                "Element2D4N"
            ]
        },
        "1_Fluid" : {
            203 : [
                "Element2D3N"
            ]
        },
        "2_Structure" : {
            NODE_IDENTIFIER : [
                "NodalConcentratedElement2D1N",
                "NodalConcentratedDampedElement2D1N",
            ],
            102 : [
                "CrBeamElement2D2N",
                "CrLinearBeamElement2D2N",
            ],
            203 : [
                "SmallDisplacementElement2D3N",
                "TotalLagrangianElement2D3N",
                "UpdatedLagrangianElement2D3N",
            ],
            204 : [
                "SmallDisplacementElement2D4N",
                "TotalLagrangianElement2D4N",
                "UpdatedLagrangianElement2D4N"
            ]
        }
    },
    
    "CONDITIONS" : {
        "0_Generic" : {
            NODE_IDENTIFIER : [
                "PointCondition2D1N"
            ],
            102 : [
                "LineCondition2D2N"
            ]
        },
        "1_Fluid" : {
            102 : [
                "WallCondition2D2N"
            ]
        },
        "2_Structure" : {
            NODE_IDENTIFIER : [
                "PointLoadCondition2D1N",
                "PointLoadCondition2D1N"
            ],
            102 : [
                "LineLoadCondition2D2N"
            ],
            204 : [
                "SurfaceLoadCondition3D4N"
            ]
        }
    }
}

THREE_D = {
    "GEOMETRY_IDENTIFIERS" : {
            NODE_IDENTIFIER : "Node",
            102 : "Line",
            203 : "Triangle",
            204 : "Quadrilateral",
            304 : "Tetrahedral",
            308 : "Hexahedral"
    },
    "ELEMENTS" : {
        "0_Generic" : {
            203 : [
                "Element3D3N"
            ],
            304 : [
                "Element3D4N"
            ],
            308 : [
                "Element3D8N"
            ],
        },
        "1_Fluid" : {
            304 : [
                "Element3D4N"
            ]
        },
        "2_Structure" : {
            NODE_IDENTIFIER : [
                "NodalConcentratedElement3D1N",
                "NodalConcentratedDampedElement3D1N"
            ],
            102 : [
                "CableElement3D2N",

                "TrussElement3D2N",
                "TrussLinearElement3D2N",
                "CrBeamElement3D2N",
                "CrLinearBeamElement3D2N",
                "SpringDamperElement3D2N"
            ],
            203 : [
                "PreStressMembraneElement3D3N",

                "ShellThinElementCorotational3D3N"
                "ShellThickElementCorotational3D3N"
            ],
            204 : [
                "PreStressMembraneElement3D4N",

                "ShellThinElementCorotational3D4N",
                "ShellThickElementCorotational3D4N"
            ],
            304 : [
                "SmallDisplacementElement3D4N",
                "TotalLagrangianElement3D4N",
                "UpdatedLagrangianElement3D4N"
            ],
            308 : [
                "SmallDisplacementElement3D8N",
                "TotalLagrangianElement3D8N",
                "UpdatedLagrangianElement3D8N"
            ]
        }
    },
    "CONDITIONS" : {
        "0_Generic" : {
            NODE_IDENTIFIER : [
                "PointCondition3D1N"
            ],
            102 : [
                "LineCondition3D2N"
            ],
            203 : [
                "SurfaceCondition3D3N"
            ],
            204 : [
                "SurfaceCondition3D4N"
            ]
        },
        "1_Fluid" : {
            203 : [
                "WallCondition3D3N"
            ]
        },
        "2_Structure" : {
            NODE_IDENTIFIER : [
                "PointMomentCondition3D1N",
                "PointTorqueCondition3D1N"
            ],
            203 : [
                "SurfaceLoadCondition3D3N"
            ],
            204 : [
                "SurfaceLoadCondition3D4N"
            ]
        }
    }
}
def print_logo():
    print('''
   _____       _                        _  __          _                      
  / ____|     | |                      | |/ /         | |                     
 | (___   __ _| | ___  _ __ ___   ___  | ' / _ __ __ _| |_ ___  ___           
  \___ \ / _` | |/ _ \| '_ ` _ \ / _ \ |  < | '__/ _` | __/ _ \/ __|          
  ____) | (_| | | (_) | | | | | |  __/ | . \| | | (_| | || (_) \__ \          
 |_____/ \__,_|_|\___/|_| |_| |_|\___| |_|\_\_|  \__,_|\__\___/|___/          
   _____                          _              _____  _             _       
  / ____|                        | |            |  __ \| |           (_)      
 | |     ___  _ ____   _____ _ __| |_ ___ _ __  | |__) | |_   _  __ _ _ _ __  
 | |    / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__| |  ___/| | | | |/ _` | | '_ \ 
 | |___| (_) | | | \ V /  __/ |  | ||  __/ |    | |    | | |_| | (_| | | | | |
  \_____\___/|_| |_|\_/ \___|_|   \__\___|_|    |_|    |_|\__,_|\__, |_|_| |_|
                                                                 __/ |        
                                                                |___/  
    ''')
 
def creat_mesh_dict(write_smp, element_type, entity_type, entity_name):
    """
    This function creat the mesh dictionary with the user specified info
    
    write_smp: type bool
    element_type: type int, elememt type needed by kratos, contains 3 digits
    entity_type: Element or Condition 
    entity_nanme: Element name or Condition name
    
    """

    mesh_dict = {'write_smp': write_smp,
                 'entity_creation': {element_type: 
                 {entity_type: {entity_name: '0'}}}}
    if(global_utils.DEBUG):
        print("Sucessfully created mesh dictionary")
    return mesh_dict

def find_element_type(problem_type, dictionary, name_of_entity):
    """
        This function return the element type (e.g: 102) for a given entity name (e.g: 'TrussElement3D2N')
    """
    for entity_type, name in dictionary[problem_type].iteritems():
        for i in range(0, len(name)):
            if name[i] == name_of_entity:
                return entity_type

def ReadDatFile(file_name):
    valid_file, nodes, geom_entities = global_utils.ReadAndParseSalomeDatFile(os.path.join(os.getcwd(),file_name))
    if not valid_file:
        raise Exception("Invalid File!\n" + file_name)
    return nodes, geom_entities

class KratosSubModelPart(object):
    """
    The attributes in the class is defined in write_mdpa_file(boundaryConditionEditor, root_path, problem_name)
    """
    pass

def write_mdpa_file(problem_name, root_path, boundaryConditionEditor):
    """
    This function goes through all the objects in the boundaryConditionEditor, assign the entities needed by kratos as input

    problem_name: type string, name of the mdpa file
    root_path: type string, where *.mdpa, *.dat files are saved
    boundaryConditionEditor: type myBcList[]
    
    """
    model = kratos_utils.MainModelPart() # Main mesh object to which we will add the submeshes (Kratos Name: ModelPart)

    if root_path == None:
        root_path = '.'

    for bc in boundaryConditionEditor:
        smp = KratosSubModelPart()
        if(global_utils.DEBUG):
            print(bc.mesh_name)
        smp.dict = {"smp_name": bc.name}
        smp.path = root_path + os.sep + bc.mesh_name + '.dat'
        smp.nodes, smp.geom_entities = ReadDatFile(smp.path)
        smp.mesh_dict = bc.mesh_dict
        model.AddMesh(smp.dict, smp.mesh_dict, smp.nodes, smp.geom_entities)
    
    mdpa_info = "mdpa for demonstration purposes"
    mdpa_file_path = root_path + os.sep + problem_name
    model.WriteMesh(mdpa_file_path ,mdpa_info)
    if(global_utils.DEBUG):
        print ("Successfully writing the mdpa file!")
