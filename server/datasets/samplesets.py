import pandas as pd

base_path = 'C:/Users/LanLe/datasets/'
dirs = ['LFM-1B', 'LFM-360K', 'ML-25M', 'ML-100K']
new_paths = [(x,x + '/' + x + '.tsv') for x in dirs]
for (name,path) in new_paths:
    df = pd.read_csv(base_path+path, sep='\t', header=None)
    sample_size = 727
    if name == 'LFM-1B' or name == 'ML-25M':
        sample_size = 10000
    df.sample(sample_size).to_csv(path, sep='\t', header=None)
