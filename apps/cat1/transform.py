def transform(cad):
    columns = cad.catContext['cai'].columns
    add_row_vals = ' + '.join(columns)
    sql_a = f"""
        SELECT
            BOOLEAN(INT(({add_row_vals}) % 2)) AS row_sum_odd_ind,
            ({add_row_vals}) AS row_sum,
            *
        FROM parquet.`{cad.catContext['cai_data_uri']}`
        WHERE _c0 != 'A'
    """
    trans_1 = cad.spark.sql(sql_a)
    trans_1.createOrReplaceTempView("trans_1")
    trans_2_aggs = ', '.join(list(map(lambda c: f'SUM({c}) AS {c}_sum', ['row_sum'] + columns)))
    trans_2_sql = f"""
        SELECT
            {trans_2_aggs}
        FROM trans_1
        GROUP BY row_sum_odd_ind
    """
    cao = cad.spark.sql(trans_2_sql)
    return cao
