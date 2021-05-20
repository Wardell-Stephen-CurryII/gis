import pandas as pd

a = [['1','2','3'],['1.0','2.0','3.0']]
result = pd.DataFrame(a)
result.to_csv('data/result/test.csv')