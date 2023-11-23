import json
import pandas as pd

MAX_LEVEL = 40
df_IDName = pd.read_json("./Json/EN_Personalities.json")
skillnamelist = [pd.read_json("./Json/EN_Skills_personality-[NUMBER].json".replace("[NUMBER]","{:02d}".format(i))) for i in range(1,13)]
df_SkillName = skillnamelist + [pd.read_json("./Json/EN_Skills.json")]

def color_to_sin(color):
    return{
        "AZURE":"GLOOM",
        "VIOLET":"ENVY",
        "AMBER":"SLOTH",
        "NONE":"NONE",
        "SHAMROCK":"GLUTTONY",
        "INDIGO":"PRIDE",
        "CRIMSON":"WRATH",
        "SCARLET":"LUST",
        "NONE":"NONE"
    }[color]

def type_to_phys(type):
    return{
        "SLASH":"SLASH",
        "PENETRATE":"PIERCE",
        "HIT":"BLUNT",
        "NONE":"NONE"
    }[type]

def find_skill_name(id):
    for index in df_SkillName:
        for i in index['dataList']:
            if (i != {} and i['id'] == id):
                return str(((i['levelList'])[len(i['levelList'])-1])['name']).replace(',','').replace('\n',' ')
    

def find_skill_desc(id):
    ret = ''
    for index in df_SkillName:
        for i in index['dataList']:
            if (i != {} and i['id'] == id):
                is_first_entry = 1
                ret += "BASE_CONDITION: " + i['levelList'][len(i['levelList'])-1]['desc'] + '\n'

                for j in i['levelList'][len(i['levelList'])-1]['coinlist']:
                    if is_first_entry == 0:
                        ret += '\n'
                    if len(j) != 0:
                        is_first = 1
                        for k in j['coindescs']:
                            if is_first == 0:
                                ret += ' + '
                            ret += '(' + k['desc'] + ')'
                            is_first = 0
                    else:
                        ret += '()'
                    is_first_entry = 0
    return "\"" + ret + "\""
        

def condense_skill_to_t3(skill):
    ret_skill = ''
    i = 0
    for tier in skill['skillData']:
        if i == 0:
            ret_skill = tier
        else:
            for key in tier:
                ret_skill[key] = tier[key]
        i+=1
    return ret_skill
            

def json_to_description(id_info, skill_info):
    ret = str(id_info['id']) + ',' 
    for i in df_IDName['dataList']:
        if i['id'] == id_info['id']:
            ret += "\"" + str(i['title']).replace('\n', ' ') + '\n' + i['nameWithTitle'] +"\""
    ret += ','
    ret += "\'" + id_info['rank'] * "0" + ','
    ret += str(id_info['unitKeywordList']) + ',' 
    ret += str(int(int(id_info['hp']['defaultStat']) + float(id_info['hp']['incrementByLevel'])*MAX_LEVEL)) + ','
    ret += str(int(int(id_info['defCorrection']))) + ','
    ret += str(max(id_info['minSpeedList'])) + ','
    ret += str(max(id_info['maxSpeedList'])) + ','
    ret += str(id_info['breakSection']['sectionList']).replace(',', '') + ','
    for i in id_info['resistInfo']['atkResistList']:
        if i['type'] == 'SLASH':
            ret += str(i['value'])
    ret += ','
    for i in id_info['resistInfo']['atkResistList']:
        if i['type'] == 'PENETRATE':
            ret += str(i['value'])
    ret += ','
    for i in id_info['resistInfo']['atkResistList']:
        if i['type'] == 'HIT':
            ret += str(i['value'])
    ret += ','
    # todo: get passive text/cost
    for i in id_info['attributeList']:
        for j in skill_info:
            skill = 0
            if j['id'] == i['skillId']:
                skill = j
                break
        if skill == 0:
            print("Error, skill not found!")
        else:
            skill = condense_skill_to_t3(skill)
            ret += str(i['skillId']) + ','
    ret = ret[:-1]
    return ret


def produce_skill_json(path):
    df = pd.DataFrame(columns=["skillID", "skillName","tier","offenseCorrection","physType","sinType","basePower","coinPower","coinNumber"])
    for i in range(1,13):
        skill_json = pd.read_json("./Json/personality-skill-[NUMBER].json".replace("[NUMBER]","{:02d}".format(i)))
        for skill in skill_json['list']:
            condensed_skill = condense_skill_to_t3(skill) # this is only the skillData
            
            df.loc[len(df.index)] = [skill['id'], find_skill_name(skill['id']), skill['skillTier'], condensed_skill['skillLevelCorrection'], 
                  type_to_phys(condensed_skill['atkType']), color_to_sin(condensed_skill['attributeType']), 
                    condensed_skill['defaultValue'], condensed_skill['coinList'][0]['scale'], len(condensed_skill['coinList'])]
    df.to_csv(path,index=False)

