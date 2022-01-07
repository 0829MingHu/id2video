#from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
from pathlib import Path
import pandas as pd
import re
from pathlib import Path


df = pd.read_csv('1.csv')
# print(df)

df = df.set_index("family")
df = df.drop_duplicates()
print(len(df))

out2 = open("all_qsub.sh","w")
i = 0
genus = ''
keyword = ''
action_list = []
vid_list = []
for folder, info in df.iterrows():
    if info['genus'] == genus or info['keyword'] == keyword:
        continue
    i+=1
    genus = info['genus'].replace(" ", "")
    keyword = info['keyword'].replace(" ", "")

    name = re.compile("[a-zA-Z]+").findall(folder)[0]
    Path('code1').mkdir(exist_ok=True)
    file = Path('code1')/f"run_{genus}_{keyword}.sh"
    with open(file,encoding='utf-8',mode='w') as out:
        out.write(f"""#!/bin/bash
#SBATCH -N 1
#SBATCH --partition=batch
#SBATCH -J {genus}
#SBATCH -o {genus}.%J.out
#SBATCH --mail-user=xiaoming-sudo@outlook.com
#SBATCH --mail-type=ALL
#SBATCH --time=24:00:00
#SBATCH --mem=50G
#SBATCH --ntasks-per-node=20\n""")
        out.write(f"""python main_mut_new_1.py "{folder}||{info['genus']}||{info['keyword']}"\n""")
    out2.write(f"sbatch {file}\n")
out2.close()