#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 17:01:53 2018

@author: tpchen
"""


'''
parameters:
    BATCH_SIZE : 64


'''


import numpy as np
import os
from DataConverter import C_tune_converter, Mapping_writer, Mapping_charbaseforlarge, t20perline


class Gen_Data_loader():
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.token_stream = []

    def create_batches(self, data_file):
        self.token_stream = []
        with open(data_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Char based
                line = line.split()
                #change element to int
                parse_line = [int(x) for x in line]
                print(len(parse_line))
                # length must be 20 (stochastic protocal)
                if len(parse_line) == 20:
                    self.token_stream.append(parse_line)
        # cut the data into integer batches
        
        self.num_batch = int(len(self.token_stream) / self.batch_size)
        self.token_stream = self.token_stream[:self.num_batch * self.batch_size]
        print(self.token_stream,self.num_batch)
        self.sequence_batch = np.split(np.array(self.token_stream), self.num_batch, 0)
        
        self.pointer = 0

    def next_batch(self):
        ret = self.sequence_batch[self.pointer]
        self.pointer = (self.pointer + 1) % self.num_batch
        return ret

    def reset_pointer(self):
        self.pointer = 0


class Dis_dataloader():
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.sentences = np.array([])
        self.labels = np.array([])

    def load_train_data(self, positive_file, negative_file):
        # Load data
        positive_examples = []
        negative_examples = []
        with open(positive_file)as fin:
            for line in fin:
                line = line.strip()
                line = line.split()
                parse_line = [int(x) for x in line]
                positive_examples.append(parse_line)
        with open(negative_file)as fin:
            for line in fin:
                line = line.strip()
                line = line.split()
                parse_line = [int(x) for x in line]
                if len(parse_line) == 20:
                    negative_examples.append(parse_line)
        self.sentences = np.array(positive_examples + negative_examples)

        # Generate labels
        positive_labels = [[0, 1] for _ in positive_examples]
        negative_labels = [[1, 0] for _ in negative_examples]
        self.labels = np.concatenate([positive_labels, negative_labels], 0)

        # Shuffle the data
        shuffle_indices = np.random.permutation(np.arange(len(self.labels)))
        self.sentences = self.sentences[shuffle_indices]
        self.labels = self.labels[shuffle_indices]

        # Split batches
        self.num_batch = int(len(self.labels) / self.batch_size)
        self.sentences = self.sentences[:self.num_batch * self.batch_size]
        self.labels = self.labels[:self.num_batch * self.batch_size]
        self.sentences_batches = np.split(self.sentences, self.num_batch, 0)
        self.labels_batches = np.split(self.labels, self.num_batch, 0)

        self.pointer = 0


    def next_batch(self):
        ret = self.sentences_batches[self.pointer], self.labels_batches[self.pointer]
        self.pointer = (self.pointer + 1) % self.num_batch
        return ret

    def reset_pointer(self):
        self.pointer = 0


'''
if __name__ == '__main__':
    BATCH_SIZE = 5
    
    gen_data_loader = Gen_Data_loader(BATCH_SIZE)

    gen_data_loader.create_batches("inputf2.txt")
'''
    



'''
step by step:
    1) open abc file in the assigned folder
    2) find the row contains '6/8' or '4/4'
    3) find the tonel in the file
    4) shift the music to C maj
    5) ...?
    6) feed in to the model
'''

'''
first, ABCLoader transfer all data into aplicable data
'''
# 59 genre

class ABCLoader():
    def __init__(self):
        self.address = 0
        self.addressOut=0
        self.addressOut_completeChar=0
        
        self.adoReel = 0
        self.adoJig = 0
        self.adoNJNR = 0
        self.Gflag = 0
        #self.checkset= []
        self.checksetG=[]
        self.valid = ['A','B','C','D','E','F','G','a','b','c','d','e','f','g',1,2,3,4,5,6,7,8]
        
        self.set1 = ['Ador', 'Dmaj', 'A', 'Bdor', 'Emin', 
                     'Cmaj', 'Amix', 'Fdor', 'Edor', 'Emaj', 
                     'Emix', 'Fmaj', 'Dmin', 'Gmin', 'Dmix', 
                     'Amin', 'Ddor', 'Cdor', 'Amaj', 'Bmin', 
                     'Gdor', 'Gmix', 'Gmaj'] 
        self.notemap={'C':5,'D':7,'E':9,'F':10,
                      'G':12,'A':14,'B':16,'c':17,
                      'd':19,'e':21,'f':22,'g':24,
                      'a':26,'b':27}
        self.genremap1 = {'jig':101, 'barndance':102, 'reel':103, 'hornpipe':104
                          ,'waltz':105, 'slip':106, 'strathspey':107, 'polka':108,
                          'slide':109, 'three-two':110, 'mazurka':111}
        self.mar,self.mir = -99,9920
        self.check_unique_token={}
        self.chkmidi2={}
        #self.cnt = 1
        self.cnt = 34
        self.cnt2 = 1
        # ^  temp map's following note +1
        # =  use the original notemap
        # Ador: +4 Dmaj: -2
        

    #1)
    def checkGenre(self,line):
        if str(line[0]) == 'R' :
            majors = line.split(' ')
            majors[1] = majors[1].replace('\n','')
            if majors[1] not in self.checksetG:
                self.checksetG.append(majors[1])

    def fileopener(self):
        #self.outfile = open(self.addressOut,'w') # complete  
        #self.outfile_comchar = open(self.addressOut_completeChar,'w') # complete char
        
        self.outReel = open(self.adoReel,'w')
        self.outJig = open(self.adoJig,'w')
        self.outNJNR = open(self.adoNJNR,'w')

        for filename in os.listdir(self.address):
            
            tmpadd = self.address+'/'+filename
            try:
                f = open(tmpadd,'r')
                #self.datapreprocessing(f)
                #self.datapreprocessing_midi2largecharbase(f)
                self.datapreprocessing_midi2GenreClass(f)
                
            except:
                print(':(')
                
        #print(self.mar,self.mir) 
        #print(self.check_unique_token)
        print(self.chkmidi2,len(self.chkmidi2))
        #self.outfile.close()
        #self.outfile_comchar.close()
        self.outReel.close()
        self.outJig.close()
        return
    def datapreprocessing_midi2GenreClass(self,file):
        line = file.readline()
        while line:
            if str(line[0]) == 'R':
                tmpp = line.split(':')
                '''
                if tmpp[1] in self.chkmidi2:
                    self.chkmidi2[tmpp[1]]+=1
                else:
                    self.chkmidi2[tmpp[1]] = 1
                '''
                if tmpp[1] == 'jig\n' or tmpp[1] == 'double jig\n' or tmpp[1] == 'Double jig\n' or tmpp[1] == 'Hop, slip jig\n' or tmpp[1] == 'Slip jig\n' or tmpp[1] == 'Single jig\n':
                    self.Gflag = 'jig'
                elif(tmpp[1] == 'reel\n' or tmpp[1] == 'Reel\n'):
                    self.Gflag = 'reel'
                else:
                    self.Gflag = 'other :('

            if str(line[0]) == 'K':
                
                majors = line.split(':')
                majors[1] = majors[1].replace('\n','')
                
                if self.Gflag == 'jig':
                    uni,self.cnt2 = Mapping_charbaseforlarge(file,self.outReel,self.chkmidi2,self.cnt2)   
                elif self.Gflag == 'reel':
                    uni,self.cnt2 = Mapping_charbaseforlarge(file,self.outJig,self.chkmidi2,self.cnt2)
                else:
                    uni,self.cnt2 = Mapping_charbaseforlarge(file,self.outNJNR,self.chkmidi2,self.cnt2)
                    
                for k,v in uni.items():
                    if k not in self.chkmidi2:
                        self.chkmidi2[k] = v
                        
            line = file.readline()
            
    def datapreprocessing_midi2largecharbase(self,file):
        # check unique tokens
        
        line = file.readline()
        while line:
            if str(line[0]) == 'K':
                
                majors = line.split(':')
                majors[1] = majors[1].replace('\n','')
                uni,self.cnt2 = Mapping_charbaseforlarge(file,self.outfile_comchar,self.chkmidi2,self.cnt2)
                
                for k,v in uni.items():
                    if k not in self.chkmidi2:
                        self.chkmidi2[k] = v
                
            line = file.readline()
        
        
    def datapreprocessing(self,file):
        
        line = file.readline()
        while line:
            # use self.checkGenre to check genre
            #self.checkGenre(line)
            if str(line[0]) == 'K':
                
                majors = line.split(' ')
                majors[1] = majors[1].replace('\n','')
                #self.checkset.append(majors[1])
                #--------------------------------------file maker-------------------------------------#
                #shift tune
                tu = C_tune_converter(majors[1])
                print(tu)
                # recover tune and write it to same file
                maxer,miner = -99,99
                maxer,miner,uniques,self.cnt= Mapping_writer(self.outfile,self.outfile_comchar,file,tu,maxer,miner,self.check_unique_token,self.cnt)
                for k,v in uniques.items():
                    if k not in self.check_unique_token:
                        self.check_unique_token[k]= v
                
                self.mar = max(maxer,self.mar)
                self.mir = min(miner,self.mir)
                
                # start processing the music data from here
                break
        
                
                
                
                
            line = file.readline()
         
'''-------------- data preprocessing -----------------'''
     
if __name__ == "__main__":
    Loader = ABCLoader()
    #outputfile = open('/home/tpchen/Desktop/coen296/codes/TrainingData2.txt','w')
    Loader.addressOut = "/home/tpchen/Desktop/coen296/codes/TrainingData3.txt"
    Loader.addressOut_completeChar = "/home/tpchen/Desktop/coen296/codes/largeTrain.txt"
    Loader.address = "/home/tpchen/Desktop/coen296/codes/midifile2"
    
    Loader.adoReel = "/home/tpchen/Desktop/coen296/codes/AllReel.txt"
    Loader.adoJig = "/home/tpchen/Desktop/coen296/codes/AllJig.txt"
    Loader.adoNJNR = "/home/tpchen/Desktop/coen296/codes/NJNR.txt"
    
    Loader.fileopener()
    
    
    
    # ================================change to 20 per line ========================================
    #f = open("/home/tpchen/Desktop/coen296/codes/TrainingDataComChar.txt",'r')
    f = open("/home/tpchen/Desktop/coen296/codes/NJNR.txt",'r')
    #fw = open("/home/tpchen/Desktop/coen296/codes/TrainingDataComChar20.txt",'w')
    fw = open("/home/tpchen/Desktop/coen296/codes/TrainableNJNR.txt",'w')
    
    t20perline(f,fw)
    frame_num = 20
    
    x = f.readline()
    sli = x.split(' ')
    alll = []
    tmp = []
    tmpprev=[]
    for i in sli:
        if i != '100':
            tmp.append(i)
        else:
            tmp.append(i)
            alll.append(tmp)
            #print(tmp)
            tmp = []
            
    tmp = []
    for x in alll:

        if len(x) < frame_num:
            continue
        
        else:
            
            loops = int(len(x)/frame_num)
            for i in range(loops):
                tmp = x[frame_num*i:frame_num*(i+1)]
                for j in tmp:
                    fw.write(str(j))
                    fw.write(" ")
                fw.write("\n")
            final = x[len(x)-20:len(x)]
            for xi in final:
                fw.write(xi)
                fw.write(" ")
            fw.write("\n")

    
    # ================================================================================================
    '''
    #=============================len check================================
    ffw = open("/home/tpchen/Desktop/coen296/codes/TrainingDataComChar20.txt",'r')
    line = ffw.readline()
    
    while line:
        x = line.split(' ')
        print(len(x))
        line = ffw.readline()
    # =====================================================================
    '''


        
        
        
        
        
        
        
        
        