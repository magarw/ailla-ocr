import json 
import os
from collections import Counter

languages = ["zoh", "cac", "mam", "miq", "mcd", "quh", "quch", "tzh"]

for lang in languages:
    num_boxes_fp = 0
    num_boxes_gold = 0
    one_changed = 0
    two_changed = 0
    three_changed = 0
    
    insertions = 0
    deletions = 0
    len_change = 0
        
    filename = f"filename_rename_lang_identifier/{lang}.json"
    with open(filename) as f:
        data = json.load(f)      
    num_pages = len(data)
    annotated_page_book = set()
    for page in data:
        id = page['id']
        split_root_file_path = page['data']['ocr'].split("/")
        bookname = split_root_file_path[-2]
        pagenum =  split_root_file_path[-1].split(".p")[0]
        annotated_page_book.add((bookname, pagenum))
        
        first_pass = page['predictions'][0]['result']
        gold_annotations = page['annotations'][0]['result']
        
        fp_coordinates = []
        go_coordinates = []
        text_fp = ""
        text_gold = ""
        # Counting number of bounding boxes per page (gold and first-pass)
        for first_pass_box in first_pass:
            if first_pass_box['type'] == "rectangle":
                fp_coordinates.append(first_pass_box['value']['points'])
                num_boxes_fp += 1
            elif first_pass_box['type'] == "textarea":
                text_fp += " ".join(first_pass_box['value']['text'])
        for gold_box in gold_annotations:
            if gold_box['type'] == "rectangle":
                try:
                    go_coordinates.append(gold_box['value']['points'])
                except:
                    pass
                num_boxes_gold += 1
            elif gold_box['type'] == "textarea":
                text_gold += " ".join(gold_box['value']['text'])
        
        # Compute boxes where 3 coordinates are identical, and only 1 was edited
        for box in fp_coordinates:
            for box2 in go_coordinates:
                common_count = 0
                if box[0] in box2:
                    common_count += 1
                if box[1] in box2:
                    common_count += 1
                if box[2] in box2:
                    common_count += 1 
                if box[3] in box2:
                    common_count += 1
               
                if common_count == 3:
                    one_changed += 1
                if common_count == 2:
                    two_changed += 1
                if common_count == 1:
                    three_changed += 1
            

        # Compare the two texts 
        len_change += len(text_fp) - len(text_gold)
        
        res_fp = Counter(text_fp)
        res_gold = Counter(text_gold)
        
        insert = res_gold - res_fp
        insertions += sum(insert.values())
        
        delete = res_fp - res_gold
        deletions += sum(delete.values())

    print(f"{lang} -  D_b = {(num_boxes_gold - num_boxes_fp)/len(data):0.2f}")
    # print(f"One Changed: {one_changed/len(data):0.2f}")
    # print(f"Two Changed: {two_changed/len(data):0.2f}")
    # print(f"Three Changed: {three_changed/len(data):0.2f}")
    print(f"Length Changed: {len_change/len(data):0.2f}")
    print(f"Insertions: {insertions/len(data):0.2f}")
    print(f"Deletions: {deletions/len(data):0.2f}")
    print("\n")
    