import os
import gc
import sys
import getpass
import argparse
from time import perf_counter 

from myClass import file_crypto

def main():
	
	t1_start = perf_counter()
	args = help()
	a = file_crypto()
	if not args.password:
		p = getpass.getpass()
		a.set_passwd(p)
	else:
		a.set_passwd(args.password)

	if args.encrypt and args.decrypt:
		print ("Cannot set encryptor and decryptor at the same time")
		sys.exit()
	if not args.object:
		print ("Output directory must be specific")
		sys.exit()

	if args.encrypt:
		print ("Validating password ... .. .")
		if not a.check_password():
			print ("Invalid password ... .. .")
			sys.exit()
		
		if os.path.isfile(args.encrypt) and os.path.isdir(args.object):				
			print ("Encrypting ... .. .")
			a.set_fi(args.encrypt)
			a.set_fo(os.path.join(args.object, os.path.basename(args.encrypt) + ".enc"))			
			if args.associate_data:
				a.set_aad(args.associate_data)
			a.encrypt_file()
			print ("Encrypt done.")
		else:
			print ("File or folder do not exist")
			sys.exit()
		
		if args.sha512:
			calc_hash = a.calculate_hash()
			print ("Plain data", calc_hash[0])
			print ("Encrypted data", calc_hash[1])

		if args.wipe:
			print ("Wiping data ... .. .")
			a.wipe_data()
			print ("Wiped.")
			args.remove = True
		
		if args.remove:
			print ("Removing data ... .. .")
			a.simple_delete()
			print ("Removed.")

	if args.decrypt:
		print ("Validating password ... .. .")
		if not a.check_password():
			print ("Invalid password ... .. .")
			sys.exit()
		
		if os.path.isfile(args.decrypt) and os.path.isdir(args.object):
			print ("Decrypting ... .. .")
			a.set_fi(args.decrypt)
			a.set_fo(os.path.join(args.object, os.path.basename(args.decrypt)[:-4]))
			if args.associate_data:
				a.set_aad(args.associate_data)
			a.decrypt_file()
			print ("Decrypt done.")
		else:
			print ("File or folder do not exist")
			sys.exit()
		
		if args.sha512:
			calc_hash = a.calculate_hash()
			print ("Encrypted data", calc_hash[0])
			print ("Plain data", calc_hash[1])

		if args.wipe:
			print ("Wiping data ... .. .")
			a.wipe_data()
			print ("Wiped.")
			args.remove = True
		
		if args.remove:
			print ("Removing data ... .. .")
			a.simple_delete()
			print ("Removed.")

	t1_stop = perf_counter() 
	print("Elapsed time during the whole program in seconds:", t1_stop-t1_start) 

	gc.collect()


if __name__ == '__main__':
	main()
