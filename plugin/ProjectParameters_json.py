"""By Oguz"""

import json

def WriteValue(_entry):
    """Writing values for int,float and str types, used in list types"""
    if isinstance(_entry,str):
        return '"' + _entry + '"'

    if isinstance(_entry,float):
        return '%.7g' % _entry
        
    if isinstance(_entry,bool):
        return "true" if _entry else "false"
        
    if isinstance(_entry,int):
        return str(_entry)

def Find_Parameters_and_Last_Key(_list):
    """Finds the key "Parameters" and the last key in the list"""
    if isinstance(_list,list) and isinstance(_list[0],dict):    
        counter=0
        last_key=""
        parameter_str=""
        for key in _list[0].keys():
            counter=counter+1
            if key=="Parameters":
                parameter_str=key
            elif counter==len(_list[0]):
                last_key=key
        return [parameter_str,last_key]
    else: raise TypeError("Unknown type '%s' for json serialization" % str(type(_list)))



def Change_Keys_and_Values(_list,_para_and_last):
    """Trial Function"""
    store_para_value=_list[0][_para_and_last[0]]
    store_lasts_value=_list[0][_para_and_last[1]]
    _list[0][_para_and_last[1]]=_list[0].pop(_para_and_last[0])
    _list[0][_para_and_last[1]]=store_lasts_value
    _list[0][_para_and_last[0]]=store_para_value
    return _list




def pp_json(json_thing, sort=False, indents=4):
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
        return None
my_dict = {}
def Find_Key_in_a_List(_list,_value):
    """Arguments=a list and a key in the list
       Returns=the index of _value in the list"""
    if not isinstance(_list,list):
        raise TypeError("Unknown type '%s' for json serialization" % str(type(_list)))
    elif isinstance(_list,list):
        for k in range(len(_list)):
            if _list[k]==_value:
                return k
            if k==len(_list)-1:
                raise TypeError("Unknown type '%s' for json serialization" % str(type(_list)))
                
def Change_Keys_and_Values_dict(_dict,_para_and_last):
    """Trial function"""
    store_para_value=_dict[_para_and_last[0]]
    store_lasts_value=_dict[_para_and_last[1]]
    _dict[_para_and_last[1]]=_dict.pop(_para_and_last[0])
    _dict[_para_and_last[1]]=store_lasts_value
    _dict[_para_and_last[0]]=store_para_value
    return _dict

def ReSort_with_Priority(_sorted_list,_name_to_be_sorted,new_location):
    """ Resort the already sorted list by putting _name_to_be_sorted in new location and putting the old value in new_location into the 
    _name_to_be_sorted's first location"""
    if _name_to_be_sorted in _sorted_list:
        a=Find_Key_in_a_List(_sorted_list,_name_to_be_sorted)
        tmp=_sorted_list[a]
        _sorted_list[a]=_sorted_list[new_location]
        _sorted_list[new_location]=tmp
        return _sorted_list
    else:
        print("something is not right")
        return _sorted_list





def WriteProjectToJson(o, level=0):
    """This function takes a dict as input and converts is to a string with specific formatting.
    It has the same purpose as the json.dump function with the difference that the order
    in which things are written can be customized. Also the formatting can be customized
    """
    # source: https://stackoverflow.com/questions/10097477/python-json-array-newlines
    INDENT = 4
    SPACE = " "
    NEWLINE = "\n"
    ret = ""
    if isinstance(o, dict):
        if len(o) == 0:
            ret += "{}"
        elif len(o) == 1: # and list(o.keys())[0] == "@table"
            ret += "{"
            for k in o.keys():
                v = o[k]
                ret += '"' + str(k) + '" : '
                ret += WriteProjectToJson(v, level + 1)

            ret += "}"
        else:
            ret += "{" + NEWLINE
            comma = ""
            sorted_o_keys=sorted(o.keys())
            if sorted_o_keys[0]!="problem_data" and level==0:
                sorted_o_keys=ReSort_with_Priority(sorted_o_keys,"problem_data",0)
            if sorted_o_keys[1]!="solver_settings" and level==0:
                sorted_o_keys=ReSort_with_Priority(sorted_o_keys,"solver_settings",1)
            if level==2 and "Parameters" in sorted_o_keys:
                a=Find_Key_in_a_List(sorted_o_keys,"Parameters")# a is 0,
                sorted_o_keys[a]=sorted_o_keys[1] # in place of Parameters, which was the first in the list, put the second value in  the list.
                sorted_o_keys.remove(sorted_o_keys[1]) #remove the second value, since it is in first place from above line.
                sorted_o_keys.append("Parameters")    # add parameters to the end of the list.
            for k in sorted_o_keys: 
                v = o[k]
                ret += comma
                comma = ",\n"
                ret += SPACE * INDENT * (level+1)
                ret += '"' + str(k) + '" :' + SPACE
                ret += WriteProjectToJson(v, level + 1)

            ret += NEWLINE + SPACE * INDENT * level + "}"
    elif isinstance(o, str):
        ret += '"' + o + '"'
    elif isinstance(o, list):
        if len(o) > 0:
            if isinstance(o[0], (int,  float, str)):
                ret += NEWLINE + SPACE * INDENT * (level+1) + "["
                num_vals = len(o)
                for i in range(num_vals):
                    entry = o[i]
                    ret += WriteValue(entry)
                    if i <= num_vals-2:
                        ret += ", "
                    else:
                        ret += "]"
            else:
                ret += "[" + ",".join([WriteProjectToJson(e, level+1) for e in o]) + "]"
        elif not o:
            return "[]"
    elif isinstance(o, bool):
        ret += "true" if o else "false"
    elif isinstance(o, int):
        ret += str(o)
    elif isinstance(o, float):
        ret += '%.7g' % o
    elif o is None:
        ret += 'null'
        raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
    return ret

##Problem Data variables
problem_name="trial_4"
model_part_name="Structure"
domain_size=3
parallel_type="OpenMP"
time_step=1.1
start_time=0.0
end_time=1.0
echo_level=1

##Problem Data Dictionary
problem_data_dict={"problem_name":problem_name,"model_part_name":model_part_name,
                        "domain_size":domain_size,"parallel_type":parallel_type,
                        "time_step":time_step,"start_time":start_time,
                        "end_time":end_time,"echo_level":echo_level}


##Add problem Data
my_dict["problem_data"]=problem_data_dict


##Solver Settings Variables
solver_type="Static"
echo_level=1
analysis_type="non_linear"
input_type="mdpa"
input_filename="trial_4"
materials_filename="StructuralMaterials.json"
model_import_settings={"input_type":input_type,"input_filename":input_filename}
material_import_settings={"materials_filename":materials_filename}
line_search=False
convergence_criterion="residual_criterion"
displacement_relative_tolerance=0.0001
displacement_absolute_tolerance=1e-9
residual_relative_tolerance=0.0001
residual_absolute_tolerance=1e-9
max_iteration=10
problem_domain_sub_model_part_list=["Parts_Parts_Auto1"]
processes_sub_model_part_list=["DISPLACEMENT_Displacement_Auto1","PointLoad2D_Load_on_points_Auto1"]
rotation_dofs=False

##Add solver type and Parameters to Solver Settings
solver_settings={}
solver_settings["solver_type"]=solver_type
solver_settings["echo_level"]=echo_level
solver_settings["analysis_type"]=analysis_type
solver_settings["model_import_settings"]=model_import_settings
solver_settings["material_import_settings"]=material_import_settings
solver_settings["line_search"]=line_search
solver_settings["convergence_criterion"]=convergence_criterion
solver_settings["displacement_relative_tolerance"]=displacement_relative_tolerance
solver_settings["displacement_absolute_tolerance"]=displacement_absolute_tolerance
solver_settings["residual_relative_tolerance"]=residual_relative_tolerance
solver_settings["residual_absolute_tolerance"]=residual_absolute_tolerance
solver_settings["max_iteration"]=max_iteration
solver_settings["problem_domain_sub_model_part_list"]=problem_domain_sub_model_part_list
solver_settings["processes_sub_model_part_list"]=processes_sub_model_part_list
solver_settings["rotation_dofs"]=rotation_dofs




##Add Solver Settings to the main dic.
my_dict["solver_settings"] = solver_settings





##constraints_process_list variables
python_module="assign_vector_variable_process"
kratos_module="KratosMultiphysics"
helpp="This process fixes the selected components of a given vector variable"
process_name="AssignVectorVariableProcess"




##Variables related to parameters_dictionary inside constraints_process_list
model_part_name="DISPLACEMENT_Displacement_Auto2"
variable_name="DISPLACEMENT"
constrained=[True,True,True]
value=[0.0,0.0,0.0]
interval=[0.0,"End"]

const_process_list_PARAMETERS_value1={}
const_process_list_PARAMETERS_value1["model_part_name"]=model_part_name
const_process_list_PARAMETERS_value1["variable_name"]=variable_name
const_process_list_PARAMETERS_value1["constrained"]=constrained
const_process_list_PARAMETERS_value1["value"]=value
const_process_list_PARAMETERS_value1["interval"]=interval




##Add keys to const_process_list
const_process_list=[{"python_module":python_module,"kratos_module":kratos_module,
                        "help":helpp,"process_name":process_name,"Parameters":const_process_list_PARAMETERS_value1}]


##Add const_process_list to main dic.
my_dict["constraints_process_list"]=const_process_list


##Add contact_process_list to main dic.
my_dict["contact_process_list"]=[]


python_module_loads_process="assign_vector_by_direction_to_condition_process"
help_loads_process_list="This process sets a vector variable value over a condition according to a given modulus an direction"
check="DirectorVectorNonZero direction"
process_name="AssignVectorByDirectionToConditionProcess"
interval_loads_process_list=[0.0,"End"]

##Load process list parameter dict.

loads_process_list_PARAMETERS_value={}
loads_process_list_PARAMETERS_value["model_part_name"]="PointLoad2D_Load_on_points_Auto1"
loads_process_list_PARAMETERS_value["variable_name"]="POINT_LOAD"
loads_process_list_PARAMETERS_value["modulus"]=10.0
loads_process_list_PARAMETERS_value["direction"]=[0.0,-1.0,0.0]
loads_process_list_PARAMETERS_value["interval"]=interval_loads_process_list

loads_process_list=[{"python_module":python_module_loads_process,"kratos_module":kratos_module,
                        "help":help_loads_process_list,"check":check,
                        "process_name":process_name,"Parameters":loads_process_list_PARAMETERS_value}]



my_dict["loads_process_list"]=loads_process_list
##add list_other_processes to main dic.
list_other_processes=[]
my_dict["list_other_processes"]=list_other_processes


##Output Config variables


GiDPostMode="GiD_PostBinary"
WriteDeformedMeshFlag="WriteDeformed"
WriteConditionsFlag="WriteConditions"
MultiFileFlag="SingleFile"
result_file_configuration={}
gidpost_flags_dict={"GiDPostMode":GiDPostMode,"WriteDeformedMeshFlag":WriteDeformedMeshFlag,
                        "WriteConditionsFlag":WriteConditionsFlag,
                        "MultiFileFlag":MultiFileFlag}

file_label="step"
output_control_type="step"
output_frequency=1
body_output=True
node_output=False
skin_output=False
plane_output=[]
nodal_results=["DISPLACEMENT","REACTION"]
gauss_point_results=["VON_MISES_STRESS"]

##result_file_configuration_dict
result_file_configuration_value={"gidpost_flags":gidpost_flags_dict,"file_label":file_label,
                                "output_control_type":output_control_type,"output_frequency":output_frequency,
                                "body_output":body_output,"node_output":node_output,"skin_output":skin_output,
                                "plane_output":plane_output,"nodal_results":nodal_results,
                                "gauss_point_results":gauss_point_results}
point_data_configuration=[]

output_configuration_value={"result_file_configuration":result_file_configuration_value,"point_data_configuration":point_data_configuration}
my_dict["output_configuration"]=output_configuration_value


if __name__ == '__main__':



    print("\n\n\033[1;37m    writting ProjectParameters file using the custom function:\033[0m")
    print(WriteProjectToJson(my_dict))




   
    
    













 ##### OLD SETTINGS


# # ##Model Settings Variables
# # model_name="my_name"
# # dimension=2
# # domain_parts_list=["Parts_Parts_Auto1"]
# # processes_parts_list=["DISPLACEMENT_Displacement_Auto2","DISPLACEMENT_Displacement_Auto3","DISPLACEMENT_Displacement_Auto4","SelfWeight2D_Self_weight_Auto1"]
# # name="my_name"
# # input_file_settings={"name":name}
# # dofs=["list"]

# # ##Model Settings Dictionary
# # model_settings_dict={}
# # model_settings_dict["model_name"]=model_name
# # model_settings_dict["dimension"]=dimension
# # model_settings_dict["domain_parts_list"]=domain_parts_list
# # model_settings_dict["processes_parts_list"]=processes_parts_list
# # model_settings_dict["input_file_settings"]=input_file_settings
# # model_settings_dict["dofs"]=dofs

# # ##Add model settings
# # my_dict["model_settings"]=model_settings_dictiguration_value["result_file_configuration"]=result_file_configuration_value


##Add result_file_configuration to main dic.





# # ##Model Settings Variables
# # model_name="my_name"
# # dimension=2
# # domain_parts_list=["Parts_Parts_Auto1"]
# # processes_parts_list=["DISPLACEMENT_Displacement_Auto2","DISPLACEMENT_Displacement_Auto3","DISPLACEMENT_Displacement_Auto4","SelfWeight2D_Self_weight_Auto1"]
# # name="my_name"
# # input_file_settings={"name":name}
# # dofs=["list"]

# # ##Model Settings Dictionary
# # model_settings_dict={}
# # model_settings_dict["model_name"]=model_name
# # model_settings_dict["dimension"]=dimension
# # model_settings_dict["domain_parts_list"]=domain_parts_list
# # model_settings_dict["processes_parts_list"]=processes_parts_list
# # model_settings_dict["input_file_settings"]=input_file_settings
# # model_settings_dict["dofs"]=dofs

# # ##Add model settings
# # my_dict["model_settings"]=model_settings_dict





# # ##Parameters(Inside model settings) Variables
# # time_step=1.0
# # start_time=0.0
# # end_time=1.0
# # time_settings={"time_step"  : time_step,"start_time" : start_time,"end_time"   : end_time}

# # solution_type="Static"
# # integration_method="Linear"
# # time_integration_settings={"solution_type":solution_type,"integration_method":integration_method}


# # line_search=False
# # convergence_criterion="Residual_criterion"
# # variable_relative_tolerance=0.0001
# # variable_absolute_tolerance=1e-9
# # residual_relative_tolerance=0.0001
# # residual_absolute_tolerance=1e-9
# # max_iteration=10
# # solving_strategy_settings={"line_search":line_search,"convergence_criterion":convergence_criterion,
# #                             "variable_absolute_tolerance":variable_absolute_tolerance,
# #                             "residual_relative_tolerance":residual_relative_tolerance,
# #                             "residual_absolute_tolerance":residual_absolute_tolerance,
# #                             "max_iteration":max_iteration}

# # model_set_parameters_dict={}
# # model_set_parameters_dict["time_settings"]=time_settings
# # model_set_parameters_dict["time_integration_settings"]=time_integration_settings
# # model_set_parameters_dict["solving_strategy_settings"]=solving_strategy_settings