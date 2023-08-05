"""这是从Head First Python书里面照抄的。用于学习代码发布
"""

def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
