# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DniPracownik(Base):
    __tablename__ = 'Dni_Pracownik'

    Typ_wolne_id = Column(ForeignKey('Typ_wolne.id'), primary_key=True, nullable=False, index=True)
    Pracownik_id = Column(ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Data_dnia_wolnego = Column('Data dnia wolnego', Date, nullable=False)
    Ilosc_godzin = Column(Integer, nullable=False)

    Pracownik = relationship('Pracownik')
    Typ_wolne = relationship('TypWolne')


class Etap(Base):
    __tablename__ = 'Etap'

    id = Column(Integer, primary_key=True)
    Nazwa_etapu = Column(String(45), nullable=False)


class LogPracy(Base):
    __tablename__ = 'Log_Pracy'

    id = Column(Integer, primary_key=True, nullable=False)
    Pracownik_id = Column(ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Zadanie_id = Column(ForeignKey('Zadanie.id'), nullable=False, index=True)
    Opis = Column(Text, nullable=False)
    Czas_pracy = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Ilosc_godzin = Column(Integer, nullable=False)

    Pracownik = relationship('Pracownik')
    Zadanie = relationship('Zadanie')


class Podsumowanie(Base):
    __tablename__ = 'Podsumowanie'

    id = Column(Integer, primary_key=True, nullable=False)
    Pracownik_id = Column(ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Miesi_c = Column('Miesi?c', Integer, nullable=False)
    Rok = Column(Integer, nullable=False)
    Wynagrodzenie = Column(Float(asdecimal=True), nullable=False)

    Pracownik = relationship('Pracownik')


class Pracownik(Base):
    __tablename__ = 'Pracownik'

    id = Column(Integer, primary_key=True)
    Imi_ = Column('Imi?', String(45), nullable=False)
    Nazwisko = Column(String(45), nullable=False)
    Stanowisko = Column(String(45), nullable=False)
    Data_ko_ca_umowy = Column('Data ko?ca umowy', DateTime)

    Zadanies = relationship('Zadanie', secondary='Wykonawcy_zadania')


class PracownikRaport(Base):
    __tablename__ = 'Pracownik_Raport'

    Pracownik_id = Column(ForeignKey('Pracownik.id'), primary_key=True, nullable=False)
    Raport_id = Column(ForeignKey('Raport.id'), primary_key=True, nullable=False, index=True)
    Liczba_godzin = Column('Liczba godzin', Integer, nullable=False)

    Pracownik = relationship('Pracownik')
    Raport = relationship('Raport')


class Projekt(Base):
    __tablename__ = 'Projekt'

    id = Column(Integer, primary_key=True)
    Opis = Column(Text, nullable=False)
    Bud_et = Column('Bud?et', Float(asdecimal=True), nullable=False)
    Data_rozpocz_cia = Column('Data rozpocz?cia', DateTime, nullable=False)
    Data_zako_czenia = Column('Data zako?czenia', DateTime)


class Raport(Base):
    __tablename__ = 'Raport'

    id = Column(Integer, primary_key=True, nullable=False)
    Sprint_id = Column(ForeignKey('Sprint.id'), primary_key=True, nullable=False, index=True)
    Czas_wygenerowania = Column('Czas wygenerowania', DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Opis = Column(Text, nullable=False)

    Sprint = relationship('Sprint')


class RolaPracownikProjekt(Base):
    __tablename__ = 'Rola_pracownik_projekt'

    Stawka = Column(Float(asdecimal=True), nullable=False)
    Pracownik_id = Column(ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Projekt_id = Column(ForeignKey('Projekt.id'), primary_key=True, nullable=False, index=True)
    Rola_pracownika_id = Column(ForeignKey('Rola_pracownika.id'), nullable=False, index=True)

    Pracownik = relationship('Pracownik')
    Projekt = relationship('Projekt')
    Rola_pracownika = relationship('RolaPracownika')


class RolaPracownika(Base):
    __tablename__ = 'Rola_pracownika'

    id = Column(Integer, primary_key=True)
    Nazwa_roli = Column(String(45), nullable=False)


class Sprint(Base):
    __tablename__ = 'Sprint'

    id = Column(Integer, primary_key=True, nullable=False)
    Projekt_id = Column(ForeignKey('Projekt.id'), primary_key=True, nullable=False, index=True)
    Data_rozpocz_cia = Column('Data rozpocz?cia', DateTime, nullable=False)
    Data_zako_czenia = Column('Data zako?czenia', DateTime)

    Projekt = relationship('Projekt')


class TypWolne(Base):
    __tablename__ = 'Typ_wolne'

    id = Column(Integer, primary_key=True)
    Nazwa_typu = Column('Nazwa typu', String(45), nullable=False)


t_Wykonawcy_zadania = Table(
    'Wykonawcy_zadania', metadata,
    Column('Pracownik_id', ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True),
    Column('Zadanie_id', ForeignKey('Zadanie.id'), primary_key=True, nullable=False, index=True)
)


class Zadanie(Base):
    __tablename__ = 'Zadanie'

    id = Column(Integer, primary_key=True, nullable=False)
    Etap_id = Column(ForeignKey('Etap.id'), nullable=False, index=True)
    Pracownik_id = Column(ForeignKey('Pracownik.id'), primary_key=True, nullable=False, index=True)
    Sprint_id = Column(ForeignKey('Sprint.id'), primary_key=True, nullable=False, index=True)
    Opis = Column(Text, nullable=False)

    Etap = relationship('Etap')
    Pracownik = relationship('Pracownik')
    Sprint = relationship('Sprint')
