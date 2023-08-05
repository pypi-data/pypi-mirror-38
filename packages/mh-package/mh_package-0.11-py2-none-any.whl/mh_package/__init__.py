from mh_package import module1
from mh_package import Birds

def joke():
    print ("in joke....0.11")
    return (u'my mh_package version 0.11.')

if __name__ == '__main__':
    print ('hello world...')
    joke()
    module1.foo1()
    myBird = Birds.Birds()
    myBird.printMembers()

