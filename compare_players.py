import sys

n_games = 5

for i in n_games:
	cmd = "python iago_client_ab.py 1 >> out.txt"
	print(cmd)
	os.system(cmd)

	cmd = "python iago_client_ab.py 2 >> out.txt"
	print(cmd)
	os.system(cmd)