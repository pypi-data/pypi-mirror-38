from pypairs import wrapper
import pandas as pd



#t = wrapper.sandbag_from_file("/Users/rfechtner/Desktop/ICMData/TrainingDataCombined/training_matrix.csv", "/Users/rfechtner/Desktop/ICMData/TrainingData1/cellAnnotation-sub.tsv", sep_annotation="\t", filter_genes_dispersion=True, processes=7, fraction=0.7, rm_zeros=True, random_subset=5)
#y = wrapper.sandbag_from_file("/Users/rfechtner/Desktop/ICMData/TestingData/sub/GSM2098545_scrbseq_2i-sub.txt",t)

a = pd.read_csv("/Users/rfechtner/Desktop/ICMData/TrainingDataCombined/training_matrix.csv")
a.set_index("Unnamed: 0", inplace=True)
b = pd.read_csv("/Users/rfechtner/Desktop/ICMData/TrainingData3/counttable_es-sub.csv", sep=" ")
b.set_index("Unnamed: 0", inplace=True)

c = a.join(b, how='outer')
c = c[~c.index.duplicated(keep='first')]
c.to_csv("/Users/rfechtner/Desktop/ICMData/TrainingDataCombined/training_matrix2.csv")
print("Done")