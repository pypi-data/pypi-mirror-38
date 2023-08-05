# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 09:00:00 2018

@author: srao
"""

import os
import glob
import subprocess
from multiprocessing import Process

def runSimulation(epVersion, parameterizeDir, programDir, folder):  
    cmd = os.path.join(programDir, "energyplus.exe")    
    idd = os.path.join(programDir, "ep"+str(epVersion)+".idd")
    outputDir = folder
    files = glob.iglob(os.path.join(outputDir, "*.idf"))
    for file in files:
        idf = file
    output = os.path.basename(idf)    
    output = os.path.splitext(output)[0]
    files = glob.iglob(os.path.join(parameterizeDir, "*.epw"))
    for fileName in files:
        weather = os.path.join(parameterizeDir, fileName)
    p = subprocess.Popen ([cmd, "-i", idd, "-d", outputDir, "-p", output, "-w", weather, idf],stdout=subprocess.PIPE, universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    for stdout_line in p.stdout:
        print(stdout_line)
    p.stdout.close()
    return_code = p.wait() 
    

if __name__ == '__main__':
    
    """multiprocess to run parallel simulations"""
    parameterizeDir =  os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')   
    programDir = os.path.dirname(os.path.abspath(__file__))
    modelRunsDir = os.path.join(parameterizeDir, "model runs")    
    folders = []
    for folder in os.listdir(modelRunsDir):
        if folder.startswith('Bundle-'):
            for file in os.listdir(os.path.join(modelRunsDir, folder)):
                if file.startswith('ESM'): 
                    folders.append(os.path.join(modelRunsDir, folder, file))      
    processes = []        
    for folder in folders:
        p = Process(target=runSimulation,args=(epVersion, parameterizeDir, programDir, folder,))
        processes.append(p)        
    for p in processes:
        p.start()
    for p in processes:
        p.join()