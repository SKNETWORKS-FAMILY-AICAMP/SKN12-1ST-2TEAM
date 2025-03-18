from mysql import connector
import pandas as pd

conn = None
cursor = None

class Insert_Data:   
    def create_schemas(self):
        try:
            conn = connector.connect(host=self.host, user=self.user, password=self.password, port=self.port) 
            cursor = conn.cursor() # 실제 db에 명령을 전달(sql)
        
            # create schemas
            insert_query = """
            create database if not exists car_recall_db
            """
            cursor.execute(insert_query)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
    
    def create_table(self):
        try:
            conn = connector.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
            cursor = conn.cursor() # 실제 db에 명령을 전달(sql)
            
            # create table car_recall_month
            insert_query = """
            create table if not exists car_recall_db.car_recall_month(
            month_id int auto_increment primary key,
            recall_year VARCHAR(10) not NULL,
            recall_month VARCHAR(10) not NULL,
            kr_recall_car int,
            kr_recall_num int,
            us_recall_car int,
            us_recall_num int,
            total_recall_car int,
            total_recall_num int
            )
            """
            cursor.execute(insert_query)
            conn.commit()
            
            # create table car_recall_brand
            insert_query = """
            create table car_recall_db.car_recall_brand(
            brand_id int auto_increment primary key,
            recall_year VARCHAR(10) not NULL,
            recall_month VARCHAR(10) not NULL,
            car_model varchar(100) not NULL,
            car_num int
            )
            """
            cursor.execute(insert_query)
            conn.commit()
        
            # create table hyundai_faq
            insert_query = """
            create table car_recall_db.hyundai_faq(
            hyundai_id int auto_increment primary key,
            hyundai_question text,
            hyundai_answer text
            )
            """
            cursor.execute(insert_query)
            conn.commit()
        
            # create table kia_faq
            insert_query = """
            create table car_recall_db.kia_faq(
                kia_id int auto_increment primary key,
                kia_question text,
                kia_answer text
            )
            """
            cursor.execute(insert_query)
            conn.commit()

            # create table recall_top10
            insert_query = """
            create table car_recall_db.recall_top10(
                top10_id int auto_increment primary key,
                top10_car_model varchar(20),
                top10_car_num int
            )
            """
            cursor.execute(insert_query)
            conn.commit()
            
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)

    def read_data(self):
        year_data = pd.read_csv(f'data/{self.file_name_dic.get('year_data_name')}')
        manufacturer_data = pd.read_csv(f'data/{self.file_name_dic.get('manufacturer_data_name')}')
        hyundai_faq_data = pd.read_csv(f'data/{self.file_name_dic.get('hyundai_faq_data_name')}')
        kia_faq_data = pd.read_csv(f'data/{self.file_name_dic.get('kia_faq_data_name')}')
        return year_data, manufacturer_data, hyundai_faq_data, kia_faq_data

    def make_top10(self):
        df = self.manufacturer_data
        df = df[df['recall_month']=='총합']
        df[df['car_model']=='현대자동차(주)']
        df = df.groupby('car_model')['car_num'].sum().reset_index()
        df = df.sort_values('car_num', ascending=False).reset_index()
        df = df.iloc[:10,1:]
        return df

    def insert_year_data(self):
        try:
            conn = connector.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
            cursor = conn.cursor() # 실제 db에 명령을 전달(sql)
            insert_query = """
            insert into car_recall_db.car_recall_month(recall_year, recall_month, kr_recall_car, kr_recall_num, us_recall_car, us_recall_num, total_recall_car, total_recall_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = [tuple(row) for row in self.year_data.itertuples(index=False, name=None)]
            cursor.executemany(insert_query, data)
            conn.commit()   
            cursor.close()
            conn.close()
            print('year_data insert success')
        except Exception as e:
            print(e)

    def insert_manufacturer_data(self):
        try:
            conn = connector.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
            cursor = conn.cursor() # 실제 db에 명령을 전달(sql)
            insert_query = """
            insert into car_recall_db.car_recall_brand (recall_year, recall_month, car_model, car_num)
        values (%s, %s, %s, %s)
            """
            data = [tuple(row) for row in self.manufacturer_data.itertuples(index=False, name=None)]
            cursor.executemany(insert_query, data)
            conn.commit()  
            cursor.close()
            conn.close()
            print('manufacturer_data insert success')
        except Exception as e:
            print(e)

    def insert_faq_top10(self):
        try:
            conn = connector.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
            cursor = conn.cursor() # 실제 db에 명령을 전달(sql)
            insert_query = """
            insert into car_recall_db.hyundai_faq(hyundai_question, hyundai_answer)
            VALUES (%s, %s)
            """
            data = [tuple(row) for row in self.hyundai_faq_data.itertuples(index=False, name=None)]
            cursor.executemany(insert_query, data)
            conn.commit()
        
            insert_query = """
            insert into car_recall_db.kia_faq(kia_question, kia_answer)
            VALUES (%s, %s)
            """
            data = [tuple(row) for row in self.kia_faq_data.itertuples(index=False, name=None)]
            cursor.executemany(insert_query, data)
            conn.commit()

            insert_query = """
            insert into car_recall_db.recall_top10(top10_car_model, top10_car_num)
            VALUES (%s, %s)
            """
            data = [tuple(row) for row in self.top10_data.itertuples(index=False, name=None)]
            cursor.executemany(insert_query, data)
            conn.commit()
            print('faq_top10 insert success')
            
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
        

    def __init__(self, args:dict, file_name_dic:dict):
        self.host = args.get('host')
        self.user = args.get('user')
        self.password = args.get('password')
        self.port = args.get('port')
        self.database = args.get('database')
        self.file_name_dic = file_name_dic
        self.year_data, self.manufacturer_data, self.hyundai_faq_data, self.kia_faq_data = self.read_data()
        self.top10_data = self.make_top10()