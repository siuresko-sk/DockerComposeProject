import os
import time
import requests
import psycopg2
import schedule

API_URL = "http://opendata.trudvsem.ru/api/v1/vacancies"

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "vacancies_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "secret_password_123")
    )

def init_db():
    """Создание таблицы, если она не существует."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            trudvsem_id VARCHAR(50) UNIQUE,
            title TEXT,
            salary_min INT,
            salary_max INT,
            company TEXT,
            city TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def etl_job():
    print("Запуск процесса ETL...")
    try:
        # 1. ищем вакансии 
        response = requests.get(API_URL, params={"text": "Аналитик", "size": 20}, timeout=30)
        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}")
            return
        
        data = response.json()
        # Проверка структуры ответа
        if "results" not in data:
            print(f"Неожиданная структура ответа: {list(data.keys())}")
            return

        vacancies = data.get("results", {}).get("vacancies", [])
        if not vacancies:
            print("Вакансии не найдены")
            return
        
        # 2. обработка и загрузка
        conn = get_db_connection()
        cur = conn.cursor()
        
        for item in vacancies:
            v = item.get("vacancy", {})
            
            v_id = v.get("id")
            title = v.get("job-name")
            salary_min = int(v.get("salary_min", 0)) if v.get("salary_min") else None
            salary_max = int(v.get("salary_max", 0)) if v.get("salary_max") else None

            company_obj = v.get("company", {})
            company = company_obj.get("name") if company_obj else "Не указана"
            
            city = "Не указан"
            addresses_obj = v.get("addresses", {})
            if addresses_obj and "address" in addresses_obj:
                address_list = addresses_obj.get("address", [])
                if address_list and len(address_list) > 0:
                    city = address_list[0].get("location", "Не указан")
            
            cur.execute("""
                INSERT INTO vacancies (trudvsem_id, title, salary_min, salary_max, company, city)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (trudvsem_id) DO NOTHING;
            """, (v_id, title, salary_min, salary_max, company, city))
            
        conn.commit()
        cur.close()
        conn.close()
        print(f"Успешно обработано вакансий: {len(vacancies)}")
        
    except Exception as e:
        print(f"Произошла ошибка в ETL процессе: {e}")

if __name__ == "__main__":
    time.sleep(5) 
    init_db()
    
    etl_job()
    
    # запуск каждую минуту для демонстрации
    # schedule.every(1).minutes.do(etl_job)
    # запуск каждые 4 часа
    schedule.every(4).hours.do(etl_job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
