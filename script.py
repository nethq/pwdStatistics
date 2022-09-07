#!/usr/bin/env python
# -*- coding: utf-8 -*-
from curses.ascii import isalpha
from dataclasses import replace
import math
import sys


#create a dictionary of names
names = {}
words = {}
name_dict_path = ""
word_dict_path = ""
output_file_path = "default_output.txt"

def load_names_to_ram(dictionary_path):
    f = open(dictionary_path)
    print("Loading names dictionary "+ dictionary_path+ " to ram")
    for line in f:
        line = line.lower().strip()
        names[hash(line)]=line
    print("Dictionary loaded")

def load_words_to_ram(dictionary_path):
    f = open(dictionary_path)
    print("Loading dictionary "+ dictionary_path+ " to ram")
    for line in f:
        line = line.lower().strip()
        words[hash(line)]=line
    print("Dictionary loaded")

def check_name(subString):
    subString = str(subString).lower().strip()
    if hash(subString) in names:
        if names[hash(subString)]==subString:
            return True
        else: 
            return False
    else:
        return False
        
def check_word(subString):
    subString = str(subString).lower().strip()
    if hash(subString) in words:
        if words[hash(subString)]==subString:
            return True
        else: 
            return False
    else:
        return False

def extract_patterns_dict_compare(file):
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
                #start from complete string and remove one character at a time
                for i in range(len(passw)):
                    buffer = passw[:i] + passw[i+1:]
                    if check_word(buffer):
                        result.append("Word | " + buffer + " -> " + email + ":" + passw)
                    if check_name(buffer):
                        result.append("Name | " + buffer + " -> " + email + ":" + passw)

    return result

def shannon_entropy(inputString):
    if inputString == "":
        return 0
    else:
        return -sum([(float(inputString.count(c))/len(inputString))*math.log(float(inputString.count(c))/len(inputString),2) for c in dict.fromkeys(inputString)])

def args():
    # -i <input-file> -o <output-file>
    if len(sys.argv) >= 7 and sys.argv[6]!="dictionary":
        input_file = sys.argv[2]
        output_file_path = sys.argv[4]
        mode = sys.argv[6]
        return input_file, output_file_path, mode
    elif len(sys.argv) >= 7 and sys.argv[6]=="dictionary":
        input_file = sys.argv[2]
        output_file_path = sys.argv[4]
        mode = sys.argv[6]
        name_dict_path = sys.argv[7]
        word_dict_path = sys.argv[8]
        return input_file, output_file_path, mode, name_dict_path, word_dict_path

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
        print("Usage: python script.py -i <input-file> -o <output-file> -m dictionary <name-dictionary> <word-dictionary>")
        sys.exit(1)
    else:
        if args()[2] == "entropy":
            write_to_file(args()[1], sort_by_shannon_entropy(analyse_through_shannon_entropy(args()[0])))
        elif args()[2] == "dictionary":
            load_names_to_ram(args()[3])
            load_words_to_ram(args()[4])
            write_to_file(args()[1], extract_patterns_dict_compare(args()[0]))
        else:
            print("Invalid mode")
            print("Usage: python script.py -i <input-file> -o <output-file> -m <mode>")
            print("Modes : 'entropy' , 'dictionary'")
            print("Usage: python script.py -i <input-file> -o <output-file> -m dictionary <name-dictionary> <word-dictionary>")
            sys.exit(1)
main()


                                    

            