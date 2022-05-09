file = 'data/4-3.txt'
file1 = 'data/output_shoot_maxd.txt'
file2 = 'data/shoot/output_shoot_maxd.txt'
file_w = open(file1, 'w')
file_ww = open(file2, 'a')
#to_get = [1,2,3,4,5,6,7,8]

with open(file) as lines:
    for line in lines:
        if len(line) == 5:
            continue
        if line[0] == 'f':
            file_w.write(" -,-,-\n")
        else:
            file_w.write(line)
file_w.close()
count = 0
with open(file1) as lines:
    for line in lines:
        if len(line) >= 2:
            if line[1] == '-':
                count += 1
        #if to_get.count(count) == 1:
        file_ww.write(line)
print(count)
file_ww.close()
