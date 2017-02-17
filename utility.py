# Utility module #

# import statements
import re

def find_type(name):
    """try to find type of the file, given name, return None if unrecognized"""
    if name.endswith(".java") or name.endswith(".rb") or name.endswith(".py"):
        return "code"
    elif name.endswith(".png") or name.endswith(".jpg") or name.endswith(".gif"):
        return "img"
    elif name.endswith(".db") or name.endswith(".xml") or name.endswith(".json"):
        return "data"
    elif name.endswith(".pdf") or name.endswith(".docx"):
        return "doc"
    else:
        return None

def clean_date(date):
    """clean up date string, by removing millisecond info"""
    # only take the text before the rightmost "." that appears in the string
    date = date.rpartition(".")[0]

    # replace all "T" delimeters, with " @ " delimeters
    date = " @ ".join(date.split("T"))
    return date

def pick_color(i):
    """pick a color from the palette, given 1-indexed number"""
    # list of colors, each corresponding to a single animal icon
    palette = ["#C0A76F", "#6B6B6B", "#FD1700", "#000000", "#FBFD06",
               "#FF6201", "#0C0970", "#EEAE19", "#9AADB3", "#77C000",
               "#FF4900", "#CEC7B7", "#FFB1AF", "#D289A6", "#63B5FF",
               "#99111B", "#0A4B20", "#D5ECD2", "#6A2D1B", "#9ACD32",
               "#1492CC", "#5C615B", "#A8A9AD", "#19A59C", "#A9EE17"]

    # return black color as default value if index not in range of palette list
    return palette[i - 1] if 1 <= i <= 25 else "#000000" 

def filter_words(text):
    """filter 'red flag' words, provided in text document, from text"""
    # get list of flagged words from text document on disk
    f = open('censored.txt', 'r')
    flagged_words = [line.strip("\r\n") for line in f]
    f.close()

    # split text into words, using various delimeters
    text_words = re.split(r' |\t|\n|-|_|\+|/|\|', text)

    # for each word, word is replaced with ****, if one of the flagged words 
    text_words = [word
                  if not re.sub(r'[^A-Z]', '', word.upper()) in flagged_words
                  else "*" * len(word)
                  for word in text_words]

    # return list of words, separated by single space
    return " ".join(text_words)
