
import re

def remove_pattern_from_string(string,patterns):
    regexPattern = '|'.join(map(re.escape,patterns))
    all_patterns = ', '.join(patterns)
    stripped_string = [re.split(regexPattern,string),all_patterns]
    return stripped_string
