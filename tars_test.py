import json

with open ("lecture_info.json", "r") as f:
    lectures = json.load(f)

note_dic = {}
for lecnum, lecture in lectures.items():
    note_dic[lecture['note']] = None

with open('test.json', 'w', encoding='UTF-8') as f : 
	json.dump(note_dic, f, indent=4, ensure_ascii=False)
