import html, re

#regex patterns
cleanr = re.compile(r'<[^>]+>')
crlfr = re.compile(r'([\s]{2,}|[\s]$)',re.MULTILINE|re.DOTALL)
crlf2r = re.compile(r'([\s]{1,}|[\s]$)',re.MULTILINE|re.DOTALL)

def cleanreview(s):
    '''CLEAN REVIEW CONTENT'''
    ns=cleanr.sub(' ',s)
    ns=crlf2r.sub(' ',ns)
    return html.unescape(ns)

def cleantitle(s):
    '''CLEAN TITLE (OBJECT) field'''
    ns=cleanr.sub(' ',s)
    ns=crlf2r.sub(' ',ns)
    return html.unescape(ns)