"""Script is used to analyse the complexity , strength and entropy of passwords in a file."""
from curses.ascii import isalpha
from operator import truediv
import sys
import math
from webbrowser import get
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
            print("-f :*n -> would get all the data between : and n")
            print("-d <dictionary-file1> <dictionary-file2> ... - would be used for dictionary mode")
            print("-l <number> - would be used to limit the lenght of the checked data")
            print("-h : help")
            print("\n\n\n")
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
    with open(file) as f:
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
    with open(file, "w") as f:
        for line in data:
            f.write(line + "")
    print("Written : " + str(len(data)) + " lines to file : " + file)

def dictionary_mode(data,dict_paths,limit):
    """Checks the data for dictionary words"""
    print("Running dictionary check")
    data_dict = []
    table = {}
    for key in dict_paths:
        table.update(dictionary_to_table(key,dict_paths[key]))
    for word in data:
        for i in range(len(word)):
            for j in range(i+1+limit,len(word)+1):
                tempword = str(word[i:j]).lower().strip()
                if tempword in table:
                    data_dict.append(word+":[{}][{}]\n".format(table[tempword],tempword))
                    break
    
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
    write_to_file(output_file, data)

# table = {}
# table.update(dictionary_to_table("words.txt","1"))
# table.update(dictionary_to_table("m-f-names.txt","2"))
# print("Checking {} -> {}".format("password",check_string("password",table)))
# print("Checking {} -> {}".format("PassworD",check_string("pass",table)))
# print("Replacement of {} : {}".format("password",get_replacement_string("password",table)))
# print("Replacement of {} : {}".format("John",get_replacement_string("jOhn",table)))

main()