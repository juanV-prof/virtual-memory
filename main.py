import sys
from memory import MemoryManager
from manager import translate

def main():
    """
    This creates a MemoryManger object to represent the parts of the 
    memory. Gets initializtion and input files as well as the output
    file name and returns the finished process. Turns VAs to PAs.
    """

    if len(sys.argv) != 4:
        print("error")
        sys.exit(1)

    init_file = sys.argv[1]

    input_file = sys.argv[2]
    output_file = sys.argv[3]

    memory = MemoryManager()

    #initializes MP and disk
    memory.initialize(init_file)

    #reads VSa from the input file
    virtual = list()
    with open(input_file, 'r') as f:
        for  line in f:
            if line.strip():
                virtual.extend(map(int,line.strip().split()))

    #translates the VAs to get the PA, error if invalid
    output = list()
    for v_address in virtual:
        p_address = translate(v_address,  memory)
        
        if p_address != -1:
            res = str(p_address)
        else:
            res = '-1'

        output.append(res)
    
    #writes outputs to output file
    with open(output_file, 'w') as f:
        f.write(' '.join(output)+ '\n')

if __name__ == '__main__':
    main()