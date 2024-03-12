from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    'postgresql+psycopg2://root:root@localhost/test_db')

sql = '''
select * from vw_artist
'''

sql = '''
select distinct * from "BILLBOARD" as b
where b.rank = 1
order by b."weeks-on-board" desc
limit 10
'''

df = pd.read_sql_query(sql, engine)

print(df)
