import string
import re

def strip_query(query):
    #Set tag query pattern
    tag_re = re.compile(r'[+|-]?\s*?#[\w|-]+')
    s = query
    poststr = s

    #Initialize addset and removeset, to store tags
    # query='#a +#b-#c'
    # addset = ['a','b']; removeset = ['c']
    addset = set()
    removeset = set()

    #Find all tags
    tags = tag_re.findall(s)
    
    #Iterate each tags in query
    for tag in tags:
        #if open with '+' add to addlist
        if tag[0]=='+':
            addset.add(tag[1:].strip()[1:])
                    
        #if open with '-' add to removelist
        elif tag[0]=='-':
            removeset.add(tag[1:].strip()[1:])
        #else, by default, open with word add to add list
        else:
            addset.add(tag[1:].strip())
        #Original string reduced by all matched tags, for testing if valid input
        poststr = poststr.replace(tag, '')

    return addset, removeset, poststr.strip() == ''
