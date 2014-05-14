import string
import re
from post.models import Post, Tag, PostTag

#Pre query processing to generate sets with tags to be added and tags to be removes
def strip_query(query):
    #Set tag query pattern
    #tag_re = re.compile(r'[+|-]?\s*?#[\w|-]+')
    """
        Thought about this in the shower just now, this should be the RegEx
        that we're looking for that strips hash-tags out the way that we
        define them to be and combines the +/- signs to the next nearest
        hashtag.

        Feel free to list more test cases, or try to break the RegEx so that
        we can improve on it further :)

        Test cases:
            #ivan-#monica                       Output: ['#ivan', '-#monica']
            #ivan-here-there-#school            Output: ['#ivan-here-there', '-#school']
            #ivan--here-#monica                 Output: ['#ivan', '-#monica']
            #ivan-here-- there - - #school      Output: ['#ivan-here', '- #school']
            +  #ivan-here-there-- - + #school   Output: ['+  #ivan-here-there', '+ #school']
    """
    tag_re = re.compile(r'[+|-]?\s*#(?:\w|(?<=\w)-(?=\w))+') 
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
        # Don't think we need this any longer, the RegEx above took care of this
        # take out trailing '-' if it exists
        #if tag[len(tag) - 1] == '-':
        #    tag = tag[:-1]

        #if open with '+' add to addlist
        if tag[0] == '+':
            addset.add(tag[1:].strip()[1:])
        #elif open with '-' add to removelist
        elif tag[0] == '-':
            removeset.add(tag[1:].strip()[1:])
        #else, by default, open with word add to add list
        else:
            addset.add(tag[1:].strip())

        #Original string reduced by all matched tags, for testing if valid input
        poststr = poststr.replace(tag, '')

    return addset, removeset, poststr.strip() == ''

#Get top 'topcnt' recent posts from addset and removeset
def getposts(addset,removeset, topcnt):

    cnt = 0
    clean_posts = []  
    
    #Remove posts with tag from removeset
    if removeset:
        remove_str = "|".join(removeset)
        pattern = re.compile('#({0})'.format(remove_str))

    while len(clean_posts) < topcnt:
        
        pids = set()

        #Retrieve top cnt to cnt+10 from each addtag
        for addtag in addset:
            pts = Tag.objects.get(value=addtag).posttag_set.all().order_by('-pid')[cnt:cnt+topcnt]
            pids = pids.union({ps.pid_id for ps in pts})

        post_results = Post.objects.filter(id__in=pids) 
        post_results = sorted(post_results, key=lambda post: -post.id)
        
        #Remove post if removeset is not empty
        if removeset:
            for post in post_results:
                if not pattern.findall(post.text):
                    clean_posts.append(post)
        else:
            clean_posts = post_results

        #Add cnt for next round of data retrieval
        cnt = cnt+ topcnt
       
    return clean_posts[:topcnt]
