import pexpect
cmd = "venv/bin/python ./pccsadmin.py put -u https://localhost:8081/sgx/certification/v4/platformcollateral"
child = pexpect.spawn(cmd)
child.expect("Please input your administrator password for PCCS service") # the string you expect
child.sendline("intel@123") # the string with which you'd like to respond
print(child.before.decode())

child.expect("Would you like to remember password in OS keyring") # the string you expect
child.sendline("n") # the string with which you'd like to respond
print(child.before.decode())

#child.expect("Do you want to save the list") # the string you expect
#child.sendline("n") # the string with which you'd like to respond
#print(child.before.decode())

#child.wait()
#print(child.before.decode())
#child.interact()
child.expect(pexpect.EOF)
print(child.before.decode())
