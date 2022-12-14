**pwdStatistics
This script is created to work on files with the following formats "**text0**:**text1**\n"  
The script will test **text1** for the mode you specify.  
The script has functionality for scanning and comparing if **text1** contains words from dictionaries, which you will specify.  
You can get a dictionary of all the english words. The script executes in 0.5 secs for a set of 11k entries and a dictionary size of 490k, both names and words combined.  

>Usage: python script.py -i **input-file** -o **output-file** -m **mode**
>>Modes : 'entropy' , 'dictionary'
>>>Usage: python script.py -i **input-file** -o **output-file** -m dictionary **name-dictionary** **word-dictionary**
----
***Concerning the upgraded script :***  
The upgraded script is more efficient in terms of space complexity, as it uses different method for storing and manipulating the loaded dictionary data, and accesses it in constant time (O(1)).  
The upgraded script was created with functionality and flexibility in terms of the data inputs, the dictionary inputs , the dictionary word lenght check limits.   
All in all the the upgraded script is the one i'd recommend if you are using a specificly structured data files, for the input.  
>-i **input-file** -o **output-file** -f **data-format** -m **mode** -d **dictionary-file1** **dictionary-file2** ...  
>-i = input file ; -o = output file ; -f = data format ; -m = mode ; -d = dictionary file ; -l = limit ; -h = help  
>mode : \"entropy\" , \"dict\", \"dr\"  
>-m entropy : calculates and writes the entropy of the data conforming to the filter  
>-m dict : checks the data for dictionary words  
>-m dr : checks the data for dictionary words and replaces them with a specified string  
>-f :*n ->would get all the data between : and n  
>-d **dictionary-file1** **dictionary-file2** ... - would be used for dictionary mode  
>-l <number** - would be used to limit the lenght of the checked data*  
>-h : help  
  
    
Example :
python3 upgraded-script.py -i passwords -o output.txt -f :*n -m entropy  
python3 upgraded-script.py -i passwords.txt -o output.txt -f :*n -m dict -d dictionary1.txt dictionary2.txt  
python3 upgraded-script.py -i passwords.txt -o output.txt -f :*n -m dr -d dictionary1.txt=str1 dictionary2.txt=str2  
python3 upgraded-script.py -i examples/email-and-pw-testset.txt -o output1.txt -f ":*\n" -m usum -d dictionary-folder/number.txt dictionary-folder/symbols.txt dictionary-folder/n-sequence.txt dictionary-folder/m-f-names.txt dictionary-folder/words.txt

