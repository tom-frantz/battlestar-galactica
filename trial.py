def seed(given_seed):
	seed_name = given_seed
	given_seed = hash(given_seed)
	print("Seed Given Hash for", seed_name + ":", given_seed)
	given_seed = int(given_seed)
	if given_seed < 0:
		given_seed = -given_seed
	while given_seed < 1000000000:
		given_seed *= 10
	if given_seed > 10000000000:
		given_seed = str(given_seed)
		given_seed = given_seed[0:10]
	print(given_seed)


seed("Memedreamslove")
seed("dank")
seed("Memedreamslove")
