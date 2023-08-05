# from mh_package import Module1
from mh_package import Birds

def joke():
    print ("in joke....0.16")
    return (u'my mh_package version 0.16.')

if __name__ == '__main__':
    print ('hello world...')
    joke()
    # Module1.foo1()
    myBird = Birds.Birds()
    myBird.printMembers()

