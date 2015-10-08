import string
from random import Random,randint
from lepl.apps.rfc3696 import HttpUrl
import sqlite3

class Url_Shortener():
	
	def __init__(self):
		self.char_set= string.ascii_letters + string.digits
		self.base= len(self.char_set)
		self.connection= sqlite3.connect('url_database')
		self.db= self.connection.cursor()
		self.db.execute("create table if not exists url_shortener(id integer primary key autoincrement,\
			long_url varchar(1000),short_url varchar(30))")
		self.validator= HttpUrl()

	def process_url(self,long_url):

		index_of_slash= long_url.rfind('/')
		domain= long_url[:index_of_slash]
		id_url= long_url[index_of_slash+1:] #get the string after the '/' which is the string to be encoded

		return index_of_slash,domain,id_url


	def encode_url(self,long_url):
		"""

		returns the short url if the long url is valid, -1 if it's invalid

		"""

		##validate the url
		if self.validator(long_url) == False:
			print " Please enter a valid URL (http://sampleurl.com) "
			return -1


		##check if the long_url is already present in the database, if yes the short_url corresponding to it
		existing_row= self.db.execute("select * from url_shortener where long_url='%s'"%long_url).fetchone()
		if existing_row!=None:
			return existing_row[2]

		domain="http://sho.rt"  #my_custom domain name
		cursor= self.db.execute("select max(id) from url_shortener")
		max_num= cursor.fetchone()[0]
		if max_num==None:
			max_num=1
		else:
			max_num+=1
		
		auto_increment_num= max_num #use the next id to encode create short url
		digits_base=[]
		while auto_increment_num > 0:
			remainder= auto_increment_num%self.base
			digits_base.append(remainder)
			auto_increment_num/=self.base
		digits_base.reverse()

		short_url= domain+'/'+''.join([self.char_set[i] for i in digits_base])

		statement= "insert into url_shortener(long_url,short_url) values('%s','%s')"%(long_url,short_url)

		self.db.execute(statement)

		return short_url

	def decode_url(self,encoded_string):

		"""

		returns the original url

		"""

		_,_,id_url= self.process_url(encoded_string)

		i=0
		orig_id=0
		for character in id_url[::-1]:
			index_of_char= self.char_set.find(character)
			orig_id+= pow(self.base,i)* index_of_char
			i+=1
		get_long_url= self.db.execute("select * from url_shortener where id=%d"%orig_id).fetchone()[1]
		return get_long_url



##test the methods

def main():
	my_url= Url_Shortener()
	while(1):
		try:
			print "\n"
			long_url= raw_input("Enter you long url: ")
			short_url= my_url.encode_url(long_url)
			if short_url == -1:
				#the URL is invalid
				continue
			print "\nHere's your short_url: ",short_url
			#print "\n\n"
			print "decoding it again to test: ",my_url.decode_url(short_url)
			my_url.connection.commit() #commit changes to the database
			print "\n"
		except:
			break

if __name__=="__main__":
	main()