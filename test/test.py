# this file contains errors on purpose

def real_err():
	int('xxx')

def err():
	real_err()

if __name__ == '__main__':
	err()
