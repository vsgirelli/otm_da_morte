import re

def escreveN_M(N_M, file_to_write):
    file_to_write.write("set N := ")
    for i in range (int(N_M[0])):
        i_to_write = i + 1
        file_to_write.write(str(i_to_write) + " ")

    file_to_write.write(";\n\n")

    file_to_write.write("set M := ")
    for i in range (int(N_M[1])):
        file_to_write.write(str(i) + " ")

    file_to_write.write(";\n\n")

    return

def escreveParamTime(line, file_to_write, task_num):
    line_normalized = re.sub("( |\n)+", " ", line)
    groups = re.findall("[0-9]+ [0-9]+", line_normalized)
    for group in groups:
        file_to_write.write(str(task_num) + " " + group + "\n")

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

        dat_inst.write(";")

    else:
        print("Nao foi possivel abrir ou escrever nos arquivos.")

    return


__main__("VFR10_15_1_Gap.txt", "VFR10_15_1_Gap.dat")
