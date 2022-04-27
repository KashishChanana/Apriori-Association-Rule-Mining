from collections import defaultdict
from collections import Counter
import itertools
import sys

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

def findpermutations(s):
    return list(itertools.permutations(s))

def get_L_1(transactions, min_sup):

    L_1_support = defaultdict(float)
    L_1 = []
    for transaction in transactions:
        for item in transaction:
            L_1_support[tuple([item])]+=1

    total_transactions = len(transactions)

    for item in L_1_support.keys():
        L_1_support[item] = L_1_support[item]/total_transactions*1.0
        
        if L_1_support[item] >= min_sup:
            L_1.append(item)
    
    # print("*************************L1******************\n")
    
    #print(L_1, L_1_support)
    
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
    #print("L_K",L_k)
    C_invalid = set()
    for c in C_k_plus_one:
        subsets = findsubsets(set(c), len(c)-1)
        # print("c",c)
        # print("subsets",subsets)
        for subset in subsets:
            if subset not in L_k:
                #C_k_plus_one.remove(c)
                #print("remove",c, "for subset", subset)
                C_invalid.add(c)
                break
    C_k_plus_one = C_k_plus_one - C_invalid
    return C_k_plus_one

def get_L_k_plus_one(transactions, L_k, support_dict, min_sup):

    total_L = L_k
    
    L_k_plus_one_support = defaultdict(float)
    L_k_plus_one = []
    i=0
    itr_count = 0
    while len(L_k)!=0:
        L_k_plus_one = []
        L_k_plus_one_support = defaultdict(float)
        C_k_plus_one = apriori_gen(L_k)
        #print("C_K_plus_one",C_k_plus_one)
        #C_k_plus_one = prune(L_k, C_k_plus_one)

        #print("C_K_plus_one", C_k_plus_one)
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
            #print(item, L_k_plus_one_support[item])
            if L_k_plus_one_support[item] >= min_sup:
                L_k_plus_one.append(item)
        itr_count+=1
        
        
        L_k = L_k_plus_one
        total_L += L_k
        support_dict= Counter(support_dict) + Counter(L_k_plus_one_support)

    #support_dict= Counter(support_dict) + Counter(L_k_plus_one_support)
    #print(support_dict, total_L)
    return total_L, support_dict


def get_rules(total_L, support_dict, min_conf):
    final_associations = {}
    final_associations_support = {}
    for L in total_L:
        if len(L)>1:
            rule_combinations = findsubsets(L,len(L)-1)
            for rule in rule_combinations:
                LHS = rule
                RHS = tuple(set(L)-set(rule))[0]
                conf = support_dict[L]/support_dict[tuple(sorted(LHS))]

                if(conf>=min_conf):
                    final_associations[(LHS,RHS)]=conf
                    final_associations_support[(LHS,RHS)] = support_dict[L]
                    # rule b->a final_association[(b,a)]=10, final_asso_supp[(a,b)]=90

    return final_associations, final_associations_support

    

     
def apriori_algorithm(transactions, min_sup, min_conf):

    L_1, support_dict = get_L_1(transactions, min_sup)
    total_L, support_dict = get_L_k_plus_one(transactions, L_1, support_dict, min_sup)

    total_itemsets = {}
    for L in total_L:
        total_itemsets[L] = support_dict[L]
    
    total_itemsets = dict(sorted(total_itemsets.items(), key=lambda item: item[1], reverse=True))
    
    final_associations, final_associations_support = get_rules(total_L, support_dict, min_conf)
    
    rules = dict(sorted(final_associations.items(), key=lambda item: item[1], reverse=True))

    original_stdout = sys.stdout

    with open('output.txt', 'w') as f:
        sys.stdout = f
        print("\n\n\n*******************Frequent Itemsets along with Support in Decreasing Order***********\n\n")
        for frequent_itemset in total_itemsets.keys():
            print(list(frequent_itemset),",", round(total_itemsets[frequent_itemset]*100, 4), "%")

    
        print("\n\n\n*******************Association Rules with Confidence in Decreasing Order***********\n\n")
        for rule in rules:
            print(list(rule[0]),"=>","[", rule[1], "], (Conf: ", round(rules[rule]*100, 4), "%, Supp:", round(final_associations_support[rule]*100, 4), "%)")
            

    sys.stdout = original_stdout
    f.close()
    
    





