#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import replace
import math
from operator import contains
import sys

#create a dictionary of names
names = {}
words = {}
output_file_path = "default_output.txt"

def load_names_to_ram(dictionary_path):
    f = open(dictionary_path)
    print("Loading names dictionary "+ dictionary_path+ " to ram")
    for line in f:
        names[hash(line)]=line
    print("Dictionary loaded")

def load_words_to_ram(dictionary_path):
    f = open(dictionary_path)
    print("Loading dictionary "+ dictionary_path+ " to ram")
    for line in f:
        words[hash(line)]=line
    print("Dictionary loaded")

def check_name(subString):
    try:        
        if subString == names[hash(subString)]:
            return True
        else:
            return False
    except:
        return False
        
def check_word(subString):
    try:        
        if subString == words[hash(subString)]:
            return True
        else:
            return False
    except:
        return False

def extract_patterns_dict_compare(file):
    print("Name dictionary path : ")
    name_dict_path = input()
    print("Word dictionary path : ")
    word_dict_path = input()
    load_words_to_ram(word_dict_path)
    load_names_to_ram(name_dict_path)
    result = []
    with open(file) as f:
        for line in f:
            print("Progress : " + line )
            if line == "":
                continue
            if ";" in line:
                line = line.replace(";",":")
            if not ":" in line:
                continue
            else :
                email = line.split(":")[0]
                passw = line.split(":")[1]
                buffer = ""
                for letter in passw:
                    buffer += letter
                    if check_word(buffer):
                        passw = passw.replace(buffer,"<word>")
                        buffer = ""
                    if check_name(buffer):
                        passw = passw.replace(buffer,"<name>")
                        buffer = ""
                result.append(email + ":" + passw)
                
             
    return result

def shannon_entropy(inputString):
    if inputString == "":
        return 0
    else:
        return -sum([(float(inputString.count(c))/len(inputString))*math.log(float(inputString.count(c))/len(inputString),2) for c in dict.fromkeys(inputString)])

def args():
    # -i <input-file> -o <output-file>
    if len(sys.argv) == 7:
        input_file = sys.argv[2]
        output_file_path = sys.argv[4]
        mode = sys.argv[6]
        return input_file, output_file_path, mode
    else:
        print("Invalid arguments")
        print("Usage: python script.py -i <input-file> -o <output-file> -m <mode>")
        print("Modes : 'entropy' , 'dictionary'")
        print("")
        sys.exit(1)
        
def write_to_file(file, patterns):
    with open(file, "w") as f:
        for pattern in patterns:
            f.write(str(pattern).replace("\n","") + "\n")
    print("Written to file - " + file)

#create new strings containing previous string and the shannon entropy of the password
def analyse_through_shannon_entropy(file):
    entropy_arr = []
    with open(file) as f:
        for line in f:
            if line == "":
                continue
            if ";" in line:
                line = line.replace(";",":")
            if not ":" in line:
                continue
            else :
                email = line.split(":")[0]
                passw = line.split(":")[1]
                #line to unicode
                new_line = str(shannon_entropy(passw))+ "->"+ email +":"+ passw
                entropy_arr.append(new_line)
    return entropy_arr
    
#sort the array by shannon entropy
def sort_by_shannon_entropy(entropy_arr):
    return sorted(entropy_arr, key=lambda x: float(x.split("->")[0]))

def main():
    if len(sys.argv) < 2:
        print("No arguments provided")
        print("Usage: python script.py -i <input-file> -o <output-file> -m <mode>")
        print("Modes : 'entropy' , 'dictionary'")
        sys.exit(1)
    else:
        input_file, output_file_path, mode = args()
        if mode == "entropy":
            entropy_arr = analyse_through_shannon_entropy(input_file)
            entropy_arr = sort_by_shannon_entropy(entropy_arr)
            write_to_file(output_file_path, entropy_arr)
        elif mode == "dictionary":
            patterns = extract_patterns_dict_compare(input_file)
            write_to_file(output_file_path, patterns)    
        else:
            print("Invalid mode")
            sys.exit(1)

    
main()

                    
                    
                                    

            