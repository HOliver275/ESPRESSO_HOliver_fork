import os
import glob

""" 
Utility script to split a list of files into n lists of a specified length, and copy each sublist into its own folder. 

author: Helen Oliver 2024
"""

"""
A function to take a big list of files and split it into a list of smaller lists of specified length.

param: all_files, the original list of files
param: files_per_folder, the number of files to put into each list
param: num_folders, the number of lists of files to split the original list into
return: all_files, a list of lists of files 
"""
def divide_chipmunks(all_files, files_per_folder, num_folders):
    # the total number of files to be split into smaller lists
    total_num_files = files_per_folder * num_folders
    
    # looping till we've got all the files
    for i in range(0, total_num_files, files_per_folder): 
        yield all_files[i:i + files_per_folder]

"""
Takes a folder of .txt files, splits them into a list of lists of specified length, and copies each sublist into a folder.

"""        
def group_files_in_folder():
    # get all the files of type ".txt" in the given folder
    #all_txt_files = glob.glob('/Users/helenoliver/Documents/ESPRESSO/working/ESPRESSO_HOliver_fork/ESPRESSO_HOliver_fork/Automation/DatasetSplitter/testsource/*.dat')
    all_txt_files = glob.glob('/srv/datasets/healthdata/text/*.txt')
    # number of folders to copy them to
    num_folders = 5
    # number of files to copy into each folder
    files_per_folder = 2
    
    # split them into sublists
    sublists = list(divide_chipmunks(all_txt_files, files_per_folder, num_folders))

    # now copy the lists of files into folders
    for i in range(num_folders):
        os.system("mkdir -p sourcedir" + str(i))

        print("About to copy the following files: ")
        print(sublists[i])
        for j in sublists[i]:
            #print("copying " + j + " to /Users/helenoliver/Documents/ESPRESSO/working/ESPRESSO_HOliver_fork/ESPRESSO_HOliver_fork/Automation/DatasetSplitter/sourcedir" + str(i))
            print("copying " + j + " to /home/kho1v23/ESPRESSO_HOliver_fork/ESPRESSO_HOliver_fork/Automation/DatasetSplitter/sourcedir" + str(i))
            #os.system("cp %s %s"%(j, "/Users/helenoliver/Documents/ESPRESSO/working/ESPRESSO_HOliver_fork/ESPRESSO_HOliver_fork/Automation/DatasetSplitter/sourcedir"+str(i)))
            os.system("cp %s %s"%(j, "/home/kho1v23/ESPRESSO_HOliver_fork/ESPRESSO_HOliver_fork/Automation/DatasetSplitter/sourcedir"+str(i)))
   
group_files_in_folder()


