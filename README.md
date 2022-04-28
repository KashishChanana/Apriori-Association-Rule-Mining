# Apriori-Association-Rule-Mining
<b>1. Name & UNI: Ashwathy Mohan Menon(am5683), Kashish Chanana (kc3419) </b>

<b>2. List of files submitted </b>

<b>3. Steps to run the code </b>

<b>4. NYC Open Data Set Chosen </b>

  *  We chose the HIV/AIDS Diagnoses by Neighborhood, Sex, and Race/Ethnicity Dataset which initially had 2,928 rows and 10 columns.
  *  Link to the data set on website: https://data.cityofnewyork.us/Health/HIV-AIDS-Diagnoses-by-Neighborhood-Sex-and-Race-Et/ykvb-493p
  *  Data Cleaning Steps:
      *  We have programattically cleaned the data and all the steps for data cleaning are mentioned in the Data Cleaning.ipynb notebook
      *  There are certain rows for which most of the columns have null values. We decided to drop those rows to get better association rules.
      *  There are certain rows for which most of the columns have unknown values. We decided to drop those rows to get better association rules.
      *  There are certain rows for which most of the columns have * values. We decided to drop those rows to get better association rules.
      *  We dropped column Year as it would not have any significance in the rules generated.
      *  Some long column names have been renamed.
      *  Column values were replaced as Column_Name=Column_Value to better understand what rules are genrated.
      *  The code for all this is present in the Data Cleaning.ipynb notebook that we have submitted with this project.
  *  After all the preprocessing we have 2507 rows and 7 columns.
  *  The data set that we have chosen is compelling because it allows us to generate association rules that give insight into how ethinicity, sex, neighbourhood give insight into weather AIDS, HIV or both are low, high or medium. It also gives insigth into the association rules between HIV and AIDS itself allowing one to understand the important associations which would help to take necessary steps and prevent an outbreak in the real world.

<b> 5. Implementation of Apriori Algorithm </b>

  * findsubsets(): Finds subsets of length n
  * findpermutations(): Finds permutations of length n
  * get_L_1(): Generates the first L1 set of individual items. Returns L1 and L1_support. Only items that pass the minimum support threshold are appended to the list.
  * apriori_gen(): Takes in the previous list generated of size k i.e. Lk and generates subsets for L_k+1. The SQL part mentioned in the paper has been implemented in this function from scratch without using python libraries. Where we use set-intersect for join and items are ordered hence item1=item2...and item4<item5 part of the paper also holds.
  * prune(): After C_k+1 subsets are generated, the prune function removes the invalid ones. If subset of the set of C_K+1 is not in Lk remove the same (Same logic as per the paper).
  * get_L_k_plus_one: Repeat till len(L_K)!=0. 
      * The initial input to this function is L1 generated via get_L_1(). If L_1 is empty break the loop and return empty set for C_k_plus_one.
      * 
  



  
      
 
   
   
