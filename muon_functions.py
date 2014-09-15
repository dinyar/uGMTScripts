import ROOT

from muon import Muon

def file_converter(f_obj): 
    # transforms data from txt-File to a dictionary the index is the frame-number
    frame_dict = {}
    for line in f_obj:
        frames = line.split()
        if frames and frames[0] == "Frame":
            frame_n = int(frames[1]) 
            frame_dict[frame_n] = frames[3:] # strips the frame identifier
    return frame_dict

def frame_printer(frame_dict, frame_numbers):
    # Prints frames specified by frame_numbers (either list/tuple or int)
    if isinstance(frame_numbers, int):
        print frame_dict[frame_numbers]
    else:
        frames = [ frame_dict[i] for i in frame_numbers ] 
        for frame in frames:
            print frame

def get_num(frame_dict, frame, link): 
    # Get the actual hex-number of frame and link
    frame_content = frame_dict[frame][link]
    frame_content = frame_content.replace("1v", "")
    num = int(frame_content, 16)
    return num


def get_masked_word(complete_word, bit_low, bit_high): 
    # Create bit mask for bit_low-bit_high
    mask = (1<<(bit_high-bit_low+1)) - 1
    mask = mask<<bit_low
    masked_word = complete_word & mask
    return masked_word>>bit_low
    
def get_muon_dict(frame_dict, link_low, link_high, frame_low, frame_high): 
    # Concatinates muon frames and returns dict
    mu_dict = {}
    frame = frame_low
    while frame < frame_high:
        mu_dict[frame] = []
        for link_n in xrange(link_low, link_high):
            # only take frames with valid bit set
            if "1v" in frame_dict[frame][link_n] and "1v" in frame_dict[frame+1][link_n]: 
                a = get_num(frame_dict, frame, link_n)
                b = get_num(frame_dict, frame+1, link_n)
                mu_dict[frame].append((b<<32) + a)
                print "found valid pair"
        frame = frame+2 

    return mu_dict



def filler1D(hist,name,value):
    hist[name].Fill(value)

def filler2D(hist,name,xvalue,yvalue):
    hist[name].Fill(xvalue,yvalue)

def hist_creator1D(namesdict,hist,title):
    for varname, hist_property in namesdict.iteritems():
        hist[varname] = ROOT.TH1D(varname+"{title}".format(title=title), "", hist_property[1], hist_property[2], hist_property[3])
        hist[varname].SetXTitle(hist_property[0])


def hist_creator2D(namesdict,hist,xname,yname,title): # xname & yname are strings!
    hist["{yname} gg {xname}".format(xname=xname,yname=yname)] = ROOT.TH2D("{title}".format(title=title),"",
        namesdict[xname][1],namesdict[xname][2],namesdict[xname][3],
        namesdict[yname][1],namesdict[yname][2],namesdict[yname][3])

def plot_modifier(hist,xlabel,ylabel,color):
    hist.GetXaxis().SetTitle("{xlabel}".format(xlabel=xlabel))
    hist.GetYaxis().SetTitle("{ylabel}".format(ylabel=ylabel))
    if color == ROOT.kBlack:
        hist.SetLineColor(color)
    else:
        hist.SetFillColor(color)
        hist.SetLineWidth(0)

def isequal(a,b): # gives 1 if a==b and 0 otherwise
    x = int(a)^int(b)
    if x==0 or x==1:
        return x
    else:
        return 1

def single_bit(num,bit): # Gets one single bit defined by num
    a = 1<<bit
    b = num&a
    return b >> bit

def num_of_ones(x): # returns num of ones in a bitword...not very elegant, works only for positive numbers!
    return bin(x).count("1")


def phi(obj,stepsize,phi_low,phi_high): # the following 2 functions are discommented in the script, but they return the physical phi and pT (see eta)
    obj.phiBits = stepsize*obj.phiBits
    if (obj.phiBits<phi_low) or (obj.phiBits>phi_high):
        print "phiBits out of range [{l},{h}]".format(l=phi_low,h=phi_high)

def pt(obj,stepsize,pt_low,pt_high):
    obj.ptBits = stepsize*obj.ptBits
    if (obj.ptBits<pt_low) or (obj.ptBits>pt_high):
        print "ptBits out of range [{l},{h}]".format(l=pt_low,h=pt_high)

def get_rank_list(frame_dict, rank_link_low, rank_link_high, rank_frame_low, rank_frame_high, rank_bitlength, free_bits): 
    # returns a list of valid ranks in the range specified
    rank_list = []
    for frame in xrange(rank_frame_low, rank_frame_high):
        for link in xrange(rank_link_low, rank_link_high+1): 
            tmp = get_num(frame_dict, frame, link)
            # gets rid of empty 12 LSBs
            ranksword = tmp >> 12
            rank2 = ranksword >> rank_bitlength
            rank1 = get_masked_word(ranksword, 1+rank_bitlength, 2*rank_bitlength)
            rank_list.append(rank1)
            rank_list.append(rank2)

    return rank_list

def find_nonzero_output(frame_dict, links=None, num_of_frames=None): # Finds the first non-zero valid (1v) entry from frame 0000 to frame "num_of_frames" in the input_links 
    # Attention: links is an array of length 2 !!!

    if num_of_frames==None:
        num_of_frames = 2**10

    if links==None:
        k0 = 0
        k1 = 4
    else:
        k0 = links[0]
        k1 = links[1]

    for j in xrange(k0, k1):
        for i in xrange(num_of_frames):
            a = frame_dict[i][j]
            if (a[:2] == "1v") and (a!="1v00000000"):
                return i
                break

def input_frames(frame_dict, link=None, num_of_frames=None): # Function made for input_files. Returns the number of valid input_frames starting from link 36 (can be modified)
    # Attention: Stops at first "0v" entry! (See code) If there should be other "1v" entries below, this function doesnt take them into consideration!

    if link==None:
        link = 36

    if num_of_frames == None:
        num_of_frames = 1024

    end_frame = num_of_frames

    for i in xrange(num_of_frames):
        a = frame_dict[i][link]
        if a[:2] == "1v":
            start_frame = i
            break

    for i in xrange(start_frame,num_of_frames):
        a = frame_dict[i][link]
        if a[:2] == "0v":
            end_frame = i
            break

    return end_frame-start_frame

def find_nonzero_intermediate(frame_dict,start_frame,link_low=None,link_high=None): # Function made for the intermediate_muons.
    # It finds the first intermediate-bitword that is identical to the first valid non-zero output-bitword. "start_frame" is the frame in which this output_word is.
    # This is to define the offset between output and intermediate if there are problems in the alignment.

    if link_low==None:
        link_low=4

    if link_high==None:
        link_high=12

    for i in xrange(start_frame+1):
        for j in xrange(link_low,link_high):
            a = frame_dict[i][j]
            b = frame_dict[start_frame][0] 
            if a==b:
                return i
                break

def zero_qual(obj, input_muon=None): # Counts the muons with quality=0 but non-zero bitword. If the function is called with 2 arguments, it counts the input_qualityBits
    vec = []
    for i in xrange(len(obj)):
        if input_muon==None:
            m = obj[i].input_qualityBits
        else:
            m = obj[i].qualityBits

        if m==0 and obj[i].bitword!=0:
            vec.append(obj[i])
    return len(vec)

def zero_pt(obj, input_muon=None): # works as the function above for "ptBits"
    vec = []
    for i in xrange(len(obj)):
        if input_muon==None:
            m = obj[i].input_ptBits
        else:
            m = obj[i].ptBits

        if m==0 and obj[i].bitword!=0:
            vec.append(obj[i])
    return len(vec)

def non_zero(muon_objs): # counts how many obj in an array are !=0
    counter = 0
    for muon in muon_objs:
        if muon.bitword != 0:
            counter += 1
    return counter

def get_muon_objects(vhdl_dict, frame_dict, start_frame, end_frame, start_link, end_link, mu_type = "IN"):
    muon_dict = get_muon_dict(frame_dict, start_link, end_link, start_frame, end_frame)
    muon_objs = []
    for frame, muons in muon_dict.iteritems():
        muon_objs += [ Muon(vhdl_dict, mu_type, bitword) for bitword in muons ]
    return muon_objs

# def non_zero_block(vhdl_dict, m_list, m_dict, muon_option=None): # Outputs have 3 links a 6 frames -> correspond to 4 muons. m_dict is a dict that contains such a "block"
#     # m_list (the output) is a list of m_dict, with all the entries transformed to objects of the Muon_class, but only if any of them is !=0. This is to ensure that no empty blocks are taken.
#     # If the function is called with 3 arguments, only the entries are taken into the list without initialising them as Muon objects.

#     h_vec = []
#     for var in m_dict:
#         h_vec.append(m_dict[var])   
#     #if any(x != 0 for x in h_vec): # not very elegant, just a prototype!
#     for m in h_vec:
#         if muon_option==None:
#             m = Muon(vhdl_dict, bitword=m)
#         m_list.append(m)

#     return m_list

