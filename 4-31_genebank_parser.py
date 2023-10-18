import pprint

def get_GenBank_items_and_sequence_from_file(filename):
    with open(filename) as file:
        return [get_ids(file), list(get_items(file)), get_sequence(file)]

def get_ids(src):
    line = src.readline()
    while not line.startswith('VERSION'):
        line = src.readline()
    parts = line.split()
    assert 3 == len(parts), parts
    giparts = parts[2].partition(':')
    assert giparts[2], giparts
    assert giparts[2].isdigit()
    return (parts[1], giparts[2])

def get_sequence(src):
    seq = ''
    line = src.readline()
    while not line.startswith('//'):
        seq += line[10:-1].replace(' ','')
        line = src.readline()
    return seq

def skip_intro(src):
    line = src.readline()
    while not line.startswith('FEATURES'):
        line = src.readline()

attribute_prefix = 21*' ' + '/'
def is_attribute_start(line):
    return line and line.startswith(attribute_prefix)

def is_feature_start(line):
    return line and line[5] != ' '

def get_items(src):
    skip_intro(src)
    line = src.readline()
    while not line.startswith('ORIGIN'):
        assert is_feature_start(line)
        feature, line = read_feature(src, line)
        #The "line" here is important because it retrieves the cursor position of the end of the read_value inner function and passes it back to the outer "read_feature" outside function

        yield feature

def read_feature(src, line):
    feature = line.split()
    props = {}
    line = src.readline()           # this actually invoked the readline() method and updates the line variable with the next line
    while not is_feature_start(line) and not line.startswith('ORIGIN'):
        if is_attribute_start(line):
            key, value = line.strip()[1:].split('=', 1)     #the one in the bracket means do only one split explicitly
            if value[0] == '"':
                value = value[1:]
                if not value.endswith('"'):
                    additional_value, line = read_value(src) #here I am using read_value to harvest rest of the multi-line value
                    #The "line" here is important because it retrieves the cursor position of the end of the read_value inner function and passes it back to the outer "read_feature" outside function
                    value += additional_value   #I am adding the rest of the multi-line value to the first line of value
                else:
                    line = src.readline()           # I am going to the next line without removing terminal " but thats OK because value is still from previous line and then a few lines later the terminal " in values gets removed before appending to dictionary
            else:
                line = src.readline()
            if value.endswith('"'):
                value = value[:-1]
            props[key] = value
        else:
            line = src.readline()
    feature.append(props)
    return feature, line

def read_value(src):
    value = ''          #this is called value but it ONLY means this in this nested inside function and will NOT change "value" in read_feature
    line = src.readline()
    while line and not line.strip().endswith('"'):
        value += line.strip()
        line = src.readline()
    value += line.strip()   #This is the last line of a multi-line value elements that HAS " at the end. This gets finally appended to value outside the loop.
    if value.endswith('"'):
        value = value[:-1]
    return value, line

if __name__ == "__main__":
    filename = "sequence.gb"
    result = get_GenBank_items_and_sequence_from_file(filename)
    pprint.pprint(result)