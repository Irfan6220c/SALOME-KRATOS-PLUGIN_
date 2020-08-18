'''
This is a brief example on how mesh files from Salome in *.dat format can be read with the Salome-kratos-converter
It works with a simple 2D cantilever example, fixed on one side and a load applied on the other side
'''

# Note that this has to be on the path in order to work, or you manually specify the path
import kratos_io_utilities as kratos_utils
import global_utilities as global_utils
import os

model = kratos_utils.MainModelPart() # Main mesh object to which we will add the submeshes (Kratos Name: ModelPart)

# Specifying the names of the submeshes (Kratos Name: SubModelPart)
smp_dict_domain    = {"smp_name": "domain"}
smp_dict_dirichlet = {"smp_name": "dirichlet"}
smp_dict_neumann   = {"smp_name": "neumann"}

file_name_domain = "domain.dat"
file_name_dirichlet = "dirichlet.dat"
file_name_neumann = "neumann.dat"

def ReadDatFile(file_name):
    valid_file, nodes, geom_entities = global_utils.ReadAndParseSalomeDatFile(os.path.join(os.getcwd(),file_name))
    if not valid_file:
        raise Exception("Invalid File!\n" + file_name)
    return nodes, geom_entities

nodes_domain,    geom_entities_domain    = ReadDatFile(file_name_domain)
nodes_dirichlet, geom_entities_dirichlet = ReadDatFile(file_name_dirichlet)
nodes_neumann,   geom_entities_neumann   = ReadDatFile(file_name_neumann)

# Here we specify which Kratos-entities will be created from the general geometric entities
mesh_dict_domain    = {'write_smp': 1,
                       'entity_creation': {204: {'Element': {'SmallDisplacementElement2D4N': '0'}}}}
mesh_dict_dirichlet = {'write_smp': 1,
                       'entity_creation': {102: {'Condition': {'LineLoadCondition2D2N': '0'}}}}
mesh_dict_neumann   = {'write_smp': 1,
                       'entity_creation': {102: {'Condition': {'LineLoadCondition2D2N': '0'}}}}
"""
model.AddMesh(smp_dict_domain,    mesh_dict_domain,    nodes_domain,    geom_entities_domain)
model.AddMesh(smp_dict_dirichlet, mesh_dict_dirichlet, nodes_dirichlet, geom_entities_dirichlet)
model.AddMesh(smp_dict_neumann,   mesh_dict_neumann,   nodes_neumann,   geom_entities_neumann)

mdpa_info = "mdpa for demonstration purposes"

model.WriteMesh("2D_cantilever", mdpa_info)
"""

class KratosSubModelPart(object):
    pass

def write_mdpa_file(problem_name, root_path, boundaryConditionEditor):
    model = kratos_utils.MainModelPart() # Main mesh object to which we will add the submeshes (Kratos Name: ModelPart)

    for bc in boundaryConditionEditor:
        smp = KratosSubModelPart()
        smp.dict = {"smp_name": bc.name}
        smp.path = root_path + os.sep + bc.name + '.dat'
        print(smp.path)
        smp.nodes, smp.geom_entities = ReadDatFile(smp.path)
        smp.mesh_dict = bc.mesh_dict
        model.AddMesh(smp.dict, smp.mesh_dict, smp.nodes, smp.geom_entities)

    mdpa_info = "mdpa for demonstration purposes"
    mdpa_file_path = root_path + os.sep + problem_name + '.mpda'
    print("in the funcrion " + mdpa_file_path)
    model.WriteMesh(mdpa_file_path ,mdpa_info)
    print ("Successfully writing the mdpa file!")

class myBcList:
    def __init__(self,name,mesh_dict):
        self.name = name
        self.mesh_dict = mesh_dict

boundaryConditionEditor = []
boundaryConditionEditor.append(myBcList('domain',mesh_dict_domain))
boundaryConditionEditor.append(myBcList('dirichlet',mesh_dict_dirichlet))
boundaryConditionEditor.append(myBcList('neumann',mesh_dict_neumann))


path = os.path.abspath("C:\\Users\\Mengj\\Desktop")
write_mdpa_file('our_test', path, boundaryConditionEditor)