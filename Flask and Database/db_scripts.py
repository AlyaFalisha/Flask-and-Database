import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' delete all tables '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    do('''CREATE TABLE IF NOT EXISTS quiz(id INTEGER PRIMARY KEY,
       name VARCHAR)''')
    
    do('''CREATE TABLE IF NOT EXISTS question(
       id INTEGER PRIMARY KEY,
       question VARCHAR,
       answer VARCHAR,
       wrong1 VARCHAR,
       wrong2 VARCHAR,
       wrong3 VARCHAR)''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz_content(
       id INTEGER PRIMARY KEY,
       quiz_id INTEGER,
       question_id INTEGER,
       FOREIGN KEY(quiz_id) REFERENCES quiz (id),
       FOREIGN KEY(question_id) REFERENCES question(id))''')
    
    close()

def add_questions():
    questions =[
        ('apa warna pelangi','merah','hitam','putih','emas'),
        ('1+3','4','9','3','5'),
        ('apa arti kata "water"', 'air','api','udara','tanah'),
        ('mana hewan yang tidak memiliki kaki','ular','ayam', 'belalang', 'sapi'),
        ('di planet mana manusia tinggal', 'bumi', 'venus', 'mars', 'saturnus'),
    ]
    open()
    cursor.executemany('''INSERT INTO question
                       (question, answer, wrong1, wrong2, wrong3)
                       VALUES(?,?,?,?,?)''',questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Level 1', ),
        ('Level 2', ),
        ('Level 3', ) 
    ]
    open()
    cursor.executemany('''INSERT INTO quiz(name)VALUES(?)''', quizes)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foeign_keys=on''')
    query = "INSERT INTO quiz_content(quiz_id, question_id) VALUES (?,?)"
    answer = input("add a link(y/n?)")
    while answer != 'n':
        quiz_id = int(input("quiz id:"))
        question_id = int(input("question id:"))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Add a link(y/n)?")
    close()

def get_question_after(question_id = 0, quiz_id = 1):
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id>? AND quiz_content.quiz_id==?
    ORDER BY quiz_content.id '''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    get_question_after()
    show_tables()

if __name__ == "__main__":
    main()