def sortByBurst(val): 
    return val[1] 

def sortByArrival(val): 
    return val[2]  



def processes_init (nOfP):
    p = []

    for x in range(nOfP):
        procPart = []
        procPart.append(x+1)
        procPart.append( int(input("Enter process ("+ str(x+1) +") burst time : \n")) )
        procPart.append( int(input("Enter process ("+ str(x+1) +") arrival time : \n")) )
        procPart.append(-1)     # completion time for process (x+1)
        procPart.append(-1)     # wait time for process (x+1)
        procPart.append(-1)     # TAT time for process (x+1)

        p.append(procPart)
    return p 

def arrival_queue_init(nOfP, p):
    arrivalQueue = []

    # push processes to the Arrival Queue
    for x in range(nOfP):
        qPart = []
        qPart.append( p[x][0] )     # process no
        qPart.append( p[x][1] )     # burst time
        qPart.append( p[x][2] )     # arrival time

        arrivalQueue.append(qPart)

    arrivalQueue.sort(key = sortByArrival)  
    return arrivalQueue


def sch_alg(alg, quantum, nOfP, arrivalQueue, p):
    if alg == 'FCFS' :
        FCFS_alg(nOfP, arrivalQueue, p)
    elif alg == 'SJF' :
        SJF_alg(nOfP, arrivalQueue, p)
    elif alg ==  'SRTF' :
        SRTF_alg(nOfP, arrivalQueue, p)
    elif alg == 'RR' :
        RR_alg(quantum, nOfP, arrivalQueue, p)
    else :
        return
        # wrong alg value !!


def FCFS_alg(nOfP, arrivalQueue, p):
    readyQueue = []
    nOfPLeft = nOfP

    cpu = 0
    # push processes to the ready queue
    while nOfPLeft > 0 :
        # push processes to the Ready Queue
        while len(arrivalQueue) > 0 :
            if arrivalQueue[0][2] <= cpu :
                newProcess = arrivalQueue.pop(0)
                readyQueue.append( newProcess )
            else:
                break

        if len(readyQueue) == 0 :
            cpu += 1 
            continue

        readyQueue.sort(key = sortByArrival)      # may cause an error if the list is empty, I DON'T KNOW !!

        qPart = readyQueue.pop(0)
        cpu += qPart[1]
        p[ qPart[0]-1 ][3] = cpu
        nOfPLeft -= 1



def SJF_alg(nOfP, arrivalQueue, p):
    readyQueue = []
    nOfPLeft = nOfP

    cpu = 0
    # add process to the CPU
    while nOfPLeft > 0 :
        # push processes to the Ready Queue
        while len(arrivalQueue) != 0 :
            if arrivalQueue[0][2] <= cpu :
                qPart = arrivalQueue.pop(0)
                readyQueue.append( qPart )
            else:
                break
        if len(readyQueue) == 0 :
            cpu += 1 
            continue

        readyQueue.sort(key = sortByBurst)  

        qPart = readyQueue.pop(0)
        cpu += qPart[1]
        p[ qPart[0]-1 ][3] = cpu
        nOfPLeft -= 1



def SRTF_alg(nOfP, arrivalQueue, p):
    readyQueue = []
    nOfPLeft = nOfP

    cpu = 0
    currentProcess = []
    # add process to the CPU
    while nOfPLeft > 0 :
        # push processes to the Ready Queue
        while len(arrivalQueue) > 0 :
            if arrivalQueue[0][2] <= cpu :
                newProcess = arrivalQueue.pop(0)
                readyQueue.append( newProcess )

                if len(currentProcess) != 0 :
                    if newProcess[1] < currentProcess[1] :
                        currentProcess[2] = cpu
                        temp = readyQueue.pop()
                        readyQueue.append( currentProcess )
                        currentProcess = temp
            else:
                break

        if len(readyQueue) == 0 and len(currentProcess) == 0 :
            cpu += 1 
            continue

        readyQueue.sort(key = sortByBurst)      # may cause an error if the list is empty, I DON'T KNOW !!

        if len(currentProcess) == 0 :
            currentProcess = readyQueue.pop(0)

        cpu += 1
        currentProcess[1] -= 1

        # print("\n cpu : " + str(cpu))
        # print("\n P No : " + str(currentProcess[0]))

        if currentProcess[1] == 0 :
            p[ currentProcess[0]-1 ][3] = cpu
            currentProcess = []
            nOfPLeft -= 1



def RR_alg(quantum, nOfP, arrivalQueue, p):
    readyQueue = []
    nOfPLeft = nOfP

    cpu = 0
    currentProcess = []
    # add process to the CPU
    while nOfPLeft > 0 :
        # push processes to the Ready Queue
        while len(arrivalQueue) > 0 :
            if arrivalQueue[0][2] <= cpu :
                newProcess = arrivalQueue.pop(0)
                readyQueue.append( newProcess )
            else:
                break
        if len(currentProcess) != 0 :
            currentProcess[2] = cpu
            readyQueue.append( currentProcess )
            currentProcess = []

        if len(readyQueue) == 0 and len(currentProcess) == 0 :
            cpu += 1 
            continue

        readyQueue.sort(key = sortByArrival)      # may cause an error if the list is empty, I DON'T KNOW !!

        if len(currentProcess) == 0 :
            currentProcess = readyQueue.pop(0)

        if currentProcess[1] < quantum :
            cpu += currentProcess[1]
            currentProcess[1] = 0
        else:
            cpu += quantum
            currentProcess[1] -= quantum

        # print("\n cpu : " + str(cpu))
        # print("\n P No : " + str(currentProcess[0]))

        if currentProcess[1] == 0 :
            p[ currentProcess[0]-1 ][3] = cpu
            currentProcess = []
            nOfPLeft -= 1
    

def Average_WT(p, nOfP):
    sum = 0 
    for x in range(nOfP):
        p[x][4] = p[x][3] - p[x][2] - p[x][1]       # WT = comp - arriv - burst
        sum += p[x][4]

    AWT = sum / nOfP
    return AWT 

def Average_TWT(p, nOfP):
    sum = 0 
    for x in range(nOfP):
        p[x][5] = p[x][3] - p[x][2]       # TAT = comp - arriv
        sum += p[x][5]
    ATAT = sum / nOfP
    return ATAT 



def print_result(p, AWT, ATAT, nOfP):
    print("\n\n")
    for x in range(nOfP):
        print("P No : " + str(p[x][0]) + " ,  P burst : " + str(p[x][1]) + "  , P arrival : " + str(p[x][2]) + "  , P completion time : " + str(p[x][3]))
        print("\n")

    print("\nWaiting Time : ")
    for x in range(nOfP):
        print("P("+ str(p[x][0]) +") WT =  " + str(p[x][4]))

    print("\n Average WT =  " + str(AWT) )

    print("\nTurn Around Time : ")
    for x in range(nOfP):
        print("P("+ str(p[x][0]) +")  TAT =  " + str(p[x][5]))

    print("\n Average TAT =  " + str(ATAT) )
 




# nOfP = int(input("Enter No of processes : \n"))
# p = processes_init (nOfP)
# arrivalQueue = arrival_queue_init(nOfP, p)

# alg = input("choose an Alg. : ")

# quantum = -1 
# if( alg == 'RR' ):
#     quantum = int(input("Enter quantum time : "))

# sch_alg(alg, quantum, nOfP, arrivalQueue, p)
# AWT = Average_WT(p, nOfP)
# ATAT = Average_TWT(p, nOfP)

# print_result(p, AWT, ATAT)
