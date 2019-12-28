import os
import sqlite3
import datetime

class Database():
    @classmethod
    def __init__(cls):

        cls.path = "./tips.db"
        cls.db = sqlite3.connect(cls.path)
        cls.cursor = cls.db.cursor()
        cls.db.execute( "CREATE TABLE IF NOT EXISTS ypallilos(id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT, meri INTEGER)")
        cls.db.execute("CREATE TABLE IF NOT EXISTS posto(id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT )")
        cls.db.execute("CREATE TABLE IF NOT EXISTS istoriko(id INTEGER PRIMARY KEY AUTOINCREMENT, tips REAL,id_postou INTEGER, apo TIMESTAMP, eos TIMESTAMP )")
        cls.db.commit()
        cls.cursor.close()
        cls.db.close()

    @classmethod
    def not_exists(cls,table,column,value):
        #Εδώ κοιτάμε αν υπάρχει καταχώρηση με το όνομα που θα δώσουμε στο ανάλογο πίνακα.Αν δεν υπάρχει επιστρέφει True, αν υπαρχει False
        db = sqlite3.connect(cls.path)
        cursor = db.cursor()
        entoli = "select * from {} where {} = ? ".format(table,column)
        cursor.execute( entoli,(value,))
        apotelesma = cursor.fetchall()

        if len(apotelesma) == 0:
            return True
        return False

    @classmethod
    def save_ypallilos(cls,name,meri):
        #Με αυτή την εντολή αποθηκεύεται στη βάση ο υπάλληλος
        table = 'ypallilos'
        column = 'name'
        if cls.not_exists(table,column, name):
            try:
                db = sqlite3.connect(cls.path)
                cursor = db.cursor()
                cursor.execute("INSERT INTO ypallilos(name,meri) values(?,?) ",(name,meri))
                db.commit()

            except :
                print ("Ο υπάλληλος δεν αποθηκεύτηκε!")

    @classmethod
    def save_posto(cls,name):
        #Με αυτή την εντολή αποθηκεύεται στη βάση το πόστο
        table='posto'
        column='name'
        if cls.not_exists(table,column, name):
            try:
            	db = sqlite3.connect(cls.path)
            	cursor = db.cursor()
            	cursor.execute("INSERT INTO posto(name) values(?) ",(name,))
            	db.commit()

            except :
                print ("Το πόστο δεν αποθηκεύτηκε!")

    @classmethod
    def save_tips(cls,tips,posto,date_in,date_out):

    	#try:
    	db = sqlite3.connect(cls.path)
    	cursor = db.cursor()
    	cursor.execute("INSERT INTO istoriko (tips,id_postou,apo,eos) values(?,?,?,?) ",(float(tips),posto,date_in,date_out))
    	db.commit()
        #except :
        	#print ("Τα tips δεν αποθηκεύτηκαν")

    @classmethod
    def update_ypallilos(cls,name,meri,id):
        #Ενημερώνει τα στοιχεία του υπαλλήλου
        try:
            db = sqlite3.connect(cls.path)
            cursor = db.cursor()
            cursor.execute("UPDATE ypallilos SET name = ? , meri = ? WHERE id= ?",(name,meri,id))
            db.commit()

        except:
            print("Δεν έγινε το update")

    @classmethod
    def update_posto(cls,name,id):
        #Ενημερώνει τα στοιχεία του πόστου
        try:
            db = sqlite3.connect(cls.path)
            cursor = db.cursor()
            cursor.execute("UPDATE posto SET name = ? WHERE id= ?",(name,id))
            db.commit()

        except:
            print("Δεν έγινε το update")

    @classmethod
    def deleteById(cls,table,id):
		#Διαγράφει μια καταχώρηση με συγκεκριμένη id από το ανάλογο table
        try:
            db = sqlite3.connect(cls.path)
            cursor = db.cursor()
            cursor.execute("DELETE ? WHERE id= ?",(table,id))
            db.commit()

        except:
            print("Δεν έγινε η διαγραφή!!!")

    @classmethod
    def selectAllFrom(cls,table):
        #Επιστρέφει όλα τα δεδομένα ενώς συγκεκριμένου πίνακa
        try:
            db=sqlite3.connect("tips.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM {} ".format(table))
            apotelesma=cursor.fetchall()
            return apotelesma

        except:
            print("Δεν μπορέσαμε να διαβάσουμε τον πίνακα {}".format(table))


    @classmethod
    def selectBy(cls,table,column,value):
        #Επιστρέφει μια καταχώρηση με συγκεκριμένο Id
        try:
            db=sqlite3.connect("tips.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM ? WHERE ? = ?",(table,column,value))
            apotelesma = cursor.fetchall()

        except:
            print("Δεν μπορέσαμε να διαβάσουμε τον πίνακα {}".format(table))
            return apotelesma

    @classmethod
    def getId(cls,table,name):
        #Επιστρέφει μια καταχώρηση με συγκεκριμένο Id
        try:
            db=sqlite3.connect("tips.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM {} WHERE name = ?".format(table),(name,))
            apotelesma = cursor.fetchall()
            return apotelesma[0][0]

        except:
            print("Δεν μπορέσαμε να διαβάσουμε τον πίνακα {}".format(table))



class Ypallilos():
    """
    Ένας υπάλληλος μπορεί να παίρνει διπλάσιο μερίδιο από έναν άλλον
    (παράδειγμα ο σερβιτόρος παίρνει 1 μερίδιο ανά βάρδια, ο captain 2 ενώ ο metr 3)
    Όταν δημιουργούμε έναν υπάλληλο πρέπει να δηλώνουμε το όνομά του, πόσα μέρη αντιστοιχεί
    το μεροκάματό του, και πόσα μεροκάματα έχει κάνει μέσα στο χρονικό περιθώριο που υπολογίζουμε
    τα tips.
    """
    def __init__(self,name,meri,merokamata =0, id = 0):
        self.name = name
        self.meri = round(meri,2)
        self.merokamata = round(merokamata,2)
        self.id = id
        self.tips= None
        self.table='ypallilos'

    def save(self):
        Database.save_ypallilos(self.name,self.meri)

    def update(self):
        Database.update_ypallilos(self,self.name,self.meri,self.id)

    def delete(self):
        Database.deleteById(self,self.table,self.id)

    @staticmethod
    def showAll():
        table = 'ypallilos'
        apotelesma = Database.selectAllFrom(table)
        for row in apotelesma:
            print(row)

    @classmethod
    def createById(cls,id):
        table=cls.table
        column='id'
        apotelesma = Database.selectBy(self,table,column,id)
        for i in apotelesma:
            print(i)
        name = apotelesma[0][1]
        meri = round(float(apotelesma[0][2]),2)
        return cls(name,meri,id=id)

    @classmethod
    def createByName(cls,name):
        table=cls.table
        column='name'
        apotelesma = Database.selectBy(self,table,column,name)
        for i in apotelesma:
            print(i)
        id = apotelesma[0][0]
        name = apotelesma[0][1]
        meri = round(float(apotelesma[0][2]),2)
        return cls(name,meri,id=id)


class Posto():
    """
    Εδώ δημιουργείται το πόστο για το οποίο χωρίζουμε τα tips.
    """
    def __init__(self,name,id=0):
        self.name = name
        self.id = int(id)
        self.table = 'posto'

    def save(self):
        Database.save_posto(self.name)

    def update(self,onoma):
        Database.update_posto(self.name,self.id)

    def showAll(self):
    	apotelesma = Database.selectAllFrom(self.table)
    	for row in apotelesma:
    		print(row)

    def delete(self):
        Database.deleteById(self,self.table,self.id)

    @classmethod
    def createById(cls,id):
        table=cls.table
        column='id'
        apotelesma = Database.selectBy(self,table,column,id)
        name = apotelesma[0][1]
        return cls(name,id=id)

    @classmethod
    def createByName(cls,name):
        table=cls.table
        column='name'
        apotelesma = Database.selectBy(self,table,column,name)
        id = apotelesma[0][0]
        name = apotelesma[0][1]
        return cls(name=name,id=id)

    def getId(self):
    	self.id = Database.getId(self.table,self.name)



class Tips():
    """
    Εδώ δημιουργούμε τα tips που θέλουμε να χωρίσουμε.
    Πρέπει να δηλώσουμε ποσό, σε ποιό πόστο απευθείνεται και από πότε
    μέχρι πότε αντιστοιχεί το συγκεκριμένο ποσό.
    """
    def __init__(self,poso,posto,date_in=datetime.datetime(2019,1,1),date_out = datetime.datetime(2019,1,6),id=0):
        self.poso = float(poso)
        self.posto = posto
        self.date_in = date_in
        self.date_out = date_out
        self.table = 'istoriko'
        self.id = id

    def save(self):
    	self.posto.getId()
    	Database.save_tips(self.poso,self.posto.id,self.date_in,self.date_out)

    @staticmethod
    def showAll():
        apotelesma = Database.selectAllFrom('istoriko')
        for row in apotelesma:
            print(row)

    def delete(self):
        Database.deleteById(self,self.table,self.id)


class Diaxoristis():
    """
    Στον διαχωριστή δηλώνουμε τους υπάλληλους που δικαιούνται tips, και αυτός
    αναλαμβάνει να χωρίσει τα tips ανάλογα τα μεροκάματα που εργάστηκαν, και το
    μερίδιο που δικαιούνται ανα μέρα.
    """
    def __init__(self,ypalliloi,tips):
        self.ypalliloi = ypalliloi
        self.tips = tips

    def meri(self):
        #Εδώ υπολογίζουμε συνολικά τα μέρη των υπαλλήλων
        meri=0
        for yp in self.ypalliloi:
            meri += yp.meri * yp.merokamata
        return float(meri)

    def ena_meros(self):
        #Εδώ υπολογίζουμε πόσα χρήματα αντιστοιχούν σε ένα μέρος των tips
        meros= self.tips.poso / self.meri()
        return round(meros,2)

    def tips_ypallilou(self,name):
        #Εδώ υπολογίζουμε τα tips που δικαιούται ο υπάλλολος που καταχωρούμε
        for yp in self.ypalliloi:
            if yp.name == name:
                meros = self.ena_meros()
                xrimata = meros * yp.meri
                xrimata*= yp.merokamata
                return round(xrimata,2)

    def ypoloipo(self):
        sinolo= 0
        for yp in self.ypalliloi:
            sinolo += self.tips_ypallilou(yp.name)
        ypoloipo= self.tips.poso - sinolo
        return round(ypoloipo,2)

    def apotelesma(self):
        print ("Τα μεροκάματα ειναι {} και βγαίνουν {} ευρώ το 1 μεροκάματο.".format(int(self.meri()),self.ena_meros()))
        print('-'*20)
        print ("Το αποτέλεσμα για το πόστο {} είναι : ".format (self.tips.posto.name))


        for yp in self.ypalliloi:
            print("* Ο υπάλληλος {}, δικαιούται {} ευρώ, από {}-{}-{} έως {}-{}-{}".format(yp.name, str(self.tips_ypallilou(yp.name)),self.tips.date_in.day,self.tips.date_in.month,self.tips.date_in.year,self.tips.date_out.day,self.tips.date_out.month,self.tips.date_out.year))
            print("-"*20)

        if self.ypoloipo() < 0:
            ypoloipo = self.ypoloipo()
            ypoloipo*= -1
            print("Με τη στρογγυλοποίηση των μεταβλητών το ποσό που μοιράστηκε είναι μεγαλύτερο και χρειαζόμαστε ακόμα άλλα {} ευρώ για να είμαστε σωστοί με το άθροισμα. \n Παρακαλώ ελέγξτε τις καταχωρήσεις σας!!!".format(str(ypoloipo)))

        elif self.ypoloipo() > 0:
            print("Το υπόλοιπο είναι {} ευρώ.".format(str(self.ypoloipo())))

        else:
            print("Δεν υπάρχει υπόλοιπο.")

    def result(self):
        result ={}
        result["money"] = self.tips.poso
        result["merokamata"] = int(self.meri())
        result["merokamato"] = self.ena_meros()
        result["posto"] = str(self.tips.posto.name)
        result["ypoloipo"] = self.ypoloipo()
        result["date_from"] = self.tips.date_in
        result["date_until"] = self.tips.date_out
        ypalliloi = []


        for yp in self.ypalliloi:
            ypallilos = {}
            ypallilos['name'] =yp.name
            ypallilos["money"] = str(self.tips_ypallilou(yp.name))
            ypallilos["merokamata"] = str(yp.merokamata)
            ypalliloi.append(ypallilos)

        result["ypalliloi"] = ypalliloi

        return result
