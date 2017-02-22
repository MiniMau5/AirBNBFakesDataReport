import re

#identifiers
###


def findMail(desc):
    # defined model by hand
    # there are plans to develop that using ML in the future
    regex = '([\w\.\_])+(([\s\_\-]at[\s\_\-])|([\s\_\-])?@([\s\_\-])?)(\w)+(([\s\_\-])|([\s\_\-]dot[\s\_\-])|([\s\_\-])?\.([\s\_\-])?)(\w)+'
    result = re.search(regex, desc)
    if result:
        return result.group(0)
    return False

# is phone regex even feasible? Probably not
def findPhone(desc):
    # regex = ''
    # result = re.search(regex, desc)
    # return result.group(0)
    return False

def isSketchy(desc):
    if findMail(desc) or findPhone(desc):
        return True
    return False

# description = ""
description = "Contact me mim-at-bnbvacation_com"
print isSketchy(description)

# attributes
###

def featContact(desc):
    regex = '(contact)'
    result = re.search(regex, desc)
    return result.group(0)
