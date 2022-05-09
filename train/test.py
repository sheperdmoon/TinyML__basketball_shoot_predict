import numpy as np
noise_level = 20
padded_data = []
seq_length = 128
dim = 3
data = [[1,2,3],[4,5,6],[7,8,9]]
tmp_data = (np.random.rand(seq_length, dim) - 0.5) * noise_level + data[0]
print(tmp_data)
tmp_data[(seq_length -
          min(len(data), seq_length)):] = data[:min(len(data), seq_length)]
print(tmp_data)