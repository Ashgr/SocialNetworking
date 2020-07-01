class UserError(Exception):
    pass

def binarySearchNetwork(network,user1,user2):
    right = right2 = len(network)
    left = left2 = 0
    user_found = [[user1],[user2]]

    while right>left or right2>left2:

        if right>left:
            mid = (left+right)//2
            if user1 == network[mid][0]:
                user_found[0].append(mid)
                left = right
            elif user1<network[mid][0]:
                right = mid
            elif user1 > network[mid][0]:
                left = mid
        if right2 > left2:
            mid2 = (left2 + right2) // 2
            if user2 == network[mid2][0]:
                user_found[1].append(mid2)
                left2 = right2
            elif user2 < network[mid2][0]:
                right2 = mid2
            elif user2 > network[mid2][0]:
                left2 = mid2

    return user_found

def create_network(file_name):
    friends = open(file_name).read().splitlines()
    network = []
    seen = []
    for line in friends[1:]:
        user = line.split()
        user[0] , user[1] = int(user[0]) , int(user[1])
        if user[0] in seen:
            indx = network[seen.index(user[0])]
            indx[1].append(user[1])
        else:
            network.append((user[0] , [user[1]]))
            seen.append(user[0])

        if user[1] in seen:
            indx = network[seen.index(user[1])]
            indx[1].append(user[0])
        else:
            network.append((user[1] , [user[0]]))
            seen.append(user[1])
    network.sort(key = lambda x: x[0])
    for frnd in network:
        two_friend = frnd[1]
        s = sorted(two_friend)
        frnd = (frnd[0],s)
    for user in network:
        user[1].sort()
    return network

def checkUser(network , user):
    for i in network:
        if i[0] == user:
            return True
    raise ValidError("User does not exist")

def getCommon(user1 , user2 , network):
    common = []
    findFriend = binarySearchNetwork(network , user1, user2)
    if user1 == findFriend[0][0]:
        user1_frineds = network[findFriend[0][1]][1]
        user2_frineds = network[findFriend[1][1]][1]
    else:
        user1_frineds = network[findFriend[1][1]][1]
        user2_frineds = network[findFriend[0][1]][1]

    i = j = 0
    while i<len(user1_frineds) and j<len(user2_frineds):
        if user1_frineds[i] < user2_frineds[j]:
            i+=1
        elif user2_frineds[j] < user1_frineds[i]:
            j+=1
        else:
            common.append(user1_frineds[i])
            j+=1
            i+=1
    return common

def numFriends(user,network):
    l = 0
    r = len(network)
    while l < r:
        mid = (l + r) // 2
        if network[mid][0] == user:
            return len(network[mid][1])
        if network[mid][0] > user:
            r = mid
        if network[mid][0] < user:
            l = mid
def list_of_friends(network,user):
    l = 0
    r = len(network)
    while l<r:
        mid = (l+r)//2
        if network[mid][0] == user:
            return network[mid][1]
        if network[mid][0] > user:
            r = mid
        if network[mid][0] <user:
            l = mid

def userExist(fileName,user1,user2):
    file = open(fileName, "r")
    exist = False
    for line in file.readlines():
        line = line.split()
        if (line[0] == str(user1) and line[1] == str(user2)) or (line[0] == str(user2) and line[1] == str(user1)):
            exist = True
    file.close()
    if not exist:
        inFile = open(fileName,"a")
        inFile.write("\n"+str(user1) + " " + str(user2))
        inFile.close()

def add_Friendship(network,user1,user2,fileName):
    for user in network:
        if user[0] == user1:
            if user2 in user[1]:
                continue
            else:
                user[1].append(user2)
                user[1].sort()
        if user[0] == user2:
            if user1 in user[1]:
                continue
            else:
                user[1].append(user1)
                user[1].sort()
    userExist(fileName,user1,user2)

def recommendationForUser(network, user):
    checkUser(network,user)
    set_of_users = []
    for i in network:
        set_of_users.append(i[0])
    freq = [0]*1000
    for one in network:
        if one[0] == user:
            for frnd in one[1]:
                for two in network:
                    if two[0] == frnd:
                        for mut in two[1]:
                            if mut == user:
                                continue
                            freq[mut]+=1
    mutual = 0
    for i in range(set_of_users[-1]+1):
        if freq[i]>mutual:
            mutual = i
            ans = freq[i]
    frnd_of_user = {}
    frnd_of_rec = {}
    for i in network:
        if i[0] == user:
            frnd_of_user = set(i[1])
        elif i[0] == mutual:
            frnd_of_rec = set(i[1])
    mutual_friends = frnd_of_user.intersection(frnd_of_rec)
    print("We recommend a friend for user with ID " + "(" + str(user) + ")" + ", the user:" + "(" + str(mutual) + ")" + ", it's mutual frined with" , mutual_friends)

facebook = create_network("FB.txt")
print(facebook)
recommendationForUser(facebook,1)
print(numFriends(1,facebook))
print(getCommon(1,3,facebook))
