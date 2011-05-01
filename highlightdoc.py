#!/usr/bin/env python
# 
# Author:	vaibhav@bhembre.com
# URL: 		http://highlightdocdemo.appspot.com/
# Runtime: Python v2.6.1
#
# Description:
# 	The following code acts as a solution to the string-search coding problem. The example (deep dish pizza) provided in the problem 
#	statement was very interesting and I tried to do my best keeping that as a frame of reference. Although, the problem looks
# 	simple at the first glance, there are infact a wide realm of test-cases which need to be covered to develop
# 	an ideal solution for the problem. I have tried to attempt an approach aimed at solving most of them as follows. 
# 	As an aside, I have also hosted a working copy on Google's AppEngine which is available at the aforementioned URL.
#
#	Input(2:string): A document string to compare against a query string.
# 	Output(1:string): A single string comprising of relevant information pertaining to the 'query' from the 'doc'.

import re

wrapTag = "Highlight" 	# Name of the tag we need to enclose the instances of matched query in.
limit = 4 				# Maximum no. of highlighted results that ought to be present in the output snippet.

def highlight_doc(doc, query):
	"""
	Args:
		doc - String that is a document to be highlighted
		query - String that contains the search query
	Returns:
		The the most relevant snippet with the query terms highlighted
	"""
	# Strip out unncessary whitespaces present in the original document
	# Includes: newline characters(LF), tabs, and CR+LF (Windows newline char)
	try:
		doc = re.sub(r"(^|[\n]+|[\t]+|(\r\n)+)", "", doc)
	except TypeError:
		return "Inputs to 'highlight_doc' must be in string format."
	
	while(True):
		# Remove trailing whitespaces from the query
		try:
			query = re.sub("[\s\t\n]*$", "", query)
		except TypeError:
			return "Inputs to 'highlight_doc' must be in string format."
		
		# Perform a naive sentence boundary detection by checking for the termination of the previous sentence
		# or start of the first sentence if it is one, till a terminal punctuation mark is encountered announcing
		# end of the current sentence. The regex is compiled into a pattern and is run over the document to
		# find a match.
		patt = re.compile("[\.!\?|^]?([A-Z]?[^\.!\?]*[\.]*\W" + query + ".*?[\.!\?])", re.IGNORECASE)
		match = patt.findall(doc)
		
		if len(match) == 0: 					# No match found till now. 
			subqlist = query.split(" ")			# But wait, don't give up yet. Try for a match for a substring of
			query = " ".join(subqlist[1:])		# the query by removing the first word. 
			if query == "":
				return "No match found." 		# None of the words match. Sigh. Better luck next time.
				break
			else:
				continue						# 'Goto' start of the while loop. Continue search for the 'new' query.
		
		else:
			mainstr = tempstr = ext = ""
			matchlist = []
			
			# This construct is used to coalesce together the results found, if present within adjacent sentences.
			# The sentences that exist separately (divided by at least another sentence) are not merged together.
			# The results are further stored in matchlist [] before pushing them onto the output stream.
			for i in range(len(match) if len(match) < limit else limit):
				if (i == 0): 
					matchlist.append(match[i])
					continue
				
				# Concatenate the recently pushed value in matchlist with the currently extracted sentence 
				# from 'match' and check if they occupy neighbouring positions in 'doc' using 'checkstr'.
				tempstr = "".join(matchlist[-1:]) + match[i]  
				
				# Check if 'tempstr' is contained as-is by 'doc'. If True, push 'tempstr' in.
				# Otherwise it means the two or more sentences,'tempstr' comprises of, are not adjacent
				# and hence have to be saved separately.
				# This ensures that adjacent sentences relevant to the query are displayed together.
				if (checkstr(tempstr, doc)):					 
					matchlist.pop()
					matchlist.append(tempstr)
				else:
					matchlist.append(match[i])
			
			# Preprocessing for the output. Create enclosing braces for our tag.
			startWrap = "[[" + wrapTag.upper() + "]]"
			endWrap = "[[END" + wrapTag.upper() + "]]"
			
			count = 0
			for outstr in matchlist	:
				if count > 0: mainstr += "..."		# If matchlist contains more than one elements, it means disjoint sentences
				else: count += 1					# exist. Display a triple dot sequence to denote the separation.
				
				# Perform a search for the query-string present within every entry of list of strings, matchlist consists of.
				# Generate a list of slightly distinct versions of the query string present. (case-sensitive)
				pattquery = re.findall(query, outstr, flags=re.IGNORECASE)
				
				# Remove duplicates from the 'pattquery' list. We do not wish to wrap a same query up by multiple markdown tags.
				pattquery = list(set(pattquery))
				
				tempstr = outstr
				for p in pattquery:
					# Place the query within the markdown tags as required before passing it onto the output snippet.
					tempstr = re.sub(p, startWrap + p + endWrap, tempstr)
				mainstr += tempstr
				
			# Remove any trailing/preceding whitespaces before returning our snippet
			mainstr = re.sub("(^[\s]*|[\s]*$)", "", mainstr)
			return mainstr
			break

def checkstr(strmatch, doc):
	"""
	Args:
		strmatch - String to be checked for a 1-1 match(presence check)
		doc - String against which strmatch is checked
	Returns:
		True, if strmatch is present as-is within doc
		False, otherwise
	"""
	return (re.search(strmatch, doc) != None)