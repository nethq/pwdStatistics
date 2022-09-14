"""Script is used to analyse the complexity , strength and entropy of passwords in a file."""
from dataclasses import replace
from enum import unique
import errno
import sys
import math
from warnings import catch_warnings

data_format = ":*\n"
input_file = ""
output_file = ""
dict_paths = {}

def dict_sorted_by_value(dict,reverse=True):
    """Sorts a dictionary by value"""
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1],reverse=reverse)}

def sort_entropy(data):
    """Sorts the data by entropy"""
    print("Sorting data")
    data.sort(key=lambda x: float(x.split(":")[0]))
    return data

def best_matches_in_table(string ,dictionaryTable, minimalWordLenght):
    """Returns the best matches for a string in a dictionary table"""
    substrings = substring_match(string,dictionaryTable,minimalWordLenght)
    temp = string.lower()
    return_list = []
    if substrings[0] == "err":
        return "err"
    #find all complete configurations of the substrings from the dictioanry table that add up to the original word
    try:
        for i in range(len(substrings)):
            if substrings[i] in temp and len(substrings[i]) > 0:
                temp = temp.replace(substrings[i],"")
                return_list.append(substrings[i])
            if temp == "":
                break
        # sort the list so that the substrings are ordered like in the original string
        return_list = sorted(return_list, key=lambda x: string.lower().find(x.lower()))
        return return_list
    except:
        print("Error in best_matches_in_table. On string {}->{}| err = {}".format(string,substrings,sys.exc_info()))
        return []

def entropy_of_string(string):
    """Calculates the Shannon entropy of a string"""
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy

def generate_entropy_values(data):
    """Generate entropy values for each string in data. Returns a dictionary of the form {entropy : data}"""
    print("Calculating entropy values")
    entropy_data_map = {}
    for word in data:
        entropy = entropy_of_string(word)
        if entropy_data_map.get(entropy) == None:
            entropy_data_map[entropy] = []
        entropy_data_map[entropy].append(word)
    return sorted(entropy_data_map.items(),reverse=False)

def check_string(string, struct):
    string = str(string).lower().strip()
    if struct.get(string) != None:
        return True
    else:
        return False

def get_replacement_string(string,struct):
    """Gets the replacement string for a string"""  
    string = string.lower().strip()
    if string in struct:
        return struct[string]

def args():
    """Checks for arguments"""
    print("Checking for arguments")
    #-i <input-file> -o <output-file> -f <data-format> -m <mode> -d <dictionary-file1> <dictionary-file2> ...
    #data-format : ":*\n"- would get all data between ":" and "\n"
    #mode : "entropy" , "dictionary"
    # -d <dictionary-file1> <dictionary-file2> ... - would be used for dictionary mode
    # -l <number> - would be used to limit the lenght of the checked data
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-h":
            print("Usage :")
            print("-i <input-file> -o <output-file> -f <data-format> -m <mode> -d <dictionary-file1> <dictionary-file2> ...")
            print("-i = input file ; -o = output file ; -f = data format ; -m = mode ; -d = dictionary file ; -l = limit ; -h = help")
            print("mode : \"entropy\" , \"dict\", \"dr\"")
            print("-m entropy : calculates and writes the entropy of the data conforming to the filter")
            print("-m dict : checks the data for dictionary words")
            print("-m dr : checks the data for dictionary words and replaces them with a specified string")
            print("-m usum : generates a unique sum for each line, corelating to the enumerated dictionaries")
            print("-f \":*n\" -> would get all the data between : and n")
            print("-d <dictionary-file1> <dictionary-file2> ... - would be used for dictionary mode")
            print("-l <number> - would be used to limit the lenght of the checked data")
            print("-h : help")

            print("Example :")
            print("python3 upgraded-script.py -i passwords.txt -o output.txt -f \":*n\" -m entropy")
            print("python3 upgraded-script.py -i passwords.txt -o output.txt -f \":*n\" -m dict -d dictionary1.txt dictionary2.txt")
            print("python3 upgraded-script.py -i passwords.txt -o output.txt -f \":*n\" -m dr -d dictionary1.txt=\"~W~\" dictionary2.txt=\"~N~\"")
            sys.exit(0)
        if sys.argv[i] == "-i":
            input_file = sys.argv[i+1]
        elif sys.argv[i] == "-o":
            output_file = sys.argv[i+1]
        elif sys.argv[i] == "-f":
            data_format = sys.argv[i+1].replace("\"","")
        elif sys.argv[i] == "-m":
            mode = sys.argv[i+1]
        elif sys.argv[i] == "-d":
            if sys.argv[i+1] == "":
                print("No dictionary files specified")
                sys.exit(1)
            elif mode == "dr":
                for j in range(i+1,len(sys.argv)):
                    if "\"" in sys.argv[j]:
                        sys.argv[j] = sys.argv[j].replace("\"","")
                    if "=" in sys.argv[j]:
                        dict_paths[sys.argv[j].split("=")[0]] = sys.argv[j].split("=")[1]
                    else:
                        dict_paths[sys.argv[j]] = sys.argv[j]
            elif mode == "dict" or mode == "usum":
                for j in range(i+1,len(sys.argv)):
                    dict_paths[sys.argv[j]] = sys.argv[j]
    if input_file == "" or output_file == "" or data_format == "" or mode == "":
        print("Invalid arguments")
        sys.exit(1)
    return input_file, output_file, data_format, mode

def dictionary_to_table(file,substituteString):
    """Loads a file into ram , returns a dictionary with the strings in the file as keys and the substituteString as values"""
    table = {}
    with open(file) as f:
        for line in f:
            line = line.strip().lower()
            if line == "":
                continue
            else:
                table[line] = substituteString
    return table

def import_data(file, data_format):
    """Extracts data using the format. Returns a list of the data."""
    data = []
    data_prefix =""
    data_suffix =""
    if not "*" in data_format:
        print("Invalid data format")
        sys.exit(1)
    elif data_format == "*":
        with open(file) as f:
            for line in f:
                data.append(line.strip())
        return data
    else:
        data_prefix = data_format.split("*")[0]
        data_suffix = data_format.split("*")[1]
    #open file with utf-8
    with open(file, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if data_prefix in line:
                data.append(line.split(data_prefix)[1].split(data_suffix)[0].strip())
    return data

def write_to_file(file, data):
    #check if data type is list
    if type(data) == list:
        with open(file, "w") as f:
            for line in data:
                if "\n" in line:
                    f.write(line)
                else:
                    f.write(line + "\n")
    elif type(data) == dict:  
        data = dict_sorted_by_value(data)
        with open(file, "w") as f:
            for key in data:
                string = str(key) + " : " + str(data[key]) + "\n"
                f.write(string)
        
    print("Written : " + str(len(data)) + " lines to file : " + file)

def dictionary_mode(data, dict_paths , limit):
    word_table = {}
    return_table = {}
    for key in dict_paths:
        word_table.update(dictionary_to_table(key,dict_paths[key]))
    for word in data:
        return_table[word] = substring_match(word,word_table,limit)
    return return_table

def unique_int_relation_table(dict_paths):
    """return dict : {<dict-path>:<replacement-int>...} Generates a unique int for each dictionary file"""
    table = {}
    i = 0
    for key in dict_paths:
        table[key] = pow(2,i)
        i += 1
    return table

def singular_usum(word,subStrLenLimit,unique_ints,word_table,debugMode=False):
    """return int : <unique-sum> Generates a unique sum for each word"""
    best_substring_matches_of_word = best_matches_in_table(word,word_table,subStrLenLimit)
    sum = 0
    for match in best_substring_matches_of_word:
        sum += unique_ints[word_table[match]]
    if debugMode:
        print("{}:{}".format(sum,word))
    return sum

def unique_sum_mode(data,dict_paths,limit,debugMode=False):
    """Generates a unique sum for each line of data , based on the dictionaries"""
    word_table = {}
    return_table = {}
    for key in dict_paths:
        word_table.update(dictionary_to_table(key,dict_paths[key]))
    unique_ints = unique_int_relation_table(dict_paths)
    print("\nUnique ints : " + str(unique_ints))
    for word in data:
        return_table[word] = singular_usum(word,limit,unique_ints,word_table,debugMode)
    return return_table
#todo
def substring_match(word, table,wordLenghtFilter, inverse = False, completeMatches = False):
    """Searches all sequential substring of the given word and returns all matches in the table. If inverse=true , starts from the end of the word, elsewise it starts from the beginning."""
    returnVar = []
    if inverse:
        for i in range(len(word)+1):
            for j in range(i+1,len(word)+1):
                tempword = str(word[i:len(word)-j]).lower().strip()
                if tempword in table and len(tempword) >= wordLenghtFilter:
                    returnVar.append(tempword)
    else:
        for i in range(len(word)):
            for j in range(i+1,len(word)+1):
                tempword = str(word[i:j]).lower().strip()
                if tempword in table and len(tempword) >= wordLenghtFilter:
                    returnVar.append(tempword)
    if len(returnVar) == 0:
        return "None"
    return sorted(returnVar, key=len, reverse=True)

def dictionary_replace_mode(data,dict_paths,limit):
    """Checks the data for dictionary words and replaces them with a specified string"""
    print("Running dictionary replace check")
    data_dict = []
    table = {}
    for dict_path in dict_paths:
        table.update(dictionary_to_table(dict_path,dict_paths[dict_path]))
    for word in data:
        temp = str(word).lower().strip()
        substring_matches = substring_match(temp,table,limit)
        if substring_matches != None:
            for match in substring_matches: 
                temp = temp.replace(match,table[match])
        data_dict.append("{}:[{}]\n".format(temp,word))
    return data_dict

def main():
    input_file, output_file, data_format, mode = args()
    print("Input file : " + input_file)
    print("Output file : " + output_file)
    print("Data format : " + data_format)
    print("Mode : " + mode)
    print("Dictionaries : " + str(dict_paths))
    if "-l" in sys.argv:
        limit = int(sys.argv[sys.argv.index("-l")+1])
    else: 
        limit = 4#default limit
    data = import_data(input_file, data_format)
    if mode == "dict":
        data = dictionary_mode(data,dict_paths,limit)
    elif mode == "dr":
        data = dictionary_replace_mode(data,dict_paths,limit)
    elif mode == "entropy":
        data = generate_entropy_values(data)
    elif mode == "usum":
        data = unique_sum_mode(data,dict_paths,limit)
    write_to_file(output_file, data)

main()