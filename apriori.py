from collections import defaultdict
from collections import Counter
import itertools

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

def findpermutations(s):
    return list(itertools.permutations(s))

def get_L_1(transactions, min_sup):

    L_1_support = defaultdict(float)
    L_1 = []
    for transaction in transactions:
        for item in transaction:
            L_1_support[item]+=1

    total_transactions = len(transactions)

    for item in L_1_support.keys():
        L_1_support[item] = L_1_support[item]/total_transactions*1.0
        
        if L_1_support[item] >= min_sup:
            L_1.append(tuple([item]))
    
    # print("*************************L1******************\n")
    
    print(L_1, L_1_support)
    
    return L_1, L_1_support

def apriori_gen(L_k):
    C_k_plus_one = set()
    for p in L_k:
        for q in L_k:
            p_intersect_q = set(p).intersection(set(q))
            if len(p_intersect_q)+1 == len(p):
                if p[-1] < q[-1]:
                    p_union_q = tuple(sorted(list(set(set().union(p,q)))))
                    C_k_plus_one.add(p_union_q)
    return C_k_plus_one
    

def prune(L_k, C_k_plus_one):
    print("L_K",L_k)
    C_invalid = set()
    for c in C_k_plus_one:
        subsets = findsubsets(set(c), len(c)-1)
        # print("c",c)
        # print("subsets",subsets)
        for subset in subsets:
            if subset not in L_k:
                #C_k_plus_one.remove(c)
                print("remove",c, "for subset", subset)
                C_invalid.add(c)
                break
    C_k_plus_one = C_k_plus_one - C_invalid
    return C_k_plus_one

def get_L_k_plus_one(transactions, L_k, support_dict, min_sup):

    total_L = L_k
    
    L_k_plus_one_support = defaultdict(float)
    L_k_plus_one = []
    i=0
    while len(L_k)!=0:
        C_k_plus_one = apriori_gen(L_k)
        print("C_K_plus_one",C_k_plus_one)
        C_k_plus_one = prune(L_k, C_k_plus_one)

        print("C_K_plus_one", C_k_plus_one)
        if C_k_plus_one == set():
            break
        for transaction in transactions:
            for candidate_c in C_k_plus_one:
                # print("look here c",set(candidate_c))
                # print("look here t",set(transaction))
                if set(candidate_c) <= set(transaction):
                    # print(True)
                    L_k_plus_one_support[candidate_c]+=1
                # else: print(False)
        # print(L_k_plus_one_support)
        total_transactions = len(transactions)
        for item in L_k_plus_one_support.keys():
            L_k_plus_one_support[item] = L_k_plus_one_support[item]/total_transactions*1.0
            print(item, L_k_plus_one_support[item])
            if L_k_plus_one_support[item] >= min_sup:
                L_k_plus_one.append(item)
        
        L_k = L_k_plus_one
        total_L += L_k

    support_dict= Counter(support_dict) + Counter(L_k_plus_one_support)
    print(support_dict, total_L)
    return total_L, support_dict


def get_rules(total_L, support_dict, min_conf):
    final_associations = {}
    for L in total_L:
        for rules in L:
            rule_combinations = findsubsets(rules,len(rules)-1)
            for rule in rule_combinations:
                LHS = rule
                RHS = tuple(set(rules)-set(rule))[0]
                conf = support_dict[rules]/support_dict[tuple(sorted(LHS))]
                print(conf)
                if(conf>=min_conf):
                    final_associations[(LHS,RHS)]=conf
    return final_associations

     
def apriori_algorithm(transactions, min_sup, min_conf):

    L_1, support_dict = get_L_1(transactions, min_sup)
    total_L, support_dict = get_L_k_plus_one(transactions, L_1, support_dict, min_sup)
    print(total_L)
    rules = get_rules(total_L, support_dict, min_conf)
    print(rules)
    

