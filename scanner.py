import re

#identifiers
###

def findMail(desc):
    regex = '([\w\.\_])+((\sat\s)|@)(\w)+((\sdot\s)|\.)(\w)+'
    result = re.search(regex, desc)
    return result.group(0)

# is phone regex even feasible? Probably not
# def findPhone(desc):
#     regex = ''
#     result = re.search(regex, desc)
#     return result.group(0)

def isSketchy(desc):
    if (findMail(desc) || findPhone(desc)):
        return True

description = ""
print isSketchy(description)

# attributes
###

def featContact(desc):
    regex = '(contact)'
    result = re.search(regex, desc)
    return result.group(0)
