s_uname="vetrivel_rs"
s_passwd="vel123"
username=input("Enter your username:")
if username==s_uname:
    print("Your username is correct")
    password=input("Enter your password:")
    if password==s_passwd:
        print("Your password is correct")
    else:
        print("Your password is wrong")
else:
    print("Your username is wrong, so your not allowed to log in")