from .utils import try_function_decorator

# work with the file object itself
@try_function_decorator("Error appending to file('$fileName')", {'fileName': 0 })
def append_content_to_file(fileName, content, options="a"):
    """ append content to file [fileName]

        fileName = str, Name of the file to be read 
        content  = str, content to be appended to the file
        return   = None
    """
    with open(fileName, options) as f:
        f.write(content)


@try_function_decorator("Error writing to file('$fileName')", {'fileName': 0 })
def write_content_to_file(fileName, content, options="w"):
    """ write content to file [fileName]

        fileName = str, Name of the file to be read 
        content  = str, content written to the file
    """
    with open(fileName, options) as f:
        f.write(content)


@try_function_decorator("Error reading file('$fileName')", {'fileName': 0 })
def read_full_file(fileName, options="rb+"):
    """Read File and return text in file
       fileName = str, Name of the file to be read (or path+fileName)
       return   = str, text in fileName
    """
    with open(fileName, options) as f:
        text = f.read()
    return text

# iterators
def file_reading_iterator(fileName, comment_char="#", options='r'):
    """generates an iterator to loop over the lines of a file"""
    # actual loop
    with open(fileName, options) as f:
        while True:
            line = f.readline()
            if not line: break
            # get rid of comment_char
            line = line.partition(comment_char)[0]
            # get rid of white spaces
            line = line.rstrip()
            # return line
            yield line


def file_reading_iterator_raw(fileName, options='r'):
    """generates an iterator to loop over the lines of a file"""
    # actual loop
    with open(fileName, options) as f:
        while True:
            line = f.readline()
            if not line: break
            # return line
            yield line
