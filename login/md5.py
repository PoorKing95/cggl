import hashlib

def md5_key(arg):
    hash = hashlib.md5()
    hash.update(arg.encode("utf8"))
    return hash.hexdigest()




