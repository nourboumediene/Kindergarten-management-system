#make sure you download mysql-python-connector 
import mysql.connector as mysql
host = "127.0.0.1"
user = "root"
password = ""
def connetion():
    #connecting to msql
    try:
        db = mysql.connect(host = host, user = user, password = password)
        print("connection etablie")
    except Exception as x :
        print(x)
        print("failed to connect")
    #connecting to existing databas
    try:
        db1 = mysql.connect(host = host, user = user, password = password, database = "creche2")
        print("connecter to creche2 database")
    except Exception as x :
        print("could not connect to creche2 data base")
        print(x)
    return db1

#afficher la bd de n'improte quelle table
def dispaly_record_table(nom_tab,cmd_handeler):
    cmd_handeler.execute(f"SELECT * from {nom_tab} ")
    records = cmd_handeler.fetchall()#command handler which the query when it's executed to fetch all the results that we get from this four table and save that into our
    print("display the records")
    for record in records: print(record)
def delete_tab(db1,nom_tab,cmd_handeler):
    try:
        cmd_handeler.execute(f"DROP TABLE {nom_tab}")
        print(f"table {nom_tab} droped succesfully")
    except Exception as x :
        print(f"table {nom_tab} could not be droped ")     
        print(x)
def recup_data(db1,nom_table,cmd_handeler):
    cmd_handeler.execute(f"""SELECT * FROM {nom_table} """)
    return cmd_handeler.fetchall()

#------------------------ADMIN-------------------
def create_admin_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS admin (id INT AUTO_INCREMENT PRIMARY KEY,id_admin VARCHAR(10), mot_de_passe VARCHAR(10) NOT NULL,nom VARCHAR(20) NOT NULL,prénom VARCHAR(20) NOT NULL)""")#this is the colomns 
        print("table admin created succesfully")
    except Exception as x :
        print("table admin could not be created ")     
        print(x)
    query = "INSERT IGNORE INTO admin (id_admin,mot_de_passe,nom,prénom) VALUES (%s,%s,%s,%s)" 
    query_vals = ("id","mdp","Creche","Creche") 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")

#------------------------INVENTAIRE-------------------
def create_inventaire_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS inventaire(id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        produit VARCHAR(30) NOT NULL,
        fournisseur VARCHAR(30) NOT NULL,
        nombre_d_unite INT,
        prix_d_unite INT NOT NULL,
        unite_de_stockage VARCHAR(10) NOT NULL,
        montant INT NOT NULL,
        date VARCHAR(7))""")#this is the colomns 
        print("table  inventaire created succesfully")
    except Exception as x :
        print("table inventaire could not be created ")     
        print(x)

def add_data_inventaire(db1,query_vals,cmd_handeler):
    query = """INSERT INTO inventaire (produit,fournisseur,nombre_d_unite,prix_d_unite,unite_de_stockage,montant,date) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)""" 
    cmd_handeler.execute(query,query_vals)
    db1.commit() 
    print(cmd_handeler.rowcount,"record inserted")
    
def up_data_inventaire(db1,query_vals,cmd_handeler):
    query= """UPDATE inventaire SET produit = %s, fournisseur = %s ,
        nombre_d_unite = %s,prix_d_unite = %s ,
        unite_de_stockage = %s,montant =  %s
        WHERE date = %s AND id = %s; """
    cmd_handeler.execute(query,query_vals)
    db1.commit()
    print(cmd_handeler.rowcount,"record inserted")
#------------------------STOCK-------------------
def create_stock_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS stock(produit VARCHAR(40) PRIMARY KEY, nb INT)""")
        print("table  stock created succesfully")
    except Exception as x :
        print("table stock could not be created ")     
        print(x)

def add_data_stock(db1,query_vals,cmd_handeler):
    query = """INSERT IGNORE INTO stock (produit,nb) 
    VALUES (%s,%s)""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted stock")

def recup_nb_stock(db1,query_vals,cmd_handeler):
    query = """Select nb FROM stock WHERE produit = %s """
    cmd_handeler.execute(query,query_vals)
    records = cmd_handeler.fetchone()
    return records

def up_data_stock(db1,query_vals,cmd_handeler):
    query = """INSERT INTO stock (produit,nb) VALUES(%s,%s)
        ON DUPLICATE KEY UPDATE produit = VALUES(produit),
        nb = nb + VALUES(nb);""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted stock")
#------------------------ENFANTS-------------------
def create_enfant_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS enfant(id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(20) NOT NULL,
        prenom VARCHAR(20) NOT NULL,
        genre VARCHAR(15) NOT NULL,
        age SMALLINT(6) NOT NULL,
        date_de_naissance DATE NOT NULL,
        lieu_de_naissance VARCHAR(25) NOT NULL,
        niveau SMALLINT(6) NOT NULL,
        classe SMALLINT(6) NOT NULL,
        frais SMALLINT(6) NOT NULL,
        transport tinyint(1) NOT NULL,
        groupe_sanguin VARCHAR(25) NOT NULL,
        allergies VARCHAR(50) NOT NULL,
        food_allergies VARCHAR(50) NOT NULL,
        vaccin VARCHAR(100) NOT NULL,
        id_parent SMALLINT(6) NOT NULL)""")
        print("table  enfant created succesfully")
    except Exception as x :
        print("table enfant could not be created ")     
        print(x)

def add_data_enfant(db1,query_vals,cmd_handeler):
    query = """INSERT INTO enfant (nom,prenom,genre,age,date_de_naissance,lieu_de_naissance,niveau,classe,
    frais,transport,groupe_sanguin,allergies,food_allergies,vaccin,id_parent) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() 
    print(cmd_handeler.rowcount,"record inserted")
    #on meme temps  on ajoutempour les frais
    q = (query_vals[0], query_vals[1], query_vals[6],query_vals[7])
    add_data_frais(db1,q,cmd_handeler)

def up_data_enfant(db1,query_vals,cmd_handeler):
    query= """UPDATE enfant SET nom = %s, prenom = %s ,
        genre = %s, age = %s ,
        date_de_naissance = %s,lieu_de_naissance =  %s,
        niveau = %s ,classe = %s,
        frais = %s, transport = %s ,groupe_sanguin = %s ,
        allergies = %s , food_allergies = %s ,
        vaccin = %s , id_parent = %s WHERE id = %s; """
    cmd_handeler.execute(query,query_vals)
    db1.commit()
    print(cmd_handeler.rowcount,"record inserted")
    q = (query_vals[0], query_vals[1], query_vals[6],query_vals[7],query_vals[15])
    up_data_frais(db1,q,cmd_handeler)

def up_data_enfant_montant(db1,query_vals,cmd_handeler):
    query = " UPDATE enfant set frais = %s WHERE id = %s"
    cmd_handeler.execute(query,query_vals)
    db1.commit() 

def supp_data_enfant(db1,query_vals,cmd_handeler):
    query = "DELETE FROM enfant WHERE id = %s"
    cmd_handeler.execute(query,query_vals)
    query = "DELETE FROM frais WHERE id = %s"
    cmd_handeler.execute(query,query_vals)
    db1.commit()

#------------------------Frais-------------------
def create_frais_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS frais(id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(20) NOT NULL,
        prenom VARCHAR(20) NOT NULL,
        niveau SMALLINT(6) NOT NULL,
        classe SMALLINT(6) NOT NULL,
        frais_inscription INTEGER(8) NOT NULL,
        frais_assurance INTEGER(8) NOT NULL,
        frais_livre INTEGER(8) NOT NULL,
        frais_mensuel INTEGER(8) NOT NULL,
        montant INTEGER(8) NOT NULL,
        etat BIT)""")#this is the colomns 
        print("table frais created succesfully")
    except Exception as x :
        print("table frais could not be created ")     
        print(x)

def add_data_frais(db1,query_vals,cmd_handeler):
    query = """INSERT IGNORE INTO frais(nom,prenom,niveau,classe) 
    VALUES (%s,%s,%s,%s)"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() 
    print(cmd_handeler.rowcount,"record inserted")

def up_data_frais(db1,query_vals,cmd_handeler):
    query = """UPDATE frais SET nom = %s,
    prenom = %s,
    niveau = %s,
    classe = %s WHERE id = %s""" 
    cmd_handeler.execute(query,query_vals)
    db1.commit()

def up_data_frais_nb(db1,query_vals,cmd_handeler):
    query = """UPDATE frais SET frais_inscription = %s,
    frais_assurance = %s,
    frais_livre = %s,
    frais_mensuel = %s,
    montant = %s ,
    etat = %s WHERE id = %s""" 
    cmd_handeler.execute(query,query_vals)
    db1.commit()

#------------------------PARENTS-------------------
def create_parents_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS parents(id INTEGER NOT NULL PRIMARY KEY,
        nom VARCHAR(20) NOT NULL,
        prenom VARCHAR(20) NOT NULL,
        contact VARCHAR(10) ,
        adresse_mail VARCHAR(60) NOT NULL,
        heure_de_travail VARCHAR(60) NOT NULL,
        adresse VARCHAR(60) NOT NULL)""")
        print("table created succesfully")
    except Exception as x :
        print("table could not be created ")     
        print(x)

def up_data_parents(db1,query_vals,cmd_handeler):
    query = """UPDATE parents SET nom =%s,prenom =%s,contact =%s,adresse_mail = %s,heure_de_travail =%s,adresse =%s WHERE id = %s;"""
    cmd_handeler.execute(query,query_vals)
    db1.commit()
    print(cmd_handeler.rowcount,"record inserted")

def add_data_parents(db1,query_vals,cmd_handeler): # a partir de enfant 
    query = """INSERT INTO parents (id,nom) 
        VALUES (%s,%s)
        ON DUPLICATE KEY UPDATE
        nom = VALUES(nom)"""
    cmd_handeler.execute(query,query_vals)
    db1.commit()
    print(cmd_handeler.rowcount,"record inserted")

#-----------------------ENFANT ARCHIVE-------------
def create_archEnf_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS archEnf(id INTEGER NOT NULL,
        nom VARCHAR(20) NOT NULL,
        prenom VARCHAR(20) NOT NULL,
        niveau SMALLINT(6) NOT NULL,
        classe SMALLINT(6) NOT NULL,
        frais SMALLINT(6) NOT NULL,
        date VARCHAR(4) )""")#this is the colomns image LONGBLOB NOT NULL
        print("table archEnf created succesfully")
    except Exception as x :
        print("table archEnf could not be created ")     
        print(x)

def add_data_archEnf(db1,query_vals,cmd_handeler):
    query = """INSERT INTO archEnf (id,nom,prenom,niveau,classe,frais,date) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() 
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("archEnf",cmd_handeler)

#------------------------PROGRAMME------------------
def create_programme_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS programme(
        id INT AUTO_INCREMENT PRIMARY KEY,
        h1_dim VARCHAR(60),h1_lun VARCHAR(60),h1_mar VARCHAR(60),h1_mer VARCHAR(60),h1_jeu VARCHAR(60),
        h2_dim VARCHAR(60),h2_lun VARCHAR(60),h2_mar VARCHAR(60),h2_mer VARCHAR(60),h2_jeu VARCHAR(60),
        h3_dim VARCHAR(60),h3_lun VARCHAR(60),h3_mar VARCHAR(60),h3_mer VARCHAR(60),h3_jeu VARCHAR(60),
        h4_dim VARCHAR(60),h4_lun VARCHAR(60),h4_mar VARCHAR(60),h4_mer VARCHAR(60),h4_jeu VARCHAR(60),
        h5_dim VARCHAR(60),h5_lun VARCHAR(60),h5_mar VARCHAR(60),h5_mer VARCHAR(60),h5_jeu VARCHAR(60),
        date VARCHAR(4),edu VARCHAR(60),niv VARCHAR(15),classe VARCHAR(60))""")#this is the colomns 
        print("table programme created succesfully")
    except Exception as x :
        print("table programme could not be created ")     
        print(x)

def add_data_prog(db1,query_vals,cmd_handeler):
    query = """INSERT INTO programme (
        h1_dim,h1_lun,h1_mar,h1_mer,h1_jeu,
        h2_dim,h2_lun,h2_mar,h2_mer,h2_jeu,
        h3_dim,h3_lun,h3_mar,h3_mer,h3_jeu,
        h4_dim,h4_lun,h4_mar,h4_mer,h4_jeu,
        h5_dim,h5_lun,h5_mar,h5_mer,h5_jeu,
        date,edu,niv,classe) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("programme",cmd_handeler)

def supp_data_prog(db1,query_vals,cmd_handeler):
    try:
        query = """DELETE FROM programme WHERE date = %s AND edu = %s AND niv = %s AND classe = %s""" 
        cmd_handeler.execute(query,query_vals)
        db1.commit() # to save the changers in the data base
        print(cmd_handeler.rowcount,"record DELETED")
        dispaly_record_table("programme",cmd_handeler)
        return cmd_handeler.rowcount
    except Exception as x:
        print(x)
        return 0


#------------------------CLASSE------------------
def create_classe_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS classe (id_classe VARCHAR(60) PRIMARY KEY)""")#this is the colomns 
        print("table classe created succesfully")
    except Exception as x :
        print("table classe could not be created ")     
        print(x)

def add_data_classe(db1,query_vals,cmd_handeler):
    query = """
    INSERT IGNORE INTO classe (id_classe) 
    VALUES (%s)""" 
    cmd_handeler.execute(query,query_vals)
    db1.commit() 

def supp_data_classe(db1,query_vals,cmd_handeler):
    query = """DELETE FROM classe WHERE id_classe = %s""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record DELETED")
    dispaly_record_table("classe",cmd_handeler)

#------------------------EDUCATEUR------------------
def create_edu_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS edu (id_edu VARCHAR(60) PRIMARY KEY)""")#this is the colomns 
        print("table edu created succesfully")
    except Exception as x :
        print("table edu could not be created ")     
        print(x)

def add_data_edu(db1,query_vals,cmd_handeler):
    query = """
    INSERT IGNORE INTO edu (id_edu) 
    VALUES (%s)""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("edu",cmd_handeler)

def supp_data_edu(db1,query_vals,cmd_handeler):
    query = """DELETE FROM edu WHERE id_edu = %s""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record DELETED")
    dispaly_record_table("edu",cmd_handeler)


#------------------------NIVEAU------------------   
def create_niv_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS niv (id_niv VARCHAR(60) PRIMARY KEY)""")#this is the colomns 
        print("table niv created succesfully")
    except Exception as x :
        print("table niv could not be created ")     
        print(x)

def add_data_niv(db1,query_vals,cmd_handeler):
    query = """ INSERT IGNORE INTO niv (id_niv) VALUES (%s)"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("niv",cmd_handeler)

def supp_data_niv(db1,query_vals,cmd_handeler):
    query = """DELETE FROM niv WHERE id_niv = %s""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record DELETED")
    dispaly_record_table("niv",cmd_handeler)

#------------------------MATIERE------------------   
def create_mat_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS mat (id_mat VARCHAR(60) PRIMARY KEY)""")#this is the colomns 
        print("table mat created succesfully")
    except Exception as x :
        print("table mat could not be created ")     
        print(x)

def add_data_mat(db1,query_vals,cmd_handeler):
    query = """ INSERT IGNORE INTO mat (id_mat) VALUES (%s)"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("mat",cmd_handeler)

def supp_data_mat(db1,query_vals,cmd_handeler):
    query = """DELETE FROM mat WHERE id_mat = %s""" 
    cmd_handeler.execute(query,query_vals)
    db1.commit()


#------------------------EMPLOYES-------------------
def create_employes_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS employes(id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(20) NOT NULL,
        prenom VARCHAR(20) NOT NULL,
        contact INT(11) NOT NULL,
        adresse_mail VARCHAR(60) NOT NULL,
        nb_jour_t INT(11) NOT NULL,
        poste VARCHAR(50) NOT NULL,
        salaire_j INT NOT NULL,
        montant_m INT NOT NULL)""")#this is the colomns 
        print("table employes created succesfully")
    except Exception as x :
        print("table employes could not be created ")     
        print(x)

def add_data_employes(db1,query_vals,cmd_handeler):
    query = """INSERT INTO employes(nom,prenom,contact,adresse_mail,nb_jour_t,poste,salaire_j,montant_m) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("employes",cmd_handeler)

def up_data_employes(db1,query_vals,cmd_handeler):
    query = """UPDATE employes SET nom = %s, prenom = %s, contact = %s, adresse_mail = %s,nb_jour_t = %s, poste = %s, salaire_j = %s, montant_m = %s WHERE id = %s""" 
    cmd_handeler.execute(query,query_vals)
    db1.commit()

def supp_data_employes(db1,query_vals,cmd_handeler):
    query = "DELETE FROM employes WHERE id = %s"
    cmd_handeler.execute(query,query_vals)
    db1.commit()
#------------------------DASHBOARD-------------------
def create_dashboard_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS dashboard(id smallint(6) AUTO_INCREMENT PRIMARY KEY,
        nb_enfant INT,
        nb_perso INT,
        montant_inven INT,
        montant_perso INT,
        montant_frais INT,
        montant_tt INT,
        revenu INT )""")#this is the colomns 
        print("table dashboard created succesfully")
    except Exception as x :
        print("table dashboard could not be created ")     
        print(x)
    query = """INSERT INTO dashboard (nb_enfant,nb_perso,montant_inven,montant_perso,montant_frais,montant_tt,revenu) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    query_vals = (0,0,0,0,0,0,0)
    cmd_handeler.execute(query,query_vals)
    db1.commit()
    print(cmd_handeler.rowcount,"record inserted")
    #mj_enf_dash(db1, cmd_handeler)
    #mj_inv_dash(db1, cmd_handeler)
    #mj_perso_dash(db1, cmd_handeler)
    #mj_rev_perso_dash(db1, cmd_handeler)
def mj_enf_dash(db1,cmd_handeler):
    #la donne dans dashboard n'est que la donne qui existe dans les autres tabs
    #recupe nb_enfant d'apres le dernier id
    query = """SELECT id FROM enfant ORDER BY id DESC""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query)
    record = cmd_handeler.fetchone()
    nb_enfant = 0
    if record != None:
        nb_enfant = record[0] 
    #the dashboard change
    query = "UPDATE dashboard SET nb_enfant = %s WHERE id = %s" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,(nb_enfant,1)) 
    db1.commit()
def mj_perso_dash(db1,cmd_handeler):
    query = """SELECT id FROM employes ORDER BY id DESC""" 
    cmd_handeler.execute(query)
    record = cmd_handeler.fetchone()
    print(record)
    nb_perso = 0
    if record != None:
        nb_perso = record[0] 
    #the dashboard change
    query = "UPDATE dashboard SET nb_perso = %s WHERE id = %s" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,(nb_perso,1)) 
    db1.commit()
def mj_rev_perso_dash(db1,cmd_handeler):
    query = "SELECT montant_m FROM employes"
    cmd_handeler.execute(query)
    records = cmd_handeler.fetchall()
    m = 0
    if records != 0:
        for row in records:
            m = m + row[0]
        print(m)
    print("m",m)
    query = "UPDATE dashboard SET montant_perso = %s WHERE id = %s"
    cmd_handeler.execute(query,(m,1)) 
    db1.commit()

def mj_inv_dash(db1,cmd_handeler):
    query = "SELECT montant from inventaire"
    cmd_handeler.execute(query)
    records = cmd_handeler.fetchall()
    montant_inven = 0
    if records != None:
        for row in records:
            montant_inven = montant_inven +row[0] 
            print(row)
    #the dashboard change
    query = "UPDATE dashboard SET montant_inven = %s WHERE id = %s" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,(montant_inven,1)) 
    db1.commit()

def mj_montant_frais_dash(db1,query_vals,cmd_handeler):
    query = "UPDATE dashboard SET montant_frais = %s WHERE id = %s"
    cmd_handeler.execute(query,(query_vals,1)) 
    db1.commit()
def mj_montant_tt_dash(db1,cmd_handeler):
    cmd_handeler.execute("SELECT montant_frais,montant_perso,montant_inven FROM dashboard WHERE id = %s",(1,))
    r = cmd_handeler.fetchone()
    query = "UPDATE dashboard SET montant_tt = %s WHERE id = %s"
    cmd_handeler.execute(query,(r[1]+r[2],1)) 
    query = "UPDATE dashboard SET revenu = %s WHERE id = %s"
    cmd_handeler.execute(query,(r[0] - r[1] - r[2],1)) 
    db1.commit()

#------------------------PLATS GOUTER-------------------
def create_plat_gout_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS plat_gout(gouter VARCHAR(60) PRIMARY KEY)""")#this is the colomns 
        print("table plat_gout created succesfully")
    except Exception as x :
        print("table plat_gout could not be created ")     
        print(x)
    dispaly_record_table("plat_gout",cmd_handeler)
    
def add_data_plat_gout(db1,query_vals,cmd_handeler):
    query = """INSERT IGNORE INTO plat_gout (gouter) 
    VALUES (%s)""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("plat_gout",cmd_handeler)

def supp_data_plat_gout(db1,query_vals,cmd_handeler):
    query = """DELETE FROM plat_gout WHERE gouter = %s"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record DELETED")
    dispaly_record_table("plat_gout",cmd_handeler)


#------------------------PLATS DEJEUNER-------------------
def create_plat_dej_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS plat_dej (dejeuner VARCHAR(60) PRIMARY KEY)""")#this is the colomns 
        print("table plat_dej created succesfully")
    except Exception as x :
        print("table plat_dej could not be created ")     
        print(x)
    #insert test
    #query = "INSERT  IGNORE INTO plat_dej (dejeuner) VALUES (%s)" 
    #cmd_handeler.execute(query,("kk",))
    #db1.commit() # to save the changers in the data base
    #print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("plat_dej",cmd_handeler)
    
def add_data_plat_dej(db1,query_vals,cmd_handeler):
    query = """INSERT IGNORE INTO plat_dej (dejeuner) 
    VALUES (%s)""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("plat_dej",cmd_handeler)

def supp_data_plat_dej(db1,query_vals,cmd_handeler):
    query = """DELETE FROM plat_dej WHERE dejeuner = %s""" # on  peut pas faire passer les var directement 
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record DELETED")
    dispaly_record_table("plat_dej",cmd_handeler)


#------------------------MENU-------------------
def create_menu_table(db1,cmd_handeler):
    try:
        cmd_handeler.execute("""CREATE TABLE IF NOT EXISTS menu(
        date VARCHAR(10) PRIMARY KEY,
        gout1_dim VARCHAR(60),
        dej_dim VARCHAR(60),
        gout2_dim VARCHAR(60),
        gout1_lun VARCHAR(60),
        dej_lun VARCHAR(60),
        gout2_lun VARCHAR(60),
        gout1_mar VARCHAR(60),
        dej_mar VARCHAR(60),
        gout2_mar VARCHAR(60),
        gout1_mer VARCHAR(60),
        dej_mer VARCHAR(60),
        gout2_mer VARCHAR(60),
        gout1_jeu VARCHAR(60),
        dej_jeu VARCHAR(60),
        gout2_jeu VARCHAR(60))""")#this is the colomns 
        print("table menu created succesfully")
    except Exception as x :
        print("table menu could not be created ")     
        print(x)

def add_data_menu(db1,query_vals,cmd_handeler):
    query = """
        INSERT INTO menu (date,gout1_dim,dej_dim,gout2_dim,
        gout1_lun,dej_lun,gout2_lun,
        gout1_mar,dej_mar,gout2_mar,
        gout1_mer,dej_mer,gout2_mer,
        gout1_jeu,dej_jeu,gout2_jeu) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE date =VALUES(date),
        gout1_dim = VALUES(gout1_dim),dej_dim =VALUES(dej_dim),gout2_dim =VALUES(gout2_dim),
        gout1_lun = VALUES(gout1_lun),dej_lun =VALUES(dej_lun),gout2_lun =VALUES(gout2_lun),
        gout1_mar = VALUES(gout1_mar),dej_mar =VALUES(dej_mar),gout2_mar =VALUES(gout2_mar),
        gout1_mer = VALUES(gout1_mer),dej_mer = VALUES(dej_mer),gout2_mer = VALUES(gout2_mer),
        gout1_jeu = VALUES(gout1_jeu),dej_jeu = VALUES(dej_jeu),gout2_jeu = VALUES(gout2_jeu);"""
    cmd_handeler.execute(query,query_vals)
    db1.commit() # to save the changers in the data base
    print(cmd_handeler.rowcount,"record inserted")
    dispaly_record_table("menu",cmd_handeler)

def recup_data_menu(db1,query_val,cmd_handeler):
    query = "SELECT * FROM menu WHERE date = %s"
    cmd_handeler.execute(query,query_val)
    record = cmd_handeler.fetchone()
    return record

def supp_data_menu(db1,query_vals,cmd_handeler):
    try :
        query = "DELETE FROM menu WHERE date = %s"
        cmd_handeler.execute(query,query_vals)
        db1.commit()
        print(cmd_handeler.rowcount,"record deleted")
        return cmd_handeler.rowcount
    except Exception as x:
        print(x)
        return 0

