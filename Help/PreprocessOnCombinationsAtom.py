import copy
def PreProcessOnCombinaions(Combined):
    for AtomIndex in range(len(Combined)):
        for combinationRelativeIndex in range(len(Combined[AtomIndex])):
            # print(Combined[AtomIndex])
            if AtomIndex>Combined[AtomIndex][combinationRelativeIndex]:
                Combined[Combined[AtomIndex][combinationRelativeIndex]].append(AtomIndex)
            
    NextClue=[]
    for AtomIndex in range(len(Combined)):
        NextClue.append(len(Combined[AtomIndex]))
    return Combined, NextClue 