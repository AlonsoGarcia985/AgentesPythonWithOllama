import os
import sqlite3
import dotenv

dotenv.load_dotenv()

DB = os.path.join(os.path.dirname(__file__), "onboarding.db")


DOCUMENTOS_REQUERIDOS = ["ine", "curp", "comprobante_domicilio", "acta_nacimiento"]

PATRON_RFC = r"^[A-Z]{4}\d{6}[A-Z0-9]{3}$"


AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
APIKEY = os.getenv('API_KEY')
VERSION = os.getenv('VERSION') 
MODEL = os.getenv('MODEL')

def conectar():
    return sqlite3.connect(DB)
