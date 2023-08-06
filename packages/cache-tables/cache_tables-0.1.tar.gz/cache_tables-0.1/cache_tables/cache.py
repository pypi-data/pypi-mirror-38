import math
from colorama import init
init()
from colorama import Fore, Style
from prettytable import PrettyTable
from lru import LRU
from random import randint

def parseAddressDA(address, blocks, block_size, word_size = 4):
    """ Helper function that will parse the address, for direct Associative method. \n
        Paramenters: \n
        \t address \n
        \t blocks \n
        \t block_size \n
        \t word_size: default is 4\n
        Return dictionary with tag, address_result, index,word_offset, byte_offset
    """
    binary_address = bin(address)[2:].zfill(32)
    byte_offset_size = int(math.log2(word_size))
    word_offset_size = int(math.log2(block_size))
    index_size = int(math.log2(blocks))
    byte_offset = int(binary_address[-byte_offset_size:],2)
    if word_offset_size == 0:
        word_offset = 0
    elif word_offset_size == 1:
        word_offset = int(binary_address[len(binary_address)-byte_offset_size-1],2)
    else:
        word_offset = int(binary_address[-byte_offset_size-byte_offset_size:-byte_offset_size],2)
    index = int(binary_address[-byte_offset_size-word_offset_size-index_size:-byte_offset_size-word_offset_size],2)
    tag = int(binary_address[:-(byte_offset_size+byte_offset_size)-1],2)
    #address_result = int(binary_address[:-byte_offset_size],2)
    return {"tag" : tag, "address_result" : address - byte_offset , "index" : index , "word_offset" : word_offset, "byte_offset" : byte_offset}

def parseAddressFA(address, word_size = 4):
    """ Helper function that will parse the address, for full Associative method. \n
        Paramenters: \n
        \t address \n
        \t word_size: default is 4\n
        Return dictionary with tag, address_result
    """
    binary_address = bin(address)[2:].zfill(32)
    byte_offset_size = int(math.log2(word_size))
    byte_offset = int(binary_address[-byte_offset_size:],2)
    tag = int(binary_address[:-(byte_offset_size)],2)
    #address_result = int(binary_address[:-byte_offset_size],2)
    return {"tag" : tag, "address_result" : address - byte_offset }


def headerDA(blocks,block_size,extended):
    """ Creates the header list . \n
        Paramenters: \n
        \t blocks \n
        \t block_size \n
        Return dictionary list with the header
    """
    if(extended):
        header =["Address","Tag","Real Address","Index","WordOffset","ByteOffset"]
    else:
        header =["Address"]
    for i in range(0,blocks):
        for x in range(0,block_size):
            header.append("B%i W%i"%(i,x))
    header.append("Result")
    return header

def flat_list(old_list):
    """Function for creating one big array from array of arrays, this is recursive so be careful"""
    new_list = []
    for element in old_list:
        if "list" in str(type(element)):
            recursive_list = flat_list(element)
            for sub_element in recursive_list:
                new_list.append(sub_element) 
        else:
            new_list.append(element)
    return new_list

def directAssociative(addresses,blocks,block_size,extended=True,pretty_print=True):
    """ Creates the full table for direct Associative mode . \n
        Paramenters: \n
        \t address \n
        \t blocks \n
        \t block_size \n
        \t extended which defaults to true, and it gaves us more information \n
        \t pretty_print which defaults to true \n
        Return full table as a list of lists with the data and also will print it, unless specified to false
    """
    table = eval(str([[" "] * block_size] * blocks))
    full_table = []
    for address in addresses:
        parseResult = parseAddressDA(address, blocks, block_size)
        index, word, address_result = parseResult["index"], parseResult["word_offset"], parseResult["address_result"]
        if address_result in table[index]:
            result = [address,Fore.GREEN + "HIT" + Style.RESET_ALL]
        elif table[index][word] == " " and len(table[index])>1 or table[index]==[" "]:
            result = [address,Fore.RED + "MISSED" + Style.RESET_ALL]
        else:
            result = [address, Fore.YELLOW + "COLLISION" + Style.RESET_ALL]
        table[index][word] = address_result
        if(extended):
            full_table.append(flat_list(eval(str([result[0],parseResult["tag"],parseResult["address_result"],index,word,parseResult["byte_offset"],table,result[1]]))))
        else:
            full_table.append(flat_list(eval(str([result[0],table,result[1]]))))
    if pretty_print:
        t = PrettyTable(headerDA(blocks,block_size,extended))
        for row in full_table:
            t.add_row(row)
        print(t)
    return full_table

def headerFA(block_size,extended=True):
    """ Creates the header list . \n
        Paramenters: \n
        \t blocks \n
        \t block_size \n
        Return dictionary list with the header
    """
    if(extended):
        header =["Address","Tag","Real Address"]
    else:
        header =["Address"]
    for x in range(0,block_size):
        header.append("W%i"%(x))
    header.append("Result")
    return header

def MRU2list(mru_list):
    array = []
    for element in mru_list:
        array.append(element[1])
    return array

def fullAssociative(addresses,block_size,mode,extended=True,pretty_print=True):
    """ Creates the full table for full associative mode, one block with n block_size . \n
        Paramenters: \n
        \t address \n
        \t block_size \n
        \t mode, can be LRU, MRU, FIFO, RANDOM
        \t pretty_print which defaults to true \n
        Return full table as a list of lists with the data and also will print it, unless specified to false
    """
    container = LRU(block_size)
    for i in range(block_size):
        container[i] = " "
    table = [" "]* block_size
    full_table = []
    iterator =  0
    for address in addresses:
        parseResult = parseAddressFA(address)
        tag, address_result = parseResult["tag"], parseResult["address_result"]
        if mode=="RANDOM":
            if address_result in table:
                result = Fore.GREEN + "HIT" + Style.RESET_ALL
            elif " " in table:
                for i in range(0,block_size):
                    if " " == table[i]:
                        table[i] = address_result
                        break
                result = Fore.RED + "MISSED" + Style.RESET_ALL
            else:
                position = randint(0,block_size - 1)
                result = Fore.YELLOW + "COLLISION" + Style.RESET_ALL
                table[position]  = address_result
        elif mode=="LRU":
            if address_result in MRU2list(container.items()):
                for element in container.items():
                    if element[1] == address_result:
                        container[element[0]] = address_result
                result = Fore.GREEN + "HIT" + Style.RESET_ALL
            elif " " in MRU2list(container.items()):
                for element in container.items():
                    if element[1] == " ":
                        container[element[0]] = address_result
                        break
                result = Fore.RED + "MISSED" + Style.RESET_ALL
                for index in range(len(table)):
                    if table[index] == " ":
                        table[index] = address_result
                        break
            else:
                element2replace = MRU2list(container.items())[block_size-1]
                index = container.peek_last_item()
                container[index] = address_result
                result = Fore.YELLOW + "COLLISION" + Style.RESET_ALL
                for index in range(len(table)):
                    if table[index] == element2replace:
                        table[index] = address_result
                        break
        elif mode=="MRU":
            if address_result in MRU2list(container.items()):
                for element in container.items():
                    if element[1] == address_result:
                        container[element[0]] = address_result
                result = Fore.GREEN + "HIT" + Style.RESET_ALL
            elif " " in MRU2list(container.items()):
                for element in container.items():
                    if element[1] == " ":
                        container[element[0]] = address_result
                        break
                result = Fore.RED + "MISSED" + Style.RESET_ALL
                for index in range(len(table)):
                    if table[index] == " ":
                        table[index] = address_result
                        break
            else:
                element2replace = MRU2list(container.items())[0]
                container[0] = address_result
                result = Fore.YELLOW + "COLLISION" + Style.RESET_ALL
                for index in range(len(table)):
                    if table[index] == element2replace:
                        table[index] = address_result
                        break
        elif mode=="FIFO":
            if address_result in table:
                result = Fore.GREEN + "HIT" + Style.RESET_ALL
            elif " " in table:
                table[iterator]  = address_result
                iterator = iterator + 1
                result = Fore.RED + "MISSED" + Style.RESET_ALL
            else:
                table[iterator]  = address_result
                iterator = iterator + 1
                result = Fore.YELLOW + "COLLISION" + Style.RESET_ALL
            if (iterator==block_size):
                iterator = 0
        if(extended):
            full_table.append(flat_list(eval(str([address,tag,address_result,table,result]))))
        else:
            full_table.append(flat_list(eval(str([address,table,result]))))
    if pretty_print:
        t = PrettyTable(headerFA(block_size,extended))
        for row in full_table:
            t.add_row(row)
        print(t)
    return full_table
    
def demo():
    """ Demo function, as its name describes it is for testing the usage of the script. Can also be seen as an example \n
        No parameters and no return
    """
    addresses = [3,180,43,2,191,88,190,14,181,44,186,253]
    print ("Example 1 \nDirect Associative, with 8 blocks of 1 word \n")
    directAssociative(addresses,8,1)
    print ("Example 2 \nDirect Associative, with 4 blocks of 2 word\n")
    directAssociative(addresses,4,2)
    print ("Example 3 \nDirect Associative, with 2 blocks of 4 word\n")
    directAssociative(addresses,2,4)
    print ("Example 4 \nFull Associative Random, with 4 word\n")
    fullAssociative(addresses,4,"RANDOM")
    print ("Example 4 \nFull Associative FIFO, with 4 word\n")
    fullAssociative(addresses,4,"FIFO")
    print ("Example 4 \nFull Associative MRU, with 8 word\n")
    fullAssociative(addresses,4,"MRU")
    print ("Example 4 \nFull Associative LRU, with 8 word\n")
    fullAssociative(addresses,4,"LRU")
