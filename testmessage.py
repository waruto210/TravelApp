import message

label1 = message.Message()

label1.register('444', '444', '444')
label1.register('555', '555', '555')

x = label1.sign_in('333', '333')
y = label1.sign_in('444', '444')
y.add_routes
print(x)
print(y)
label1.update_message()

label2 = message.Message()
z = label2.sign_in('111', '111')
print(z)
