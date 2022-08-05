class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binary image
        return: a list/dict of regions"""
        def recursiveReassign(cur, newVal):
            if cur not in pointsRegions or pointsRegions[cur] == newVal:
                return
            pointsRegions[cur] = newVal
            recursiveReassign((cur[0]-1,cur[1]), newVal) # go up first
            recursiveReassign((cur[0],cur[1]-1), newVal) # then go left

        regions = dict()
        pointsRegions = dict() #key=tuple (index location) value = regionNumber - we'll reverse this at the end to produce regions

        curRegion = 0
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                if image[row][col] == 0: #found a colored dark pixel, now decide which region it belongs to
                    #neither up nor left are assigned
                    if (row-1,col) not in pointsRegions and (row,col-1) not in pointsRegions:
                        curRegion += 1
                        pointsRegions[(row,col)] = curRegion
                    #up is assigned
                    elif (row-1,col) in pointsRegions:
                        pointsRegions[(row,col)] = pointsRegions[(row-1,col)]
                        if (row,col-1) in pointsRegions and pointsRegions[(row,col-1)] != pointsRegions[(row,col)]: #up disagrees with left!
                            recursiveReassign((row,col-1),pointsRegions[(row,col)])
                            curRegion -= 1
                    #left is assigned and up isn't
                    else:
                        pointsRegions[(row,col)] = pointsRegions[(row,col-1)]

        for key in pointsRegions.keys():
            if pointsRegions[key] in regions:
                regions[pointsRegions[key]].add(key)
            else: regions[pointsRegions[key]] = {key}
        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pixels in a region
        returns: region statistics"""

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)

        return 0

    def mark_image_regions(self, image, stats): 
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text. 
        takes as input
        image: a list/dict of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""

        return image

