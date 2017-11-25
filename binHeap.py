from cell import Cell

class BinaryHeap:
    def __init__(self):
        # heapList will hold our data
        # initialize with root with f key of 0 in order to
        self.heapList = [Cell(-1,-1)]
        # size holds the current size of the heap
        self.size = 0

    def pushUp(self, i):
        # we use this integer division to make sure that the current node
        # has a parent in the heap; if the current index is at the top, the loop will break
        while (i / 2) > 0:
            # TODO: change the heaplist to properly calculate for cell objects
            # compare the values in the heaplist
            # if the current cell value is smaller than the cell value above, swap the
            # cells placements in the tree
            if self.heapList[i].f < self.heapList[i/2].f:
                self.swapNode(i, (i / 2))
            i = i / 2

    def insert(self, key):
        # add the key to the list
        self.heapList.append(key)
        print "Added: " , key.coordinate , "\n"
        # increment the size of the list
        self.size += 1
        # push the new node up the list
        self.pushUp(self.size)

    def pushDown(self, i):
        # moves down the list until at the bottom
        while (i * 2) <= self.size:
            #uses the smallest child method to get the smallest of the two children from the current node
            smallestChild = self.getSmallestChild(i)
            if self.heapList[i].f > self.heapList[smallestChild].f:
                self.swapNode(i, smallestChild)
            i = smallestChild

    def getSmallestChild(self, i):
        smallest = 0
        # hit the bottom of the tree, no right child
        if (i * 2) + 1 > self.size:
            smallest = i * 2
        else:
            # check which child is smallest
            if self.heapList[i * 2].f < self.heapList[(i * 2) + 1].f:
                # left child is smallest
                smallest = i * 2
            else:
                # right child is smallest
                smallest = (i * 2) + 1
        return smallest

    # removes the index
    def popIndex(self, i):
        popped = self.heapList[i]
        self.heapList[i] = self.heapList[self.size]
        self.size -= 1
        self.heapList.pop()
        self.pushDown(i)
        return popped

    # returns minimum f cell
    def pop(self):
        return self.popIndex(1)

    # implement when we hit it
    def remove(self, key):
        # find the cell object
        self.popIndex(self.findIndexByKey(1,key))
        # pop its index

    def contains(self,key):
        exists = False
        if self.findIndexByKey(1,key) != -1:
            exists = True
        return exists

    # recursive method traversing the heapList, returning the index of the located cell
    # IMPORTANT: must initially pass in '1' as 'i' argument
    def findIndexByKey(self, i, key):
        #check given node, check if has left child
        if i <= self.size:
            if key == self.heapList[i]:
                return i
        if (i * 2) <= self.size:
            #check if child is what were trying to find
            if key == self.heapList[(i*2)]:
                #child is what were trying to find, return index
                print self.heapList[i*2].f
                return i*2
            # recursive call to go down left child
            index = self.findIndexByKey(i*2, key)
            if index != -1:
                return index
            #check for right child
            if (i * 2) + 1 <= self.size:
                # check if right child is what were looking for
                if key == self.heapList[(i*2)+1]:
                    print self.heapList[i*2+1].f
                    return (i*2)+1
                # recrsuve call to go down right child
                index = self.findIndexByKey((i*2)+1, key)
                if index != -1:
                    return index
        # end of tree, or item not found
        return -1

    # helper method that swaps two nodes in the tree
    def swapNode(self, i , j):
        temp = self.heapList[i]
        self.heapList[i] = self.heapList[j]
        self.heapList[j] = temp


# used to test the Binary Heap
# def main():
#     bHeap = BinaryHeap()
#     c1 = Cell(1,1)
#     c1.f = 0
#     c2 = Cell(1,2)
#     c2.f = 4
#     c3 = Cell(1,5)
#     c3.f = 66
#     c4 = Cell(1,3)
#     c4.f = 3
#     c5 = Cell(1,4)
#     c5.f = 2
#     bHeap.insert(c1)
#     bHeap.insert(c2)
#     bHeap.insert(c3)
#     bHeap.insert(c4)
#     bHeap.insert(c5)
#     print bHeap.findIndexByKey(1,c2)
#
#
#
# if __name__ == "__main__":
#     main()
