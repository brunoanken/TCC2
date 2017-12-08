import os
import subprocess
import sys

# TODO pensar na segurança dos arquivos criados
# AFINAL DE CONTAS O SEU TCC É NA ÁREA DE SEGURANÇA, NÉ...

os.chdir("/home/anken/Documents/TCC2/rede/data/01")


test = open('test.txt', 'w')
proc = subprocess.Popen(['nfdump', '-r', 'nfcapd.201303012355'],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

#ISSO DEU CERTO AHEUEAHAEUODHNSAOUDGWABIUYDPAGDFSAPIDUŚAGHDUIWGDPWAISA
for line in proc.stdout:
    sys.stdout.write(line)
    test.write(line)
proc.wait


#user = subprocess.check_output(['nfdump', '-r', 'nfcapd.201303012355', '-i', 'test.txt'])

#print("resultado: ", user)

# text_file = open("Output.txt", "w")
# text_file.write(str(user))
# text_file.close()

#os.system("nfdump -r nfcapd.201303012355 -o csv > output.csv")
#os.system("nfdump -R /home/anken/Documents/TCC2/dados_toledo/data/01 -o csv > output.csv")

# print('\ntest')
# print(test)
# print('\ntest')

# with open("Output.txt", "w") as text_file:
#     print(test, file=text_file)


#proc = subprocess.check_call(['nfdump',  '-r', 'nfcapd.201303012355'])
#output = proc.stdout.read()
# output = subprocess.Popen("nfdump", "-r", "nfcapd.201303012355")
# print ("Output: ", output)
