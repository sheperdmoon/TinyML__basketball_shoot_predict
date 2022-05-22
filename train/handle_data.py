import data_view as dv

file_name = input("请输入文本名称\n")
who = input("请输入收集者编号（lyl-0，xzy-1,xmh-2,ljr-3,mxd-4)\n")
file1 = 'data/' + file_name + '.txt'
# file1_5 = 'data/' + file_name + 'clean.txt'
file2 = 'data/' + file_name + 'final.txt'
# file_w = open(file1_5, 'w')
file_ww = open(file2, 'w')
to_discard = []

# with open(file1) as lines:
#     for line in lines:
#         if len(line) == 5:
#             continue
#         if line[0] == 'f':
#             file_w.write(" -,-,-\n")
#         else:
#             file_w.write(line)
# file_w.close()

count = 0
first = 1
with open(file1) as lines:
    for line in lines:
        if first == 1:
            if len(line) == 1:
                first = 0
                continue
            if len(line) >= 2 and line[len(line)-2] == '-':
                first = 0
            else:
                to_discard = [int(i) for i in line.split(',')]
                first = 0
                #print(to_discard)
                continue
        if len(line) >= 2:
            if line[len(line)-2] == '-':
                count += 1
        if to_discard.count(count) != 1:
            file_ww.write(line)
print("收集了", count - len(to_discard), "组数据")
file_ww.close()
dv.show(file2, int(who))
