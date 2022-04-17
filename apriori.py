from collections import defaultdict

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
            L_1.append(item)
    
    return L_1, L_1_support

def apriori_gen(L_k):
    pass

def prune(L_k, C_k_plus_one):
    pass

def get_L_k_plus_one(transactions, L_k, support_dict, min_sup, min_conf):

    total_L = L_k
    
    L_k_plus_one_support = defaultdict(float)
    L_k_plus_one = []

    while len(L_k)!=0:
        C_k_plus_one = apriori_gen(L_k)
        C_k_plus_one = prune(L_k, C_k_plus_one)
        for transaction in transactions:
            for candidate_c in C_k_plus_one:
                if candidate_c < transaction:
                    L_k_plus_one_support[candidate_c]+=1

        total_transactions = len(transactions)
        for item in L_k_plus_one_support.keys():
            L_k_plus_one_support[item] = L_k_plus_one_support[item]/total_transactions*1.0
            
            if L_k_plus_one_support[item] >= min_sup:
                L_k_plus_one.append(item)
        
        L_k = L_k_plus_one
        total_L += L_k

    support_dict|=L_k_plus_one_support
    return total_L, support_dict


def get_rules(L_k, min_sup, min_conf):
    pass

def apriori_algorithm(transactions, min_sup, min_conf):

    L_1, support_dict = get_L_1(transactions, min_sup)
    total_L, support_dict = get_L_k_plus_one(transactions, L_1, support_dict, min_sup)
    rules = get_rules(total_L, support_dict, min_conf)
    print(rules)
    

