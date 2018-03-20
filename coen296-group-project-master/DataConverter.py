#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 19:03:43 2018

@author: tpchen
"""

def handle_everything(para,storehere,mapper):
    note = ['A','B','C','D','E','F','G','a','b','c','d','e','f','g']
    the_num = -9999
    for tok in para: # para = ['"G"','' ,'A2B','G6','GF','B,2']
        if tok[0] == '"': # the tonel indicator, ignore
            continue
        # if tok is ABCDEFGabcdefg, start manipulating the number until the next letter.
        else:
            for char in tok:
                if char in note and the_num == -9999: # means it is the first char
                    the_num = mapper[char]
                    
                if char in note and the_num != -9999: # means we've meet the next note
                    storehere.append(the_num)
                    the_num = mapper[char]

    return storehere
def Mapping_charbaseforlarge(inf,ouf,uni,cnt):
    line = inf.readline()
    array = []
    while line:
        x = line.split('|')
        for i in x:
            if i != '' and i !='\n':
                for char in i:
                    if char in uni:
                        array.append(str(uni[char]))
                    if char not in uni:
                        uni[char] = cnt
                        array.append(str(uni[char]))
                        cnt+=1
        
        line = inf.readline()
    for writedown in array:
        ouf.write(writedown)
        ouf.write(" ")
    ouf.write("100 ")
    return uni,cnt

def Mapping_writer(out,out_comchar,infile,mapper,dimension_max,dimension_min,uniques,cnt):
    # put a genre as start token :D
    
    '''
    input:
        1.genre 2.several notes
        
        runrunrun....
        
        write down :D
        
    '''
    line = infile.readline()
    array =[]

    while(line):
        #print(line)
        line= infile.readline()
        x =line.split('|')
        #print(x)
        for i in x:
            # ----------------------------------tokenize-----------------------------------
            #paragraph = i.split(' ')
            #array = handle_everything(paragraph,array,mapper)
            
            
            if i != '' and i != '\n':
                for index,char in enumerate(i):
                    #complete char base (without |, of course)
                    '''
                    if char in uniques:
                        array.append(str(uniques[char]))
                    if char not in uniques :
                        uniques[char] = cnt
                        array.append(str(uniques[char]))
                        cnt +=1
                    '''
                        
         
                    #char base w/ blah blah feature
                    
                    if char in mapper:
                        dimension_max = max(dimension_max,mapper[char])
                        dimension_min = min(dimension_min,mapper[char])
                        array.append(str(mapper[char]))
                    else:
                        if char in uniques:
                            array.append(str(uniques[char]))
                        if char not in uniques :
                            uniques[char] = cnt
                            array.append(str(uniques[char]))
                            cnt +=1
                        
    #total char base       
    '''        
    #print(array)
    print(uniques)
    #complete char base (without any modification)
    for writedown in array:
        out_comchar.write(writedown)
        out_comchar.write(" ")
    out_comchar.write("100 ")
    '''
    
    #with tune shift
    
    
    for writedown in array:
        out.write(writedown)
        out.write(" ")
    out.write("110 ")
    
    
    
    
    
    return dimension_max,dimension_min,uniques,cnt

def C_tune_converter(char):
    # C is 6, 6 is C
    #max : 33 min : 1
    tu = {'C':6,'D':8,'E':10,'F':11,
          'G':13,'A':15,'B':17,'c':18,
          'd':20,'e':22,'f':23,'g':25,
          'a':27,'b':28}
    
    if char == 'Ador':
        tu['F']+=1
        tu['f']+=1
        for k,v in tu.items():
            tu[k] = v + 3
    # D major 
    elif char == 'Dmaj':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1

        for k,v in tu.items():
            tu[k] = v - 2
    # A
    elif char == 'A':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1
        tu['g']+=1
        tu['G']+=1
        for k,v in tu.items():
            tu[k] = v + 3
    # B dorian
    elif char == 'Bdor':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1
        tu['g']+=1
        tu['G']+=1
        for k,v in tu.items():
            tu[k] = v + 1
    # E minor
    elif char == 'Emin':
        tu['f']+=1
        tu['F']+=1

        for k,v in tu.items():
            tu[k] = v - 4
    # C major
    #elif char == 'Cmaj':
    
    # A mixolydian
    elif char == 'Amix':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1

        for k,v in tu.items():
            tu[k] = v + 3
    # F dorian
    elif char == 'Fdor':
        tu['A']-=1
        tu['a']-=1
        tu['B']-=1
        tu['b']-=1
        tu['E']-=1
        tu['e']-=1

        for k,v in tu.items():
            tu[k] = v - 5
    # E dorian
    elif char == 'Edor':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1

        for k,v in tu.items():
            tu[k] = v - 4
            
    # E major
    elif char == 'Emaj':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1
        tu['G']+=1
        tu['g']+=1
        tu['D']+=1
        tu['d']+=1

        for k,v in tu.items():
            tu[k] = v - 4
    # E mixolydian
    elif char == 'Emix':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1
        tu['G']+=1
        tu['g']+=1

        for k,v in tu.items():
            tu[k] = v - 4
    # F major
    elif char == 'Fmaj':
        tu['B']-=1
        tu['b']-=1

        for k,v in tu.items():
            tu[k] = v - 5
    # D minor
    elif char == 'Dmin':
        tu['B']-=1
        tu['b']-=1

        for k,v in tu.items():
            tu[k] = v - 2
    # G minor
    elif char == 'Gmin':
        tu['B']-=1
        tu['b']-=1
        tu['E']-=1
        tu['e']-=1

        for k,v in tu.items():
            tu[k] = v -5
    # D mixolydian
    elif char == 'Dmix':
        tu['f']+=1
        tu['F']+=1

        for k,v in tu.items():
            tu[k] = v - 2
    # A minor:
    elif char == 'Amin':

        for k,v in tu.items():
            tu[k] = v + 3
    # D dorian
    elif char == 'Ddor':

        for k,v in tu.items():
            tu[k] = v + 1
    # C dorian
    elif char == 'Cdor':
        tu['B']-=1
        tu['b']-=1
        tu['E']-=1
        tu['e']-=1
    # A major
    elif char == 'Amaj':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1
        tu['G']+=1
        tu['g']+=1

        for k,v in tu.items():
            tu[k] = v + 3
    # B minor
    elif char == 'Bmin':
        tu['f']+=1
        tu['F']+=1
        tu['c']+=1
        tu['C']+=1

        for k,v in tu.items():
            tu[k] = v + 1
    # G dorian
    elif char == 'Gdor':
        tu['b']-=1
        tu['B']-=1

        for k,v in tu.items():
            tu[k] = v + 5
            
    # G mixolydian
    elif char == 'Gmix':
        for k,v in tu.items():
            tu[k] = v + 5
    
    # G major
    elif char == 'Gmaj':
        tu['f']+=1
        tu['F']+=1
        for k,v in tu.items():
            tu[k] = v + 5
    return tu