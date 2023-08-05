from mh_package import Birds
from mh_package import tfs_process

def joke():
    print ("in joke....0.17")
    return (u'my mh_package version 0.17.')

if __name__ == '__main__':
    print ('hello world...')
    joke()
    myBird = Birds.Birds()
    myBird.printMembers()

