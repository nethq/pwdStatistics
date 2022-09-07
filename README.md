#pwdStatistics
This script is created to work on files with the following formats "#text0#:#text1#\n"
The script will test #text1# for the mode you specify. 
The script has functionality for scanning and comparing if #text1# contains words from dictionaries, which you will specify.
You can get a dictionary of all the english words. The script executes in 0.5 secs for a set of 11k entries and a dictionary size of 490k, both names and words combined.

>Usage: python script.py -i #input-file# -o #output-file# -m #mode#
>>Modes : 'entropy' , 'dictionary'
>>>Usage: python script.py -i #input-file# -o #output-file# -m dictionary #name-dictionary# #word-dictionary#