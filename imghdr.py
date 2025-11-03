# Temporary replacement for removed imghdr (Python 3.13+)
def what(file, h=None):
    # very minimal fallback: always return "jpeg" if bytes start with JPEG header
    if h and h.startswith(b"\xff\xd8"):
        return "jpeg"
    if h and h.startswith(b"\x89PNG"):
        return "png"
    if h and h[0:6] in (b'GIF87a', b'GIF89a'):
        return "gif"
    return None
