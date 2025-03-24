import pickle

from pandas import DataFrame

MATERIALS_MAP = {
    "leather": 0,
    "fabric": 1
}

def save_map_of_materials():
    with open("data/materials_map.llm.map", "wb") as file:
        pickle.dump(MATERIALS_MAP, file)
        

def map_non_numeric_columns(sofa_frame: DataFrame):
    sofa_frame["cover_material"] = sofa_frame["cover_material"].map(MATERIALS_MAP)
    save_map_of_materials()