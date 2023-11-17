import pandas as pd


df = pd.DataFrame([{"id": 1027716903, 
                    "step": 7, 
                    "name": "LaKristens", 
                    "first": "Kristi", 
                    "last": "Lyapistova", 
                    "premium": "None", 
                    "summa": 10, 
                    "email": "mail@lyapistova.ru", 
                    }])

with open("chanel.txt", "r") as f:
    while f:
        line = f.readline().split()
        if len(line) > 5:
            if line[3] == "Piskynova":
                line = ['#1', 'rozza_piskunova', '841909876', 'Piskynova Rozza', 'None', 'None']
            if line[4] == "Sofia":
                line = ['#1', 'None', '6280511951', '✨️♡ Sofia ♡✨️', 'None', 'None']
            if line[3] == "Марина":
                line = ['#1', 'None', '1190172314', 'Марина Д.', 'None', 'None']
            if len(line) == 7:
                line[3] = line[3] + " " + line[4]
                line.pop(4)
            if line[3] == "Юлия":
                line = ['#1', 'None', '1444268710', 'Юлия Зорина', 'Юлия Зорина', 'None']
        
        if not line:
            break

        if line[0] == "#1":
            if len(line) != 6:
                print(line)
            else:
                print(df.loc[df.id == int(line[2])]) if len(df.loc[df.id == int(line[2])]) else None
                df.loc[len(df)] = [int(line[2]), 0, line[1], line[3], line[4], line[5], 0, None]
        else:
            if len(line) == 4:
                if line[1] == "None":
                    print(line)
                else:
                    assert len(df[df.name == line[1]]) == 1
                    df.loc[df.loc[df.name == line[1]].index[0], "step"] = 7
                    df.loc[df.loc[df.name == line[1]].index[0], "email"] = line[2]
                    df.loc[df.loc[df.name == line[1]].index[0], "summa"] = int(line[3])
            else:
                print(line)

df.to_csv("dada.csv", index=False)