#!/usr/bin/env python
# 
# Author:	vaibhav@bhembre.com
# URL: 		http://highlightdocdemo.appspot.com/
# Runtime: Python v2.6.1
#
# Description:
# 	This code file contains test cases to run against the 'highlightdoc' module. The test cases are elaborated upon
# 	at the place of their definition. A sample string is assumed as the document to compare against, for our convenience.

import highlightdoc
import re
import unittest

doc = "There is a fire man. There is a fire dog. There is a fat dog. \
			There is a fire boy. There is a fat man."

class TestHighlight(unittest.TestCase):
	
	def setUp(self):
		""" Set up a new instance of helper class before running every test. """
		self.doc = doc
		self.h = Helper()
	
	def test_snippetsize(self):
		""" Test case to verify if the snippet size is greater than the query size. """
		query = "boy"
		outstr = "There is a fire " + self.h.tagQuery(query) + "."
		teststr = self.h.testQuery(query)
		self.h.outTest("Snippet-size", query, outstr, teststr)
		
		self.assertEqual(outstr, teststr)
		assert len(teststr) >= len(query), "Snippet size less than query size test fails."
	
	def test_case_insensitivity(self):
		""" Test case to check if search result yields to queries in a case-insensitive
			manner."""
		query = "Fat"
		oritext = "fat"
		outstr = "There is a " + self.h.tagQuery(oritext) + " dog." \
				+ self.h.ext + " There is a " + self.h.tagQuery(oritext) + \
				" man."
		teststr = self.h.testQuery(query)
		self.h.outTest("Case-sensitivity", query, outstr, teststr)
		
		self.assertEqual(outstr, teststr, "Case-sensitivity test fails.")
	
	def test_multiline(self):
		""" Test case to verify if the snippet containing the results span from different
			parts of the document. A relevant snippet can contain two non-adjacent sentences
			in which case it should constitute of a triple dot sequence ('...')  marking 
			the separation. """
		query = "fire"
		teststr = self.h.testQuery(query)
		self.h.outTest("Multiple Sentences Display", query, "...", teststr)
		
		assert (re.search("[\.]{3,4}", teststr) != None), "Multiple sentence test fails."
	
	def test_singleline(self):
		""" A snippet comprising entirely of a sequence of adjacent sentences should not contain 
			a triple dot sequence string ('...'). """
		query = "dog"
		teststr = self.h.testQuery(query)
		self.h.outTest("Adjacent sentences display", query, "...", teststr)
		
		assert (re.search("[\.]{3,4}", teststr) == None), "Adjacent sentences test fails."
		
	def test_query_not_success(self):
		""" A proper message should be displayed in case the query is unable to produce a match 
			within the document. """
		query = "a fat clout"
		teststr = self.h.testQuery(query)
		self.h.outTest("Search Not Successful", query, "\"\"", teststr)
		
		assert (teststr == "No match found."), "Query not successful test fails."
		
	def test_query_till_last_word(self):
		""" If the original query does not generate a match, try again by truncating the inital bits of
			the query and see if the remaining generate a result. Keep doing this till the last word. The pattern
			of removing the first word is chosen as it usually contains an adjective or adverb part-of-speech
			whereas the latter part consists of the noun, the results containing would be more suited to the 
			intent of the user querying. However, this is an extremely naive way of searching for a match and 
			superior NLP/IR techniques need to be in place to keep the user happy. """
		query = "a super fast dog"
		teststr = self.h.testQuery(query)
		self.h.outTest("Query until last word", query, "\"\"", teststr)
		
		assert (teststr != "No match found."), "Query till last word test fails."
		
	def test_nonstring_input(self):
		""" Verifies if both the inputs to the highlightdoc function are of type string. """
		query = 121
		teststr = self.h.testQuery(query)
		testerr = "Inputs to 'highlight_doc' must be in string format."
		
		self.h.outTest("Nonstring input", query, "121", teststr)
		
		self.assertEqual(teststr, testerr, "Nonstring input test fails.")
		
# Helper class for helping print/test the test cases		
class Helper(object):

	def __init__(self):
		self.wrapTag = "highlight"
		self.startWrapTag = "[[" + self.wrapTag.upper() + "]]"
		self.endWrapTag = "[[END" + self.wrapTag.upper() + "]]"
		self.ext = "..."
	
	# Construct the 'tag-wrapper'.
	def tagQuery(self, query):
		return self.startWrapTag + query + self.endWrapTag
	
	# Call highlight_doc function once invoked. 
	# document is passed through globally declared 'doc' while query is passed from the
	# input parameter.	
	def testQuery(self, query):
		return highlightdoc.highlight_doc(doc, query)
	
	# Make it look nice on the outputstream.
	def outTest(self, tag, query, outstr, teststr):	
		print "\n" + ("-"*40)
		print "Testing: " + tag
		print "Query: " + str(query) + "\n"
		print outstr
		print "AND"
		print teststr
	
if __name__ == '__main__':
	unittest.main()