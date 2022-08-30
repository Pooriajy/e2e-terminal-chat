import rsa

def new_encryption_key():
    public,private = rsa.newkeys(512)
    return [public,private]
