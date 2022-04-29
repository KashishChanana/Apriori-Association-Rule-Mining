from collections import defaultdict
from collections import Counter
import itertools
import sys

def findsubsets(s, n):
    """
    Generates subsets of size n from the given set s
    """
    return list(itertools.combinations(s, n))

def findpermutations(s):
    """
    Generates permutations of size n from the given set s
    """
    return list(itertools.permutations(s))

def get_L_1(transactions, min_sup):
    """
    Generates the L1 itemsets i.e, itemsets with one item
    """

    L_1_support = defaultdict(float)
    L_1 = []
    # counting the frequencies of each item in the the trasactions list
    for transaction in transactions:
        for item in transaction:
            L_1_support[tuple([item])]+=1

    total_transactions = len(transactions)

    # thresholding the items based on the min support
    for item in L_1_support.keys():
        L_1_support[item] = L_1_support[item]/total_transactions*1.0
        
        # appending to L1, the items that exceed the min support
        if L_1_support[item] >= min_sup:
            L_1.append(item)
    # returning the L1 set and L1 support dictionary that stores support for each item
    return L_1, L_1_support

def apriori_gen(L_k):
    """
    Implemented the SQL portion of algorithm from scratch
    """
    C_k_plus_one = set()
    # choose one set from Lk
    for p in L_k:
        # choose another set from Lk
        for q in L_k:  
            # taking join between the two sets
            p_intersect_q = set(p).intersection(set(q)) 
            # ensuring only one item is different ( this will be the last item given that our itemsets are ordered)
            if len(p_intersect_q)+1 == len(p): 
                if p[-1] < q[-1]:
                    # finding new set which is (p + new item) since all n-1 items are same in both the sets
                    p_union_q = tuple(sorted(list(set(set().union(p,q))))) 
                    C_k_plus_one.add(p_union_q)
    return C_k_plus_one
    

def prune(L_k, C_k_plus_one):
    """
    Pruning out invalid subsets generated.
    According to paper,  Rakesh Agrawal and Ramakrishnan Srikant: Fast Algorithms for Mining Association Rules in Large Databases, VLDB 1994
    Let L3 be ((1 2 31, (1 2 4}, (1 3 4}, (1 3 5}, (2 3 4)). 
    After the join step, C4 will be { { 1 2 3 4}, (13 4 5) }.
    The prune step will delete the itemset (1 3 4 5) because the itemset (1 4 5) is not in L3.
    We will then be left with only (1 2 3 4) in C4. 
    This is implemented below.
    """
    C_invalid = set()
    for c in C_k_plus_one:
        subsets = findsubsets(set(c), len(c)-1)
        for subset in subsets:
            if len(subset)>1:
                subset = tuple(sorted(subset))
            if subset not in L_k:
                C_invalid.add(c)
                break
    # removing invalid subsets form Ck+1
    C_k_plus_one = C_k_plus_one - C_invalid 
    return C_k_plus_one

def get_L_k_plus_one(transactions, L_k, support_dict, min_sup):
    """
    Generates Lk+1 itemsets till support threshold matches the frequent itemsets' support
    """
    total_L = L_k
    itr_count = 0

    while len(L_k)!=0:
        L_k_plus_one = []
        L_k_plus_one_support = defaultdict(float)
        # generate candidates from Lk
        C_k_plus_one = apriori_gen(L_k)
        # prune candidate set C_k_plus_one
        C_k_plus_one = prune(L_k, C_k_plus_one)

        # break if we get empty candidate set
        if C_k_plus_one == set():
            break
        
        # frequency counts of the candidates generated in Ck+1
        for transaction in transactions:
            for candidate_c in C_k_plus_one:
                if set(candidate_c) <= set(transaction):
                    L_k_plus_one_support[candidate_c]+=1
            
        total_transactions = len(transactions)
        # thresholding based on min support criterion
        for item in L_k_plus_one_support.keys():
            L_k_plus_one_support[item] = L_k_plus_one_support[item]/total_transactions*1.0
            # appending those frequent itemsets that meet the support threshold
            if L_k_plus_one_support[item] >= min_sup:
                L_k_plus_one.append(item)

        # keeping count of iteration
        itr_count+=1
        # turning Lk to Lk+1 to ensure continuity of the loop
        L_k = L_k_plus_one
        # keeping track of all frequent itemsets obtained till now
        total_L += L_k
        # updating support dictionary
        support_dict= Counter(support_dict) + Counter(L_k_plus_one_support)

    # return all frequent itemsets along with support dictionary
    return total_L, support_dict


def get_rules(total_L, support_dict, min_conf):
    """
    Generating association rules based on the desired confidence
    """
    final_associations = {}
    final_associations_support = {}
    for L in total_L:
        if len(L)>1:
            # this generates rules such as LHS has atleast one element and RHS has exactly one element
            rule_combinations = findsubsets(L,len(L)-1) 
            # if L = (a, b), rule_combinations will create possible LHS sets, i.e, both a & b
            for rule in rule_combinations:
                LHS = rule
                # while subtracting rule from L, we create exactly one element in RHS, which is not there in RHS
                RHS = tuple(set(L)-set(rule))[0]
                # finding confidence as a ratio of supports
                conf = support_dict[L]/support_dict[tuple(sorted(LHS))] 

                # thresholding by min confidence
                if(conf>=min_conf): 
                    final_associations[(LHS,RHS)]=conf
                    final_associations_support[(LHS,RHS)] = support_dict[L]

    # returning final rules and their corresponding support
    return final_associations, final_associations_support

    
     
def apriori_algorithm(transactions, min_sup, min_conf):

    # generating the frequent item sets containing one item i.e, the L1 itemset
    L_1, support_dict = get_L_1(transactions, min_sup)

    # continuing to generate itemsets from the previously obtained frequent itemsets
    total_L, support_dict = get_L_k_plus_one(transactions, L_1, support_dict, min_sup)

    total_itemsets = {}
    for L in total_L:
        total_itemsets[L] = support_dict[L]
    
    # sorting itemsets based on support value obtained (descending order)
    total_itemsets = dict(sorted(total_itemsets.items(), key=lambda item: item[1], reverse=True))
    
    # generating rules from L (i.e, the itemsets that meet the min support criterion)
    final_associations, final_associations_support = get_rules(total_L, support_dict, min_conf)
    
    # sorting rules based on confidence scores in descending order
    rules = dict(sorted(final_associations.items(), key=lambda item: item[1], reverse=True))

    # Writing out output into file 
    original_stdout = sys.stdout

    # open the output file in write mode
    with open('output.txt', 'w') as f:
        sys.stdout = f

        # printing frequent itemsets
        print("==Frequent itemsets (min_sup={}%)\n\n".format(min_sup*100))
        for frequent_itemset in total_itemsets.keys():
            print(list(frequent_itemset),",", round(total_itemsets[frequent_itemset]*100, 4), "%")

        # printinh high confidence association rules
        print("\n\n==High-confidence association rules (min_conf={}%)".format(min_conf*100))
        for rule in rules:
            print(list(rule[0]),"=>","[", rule[1], "] (Conf: ", round(rules[rule]*100, 4), "%, Supp:", round(final_associations_support[rule]*100, 4), "%)")
            

    sys.stdout = original_stdout
    f.close()
    
    