import heapq
import os

class BinaryTree:
    def __init__(self,value,freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
        
    ## overloading the function to tells function on which basis we have to compare
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __eq__(self,other):
        return self.freq == other.freq

class Huffmancode:
    
    def __init__(self ,path) :
        self.path = path
        self.__heap =[]  #iterable to push values in heap
        self.__code = {}
        self.__reversecode = {}

    def __freq_from_text(self ,text):
        freq_dict ={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char] = 0

            freq_dict[char] += 1
        return freq_dict  
    
    def __Build_heap(self,freq_dict):
        for key in freq_dict:
            freq = freq_dict[key]
            binary_tree_node = BinaryTree(key,freq)
            heapq.heappush(self.__heap , binary_tree_node)
            
    def __Build_Binary_Tree(self):
        while len(self.__heap) > 1:
            binary_tree_node_1 =heapq.heappop(self.__heap)
            binary_tree_node_2 =heapq.heappop(self.__heap)
            sum_of_freq = binary_tree_node_1.freq + binary_tree_node_2.freq
            newnode = BinaryTree(None,sum_of_freq)
            newnode.left = binary_tree_node_1
            newnode.right = binary_tree_node_2 
            heapq.heappush(self.__heap,newnode)   
        return 
    
    ## recussive funct
    def __Build_Tree_Code_Helper(self , root,curr_bits):
        if root is None:
            return 
        if root.value is not None:
            self.__code[root.value] = curr_bits
            self.__reversecode[curr_bits] = root.value
            return
        
        self.__Build_Tree_Code_Helper(root.left,curr_bits + '0')
        self.__Build_Tree_Code_Helper(root.right , curr_bits+'1')
    
    
    def __Build_Tree_Code(self):
        root = heapq.heappop(self.__heap)
        self.__Build_Tree_Code_Helper(root ,'')
        
    def __Build_Encoded_Text(self ,text):
        encoded_text = ''
        for char in text:
            encoded_text += self.__code[char]
        
        return encoded_text
    
    def __Build_padded_Text(self,encoded_text):
        padding_val = 8 - (len(encoded_text) % 8)
        
        for i in range(padding_val):
            encoded_text += '0'
        
        padded_info = "{0:08b}".format(padding_val)
        padded_encode_text = padded_info + encoded_text
        return padded_encode_text 
    
    def __Bild_Byte_Array(self,padded_text):
        array = []
        for i in range(0,len(padded_text) , 8):
            byte = padded_text[i : i+8] # slicing in 8 bits
            array.append(int(byte,2))
            
        return array
    
    def compression(self):
        # text = 'bdadhjkdasdjashkdhasfh'
        print("PROGRAM STARTED....")
        print("COMPRESSION STARTS")
        #To access the file and extract text from that file.
        
        filename,file_extension = os.path.splitext(self.path)
        output_path = filename + '.bin'
        
        # file comprehension
                    #reading file                    #'wb' -> writin in binary
        with open (self.path,'r+') as file , open(output_path,'wb') as output:
            text = file.read()
            text = text.rstrip()
        # STRIP TO REMOVE EXTRA SPACES
            freq_dict = self.__freq_from_text(text)
            build_heap = self.__Build_heap(freq_dict) 
            self.__Build_Binary_Tree()
            self.__Build_Tree_Code()
            encoded_text = self.__Build_Encoded_Text(text)
            
            #padding of encoded_text
            padded_text = self.__Build_padded_Text(encoded_text)
            bytes_array = self.__Bild_Byte_Array(padded_text)
            
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
    
        print("Compressed Successfully")
        return output_path
    
    
    # decompression
       
    def __Remove_Padding(self,text):
        padded_info = text[:8]
        extra_padding = int(padded_info,2) #integer val
        text = text[8:]
        padding_removed_text = text[:-1*extra_padding] #negative slicing
        return padding_removed_text 
    
    def __Decompress_Text(self,text):    
        decoded_text = ''
        current_bits = ''
        for bit in text:
            current_bits += bit
            if current_bits in self.__reversecode:
                character = self.__reversecode[current_bits]
                decoded_text += character
                current_bits = ""
        return decoded_text
   
    def decompress(self, input_path):
        print("DECOMPRESSION START")
        filename,file_extension = os.path.splitext(input_path)
        output_path = filename + '_decompressed' + '.txt'
        # rb -> used to read binary file
        # w -> used to write text
        with open(input_path,'rb') as file , open(output_path,'w') as output:
            bit_string = '' # store decompress data
            byte = file.read(1)  #reading file 1 by 1
            while byte:
                byte = ord(byte) # converts into integer
                bits = bin(byte)[2:].rjust(8,'0') #bin method convert it into binary && rjust method for slicing
                bit_string += bits
                byte = file.read(1) 
                
            actual_text = self.__Remove_Padding(bit_string)    
            decompressed_text = self.__Decompress_Text(actual_text)
            output.write(decompressed_text)
            
            print("DECOMPRESED SUCCESSFULL")
        return    


path = input("ENTER THE PATH OF YOUR FILE....")
h = Huffmancode(path)
compressed_file = h.compression()
h.decompress(compressed_file)
print("PROGRAM ENDED...")
