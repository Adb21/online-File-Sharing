from fuzzywuzzy import fuzz 

class ProfileChecker:

	def __init__(self):
		self.total_score = 0
		self.matching_attributes=[]
		self.non_matching_attributes=[]
		self.ignored_attributes=[]

	# this method compares 2 profiles baseed on fields passed
	def find_duplicates(self,profiles=[],fields=[],strScore=80):
		try:
			for field in fields:
				if profiles[0][field] == None or profiles[1][field] == None:
					self.ignored_attributes.append(field)
					continue

				# check for fields of type String
				if type(profiles[0][field]) == str or type(profiles[1][field]) == str:
					profiles[0][field] = profiles[0][field].lower()
					profiles[1][field] = profiles[1][field].lower()
					if field == 'email' or field == 'first_name' or field == 'last_name':
						continue

					score = self.getScore(profiles[0][field],profiles[1][field])
					if score>strScore:
						self.total_score += 1
						self.matching_attributes.append(field)
					else:
						self.total_score -= 1
						self.non_matching_attributes.append(field)

				# check for fields of type Integer
				if type(profiles[0][field]) == int or type(profiles[1][field]) == int:
					score = self.getScore(profiles[0][field],profiles[1][field])
					if profiles[0][field] == profiles[1][field]:
						self.total_score += 1
						self.matching_attributes.append(field)
					else:
						self.total_score -= 1
						self.non_matching_attributes.append(field)

			# update score with combinations of email+first_name+last_name
			self.checkCombinations(profiles[0],profiles[1])

			if len(self.matching_attributes)==0:
				self.matching_attributes.append(None)
			if len(self.non_matching_attributes)==0:
				self.non_matching_attributes.append(None)
			if len(self.ignored_attributes)==0:
				self.ignored_attributes.append(None)

			return {'result':'Duplicate' if self.total_score > 1 else 'Not Duplicate','total_score':self.total_score,'matching_attributes':self.matching_attributes,'non_matching_attributes':self.non_matching_attributes,'ignored_attributes':list(set(self.ignored_attributes))}
		
		except Exception as e:
			print(f"error : {e}")
			return None

	# this method returns score of 2 string comparision using fuzzywuzzy lib
	def getScore(self,str1,str2):
		return fuzz.partial_ratio(str1,str2)

	# this method will update score based on combination of email+first_name+last_name
	def checkCombinations(self,cmb1 = {},cmb2 = {}):
		strScore = []

		# baseCase: ['email','first_name','last_name']
		score = self.getScore(
			f"{cmb1['email']}{cmb1['first_name']}{cmb1['last_name']}",
	    	f"{cmb2['email']}{cmb2['first_name']}{cmb2['last_name']}"
	    )
		
		if score > 80:
			
			self.total_score += 1
			self.matching_attributes.extend(['email','first_name','last_name'])
			return

		else:
		    # case 0 : ['email','first_name']
			strScore.append(self.getScore(
				f"{cmb1['email']}{cmb1['first_name']}",
		    	f"{cmb2['email']}{cmb2['first_name']}"
		    ))

		    # case 1 : ['email','last_name']
			strScore.append(self.getScore(
				f"{cmb1['email']}{cmb1['last_name']}",
		    	f"{cmb2['email']}{cmb2['last_name']}"
		    ))

		    # case 2 : ['first_name','last_name']
			strScore.append(self.getScore(
				f"{cmb1['first_name']}{cmb1['last_name']}",
		    	f"{cmb2['first_name']}{cmb2['last_name']}"
		    ))
			
		case = strScore.index(max(strScore))
		
		if case == 0 and strScore[case]>80 :
			self.total_score += 1
			self.matching_attributes.extend(['email','first_name'])
			self.ignored_attributes.extend(['last_name'])
		elif case == 1 and strScore[case]>80 :
			self.total_score += 1
			self.matching_attributes.extend(['email','last_name'])
			self.ignored_attributes.extend(['first_name'])
		elif case == 2 and strScore[case]>80 :
			self.total_score += 1
			self.matching_attributes.extend(['first_name','last_name'])
			self.ignored_attributes.extend(['email'])
		else:
			self.ignored_attributes.extend(['email','first_name','last_name'])

