def copy(source, destination):
    f1 = open(source)
    f2 = open(destination, 'w')
    f2.write(f1.read())
    f1.close()
    f2.close
