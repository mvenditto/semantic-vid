def chunk(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

def paginate(videos):
	return chunk(list(videos), 4)
