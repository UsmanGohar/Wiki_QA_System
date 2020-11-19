# Name: Usman Gohar
# Programming Assignment 5
# Question Answering System
# NLP FALL 2017
# Date: 06/12/17

# The objective of the assignment is to design a question answering system based on "WH" questions. (Who, What, Where, When)
# The system should answer in complete senetences e.g When was George Washington Born? System: George Washington was born on Feb 22,1732
# The system should not return gibberish and instead return, answer not found. 
# The system runs interactively and asks the user for question, until Exit is typed.
# It is assumed that the user will ask the correct question and not give inappropriate question forms.
# Query's are fed to Wikipedia to retrieve information

# Algorithm:

# The following steps are being followed for the implementation of the system

	# 1) User asks a WH question
	# 2) The query is tokenized to retrieve the individual words in the question
	# 3) The system searches for multiple patterns reformulated from the question. After studying Wikipedia, I realized most of the pages can be correctly retrieved
	#    if the WH word and the articles i.e is,was etc are removed and searched from. This means removing n-grams from the end of the question until the 3rd word in
	#    the question. This method has very high likelihood of finding a relevant page.
	# 4) After page is retrieved, one of these things is done. First the infobox is checked. For most of the When questions, the dates are listed there. Similarly
	#    the locations are almost always included in the infoboxes for Where questions. For the rest of the WH questions, the summary of the page is retrieved and
	#    the he pattern is searched for.
	# 5) If the pattern is matched, it is printed to the output else the system concedes its failure.

# TEST CASE

# 1) Input: Who is Governor Of Minnesota?
# 2) Tokenize the query to n-grams and removed Who, is and ?
# 3) Search for the different reformulations formed by stripping from the end of the query e.d Governor of Minnesota, Governor of, Governor etc.
# 4) The page and its summary is retrieved. The pattern is matched and returned.
# 5) Output: Mark Dayton is the Governor of Minnesota

import wptools
import nltk
import re

def stem(word):			# Stem function designed to stem words. This is very helpful in getting page retrievals since Wikipedia will not retrieve a page if
				# the word is ending in non-root form

     for ending in ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']:	# An array containing various possible stems
         if word.endswith(ending):							# If the word end with the above stems
             return word[:-len(ending)]							# Strip the stem and return
     return word

print "\nThis is a question answering system by Usman Gohar. Please ask questions start with When, Who, What & Where. Type 'Exit' to quit\n"

while(question!="Exit"):# Keep asking the user for questions until Exit is typed
     question=raw_input("User:")			# User enters question
     tokens = nltk.word_tokenize(question)		# Tokenize the question into n-grams
     count=len(tokens)                                  # Find the length of the query.  This is used to determine positions of keywords
     if question=="Exit":				# If Exit is typed, end program
          
          print "Thank you. Have a nice day"
          break

     if "When" and "born" in question:		# If the question is about when a person was born, search for birth date in infobox. Works almost everytime
          test=1
          i=0;					# Counter to check when to stop searching for page when all reformulations are exhausted
          while True:
               try:				# Error handling system to prevent program for crashing if page not found
                    ella = wptools.page(" ".join(tokens[2:count-i]),silent=True).get()   # Search for the n-gram query in Wikipedia. This will loop through all reformulations
                    dict=ella.data['infobox']		# If found, retrieve infobox
                    a=dict["birth_date"]			# Search for birth_date in infobox
                    a=a.split('|')				# Strip unnecessary items
                    r8=re.sub(r"When was (.*)", r" ".join(tokens[2:count-i]) + ' was born on ' + a[1] + '/' + a[2] +'/' + a[3].strip('}') ,question)	# Reformulate query to print answer
                    print "System -> " + r8			# Print output
                    i=i+1
                    break
               except:
                    i=i+1					# If failed, continue to next reformulation
                    if (i==count):				# If all reformulations tested, end search
                         print "Sorry, answer not found"
                         break

     if "When" in question and test==0:             # If when question but not about birth_date
          i=0;                                   # Counter to check when to stop searching for page when all reformulations are exhausted
          while True:
               try:                           # Error handling system to prevent program for crashing if page not found
                    ella=wptools.page(" ".join(tokens[2:count-i]),silent=True).get()    # Search for the n-gram query in Wikipedia. This will loop through all reformulations
                    data=ella.data['extext']              # If found, retrieve summary
                    data=data.encode("utf-8")             # Convert to string
                    r8=re.sub(r"When was (.*)?", r" ".join(tokens[2:count-2]) + " was " + "".join(tokens[count-2]) ,question)   # Reformulate query to print answer
                    matchObj = re.search(r8 + " (in|on) \w+",data)       # Search for is|on
                    print matchObj.group()                #  # Print output
                    i=i+1
                    break
               except:
                    i=i+1
                    if(i==count):
                         print "Sorry, answer not found"
                         break

# THE COMMENTS ARE THE SAME FOR THE REST SO WERE NOT REPEATED UNLESS SOMETHING DIFFERENT IS TO BE EXPLAINED

     if "Where" in question:         # If Where question
          i=0
          while True:
               try:
                    ella=wptools.page(" ".join(tokens[2:count-i]),silent=True).get()
                    dict=ella.data['infobox']
                    a=dict["location"]
                    a=re.sub(r'[\[\]]', '', a)
                    cleanr = re.compile('<.*?>')  #Remove html tags such as <br> (All tags within <> will be removed)
                    a = re.sub(cleanr, '', a)
                    r8=re.sub(r"Where is (.*)", r" ".join(tokens[2:count-1]) + ' is in ' + a,question)
                    print r8
                    i=i+1
                    break
               except:
                    i=i+1
                    if(i==count-2):
                         print "Sorry, answer not found"
                         break
     if "What" in question:          # If What question
          i=0
          while True:

               try:
                    ella=wptools.page(" ".join(tokens[2:count-i]),silent=True).get()
                    data=ella.data['extext']
                    data=data.encode("utf-8")
                    data=re.sub(r'[\*]', '',data)
                    matchObj=re.search(r"^([^.]*).*",data)
                    print "\n" + "System: " + matchObj.group(1)
                    i=i+1
                    break
               except:
                    i=i+1
                    if(i==count-2):
                         print "Sorry, answer not found"
                         break

     if "Who" in question:           # If Who question

          i=0
          while True:
               if ''.join(tokens[1])=="is":        # This means the question is usually about a person, which means the answer can be found at the top of the summary
                    
                    try:
                         if ''.join(tokens[2])=="the":
                              ella=wptools.page(" ".join(tokens[3:count-i]),silent=True).get()
                         else:
                              ella=wptools.page(" ".join(tokens[2:count-i]),silent=True).get()
                              dict=ella.data['infobox']
                              a=dict["incumbent"]
                              a=re.sub(r'[\[\]]', '', a)
                              q=question.split(" ")
                              print "System: " + a + " is " + " ".join(tokens[2:count-1])
                              i=i+1
                              break

                    except:
                         i=i+1
                         if(i==count-2):
                              print "Sorry, answer not found"
                              break
               print "Sorry, answer not found"
               break
