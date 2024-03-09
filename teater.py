import sqlite3

def create_db():
    # lager db fil hvis ikke allerede eksisterer
    f = open("teater.db", "w")
    # lager tabeller fra teater.sql
    with open("teater.sql", "r") as create_sql:
        create_script = create_sql.read()
    con = sqlite3.connect("teater.db")
    cursor = con.cursor()
    cursor.executescript(create_script)
    con.commit()
    # leser inn sql script og setter inn i tabeller
    with open("insert_teater.sql", "r") as insert_sql:
        insert_script = insert_sql.read()
    cursor.executescript(insert_script)
    con.commit()

    billetid_count = 0
    # sett inn stoler for Hovedscenen
    cursor.execute('''insert into Billettkjop values (0, '2024-03-09', '16:00:00', 0)''') # billettkjøp for å samle opp seter som er tatt i Hovedscenen
    f = open("hovedscenen.txt", "r")
    dato = f.readline()
    words = dato.split()
    for word in words:
        if len(word) == 10 and word[4] == "-" and word[7] == "-":
            dato =  word
    cursor.execute('''select fid from Forestilling where dato = ? and stykkeid = 0''', (dato,))
    fid = cursor.fetchone()[0]
    stol_count = 524
    galleri = f.readline().strip()
    for i in range(4, 0, -1):
        line = f.readline()
        for j in range(len(line)-2, -1, -1):
            cursor.execute('''insert into Stol values ('Trøndelag Teater', 'Hovedscenen', ?, ?, ?)''', (stol_count, i, galleri,)) # setter inn stolen uansett
            if line[j] == '1':
                # dersom stolen er tatt, registrer kjøpet
                cursor.execute('''insert into Billett values(?, ?, ?, ?, 'Hovedscenen', 'Trøndelag Teater', ?, 0, 'Ordinær')''', (billetid_count, stol_count, i, galleri, fid,))
                billetid_count += 1
            stol_count -= 1
    parkett = f.readline().strip()
    for i in range(18, 0, -1):
        line = f.readline()
        for j in range(len(line)-2, -1, -1):
            if line[j] == 'x':
                stol_count -= 1
                continue
            cursor.execute('''insert into Stol values ('Trøndelag Teater', 'Hovedscenen', ?, ?, ?)''', (stol_count, i, parkett,)) # setter inn stolen uansett
            if line[j] == '1':
                # dersom stolen er tatt, registrer kjøpet
                cursor.execute('''insert into Billett values(?, ?, ?, ?, 'Hovedscenen', 'Trøndelag Teater', ?, 0, 'Ordinær')''', (billetid_count, stol_count, i, parkett, fid,))
                billetid_count += 1
            stol_count -= 1
    f.close()

    # sett inn stoler for Gamle scene
    cursor.execute('''insert into Billettkjop values (1, '2024-03-09', '16:00:00', 0)''') # billettkjøp for å samle opp seter som er tatt i Hovedscenen
    f = open("gamle-scene.txt", "r")
    dato = f.readline()
    words = dato.split()
    for word in words:
        if len(word) == 10 and word[4] == "-" and word[7] == "-":
            dato =  word
    cursor.execute('''select fid from Forestilling where dato = ? and stykkeid = 1''', (dato,))
    fid = cursor.fetchone()[0]
    galleri = f.readline().strip()
    for i in range(3, 0, -1):
        line = f.readline()
        for j in range(len(line)-1, 0, -1):
            cursor.execute('''insert into Stol values ('Trøndelag Teater', 'Gamle scene', ?, ?, ?)''', (j, i, galleri,)) # setter inn stolen uansett
            if line[j] == '1':
                # dersom stolen er tatt, registrer kjøpet
                cursor.execute('''insert into Billett values(?, ?, ?, ?, 'Gamle scene', 'Trøndelag Teater', ?, 0, 'Ordinær')''', (billetid_count, j, i, galleri, fid,))
                billetid_count += 1
    balkong = f.readline().strip()
    for i in range(4, 0, -1):
        line = f.readline()
        for j in range(len(line)-1, 0, -1):
            cursor.execute('''insert into Stol values ('Trøndelag Teater', 'Gamle scene', ?, ?, ?)''', (j, i, balkong,)) # setter inn stolen uansett
            if line[j] == '1':
                # dersom stolen er tatt, registrer kjøpet
                cursor.execute('''insert into Billett values(?, ?, ?, ?, 'Gamle scene', 'Trøndelag Teater', ?, 0, 'Ordinær')''', (billetid_count, j, i, balkong, fid,))
                billetid_count += 1
    parkett = f.readline().strip()
    for i in range(10, 0, -1):
        line = f.readline()
        for j in range(len(line)-1, 0, -1):
            cursor.execute('''insert into Stol values ('Trøndelag Teater', 'Gamle scene', ?, ?, ?)''', (j, i, parkett,)) # setter inn stolen uansett
            if line[j] == '1':
                # dersom stolen er tatt, registrer kjøpet
                cursor.execute('''insert into Billett values(?, ?, ?, ?, 'Gamle scene', 'Trøndelag Teater', ?, 0, 'Ordinær')''', (billetid_count, j, i, parkett, fid,))
                billetid_count += 1
    con.commit()
    con.close()

if __name__=="__main__":
    create_db()
