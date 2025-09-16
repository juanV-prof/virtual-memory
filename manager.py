def translate(va, memory):
    """
    This function translates a Virtual address into 
    a Physical address and uses demand paging. 
    """
    s, p, w, pw = extract(va)

    if pw >= memory.PM[2*s]:
        return -1
    
    #checks if PT is already in PM
    st_entry = memory.PM[2 *s + 1]
    if st_entry < 0:
        frame = memory.allocate()
        memory.read(abs(st_entry), frame)
        memory.PM[2 * s  + 1] = frame

    pt_base = memory.PM[2 * s + 1] * 512
    pt_entry = memory.PM[pt_base + p]

    if pt_entry < 0:
        frame = memory.allocate()
        memory.read(abs(pt_entry), frame)
        memory.PM[pt_base +p] = frame

        
    frame = memory.PM[pt_base + p]
    frame = frame * 512 + w
    return frame

def extract(va):
    #parts of VA are extracted
    s = va >> 18
    p = (va >> 9) & 0x1FF
    w = va & 0x1FF
    pw = va &  0x3FFFF

    return s, p, w, pw