import re

def transform_sql(SqlToGetValue,csvMap):
    keys = re.findall(r':\w+',SqlToGetValue)
    for item in keys:
        key = item[1:]
        valve = csvMap[key]
        valve_ = '\'' + valve + '\''
        SqlToGetValue = SqlToGetValue.replace(item,valve_)
    return SqlToGetValue



if __name__ == '__main__':
    SqlToGetValue1 = 'SELECT SUBSTR(:StreetCode,1,9) FROM DUAL'
    SqlToGetValue2 = 'SELECT TRANSFORMCODE(:CommCode,:ServiceSite) FROM DUAL'
    SqlToGetValue3 = 'SELECT t.CODE FROM FP_DIC_SEX@LINK_HDRDC t WHERE t.FP_CODE=:Sex '
    SqlToGetValue4 = 'SELECT t.CODE FROM FP_DIC_NATIONALITY@LINK_HDRDC t WHERE t.FP_CODE=:Nationality '
    SqlToGetValue5 = 'SELECT t.CODE FROM FP_DIC_POLITY@LINK_HDRDC t WHERE INSTR(t.FP_CODE,:Polity)>0'
    SqlToGetValue6 = 'SELECT t.CODE FROM FP_DIC_EDULEVEL@LINK_HDRDC t WHERE INSTR(t.FP_CODE,:EduLevel)>0'
    SqlToGetValue7 = 'SELECT t.CODE FROM FP_DIC_RPRTYPE@LINK_HDRDC t WHERE t.FP_CODE=:RprType '
    SqlToGetValue8 = 'SELECT t.CODE FROM FP_DIC_MARRSTATUS@LINK_HDRDC t WHERE t.FP_CODE=:MarrStatus '
    SqlToGetValue9 = 'SELECT t.CODE FROM FP_DIC_ISLIVINGCARD@LINK_HDRDC t WHERE t.FP_CODE=:IsLivingCard '
    SqlToGetValue10 = 'SELECT t.CODE FROM FP_DIC_MARRPROOF@LINK_HDRDC t WHERE t.FP_CODE=:MarrProof  '
    csvMap = {'StreetCode':'100230214','CommCode':'122212121','ServiceSite':'www.baidu.com','Sex':'男','Nationality':'中国',
              'Polity':'China','EduLevel':'大学','RprType':'无','MarrStatus':'未婚','IsLivingCard':'True','MarrProof':'无'}
    result_sql = transform_sql(SqlToGetValue10,csvMap)
    print(result_sql)