import pymysql


def mySQLconnect(hostname_in, username_in, password_in, dbname):

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


def get_DB_testcases(type, chapter_code):
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


def delete_phrase(mysql_conn, label_name):
    delete_vocab_cmd = "delete from COST_AI_LABEL_PHRASE_SYNPHRASE where label_id = (select id from COST_AI_LABEL where name = '{}');"
    runMysqlQuery(mysql_conn, delete_vocab_cmd.format(label_name))


def main():
    delete_phrase()

if __name__ == "__main__":
    main()
