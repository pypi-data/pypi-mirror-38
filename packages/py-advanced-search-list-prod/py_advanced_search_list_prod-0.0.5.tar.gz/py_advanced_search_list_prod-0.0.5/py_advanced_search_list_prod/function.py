from fuzzywuzzy import fuzz
from fuzzywuzzy import process
db_list =[
    [1, "redmi S3","img1"],
    [2, "oneplus 3","moto"],
    [3, "oneplus 1","img3"],
    [4, "moto 3","img4"],
]
def search(list, limit, score_cutoff):
    result = process.extractBests(list, db_list, limit=limit, score_cutoff=score_cutoff)
    list = []
    for each in result:
        dict = {}
        dict["id"] = each[0][0]
        dict["name"] = each[0][1]
        dict["img_url"] = each[0][2]
        list.append(dict)
    return list