class MemoryManager:
    """
    This class is used to represent the
    physical memory, disk, free/used frames based on 
    the specifications of the project
    """
    def __init__(self):
        self.PM = [0] * 524288
        self.D = list()
        for _ in range(1024):
            block = [0] * 512
            self.D.append(block)
        self.free_frames = list()
        self.used_frames = set([0, 1])

    def initialize(self, file):
        #initializes based on init file
        with open(file, 'r') as f:
            lines = list()

            for line in f:
                stripped = line.strip()
                if stripped:
                    lines.append(stripped)
        #we get the ST entries based on the first line, theyre put in PM
        st_entries = list(map(int, lines[0].split()))
        for i in range(0, len(st_entries), 3):
            s, z, loc =  st_entries[i], st_entries[i+1], st_entries[i+2]
            self.PM[2 * s] = z
            
            self.PM[2 *s + 1] = loc
            
            if loc > 0:
                self.used_frames.add(loc)
        #we get PT entires based on second line
        pt_entries = list(map(int, lines[1].split()))
        for i in range(0, len(pt_entries), 3):
            s, p, loc = pt_entries[i], pt_entries[i +1], pt_entries[i + 2]
            pt_base = self.PM[2 * s + 1]
            #PTs are put in either PM or Disk array
            if pt_base > 0:
                self.PM[pt_base* 512 + p]  = loc

                if loc > 0:

                    self.used_frames.add(loc)
            else:
                self.D[abs(pt_base)][p ] = loc
                if loc > 0:
                    self.used_frames.add(loc)

        
        self.free_frames = list()
        for frame in range(0, 1024):
            if frame not in self.used_frames:
                self.free_frames.append(frame)  
    
    def read(self, bloc, fram):
        #reads a block from disk to PM
        start = fram * 512
        self.PM[start: start + 512] = self.D[bloc][:]

    def allocate(self):
        #allocates a free frame
        if not self.free_frames:
            raise Exception("No More Frames Available")
        frame = self.free_frames.pop(0)
        
        self.used_frames.add(frame)

        return frame




