def convert_to_ordinal_number(number):
	"""Converts a number to an ordinal number"""
	
	if number % 100//10 != 1:
		if number % 10 == 1:
			ordinal_number = u"%d%s" % (number, "st")
		elif number % 10 == 2:
			ordinal_number = u"%d%s" % (number, "nd")
		elif number % 10 == 3:
			ordinal_number = u"%d%s" % (number, "rd")
		else:
			ordinal_number = u"%d%s" % (number, "th")
	else:
		ordinal_number = u"%d%s" % (number, "th")

	return ordinal_number