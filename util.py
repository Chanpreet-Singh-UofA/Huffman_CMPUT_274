#----------------------------------------
# 
#
# Name : Chanpreet Singh
# ID   : 1576137
#
# CMPUT 274 - Tangible computing - Fall 2019
#
# Assignment 1 : Huffman Coding
#
#----------------------------------------

import bitio
import huffman
import pickle


def read_tree(tree_stream):
	'''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
  '''

	#To know which fuction is causing error.  
	try:
		un_pickled_tree = pickle.load(tree_stream)
		return un_pickled_tree 
	except:
		print('Error in read_tree()')



def decode_byte(tree, bitreader):
	"""
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
  """

  	#Variable path is used since i found using tree a bit misleading according to my logarithm
	path=tree
	try:
		#Path is followed until a leaf is reached.
		while isinstance(path,huffman.TreeBranch):
			
			#A bit is returned by by using readbit() of bitreader class from bitio.py file 
			Returned_bit = bitreader.readbit()
			# If the bit is 0 then path is directed to left or viseversa since 0's are on left brance and 1's on right.
			if Returned_bit == 0:
				path = path.getLeft()

			elif Returned_bit==1:
				path = path.getRight()
			else:
				print('Check decode_byte() -- Returned_bit is not 1 or 0')
			
		#once a leaf is reached loop ends and value of leaf is returned.
		leaf_value=path.getValue()
		return leaf_value
	except:
		print('Error in decode_byte()')
	

def decompress(compressed, uncompressed):

	'''First, read a Huffman tree from the 'compressed' stream using your
	    read_tree function. Then use that tree to decode the rest of the
	    stream and write the resulting symbols to the 'uncompressed'
	    stream.

	    Args:
	      compressed: A file stream from which compressed input is read.
	      uncompressed: A writable file stream to which the uncompressed
	          output is written.
	'''

	try:
		read_huffman = read_tree(compressed)
		bitio_instance=bitio.BitReader(compressed)
		#condition is used to stop the while loop.
		condition = False

		while condition!=True:
		
			try:
				#value of leaf is returned by decode_byte which is then written into umcompressed file stream.
				symbols = decode_byte(read_huffman, bitio_instance)

				(bitio.BitWriter(uncompressed)).writebits(symbols, 8)

			#When file ends exception is raised then condition is changed and loop ends.
			except:
					condition = True
		#flush() is used to flush the internal buffer
		(bitio.BitWriter(uncompressed)).flush()

	except:
		print('Error in decompress()')



def write_tree(tree, tree_stream):
		
	'''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
  '''	

	try:
		pickle.dump(tree,tree_stream)
	except:
		print('Error in write_tree()')

def compress(tree, uncompressed, compressed):
	'''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
  '''

	try:  

		#Given tree is written first then we initialize some classes for easy accessibility of their functions in our program.
		upload_tree=write_tree(tree,compressed)
		#As suggested in assignment we make encoding table
		made_table = huffman.make_encoding_table(tree)
		bit_read = bitio.BitReader(uncompressed)
		bit_write=bitio.BitWriter(compressed)

		condition=False 

		while condition!=True:

			try:
				read_bit = bit_read.readbits(8)
					# We use read_bit value and match it with keys of of our made_table and corresponding value is stored into path. 
				path=list(made_table[read_bit])
					#path is made a list for iterating, containg Trues or False which lead to a particular leaf.
				for i in path:
					if i==True or i==False:
							#we take each value of path and write 1 for True and 0 for False.
						bit_write.writebit(i)   
					else:
						print('Error is in compress(), path contain value other then true or false')

			except EOFError:
				condition=True
		#Once file ends then end-of-file i.e. None is added at last node and loop conditions are changed to stop the loop.
		path_end=list(made_table[None])

		for k in path_end:
			bit_write.writebit(k)
			


		#flush() is used to flush the internal buffer
		bit_write.flush()
	except:
		print('Error in Compress()')




