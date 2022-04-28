# Apriori-Association-Rule-Mining
<b>1. Name & UNI: Ashwathy Mohan Menon(am5683), Kashish Chanana (kc3419) </b>

<b>2. List of files submitted </b>

The following files have been submitted -
1. Data Cleaning HW3.ipynb - This file contains the steps we undertook to clean the data.
2. INTEGRATED_DATASET.csv - Contains the cleaned data obtained after undertaking the data cleaning steps.
3. apriori.py - python file that implements the Apriori Association Rule Mining Algorithm
4. main.py - python file responsible for running the program
5. output.txt - example run output obtained as a result of running the apriori algorithm

<b>3. Steps to run the code </b>

Use the following command to run the code -
`python3 main.py INTEGRATED_DATASET.csv <minimum support> <minimum confidence>`

Example - `python3 main.py INTEGRATED_DATASET.csv 0.01 0.7`

<b>4. NYC Open Data Set Chosen </b>

  *  We chose the HIV/AIDS Diagnoses by Neighborhood, Sex, and Race/Ethnicity Dataset which initially had 2,928 rows and 10 columns.
  *  Link to the data set on website: https://data.cityofnewyork.us/Health/HIV-AIDS-Diagnoses-by-Neighborhood-Sex-and-Race-Et/ykvb-493p
  *  Data Cleaning Steps:
      *  We have programattically cleaned the data and all the steps for data cleaning are mentioned in the Data Cleaning HW3.ipynb notebook.
      
      *  There are certain rows for which most of the columns have null values. We decided to drop those rows to get better association rules. We used the  `data_cleaned  = data[~data.isna().any(axis=1)]` for this purpose.
      
      *  There are certain rows for which most of the columns have unknown values. We decided to drop those rows to get better association rules. We used ` data_cleaned = data_cleaned[~data_cleaned.isin(['*']).any(axis=1)]`
      
      *  There are certain rows for which most of the columns have * values. We decided to drop those rows to get better association rules. We used `data_cleaned = data_cleaned[~data_cleaned.isin(['Unknown']).any(axis=1)]`
      
      *  We dropped column 'Year' as it would not have any significance in the rules generated. The years ranged over a very short tenure, approx. 3 years. This was a very short tenure to be resulting in any vital information. We also removed the columns 'TOTAL NUMBER OF CONCURRENT HIV/AIDS DIAGNOSES	PROPORTION OF CONCURRENT',  'HIV/AIDS DIAGNOSES AMONG ALL HIV DIAGNOSES', these columns were removed  as they presented redundant information. We used the `data_cleaned = data_cleaned.drop(columns=['YEAR', 'TOTAL NUMBER OF CONCURRENT HIV/AIDS DIAGNOSES	PROPORTION OF CONCURRENT', 'HIV/AIDS DIAGNOSES AMONG ALL HIV DIAGNOSES'])`
      
      *  Long column names have been renamed for columns 'HIV DIAGNOSES PER 100,000 POPULATION' to  'HIV PER 100K' and ''AIDS DIAGNOSES PER 100,000 POPULATION': 'AIDS PER 100K'.  This was done using - `data_cleaned = data_cleaned.rename(columns={"HIV DIAGNOSES PER 100,000 POPULATION": "HIV PER 100K", "AIDS DIAGNOSES PER 100,000 POPULATION": "AIDS PER 100K"`
      
      *  For columns with numerical attributes- these columns include (	'TOTAL NUMBER OF HIV DIAGNOSES', 'HIV PER 100K', 'TOTAL NUMBER OF AIDS DIAGNOSES', 'AIDS PER 100K') - we used qcut function of pandas to bin these into Low, Medium, High categories and convert the numerical attributes to categorical attributes for better understanding and rule mining. Qcut provides for Quantile-based discretization function. This enables us to discretize variable into equal-sized buckets based on rank or based on sample quantiles. For example 1000 values for 10 quantiles would produce a Categorical object indicating quantile membership for each data point.
      `to_bin_columns= ['TOTAL NUMBER OF HIV DIAGNOSES', 'HIV PER 100K', 'TOTAL NUMBER OF AIDS DIAGNOSES', 'AIDS PER 100K']`
      
       `for to_bin in to_bin_columns:`
       
       `data_cleaned['to_bin']=pd.qcut(np.array(data_cleaned['to_bin']).astype('float32'), 4,  duplicates='drop',labels=["Low", "Medium", "High"])`
      
      *  Column values were replaced as Column_Name=Column_Value to better understand what rules are generated. For example: Column Sex with Values Male/ Female has now rows as Sex = Male or Sex = Female. This was done using 
      
      `for column in data_cleaned.columns: data_cleaned[column] = data_cleaned[column].apply(lambda x: column+"="+ str(x))`
      
      *  The code for all this is present in the Data Cleaning HW3.ipynb notebook that we have submitted with this project.
      
  *  After all the data preprocessing & cleaning we have 2507 rows and 7 columns.
  
  *  <b> Reason for choosing this dataset </b> - The data set that we have chosen is compelling because it allows us to generate association rules that give insight into how ethinicity, sex, neighbourhood give insight into weather AIDS, HIV or both are low, high or medium. It also gives insigth into the association rules between HIV and AIDS itself allowing one to understand the important associations which would help to take necessary steps and prevent an outbreak in the real world. Through this dataset, we also highlight the difference between HIV and AIDS, a notion that is commonly missed. HIV, for one, is a virus, a small infectious agent that multiplies itself by taking control of cells inside a host. AIDS, on the other hand, is a syndrome, a group of connected symptoms that are usually caused by a single disease or virus. Through this dataset, we are able to show the correlation (if any) that might exist between the two, HIV and AIDS. Upon understanding this, we're also able to understand the spread in terms of demographics (as described as neighborhood in the dataset), sex, race and/or ethinicity. Understanding the relation between hiv/aids on the grounds mentioned before, can help understand which communities are affected the most and where we can concentrate most of the efforts in order to assist the affected and also send out information to the general public abouts its rampant existance in their community.

<b> 5. Implementation of Apriori Algorithm </b>

 a. In main.py
  * Function Read to CSV file and store transactions in transactions list.
  * Parse DataFile name, minimum support and minimum confidence from command line
  * Call function read and store transactions in a list.
  * Call apriori_algorithm from apriori.py

 b. In apriori.py
  
  * findsubsets(): Finds subsets of length n
  * findpermutations(): Finds permutations of length n
  * get_L_1(): Generates the first L1 set of individual items. Returns L1 and L1_support. Only items that pass the minimum support threshold are appended to the list.
  * apriori_gen(): Takes in the previous list generated of size k i.e. Lk and generates subsets for L_k+1. The SQL part mentioned in the paper has been implemented in this function from scratch without using python libraries. Where we use set-intersect for join and items are ordered hence item1=item2...and item4<item5 part of the paper also holds.
  * prune(): After C_k+1 subsets are generated, the prune function removes the invalid ones. If subset of the set of C_K+1 is not in Lk remove the same (Same logic as per the paper).
  * get_L_k_plus_one(): Repeat till len(L_K)!=0. 
      * The initial input to this function is L1 generated via get_L_1(). If L_1 is empty break the loop and return empty set for C_k_plus_one.
      * Else for all transactions for all candidate sets in C_k_plus_one if candidate set is subset of transaction increase count of candidate by 1.
      * For all candidates calculate support by diving the total_count of that candidate occurence by total number of transactions.
      * Append to L_K_plus_one all candidates that pass the minimum support threshold.
      * Update LK to L_k+1
      * Append LK to total_L and L_K_plus_one_support to support_dict
  * get_rules(): For sets in total_L with length>1 i.e. atleast 2 items in the set, generate rule combinations, example A->B or B->A and calculate confidence for the rule. If confidence is greater than minimum confidence threshold add it to the final_association rule dictionary and add support of the rule to the final_association_support dictionary.
  * apriori_algorithm(): Calls all the above functions in required order.
    * Calls get_L_1()
    * Calls get_L_k_plus_one()
    * Sorts total item sets in decreasing order of support
    * Calls get_rules()
    * Sorts rules in decreasing order of confidence.
    * Prints support and association rules in required format by writing the output to file.

 <b> 6. Results derived on `python3 main.py INTEGRATED_DATASET.csv 0.01 0.7`</b>
  
  * After empirically trying various combinations of support and confidence we decided to go with values 0.01 for support and 0.7 for confidence as they give a reasonable number of association rules that are relevant and interesting. 0.01 support makes sense as discussed in class - high levels of support doesn't garner enough frequent itemsets that might give good quality association rules, therefore realistically speaking using low support allows us to capture more information. Confidence value of 0.7 was also empirically selected by studying the nature & varity of the rules generated.
 
  * We were able to generate some interesting associations that gave us insight into the associations between different items in the market basket.
  * For example, some sample rules generated and their implications:
 1. ['RACE/ETHNICITY=Native American'] => [ TOTAL NUMBER OF AIDS DIAGNOSES=Low ], (Conf:  100.0 %, Supp: 12.8041 %) - This indicates an interesting association between race and total number of aids diagnoses.  Such a rule helps studying the demographics of AIDS based on Race. People of Native American race have low total number of HIV diagnosis.
2. ['RACE/ETHNICITY=Multiracial'] => [ AIDS PER 100K=Low ] (Conf:  96.1194 %, Supp: 12.844 %) - This rule also sheds light on race and AIDS diagnosis. As we can see people of multiracial race tend to have lower AIDS diagnosis per 100K population. 
 
3. ['RACE/ETHNICITY=Black', 'SEX=Male'] => [ HIV PER 100K=High ] (Conf:  88.6905 %, Supp: 5.9434 %) - In continuation of the previous rule, if we have a population of Black Males, it's likely that HIV cases PER 100K population is High. This again sheds light on how the disease is spread across different communities based on Race and Gender. Such a rule can be helpful in analyzing patterns and taking preventative measures in the communities that are high risk.
 
 4. ['Neighborhood (U.H.F)=South Beach - Tottenville', 'SEX=Female'] => [ HIV PER 100K=Low ] (Conf:  92.8571 %, Supp: 1.0371 %) - This rule is also interesting as it talks about the Neighborhood, the geographic location of where people are loacted. As per this rule, for female folks located in the South Beach - Tottenville location, it is likely that the HIV diagnosis per 100K population is low, marking this region safer in terms of HIV diagosis for females.
 
 5. ['HIV PER 100K=Medium', 'RACE/ETHNICITY=White'] => [ SEX=Male ] (Conf:  86.4865 %, Supp: 2.5529 %) - A rule like this, helps analyze the flip rules slighly better, i.e, In case we have Medium levels of HIV per 100K population diagnosis and the race is Whilte, its likely the sex affected is Male. 
 
There were several other interesting associations that were obtained as a result of running the apriori algorithm. In totality, we have generated approximately 124 rules and discovered many such associations. These rules are useful in the sense that one can plan many preventive and curative measures according to the associations. This also shows how infection rates differ with race, neighborhood and sex demographics.
 
 
 
  



  
      
 
   
   
