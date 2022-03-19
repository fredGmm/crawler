#!/usr/bin/python3


from P4 import P4, P4Exception  # Import the module

p4 = P4()  # Create the P4 instance
p4.port = " "
p4.user = " "
p4.client = " "  # Set some environment variables
p4.password = ""

try:  # Catch exceptions with try/except
    p4.connect()  # Connect to the Perforce server
    #  info = p4.run( "info" )        # Run "p4 info" (returns a dict)
    #   for key in info[0]:            # and display all key-value pairs
    #     print(key)
    #   p4.run( "edit", "file.txt" )   # Run "p4 edit file.txt"
    #   p4.run()
    ret = p4.run("describe", 20)
    print(ret)
    ret2 = p4.run("depots")
    print(ret2)
    # tapdApi.pushChangelist(20, )

    p4.disconnect()  # Disconnect from the server
except P4Exception:
    for e in p4.errors:  # Display errors
        print(e)

# 第一个注释
print("Hello, Python!")  # 第二个注释
