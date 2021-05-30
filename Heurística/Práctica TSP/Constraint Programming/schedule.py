from constraint import *

def LuciAndreaSubject (social, physical):
	if (physical == 'Andrea'):
		return social == 'Lucia'
	return True

def JuanNoLecture(monday, thursday, natural, social):
	if(monday == 'Natural Science') or (thursday == 'Natural Science'):
		return not (natural == 'Juan')
	if(monday == 'Social Science') or (thursday == 'Social Science'):
		return not (social == 'Juan')



def only2classesPerTeacher (*subject):
	juan  = 0
	lucia  = 0
	andrea  = 0
	for x in subject:
		if x =='Juan':
			juan+= 1
		elif x == 'Lucia':
			lucia+= 1
		elif x == 'Andrea':
			andrea+= 1
	return juan == 2 and lucia == 2 and andrea ==2

def maximumSlotsSubject(*slots):
	math = 0
	english = 0
	natural  = 0
	social  = 0
	spanish  = 0
	physical  = 0
	for x in slots:
		if x == 'Natural Science':
			natural+= 1
		elif x == 'Social Science':
			social+= 1
		elif x == 'Spanish L.':
			spanish+= 1
		elif x == 'Mathematics':
			math+= 1
		elif x == 'English':
			english+= 1
		else:
			physical+= 1
	return natural == 2 and social == 2 and spanish == 2 and math == 2 and english == 2 and physical == 1

#MAKE TWO DIFFERENT RESTRICTIONS
def MathNotSameDay(*slots):
	english = 0
	math = 0
	natural  = 0
	for x in slots:
		if x == 'Mathematics':
			math+= 1
		if x == 'Natural Science':
			natural+= 1
		if x == 'English':
			english+= 1
	if natural >=1:
		#This will return false in case math appears
		return not math>=1
	if english>=1:
		return not math>=1
	return math>=1 #in future check if this line can dissapear. itsupposily forces the day to have either natural or math but not both

def ContinuosSocial(*slots):
	for index, x in enumerate(slots):
		if x == 'Social Science':
			if(index+1 <= len(slots)-1):
				return (slots[index+1] == 'Social Science')
			return False
	return True

if __name__ == '__main__':

	var=Problem()

	var.addVariables(['Monday 9-10', 'Monday 10-11', 'Monday 11-12', 'Tuesday 9-10', 'Tuesday 10-11', 'Tuesday 11-12', 'Wednesday 9-10', 'Wednesday 10-11', 'Wednesday 11-12', 'Thursday 9-10', 'Thursday 10-11'],['Natural Science', 'Social Science', 'Spanish L.', 'Mathematics', 'English', 'Physical Education'])
	var.addVariables(['Natural', 'Social', 'Spanish', 'Math', 'English Language', 'PE'],['Lucia', 'Andrea', 'Juan'])

	var.addConstraint(NotInSetConstraint(['Mathematics']),('Monday 10-11', 'Monday 11-12', 'Tuesday 10-11', 'Tuesday 11-12', 'Wednesday 10-11', 'Wednesday 11-12', 'Thursday 10-11'))
	var.addConstraint(NotInSetConstraint(['Natural Science']), ('Monday 9-10', 'Monday 10-11', 'Tuesday 9-10', 'Tuesday 10-11','Wednesday 9-10', 'Wednesday 10-11', 'Thursday 9-10'))
	var.addConstraint(only2classesPerTeacher, ('Natural', 'Social', 'Spanish', 'Math', 'English Language', 'PE'))
	var.addConstraint(maximumSlotsSubject, ('Monday 9-10', 'Monday 10-11', 'Monday 11-12', 'Tuesday 9-10', 'Tuesday 10-11', 'Tuesday 11-12', 'Wednesday 9-10', 'Wednesday 10-11', 'Wednesday 11-12', 'Thursday 9-10', 'Thursday 10-11'))
	var.addConstraint(MathNotSameDay, ('Monday 9-10', 'Monday 10-11', 'Monday 11-12'))
	var.addConstraint(MathNotSameDay, ('Tuesday 9-10', 'Tuesday 10-11', 'Tuesday 11-12'))
	var.addConstraint(MathNotSameDay, ('Wednesday 9-10', 'Wednesday 10-11', 'Wednesday 11-12'))
	var.addConstraint(MathNotSameDay, ('Thursday 9-10', 'Thursday 10-11'))
	var.addConstraint(ContinuosSocial, ('Monday 9-10', 'Monday 10-11', 'Monday 11-12'))
	var.addConstraint(ContinuosSocial, ('Tuesday 9-10', 'Tuesday 10-11', 'Tuesday 11-12'))
	var.addConstraint(ContinuosSocial, ('Wednesday 9-10', 'Wednesday 10-11', 'Wednesday 11-12'))
	var.addConstraint(ContinuosSocial, ('Thursday 9-10', 'Thursday 10-11'))
	#Thursday is imposible to have Social because we only have two hours and we know 1 of them is either Maths or Natural
	var.addConstraint(LuciAndreaSubject, ('Social', 'PE'))
	var.addConstraint(JuanNoLecture, ('Monday 9-10', 'Thursday 9-10', 'Natural', 'Social'))


	solutions = var.getSolutions()
	for isolution in solutions:
		print("Monday\t\t{0} | {1} | {2}\n\nTuesday\t\t{3} | {4} | {5}\n\nWednesday\t{6} | {7} | {8}\n\nThursday\t{9} | {10}\n\nNatural Science - {11}\n\nSocial Science - {12}\n\nSpanish - {13}\n\nMathematics - {14}\n\nEnglish - {15}\n\nPhysical Education - {16}\n".format(isolution['Monday 9-10'], isolution['Monday 10-11'], isolution['Monday 11-12'], isolution['Tuesday 9-10'],
isolution['Tuesday 10-11'], isolution['Tuesday 11-12'], isolution['Wednesday 9-10'], isolution['Wednesday 10-11'], isolution['Wednesday 11-12'], isolution['Thursday 9-10'], isolution['Thursday 10-11'], isolution['Natural'], isolution['Social'], isolution['Spanish'], isolution['Math'], isolution['English Language'], isolution['PE']))
		print("---------------------------------------------")
	print(" #{0} solutions have been found: ".format(len (solutions)))
