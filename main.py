from packages.model import *
from packages.utils import replace_within_double_curly_brackets
from packages.api_calls import get_champion_SnW, get_champion_powerSpikes, get_champion_counters


import json
from tqdm import tqdm
import numpy as np

if __name__ == "__main__":


    with open("./champion_mapping.json", "r") as file:
        champion_mapping : dict = json.load(file)

    champion_names : list[str] = list(champion_mapping.keys())

    champion_names = [s.lower() for s in champion_names]

    row_idx : int = 0

    lines : list = []
    for champion_name in tqdm(champion_names):
        snw : dict = get_champion_SnW(champion_name)
        snwDataList : list = snw["data"]["guidesByRoleData"]
        
        powerSpikes : dict = get_champion_powerSpikes(champion_name)
        powerSpikesDataList : list = powerSpikes["data"]["powerSpikesData"]

        counters : dict = get_champion_counters(champion_name)
        champMU : list = counters["data"]["championMatchupSpecificData"]
        champRole : list = counters["data"]["championRoleData"]

        
        for pwData, snwData, champMUData, champRoleData in zip(powerSpikesDataList, snwDataList, champMU, champRole):
            # For champRoleData
            champRoleDataList : list = champRoleData["flatData"]["counterTips"]
            for counterTips in champRoleDataList:
                dataCounterTips : dict = {
                    "text" : replace_within_double_curly_brackets(counterTips["text"])
                }
                lines.append(dataCounterTips)
            
            # For champMU data
            dataChampMU : dict = {
                "text": replace_within_double_curly_brackets(champMUData["flatData"]["matchupTips"])
            }
            lines.append(dataChampMU)
            

            # For Strenght and weaknesses
            dataSW1 : dict = {
                "text": replace_within_double_curly_brackets(snwData["flatData"]["strengths"]),
                
            }

            dataSW2 : dict = {
                "text": replace_within_double_curly_brackets(snwData["flatData"]["weaknesses"])
            }
            
            lines.append(dataSW1)
            lines.append(dataSW2)
            
            # For Power spikes
            pwGameStages = pwData["flatData"]["gameStages"]
            for pwGS in pwGameStages:
                dataPS1 : dict = {
                    "text": replace_within_double_curly_brackets(pwGS["gamePlan"])
                }
                dataPS2 : dict = {
                    "text": replace_within_double_curly_brackets(pwGS["powerSpikeDescription"])
                }

                lines.append(dataPS1)
                lines.append(dataPS2)

    db_size = len(lines)
    train_size = round(db_size * 0.80)

    np.random.shuffle(lines)
    train_data = lines[:train_size]
    test_data = lines[train_size + 1:]

    with open("train-lol-champs.jsonl", "w") as f:
        for line in train_data:
            f.write(json.dumps(line) + "\n")

    with open("test-lol-champs.jsonl", "w") as f:
        for line in test_data:
            f.write(json.dumps(line) + "\n")


            






