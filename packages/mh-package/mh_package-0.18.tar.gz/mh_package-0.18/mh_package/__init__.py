from mh_package import Birds

def joke():
    print ("in joke....0.18")
    return (u'my mh_package version 0.18.')

if __name__ == '__main__':
    print ('hello world...')
    joke()
    myBird = Birds.Birds()
    myBird.printMembers()

