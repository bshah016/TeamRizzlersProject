def getCol(containers):
    smallest = [[0,0],999]
    for col in containers:
        if len(col) and col[0][1] < smallest[1]:
            smallest[0] = col[0][0]
            smallest[1] = col[0][1]
    if smallest[1] == 999:
        return 0
    containers[smallest[0][1]].pop(0)
    return smallest

def getDistance(i,j,heights,containers):
    min_no_container = 1000
    no_container_ind = -1
    min_with_container = 1000
    container_ind = -1
    for ind in range(len(heights)):
        if ind != j and heights[ind] < 8:
            if len(containers[ind]) == 0:
                if abs(i-heights[ind]) + abs(j-ind) < min_no_container:
                    min_no_container = abs(i-heights[ind]) + abs(j-ind)
                    no_container_ind = ind
            else:
                if abs(i-heights[ind]) + abs(j-ind) < min_with_container:
                    min_with_container = abs(i-heights[ind]) + abs(j-ind)
                    container_ind = ind
    if min_no_container < 1000:
        return [min_no_container,no_container_ind]
    elif min_with_container < 1000:
        return [min_with_container,container_ind]
    moves_to_buffer = (7-i+j+4)
    return [moves_to_buffer,-1]

def getClosestDistance(i,j,heights):
    mindist = 1000
    container_ind = -1
    for ind in range(len(heights)):
        if heights[ind] < 8:
            if abs(i-heights[ind]) + abs(j-ind) < mindist:
                mindist = abs(i-heights[ind]) + abs(j-ind)
                container_ind = ind
    return [mindist, container_ind]
    

def getMass(ship):
    left = 0
    right = 0
    for row in ship:
        for num in range(6):
            left += row[num][0]
            right += row[num+6][0]
    return [left,right]

def main():
    # signing in
    print("Hello and welcome to Mr Keogh's shipping dock.")
    print("Enter your full name to sign in and start working")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    print("Welcome " + first_name + " " + last_name)

    # selecting manifest
    manifest_file_name = input("Please enter the manifest file name that you would like to open: ")
    file = open(manifest_file_name, "r")
    ship = [[],[],[],[],[],[],[],[]]
    for line in file:
        row = int(line[2:3])
        # col = int(line[4:6])
        weight = line[10:15].lstrip('0')
        if weight == "":
            weight = "0"
        name = line[18:].strip()
        ship[row-1].append([int(weight),name])

    for s in ship:
        print(s)
        print()

    # selecting task
    print("What would you like to do?")
    print("1. Offload containers from the ship onto the buffer or trucks")
    print("2. Balance the ship")
    selection = input()
    while selection != "1" and selection != "2":
        print("Invalid selection, please type 1 or 2")
        selection = input()

    # for offloading containers
    if(selection == "1"):
        container_freq = {}
        print("Once you are done with entering containers, enter q to quit")
        while(1):
            container_name = input("Please enter a container you would like to remove from the ship: ")
            if(container_name == "q"):
                break
            elif container_name in container_freq:
                container_freq[container_name] += 1
            else:
                container_freq[container_name] = 1
        # start A* with manhattan
        heights = [0,0,0,0,0,0,0,0,0,0,0,0]
        bufferheights = [0,0,0,0,0,0,0,0,0,0,0,0]
        for row in ship:
            for i in range(len(row)):
                if row[i][1] != "UNUSED":
                    heights[i] += 1
        containers = {}
        for i in range(len(ship)):
            for j in range(len(ship[i])):
                if ship[i][j][1] in container_freq:
                    if ship[i][j][1] in containers:
                        containers[ship[i][j][1]].append([[i,j],heights[j] - 1 - i])
                    else:
                        containers[ship[i][j][1]] = [[[i,j],heights[j] - 1 - i]]
        for container in containers:
            containers[container].sort(key=lambda x:x[1])
            while len(containers[container]) > container_freq[container]:
                containers[container].pop(container_freq[container])
        # print(containers)
        containers_by_col = [[],[],[],[],[],[],[],[],[],[],[],[]]
        for container in containers:
            for elem in containers[container]:
                containers_by_col[elem[0][1]].append(elem)
        for col in containers_by_col:
            col.sort(key=lambda x:x[1])
            # print(col)
        
        # start moving containers
        total_distance = 0
        buffercount = 0
        smallest = getCol(containers_by_col)
        while smallest != 0:
            print(smallest)
            print(containers_by_col)
            for i in range(smallest[1]):
                dist = getDistance(heights[smallest[0][1]]-1,smallest[0][1],heights,containers_by_col)
                total_distance += dist[0]
                heights[smallest[0][1]] -= 1
                if dist[1] != -1:
                    heights[dist[1]] += 1
                else:
                    dst = getClosestDistance(7,11,bufferheights)
                    total_distance += (dst*2)
                    buffercount += 1
                print(heights)
            total_distance += (7-smallest[0][0]+smallest[0][1])
            for elem in containers_by_col[smallest[0][1]]:
                elem[1] -= (smallest[1] + 1)
                print(elem)
            heights[smallest[0][1]] -= 1
            print(heights)
            print(total_distance)
            smallest = getCol(containers_by_col)
        for i in range(buffercount):
            total_distance += (getClosestDistance(7,0,heights) + 4)





        
    # for balancing ship
    elif(selection == "2"):
        # start A*
        masses = getMass(ship)
        average = (masses[0] + masses[1])/2
        deficit = average - min(masses[0],masses[1])
        lowerbound_deficit = (0.9*max(masses[0],masses[1]) - min(masses[0],masses[1]))/1.9
        print(deficit)
        print(lowerbound_deficit)


    
    file.close()

if __name__ == "__main__":
    main()