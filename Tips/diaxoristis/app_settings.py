# app_settings.py

#from app_settings import MY_SETTING στο views για παράδειγμα

# project's settings.py
#APP_NAME_MY_SETTING = 'something else'

from django.conf import settings


MyEmployees=[]
#Αποθηκεύω το πόστο για να το χρησιμοποιήσω σε άλλα views
MyPosto = ""
#Αποθηκεύω την ημ/νια από, για να το χρησιμοποιήσω σε άλλα views
date_from = ""
#Αποθηκεύω την ημ/νια μέχρι, για να το χρησιμοποιήσω σε άλλα views
date_until = ""
#Αποθηκεύω το ποσό για να το χρησιμοποιήσω σε άλλα views
Money = ""
#Εδώ βάζω σε ποιό φορμάτ θα γράφεται η ημερομηνία
DATE_INPUT_FORMATS = ['%d-%m-%Y',]
#Από εδώ ξέρουμε ποιά είναι τα extra fields της form των υπαλλήλων στο StepTwoView
Dynamic_Fields =[]
#Δημιουργείτε ένα instance του Diaxoristis απ΄ό το tipsLib
Diaxoristis = None
# Εδώ αποθηκεύεται το αποτέλσμα για να το χρησιμοποιήσουμε στο τελευταίο βήμα
Result_Tips = {}
