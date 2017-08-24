
read = open("raw_questions", "r")

write = open("questions", "a")



for line in read:
	if(line[:10] =="AnswerPass"):
		#write.write(line)
		continue
	if(line.split()[0] == "Answers" or line.split()[0] == "Read" ):
		continue
	if(line[0] == " "):
		continue
	if(len(line.split()) == 1):
		continue
	write.write(line)