import sqlite3

DB = "onboarding.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("DROP TABLE IF EXISTS empleados")
    cur.execute("DROP TABLE IF EXISTS departamentos")
    cur.execute("DROP TABLE IF EXISTS puestos_rangos")


    cur.execute("""
                CREATE TABLE departamentos
                (
                    id     INTEGER PRIMARY KEY,
                    nombre TEXT    NOT NULL,
                    activo INTEGER NOT NULL DEFAULT 1
                )
                """)


    cur.execute("""
                CREATE TABLE puestos_rangos
                (
                    id          INTEGER PRIMARY KEY,
                    nivel       TEXT NOT NULL,
                    salario_min REAL NOT NULL,
                    salario_max REAL NOT NULL
                )
                """)


    cur.execute("""
                CREATE TABLE empleados
                (
                    id              INTEGER PRIMARY KEY,
                    rfc             TEXT UNIQUE NOT NULL,
                    nombre          TEXT        NOT NULL,
                    departamento_id INTEGER,
                    puesto          TEXT,
                    salario         REAL,
                    fecha_ingreso   TEXT
                )
                """)

    # Estas son las inserciones con los datos del json
    departamentos = [
        (1, "Recursos Humanos", 1),
        (2, "Finanzas", 1),
        (3, "Ingeniería", 1),
        (4, "Marketing", 1),
    ]
    cur.executemany(
        "INSERT INTO departamentos (id, nombre, activo) VALUES (?, ?, ?)",
        departamentos,
    )

    rangos = [
        (1, "junior", 8000, 15000),
        (2, "semi", 15000, 22000),
        (3, "senior", 22000, 40000),
        (4, "director", 40000, 80000),
    ]
    cur.executemany(
        "INSERT INTO puestos_rangos (id, nivel, salario_min, salario_max) VALUES (?, ?, ?, ?)",
        rangos,
    )

    empleados = [
        (1, "GOME850101AB1", "Gabriel Gómez", 2, "Analista Financiero", 18000, "2022-01-15"),
        (2, "LORA920605CD3", "Laura Lara", 1, "Coordinadora de RH", 25000, "2021-06-05"),
        (3, "MART780312EF5", "Mario Martínez", 3, "Líder Técnico", 45000, "2020-03-12"),
    ]
    cur.executemany(
        "INSERT INTO empleados "
        "(id, rfc, nombre, departamento_id, puesto, salario, fecha_ingreso) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        empleados,
    )

    conn.commit()
    conn.close()



if __name__ == "__main__":
    init_db()
