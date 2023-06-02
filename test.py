a=[1,2,3,4,5,6]
b=0
for i in a:
    if i>3:
        b=a.index(i)
        break

x=a[:b]
y=a[b:]
print(x,y)

