"""Script is used to analyse the complexity , strength and entropy of passwords in a file."""
from curses.ascii import isalpha
import sys
import math
data_format = ":*\n"
input_file = ""
output_file = ""
dict_paths = []

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

def check_string(string,hashTable):
    teststr = str(string).lower().strip()
    if hash(teststr) in hashTable:
        if teststr == hashTable[hash(teststr)]:
            return True
        else:
            return False
    else:
        return False

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
            print("data-format : uses * as a wildcard")
            print("mode : \"entropy\" , \"dictionary\"")
            print("-d <dictionary-file1> <dictionary-file2> ... - would be used for dictionary mode")
            print("-l <number> - would be used to limit the lenght of the checked data")
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
            for j in range(i+1, len(sys.argv)):
                dict_paths.append(sys.argv[j])
    if input_file == "" or output_file == "" or data_format == "" or mode == "":
        print("Invalid arguments")
        sys.exit(1)
    return input_file, output_file, data_format, mode

def dictionary_to_hashTable(file):
    print("Loading dictionary : " + file)
    hashTable = {}
    with open(file) as f:
        for line in f:
            if line == "":
                continue
            else:
                hashTable[hash(line.lower().strip())] = line.lower().strip()
    return hashTable

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

def main():
    input_file, output_file, data_format, mode = args()
    print("Input file : " + input_file)
    print("Output file : " + output_file)
    print("Data format : " + data_format)
    print("Mode : " + mode)
    limit = 3 #default
    if "-l" in sys.argv:
        limit = int(sys.argv[sys.argv.index("-l")+1])
    print("Limit : " + str(limit))
    data = data_from_file(input_file, data_format)
    return_data = []
    print("Data loaded from file")
    if mode == "entropy":
        data = data_entropy_check(data)
    elif mode == "dictionary":
        for path in dict_paths:
            hashTable = dictionary_to_hashTable(path)
            for word in data:
                for i in range(len(word)):
                    for j in range(i+limit, len(word)):
                        if check_string(str(word[i:j]),hashTable):
                            return_data.append("("+path+")-["+word[i:j]+"]={"+word+"}\n")
                            break
                            
    else:
        print("Invalid mode")
        sys.exit(1)
    write_to_file(output_file, return_data)
    print("Finished")

main()