#--------------------------------
#This script gets the least utilization percentage of every last material sheet from
#the entire project after clicking on the optimization button
#
#Note: Before using this script, you MUST click on optimizer button first
#--------------------------------

import os
from pathlib import Path
import re
import time
import pyperclip


def main():

    NETSOL_PERCENTAGE = 50

    filePath = os.getcwd()
    path = Path(filePath)
    filePath = path.parent.parent.absolute() / "Data"
    projectName = input("Enter Project Name: ")
    if (projectName.strip() == ""):
        #projectName =os.path.basename(filePath)
        #print("Input Project Name")
        main()
           
    inptPrcnt = inputPercentage(NETSOL_PERCENTAGE)
                   
    file=filePath.__str__()+"\\"+projectName+".R41"
    print(file)

    try:
        res_arr = findLowNetsol(file, inptPrcnt)
        
        if (len(res_arr) > 0):
            if (res_arr[0] == "error"):
                print("Error: you MUST click on optimizer button before using this script")
            else:
                #print to screen (line by line)
                print("\n".join(res_arr))
            
                #copy to clipboard
                copyClipboard(res_arr)
                
                #print to paper
                printToPaper(res_arr, inptPrcnt, projectName)
                return
        else:
            print("No results, try to use other percentage %")
            
    except:
        print("Error: File was not found!!")
        main()
			
 
    




def findLowNetsol(f, perc):
    match_string = "LAYOUTS-"
    all_list = []
    results = []
    with open(f, 'r') as file:
        filedata = file.read()
        filedata_arr= filedata.split('\n')
        
        single_list = []
        for i in range(len(filedata_arr)-1) :
            if ('NETTOPP' in filedata_arr[i] or 'BRUTOPP' in filedata_arr[i] or ('PP' in filedata_arr[i] and 'BEM' in filedata_arr[i+1]) or 'BUNDLENO' in filedata_arr[i]):      
                single_list.append(filedata_arr[i])
                
            if (len(single_list) == 4):
                NETTOPP = int(''.join([n for n in single_list[0] if n.isdigit()]))
                BRUTOPP = int(''.join([n for n in single_list[1] if n.isdigit()]))
                netsolResult = NETTOPP*100/BRUTOPP
                single_list.append(netsolResult)
                all_list.append(single_list)
                
                #print(single_list[2])
                if ('wincut' not in single_list[2] and 'XML' not in single_list[2] ):
                    return ["error"]
                single_list[2] = Path(filedata_arr[i][2:]).stem
                single_list = []
    
    
    all_list_filtered = []  
    for i in range(len(all_list)-1) :
        if (all_list[i][2] == all_list[i+1][2]):
            continue
        else:
            if (all_list[i][4] < perc):
                all_list_filtered.append(all_list[i])
                rowNum = ''.join([n for n in all_list[i][3] if n.isdigit()])
                results.append(rowNum)
    if (all_list[-1][4] < perc):
        all_list_filtered.append(all_list[-1])
        rowNum = ''.join([n for n in all_list[-1][3] if n.isdigit()])
        results.append(rowNum)
        
    return results 







def inputPercentage(default_percent):

    while True:
        utilPercent = input("Enter utilization percentage %: ")
    
        if (utilPercent == ""):
            utilPercent = default_percent
            break
        else:
            if (utilPercent.isnumeric()):
                utilPercent = int(utilPercent)
                if (utilPercent in range(1,100)):
                    break
                else:    
                    print("Error: Please enter valid number betwen 1 and 100")                  
            else:
                print("Error: Please enter valid number betwen 1 and 100")
                  
            
    return utilPercent




def copyClipboard(lst):
    str = ','.join(lst)
    pyperclip.copy(str)



def printToPaper(lst, perc, project):
    with open('print_netsol_result.txt', 'w') as f:
        f.write(project.upper())
        f.write('\n')
        f.write("netsol < " + str(perc) + "%")
        f.write('\n')
        f.write('------------------')
        f.write('\n')
        for line in lst:
            f.write(line)
            f.write('\n')   
        f.write('\n')
        f.write('------------------')
        f.write('\n')
        f.write('Total: ' + str(len(lst)) + ' documents')
        
        
    os.startfile("print_netsol_result.txt", "print")

    #delete file after printing
    #time.sleep(4) 
    #os.remove("print_netsol_result.txt")        















if __name__ == "__main__":
    main()


