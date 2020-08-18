# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 18:30:09 2018

@author: irfan
"""
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


def WriteMaterialToJson(o, level=0):
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
                ret += WriteMaterialToJson(v, level + 1)

            ret += "}"
        else:
            ret += "{" + NEWLINE
            comma = ""
            for k in reversed(sorted(o.keys())): # reversed to make i better readable
                v = o[k]
                ret += comma
                comma = ",\n"
                ret += SPACE * INDENT * (level+1)
                ret += '"' + str(k) + '" :' + SPACE
                ret += WriteMaterialToJson(v, level + 1)

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
                ret += "[" + ",".join([WriteMaterialToJson(e, level+1) for e in o]) + "]"
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




import json
structuralmaterials_dict = {}

Properties_dict={}

Properties_dict[ "model_part_name"] = "Parts_Parts_Auto1"

Properties_dict[ "properties_id" ]=1



Materials_dict={}

Materials_dict["constitutive_law"]={}
Materials_dict["constitutive_law"]["name"]="KratosMultiphysics.StructuralMechanicsApplication.LinearElastic3DLaw"

variables_dict={}
variables_dict["DENSITY"]=7850.0
variables_dict["YOUNG_MODULUS"]=206900000000.0
variables_dict[ "POISSON_RATIO"]= 0.29

variables_dict[ "CROSS_AREA" ]= 1.0

variables_dict[ "I33"  ]= 1.0

tables_dict={}





Materials_dict["Variables"]=variables_dict
Materials_dict ["Tables"  ]= tables_dict
Properties_dict["Material"]=Materials_dict

structuralmaterials_dict["properties"]=[]
structuralmaterials_dict["properties"].append(Properties_dict)



if __name__ == '__main__':

    print("\033[1;37m    writting Matrials file using the json mpdule of python:\033[0m")
    print(json.dumps(structuralmaterials_dict,sort_keys=False,indent=4))

    print("\n\n\033[1;37m    writting Matrials file using the custom function:\033[0m")
    print(WriteMaterialToJson(structuralmaterials_dict))



