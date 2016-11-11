
import re

def remove_pattern_from_string(string,patterns):
    regexPattern = '|'.join(map(re.escape,patterns))
    stripped_string = re.split(regexPattern,string)
    return stripped_string
