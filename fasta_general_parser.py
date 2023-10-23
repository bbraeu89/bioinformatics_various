#Reading sequences in FASTA files

def get_items_from_file(filename, testfn=None):
    """Return all the items in the file name filename; if testfn
    then include only those items for which testfn is true"""
    with open(filename) as file:
        return get_items(file, testfn)
    
def find_item_in_file(filename, testfn=None):
    """Return the first item in the file named filename; if testfn
    then return the first item for which testfn is true"""
    with open(filename) as file:
        return find_item(file,testfn)   
    
def find_item(src, testfn):
    """Return the first item in src; if testfn then return the first item for which testfn is true"""
    gen = item_generator(src, testfn)
    item = next(gen)
    if not testfn:
        return item
    else:
        try:
            while not testfn(item):
                item = next(gen)
            return item
        except StopIteration:
            return None

def get_items(src, testfn=None):
    """Return all the items in src; if testfn then include
    only those items for which testfn is true"""
    return [item for item in item_generator(src) if not testfn or testfn(item)]

def item_generator(src):
    """Return a generator that produces a FASTA sequence from src each time it is called"""
    skip_intro(src)
    seq = ''
    description = src.readline().split('|')
    line = src.readline()
    while line:
        while line and line[0] != '>':
            seq += line
            line = src.readline()
        yield (description, seq)
        seq = ''
        description = line.split('|')
        line = src.readline()

def skip_intro(src):
    """skip introductory text that appears in src before the first item"""
    pass    #no introduction in a FASTA file
