# coding: utf-8
from my_app import db


class DniPracownik(db.Model):
    __tablename__ = 'Dni_Pracownik'

    Typ_wolne_id = db.Column(db.ForeignKey('Typ_wolne.id'), primary_key=True, nullable=False, index=True)
    Pracownik_id = db.Column(db.ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Data_dnia_wolnego = db.Column('Data dnia wolnego', db.Date, nullable=False)
    Ilosc_godzin = db.Column(db.Integer, nullable=False)

    Pracownik = db.relationship('Pracownik')
    Typ_wolne = db.relationship('TypWolne')


class Etap(db.Model):
    __tablename__ = 'Etap'

    id = db.Column(db.Integer, primary_key=True)
    Nazwa_etapu = db.Column(db.String(45), nullable=False)


class LogPracy(db.Model):
    __tablename__ = 'Log_Pracy'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Pracownik_id = db.Column(db.ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Zadanie_id = db.Column(db.ForeignKey('Zadanie.id'), nullable=False, index=True)
    Opis = db.Column(db.Text, nullable=False)
    Czas_pracy = db.Column(db.DateTime, nullable=False,
                           server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Ilosc_godzin = db.Column(db.Integer, nullable=False)

    Pracownik = db.relationship('Pracownik')
    Zadanie = db.relationship('Zadanie')


class Podsumowanie(db.Model):
    __tablename__ = 'Podsumowanie'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Pracownik_id = db.Column(db.ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Miesi_c = db.Column('Miesi?c', db.Integer, nullable=False)
    Rok = db.Column(db.Integer, nullable=False)
    Wynagrodzenie = db.Column(db.Float(asdecimal=True), nullable=False)

    Pracownik = db.relationship('Pracownik')


class Pracownik(db.Model):
    __tablename__ = 'Pracownik'

    id = db.Column(db.Integer, primary_key=True)
    Imi_ = db.Column('Imi?', db.String(45), nullable=False)
    Nazwisko = db.Column(db.String(45), nullable=False)
    Stanowisko = db.Column(db.String(45), nullable=False)
    Data_ko_ca_umowy = db.Column('Data ko?ca umowy', db.DateTime)

    Zadanies = db.relationship('Zadanie', secondary='Wykonawcy_zadania')


class PracownikRaport(db.Model):
    __tablename__ = 'Pracownik_Raport'

    Pracownik_id = db.Column(db.ForeignKey('Pracownik.id'), primary_key=True, nullable=False)
    Raport_id = db.Column(db.ForeignKey('Raport.id'), primary_key=True, nullable=False, index=True)
    Liczba_godzin = db.Column('Liczba godzin', db.Integer, nullable=False)

    Pracownik = db.relationship('Pracownik')
    Raport = db.relationship('Raport')


class Projekt(db.Model):
    __tablename__ = 'Projekt'

    id = db.Column(db.Integer, primary_key=True)
    Opis = db.Column(db.Text, nullable=False)
    Bud_et = db.Column('Bud?et', db.Float(asdecimal=True), nullable=False)
    Data_rozpocz_cia = db.Column('Data rozpocz?cia', db.DateTime, nullable=False)
    Data_zako_czenia = db.Column('Data zako?czenia', db.DateTime)


class Raport(db.Model):
    __tablename__ = 'Raport'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Sprint_id = db.Column(db.ForeignKey('Sprint.id'), primary_key=True, nullable=False, index=True)
    Czas_wygenerowania = db.Column('Czas wygenerowania', db.DateTime, nullable=False,
                                   server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Opis = db.Column(db.Text, nullable=False)

    Sprint = db.relationship('Sprint')


class RolaPracownikProjekt(db.Model):
    __tablename__ = 'Rola_pracownik_projekt'

    Stawka = db.Column(db.Float(asdecimal=True), nullable=False)
    Pracownik_id = db.Column(db.ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Projekt_id = db.Column(db.ForeignKey('Projekt.id'), primary_key=True, nullable=False, index=True)
    Rola_pracownika_id = db.Column(db.ForeignKey('Rola_pracownika.id'), nullable=False, index=True)

    Pracownik = db.relationship('Pracownik')
    Projekt = db.relationship('Projekt')
    Rola_pracownika = db.relationship('RolaPracownika')


class RolaPracownika(db.Model):
    __tablename__ = 'Rola_pracownika'

    id = db.Column(db.Integer, primary_key=True)
    Nazwa_roli = db.Column(db.String(45), nullable=False)


class Sprint(db.Model):
    __tablename__ = 'Sprint'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Projekt_id = db.Column(db.ForeignKey('Projekt.id'), primary_key=True, nullable=False, index=True)
    Data_rozpocz_cia = db.Column('Data rozpocz?cia', db.DateTime, nullable=False)
    Data_zako_czenia = db.Column('Data zako?czenia', db.DateTime)

    Projekt = db.relationship('Projekt')


class TypWolne(db.Model):
    __tablename__ = 'Typ_wolne'

    id = db.Column(db.Integer, primary_key=True)
    Nazwa_typu = db.Column('Nazwa typu', db.String(45), nullable=False)


t_Wykonawcy_zadania = db.Table(
    'Wykonawcy_zadania', db.metadata,
    db.Column('Pracownik_id', db.ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True),
    db.Column('Zadanie_id', db.ForeignKey('Zadanie.id'), primary_key=True, nullable=False, index=True)
)


class Zadanie(db.Model):
    __tablename__ = 'Zadanie'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Etap_id = db.Column(db.ForeignKey('Etap.id'), nullable=False, index=True)
    Pracownik_id = db.Column(db.ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Sprint_id = db.Column(db.ForeignKey('Sprint.id'), primary_key=True, nullable=False, index=True)
    Opis = db.Column(db.Text, nullable=False)

    Etap = db.relationship('Etap')
    Pracownik = db.relationship('Pracownik')
    Sprint = db.relationship('Sprint')
