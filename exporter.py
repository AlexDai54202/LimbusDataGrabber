import pandas as pd
from module import *

### Units

identity_output = ('id,name,rarity,affiliation,hp,def,minspeed,maxspeed,staggerperiods,slashres,pierceres,bluntres,')
identity_output += "s1ID,"
identity_output += "s1ID,".replace('1','2')
identity_output += "s1ID\n".replace('1','3')
cur_num = 1
while cur_num < 13:
    df_ID = pd.read_json("./Json/personality-"+ ('0' + str(cur_num) if cur_num < 10 else str(cur_num)) +".json")
    df_ID_skill = pd.read_json("./Json/personality-skill-"+ ('0' + str(cur_num) if cur_num < 10 else str(cur_num)) +".json")
    for i in range(df_ID.size):
        identity_output += (json_to_description(df_ID.iloc[i][0], df_ID_skill['list']).replace("\n"," ")) + '\n'
    cur_num += 1

text_file = open("unit.csv", "w", encoding='utf-8')
text_file.write(identity_output)
text_file.close()

### Skills

produce_skill_json("skills.csv")