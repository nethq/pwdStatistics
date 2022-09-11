"""Script is used to analyse the complexity , strength and entropy of passwords in a file."""
from enum import unique
import sys
import math

data_format = ":*\n"
input_file = ""
output_file = ""
dict_paths = {}

def sort_by_entropy(data):
    """Sorts data by entropy"""
    print("Sorting data by entropy")
    data.sort(reverse=True)
    return data

def data_entropy_check(data):
    """Check all data entries for entropy"""
    print("Running entropy check")
    data_entropy = []
    for word in data:
        data_entropy.append(str(entropy_of_string(word))+":"+word)
    return sort_by_entropy(data_entropy)

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
            print("-f :*n -> would get all the data between : and n")
            print("-d <dictionary-file1> <dictionary-file2> ... - would be used for dictionary mode")
            print("-l <number> - would be used to limit the lenght of the checked data")
            print("-h : help")

            print("Example :")
            print("python3 upgraded-script.py -i passwords.txt -o output.txt -f :*n -m entropy")
            print("python3 upgraded-script.py -i passwords.txt -o output.txt -f :*n -m dict -d dictionary1.txt dictionary2.txt")
            print("python3 upgraded-script.py -i passwords.txt -o output.txt -f :*n -m dr -d dictionary1.txt=~W~ dictionary2.txt=~W~")
            sys.exit(0)
        if sys.argv[i] == "-i":
            input_file = sys.argv[i+1]
        elif sys.argv[i] == "-o":
            output_file = sys.argv[i+1]
        elif sys.argv[i] == "-f":
            data_format = sys.argv[i+1]
        elif sys.argv[i] == "-m":
            mode = sys.argv[i+1]
        elif sys.argv[i] == "-d":
            if sys.argv[i+1] == "":
                print("No dictionary files specified")
                sys.exit(1)
            elif mode == "dr":
                for j in range(i+1,len(sys.argv)):
                    if "=" in sys.argv[j]:
                        dict_paths[sys.argv[j].split("=")[0]] = sys.argv[j].split("=")[1]
                    else:
                        dict_paths[sys.argv[j]] = sys.argv[j]
            elif mode == "dict":
                for j in range(i+1,len(sys.argv)):
                    dict_paths[sys.argv[j]] = sys.argv[j]
    if input_file == "" or output_file == "" or data_format == "" or mode == "":
        print("Invalid arguments")
        sys.exit(1)
    return input_file, output_file, data_format, mode

def dictionary_to_table(file,substituteString):
    """Loads a file into ram , returns a dictionary with the strings in the file as keys and the substituteString as values"""
    print("Loading dictionary : " + file)
    table = {}
    with open(file) as f:
        for line in f:
            line = line.strip().lower()
            if line == "":
                continue
            else:
                table[line] = substituteString
    return table

def data_from_file(file, data_format):
    """Extracts data from a file using a format"""
    data = []
    data_prefix =""
    data_suffix =""
    if not "*" in data_format:
        print("Invalid data format")
        sys.exit(1)
    else:
        data_prefix = data_format.split("*")[0]
        data_suffix = data_format.split("*")[1]
    #open file with utf-8
    with open(file, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if data_prefix in line:
                data.append(line.split(data_prefix)[1].split(data_suffix)[0].strip())
    return data

def entropy_of_string(string):
    """Calculates the Shannon entropy of a string"""
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy

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
        with open(file, "w") as f:
            for key in data:
                f.write(key + " : " + str(data[key]) + "\n")
        
    print("Written : " + str(len(data)) + " lines to file : " + file)

def dictionary_mode(data, dict_paths , limit):
    word_table = {}
    return_table = {}
    for key in dict_paths:
        word_table.update(dictionary_to_table(key,dict_paths[key]))
    for word in data:
        return_buffer = []
        for i in range(len(word)):
            for j in range(i+limit,len(word)+1):
                tempword = str(word[i:j]).lower().strip()
                
                if word_table.get(tempword) != None:
                    return_buffer.append(tempword)
                    break
        if len(return_buffer) > 0:
            return_table[word] = return_buffer
    return return_table

def unique_int_relation_table(dict_paths):
    """Generates a unique integer identifier for each dictionary . Used for the unqsum mode"""
    table = {}
    i = 0
    for key in dict_paths:
        table[key] = pow(2,i)
        i += 1
    return table

def unique_sum_mode(data,dict_paths,limit):
    """Generates a unique sum for each line, corelating to the enumerated dictionaries"""
    print("Running unique sum check")
    data_dict = []
    dict_paths = unique_int_relation_table(dict_paths)
    table  = {}
    for dict in dict_paths:
        table.update(dictionary_to_table(dict,dict))
    for word in data:
        tempsum = 0
        for i in range(len(word)):
            for j in range(i+1+limit,len(word)+1):
                tempword = str(word[i:j]).lower().strip()
                if tempword in table:
                    tempsum += dict_paths[table[tempword]]
        data_dict.append(str(tempsum) + " : " + word)
    return data_dict
    
def dictionary_replace_mode(data,dict_paths,limit):
    """Checks the data for dictionary words and replaces them with a specified string"""
    print("Running dictionary replace check")
    data_dict = []
    table = {}
    for dict_path in dict_paths:
        table.update(dictionary_to_table(dict_path,dict_paths[dict_path]))
    for word in data:
        temp = word
        for i in range(len(word)):
            for j in range(i+1+limit,len(word)+1):
                tempword = str(word[i:j]).lower().strip()
                if tempword in table:
                    word = word.replace(tempword,table[tempword])
        data_dict.append("{}:[{}]\n".format(temp,word))
    return data_dict

def entropy_mode(data):
    """Calculates the entropy of the data"""
    print("Running entropy check")
    data_entropy = []
    for word in data:
        data_entropy.append(str(entropy_of_string(word) + ":" + word))
    return sort_by_entropy(data_entropy)

def sort_entropy(data):
    """Sorts the data by entropy"""
    print("Sorting data")
    data.sort(key=lambda x: float(x.split(":")[0]))
    return data

def main():
    input_file, output_file, data_format, mode = args()
    if "-l" in sys.argv:
        limit = int(sys.argv[sys.argv.index("-l")+1])
    else: 
        limit = 4#default limit
    data = data_from_file(input_file, data_format)
    if mode == "dict":
        data = dictionary_mode(data,dict_paths,limit)
    elif mode == "dr":
        data = dictionary_replace_mode(data,dict_paths,limit)
    elif mode == "entropy":
        data = entropy_mode(data)
    elif mode == "usum":
        data = unique_sum_mode(data,dict_paths,limit)
    write_to_file(output_file, data)

main()
# dict_paths = {}
# dict_paths = {"test.txt":"","test2.txt":"","test3.txt":"","test4.txt":"","test5.txt":""}
# print(unique_int_relation_table(dict_paths))