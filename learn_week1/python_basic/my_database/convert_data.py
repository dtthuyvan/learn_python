from bson.objectid import ObjectId

def convert_list_objectid_to_str(data_list):
    result_list = []
    for item in data_list:
        new_item = convert_obj_objectid_to_str(item)
        result_list.append(new_item)
    return result_list

def convert_obj_objectid_to_str(data):
    new_item = data.copy()
    if '_id' in new_item and isinstance(new_item['_id'], ObjectId):
        new_item['_id'] = str(new_item['_id'])
    return new_item

if __name__ == "__main__":
    input_list = [
        {
            '_id': ObjectId('688084e0d3055354eb8df58a'), 
            'name': 'Ha Long Bay', 
            'sub_title': 'Di Sản Thiên Nhiên Thế Giới', 
            'description': '', 
            'image': '', 
            'price_tour': '140', 
            'guide_id': '3'
        },
        {
            '_id': ObjectId('688084e0d3055354eb8df58b'), 
            'name': 'Sapa', 
            'sub_title': 'Thị Trấn Trong Sương', 
            'description': '', 
            'image': '', 
            'price_tour': '120', 
            'guide_id': '5'
        }
    ]

    output_list = convert_list_objectid_to_str(input_list)

    import json
    print(json.dumps(output_list, indent=4))

    print("\nSource:", type(input_list[0]['_id']))
    print("Result:", type(output_list[0]['_id']))
