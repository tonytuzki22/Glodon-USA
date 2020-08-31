import pymysql
import pandas as pd
import codecs


def read_excel_file_to_dict(input_file,sheet=None,key_index_field=0):
    return_dataset=dict()
    if sheet!=None:
        solution_code_keywords_df = pd.read_excel(input_file, dtype=str,sheet_name = sheet)
    else:
        solution_code_keywords_df = pd.read_excel(input_file, dtype=str)
    column_names = list(solution_code_keywords_df.columns.values)
    for i in range(len(solution_code_keywords_df)):
        key_list = []
        row_dataset = []
        for j in range(len(column_names)):
            value = solution_code_keywords_df.loc[i, column_names[j]] if not pd.isnull(
                solution_code_keywords_df.loc[i, column_names[j]]) else ''

            if j<=key_index_field:
                key_list.append(value.strip())


            else:
                row_dataset.append(value)
        key=''
        if len(key_list)==1:
            key = key_list[0]
        else:
            key = tuple(key_list)
        if key not in return_dataset:
            return_dataset[key] = []
        if key:
            return_dataset[key].append(row_dataset)
    return return_dataset



def write_resultset_to_excel_file(resultset,file_name,columns_name):

    result_df = pd.DataFrame.from_records(resultset, columns=columns_name)
    writer = pd.ExcelWriter(file_name)
    result_df.to_excel(writer, 'sheet1', index=False, columns=columns_name)
    writer.save()

def read_excel_file_to_list(input_file,sheet=None):
    return_dataset=[]
    if sheet!=None:
        solution_code_keywords_df = pd.read_excel(input_file, dtype=str,sheet_name = sheet)
    else:
        solution_code_keywords_df = pd.read_excel(input_file, dtype=str)
    column_names = list(solution_code_keywords_df.columns.values)
    for i in range(len(solution_code_keywords_df)):
        row_dataset = []
        for j in range(len(column_names)):
            value = solution_code_keywords_df.loc[i, column_names[j]] if not pd.isnull(
                solution_code_keywords_df.loc[i, column_names[j]]) else ''
            row_dataset.append(value)
        return_dataset.append(row_dataset)
    return return_dataset





def read_text_file_to_dataset(input_file,sep='|',header=None,key_index_field=0):
    return_dataset=[]
    with codecs.open(input_file, mode="r", encoding="utf-8") as lines:
        if header!=None:
            column_names = lines.readline().replace('\r\n','').replace('\n','').replace('\r','').split(sep)
        for line in lines:
            fields = line.replace('\r\n','').replace('\n','').replace('\r','').split(sep)
            return_dataset.append(fields)
    return return_dataset


# In[11]:


def mySQLconnect(hostname_in,username_in,password_in,dbname):

    hostname = hostname_in
    username = username_in
    portnum = '3306'
    password = password_in
    #password = 'Em19940201!'
    charset = 'utf8'
    autocommit_in = True
    return pymysql.connect(host=hostname, port=int(portnum), user=username, passwd=password, db=dbname, charset=charset,
                           autocommit=autocommit_in)


def runMysqlQuery(conn, query_str):
    cursor = conn.cursor()
    cursor._defer_warnings = True
    try:
        cursor.execute(query_str)

    except Exception as e:
        print("query_str {}  Error {}".format(query_str, e.args))
        cursor.close()
        return []
    result = cursor.fetchall()
    cursor.close()
    return result


# In[12]:


def get_DB_testcases(type,chapter_code):
    # CORRECTED_VALUETYPE_NAME = '{}' and 
    query_cmd = "select distinct DBID,ITEMCODE, RESULT_ID,RESULT_DETAIL_ID,SPECID,SPEC_NAME,SPEC, CORRECTED_STANDARD_CATEGORY_NAME, "                 "CORRECTED_VALUETYPE_NAME, ACTUAL_VALUE, CORRECTED_VALUE, EXPECT_VALUE, STATUS from HQ_product_20200518.view_UI校验_errors "                 "where  清单类别 ='{}' and left(ITEMCODE,4) = '{}'order by ITEMCODE,SPECID,RESULT_ID,RESULT_DETAIL_ID;"
    dbid_query_cmd = "select DBID,region_name from COST_AI_DBID_SERIES_LOOKUP;"
    count=0
    count=0
    item_code_count=0
    dbid_name_dict=dict()
    mysql_host_domain, username, password, cost_estimation_dbname = 'localhost', 'root', 'qwer1234!', 'TESTCASES'
    mysql_conn = mySQLconnect(mysql_host_domain, username, password, cost_estimation_dbname)
    dataset=runMysqlQuery(mysql_conn, query_cmd.format(type,chapter_code))
    dbid_dataset=runMysqlQuery(mysql_conn, dbid_query_cmd)
    for i in range(len(dbid_dataset)):
        dbid, region_name = dbid_dataset[i]
        if dbid not in dbid_name_dict:
             dbid_name_dict[dbid]=region_name

    