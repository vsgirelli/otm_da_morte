import re

ARQUIVOS_TXT = ["VFR100_60_1_Gap.txt", "VFR10_15_1_Gap.txt", "VFR20_10_3_Gap.txt", "VFR20_20_1_Gap.txt", "VFR500_40_1_Gap.txt",
                "VFR500_60_3_Gap.txt", "VFR600_20_1_Gap.txt", "VFR60_10_3_Gap.txt", "VFR60_5_10_Gap.txt", "VFR60_5_10_Gap.txt",
                "VFR700_20_10_Gap.txt" ]

def escreveN_M(N_M, file_to_write):
    file_to_write.write("set N := ")
    for i in range (int(N_M[0])):
        i_to_write = i + 1
        file_to_write.write(str(i_to_write) + " ")

    file_to_write.write(";\n\n")

    file_to_write.write("set M := ")
    for i in range (int(N_M[1])):
        i_to_write = i + 1
        file_to_write.write(str(i_to_write) + " ")

    file_to_write.write(";\n\n")

    file_to_write.write("param m := " + str(N_M[1] + ";\n\n"))

    return

def escreveParamTime(line, file_to_write, task_num):
    line_normalized = re.sub("( |\n)+", " ", line)
    groups = re.findall("[0-9]+ [0-9]+", line_normalized)
    for group in groups:
        group_elements = group.split(" ")
        maq_to_write = int(group_elements[0]) + 1
        file_to_write.write(str(task_num) + " " + str(maq_to_write) + " " + str(group_elements[1]) + "\n")

    return

def __main__(file_to_read, dat_to_create):

    txt_inst = open(file_to_read, "r")
    dat_inst = open(dat_to_create, "w+")

    if txt_inst.mode == 'r' and dat_inst.mode == 'w+':
        # Primeira linha do txt contem numero de maquinas e tarefas
        N_M = re.sub("( |\n)+", " ", txt_inst.readline()).split(" ")
        escreveN_M(N_M, dat_inst)
        dat_inst.write("param: T: time :=\n")
        task_num = 1
        for line in txt_inst:
            escreveParamTime(line, dat_inst, task_num)
            task_num+=1

        dat_inst.write(";\n")
    else:
        print("Nao foi possivel abrir ou escrever nos arquivos.")

    return


for file_to_read in ARQUIVOS_TXT:

    __main__(file_to_read, file_to_read.replace("txt", "dat"))