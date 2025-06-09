import pexpect
cmd = "venv/bin/python ./pccsadmin.py fetch"
child = pexpect.spawn(cmd)
child.expect("Please input ApiKey for Intel PCS") # the string you expect
child.sendline("115d3d4afdbe4331afb9817d68f87b0b") # the string with which you'd like to respond
print(child.before.decode())
child.expect("Would you like to remember Intel PCS ApiKey in OS keyring") # the string you expect
child.sendline("n") # the string with which you'd like to respond
print(child.before.decode())
child.expect("Do you want to save the list") # the string you expect
child.sendline("n") # the string with which you'd like to respond
print(child.before.decode())
child.wait()
child.expect(pexpect.EOF)
print(child.before.decode())
