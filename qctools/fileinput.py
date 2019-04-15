from __future__ import print_function
import tempfile            # generate Tempfiles
import subprocess          # Commando line commands
import os


"""
#*****************************************************#
#                                                     #
#  OPEN File in EDITOR e.g VIM
#                                                     #
#-----------------------------------------------------#
"""


def file_input_via_editor(initial_msg, editor='vim'):
    """ get write a initial_msg to a file and opens it in an editor, e.g. VIM
        utilizing the tempfile module to create a tmp file, that is
        automatically deleted afterwards.
        It returns afterwards the edited content of the file as a string

        initialMessage = str,  initial Message written in Vim File
        return         = str,  user edited Message in Vim File
                               drawback, also inclueds the initial Message!
    """
    EDITOR = os.environ.get('EDITOR', editor)

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_msg)
        # flush msg to file
        tf.flush()
        # open the file using EDITOR
        subprocess.call([EDITOR, tf.name])
        # go back to the beginning
        tf.seek(0)
        # read context of file
        msg = tf.read()

    return msg


"""
#*****************************************************#
#                                                     #
#   Grep Routines
#                                                     #
#-----------------------------------------------------#
"""


def pygrep_str(text, keyword, length=100, ishift=0, begin=0):
    """ greps part of a text, the fragment Text has lenght characters
        and is the text in shift characters from the keyword
        uses the str.find() function of python, begin gives in
        characters the start where it will start to search for the keyword.
    """

    # get position of keyword in text
    istart = text.find(keyword, begin)

    #
    if istart == -1:
        print("pygrep error: '%s' not found in text!" % keyword)
        return None, begin
    #
    if istart + ishift + length > len(text):
        return text[istart + ishift:], -1
    #
    else:
        return (text[istart + ishift: istart + ishift + length],
                istart + ishift + length)


def partial_string(string, ishift, ilen):
    """ return partial string """
    if len(string) < ishift+ilen:
        return string[ishift:]
    return string[ishift: ishift + ilen]


def pygrep_iterator(iterator, keyword, ilen=100, ishift=0, begin=0):
    """ """

    ibuffer = -1
    out_str = ""
    maxlen = ishift + ilen
    #
    for line in iterator:
        if keyword in line:
            out_str = keyword + line.partition(keyword)[2]
            ibuffer = len(out_str)
            break
    # did not find output in file
    if ibuffer == -1:
        return (None, -1)
    # just single line input
    if ibuffer > maxlen:
        return (partial_string(out_str, ishift, ilen), 1)
    # multi line grep
    for line in iterator:
        ibuffer += len(line)
        out_str += line
        if ibuffer > maxlen:
            return (partial_string(out_str, ishift, ilen), 1)

    return (out_str, 1)


def pygrep_iterator_lines(iterator, keyword, ilen=10, ishift=0):
    """ """
    assert ishift >= 0
    #
    istart = 0
    #
    out_str = ""
    icount = -1
    # check shift
    if ishift == 0:
        istart = 1
    # get keyword
    for line in iterator:
        if keyword in line:
            out_str = line
            icount = 1
            break
    # did not find item in iterator
    if icount == -1:
        return (None, -1)
    # only get first item
    if istart == 1 and ilen == 1:
        return (out_str[:-1], 1)
    # skip ishift lines!
    if ishift != 0:
        out_str = ""
        if ishift == 1:
            pass
        else:
            for line in iterator:
                icount += 1
                if icount == ishift:
                    break
    else:
        icount = ishift
    # if end of file before end of iskip
    if icount != ishift:
        return (None, -1)
    # get all remaining lines
    for line in iterator:
        out_str += line
        istart += 1
        if istart == ilen:
            break
    # return output
    return out_str[:-1], 1


def pyxgrep_iterator_lines(iterator, keyword, ilen=10, ishift=0):
    """ """
    assert ishift >= 0
    #
    istart = 0
    #
    icount = -1
    # check shift
    if ishift == 0:
        istart = 1
    # get keyword
    for line in iterator:
        if keyword in line:
            out_str = [line]
            icount = 1
            break
    # did not find item in iterator
    if icount == -1:
        return (None, -1)
    # only get first item
    if istart == 1 and ilen == 1:
        return (out_str, 1)
    # skip ishift lines!
    if ishift != 0:
        out_str = []
        if ishift == 1:
            pass
        else:
            for line in iterator:
                icount += 1
                if icount == ishift:
                    break
    else:
        icount = ishift
    # if end of file before end of iskip
    if icount != ishift:
        return (None, -1)
    # get all remaining lines
    for line in iterator:
        out_str.append(line)
        istart += 1
        if istart == ilen:
            break
    # return output
    return out_str, 1
