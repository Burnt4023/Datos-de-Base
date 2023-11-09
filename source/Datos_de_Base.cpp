  #include "assets\DdB\DdB.h"

  int main() {
    system("chcp 65001");
    sqlite3 * db;
    int rc = sqlite3_open("data/Datos.db", & db);

    if (rc) {
      std::cerr << "Error al abrir la base de datos: " << sqlite3_errmsg(db) << std::endl;
      return rc;
    }
    
    const char * createTableSQL = "CREATE TABLE IF NOT EXISTS MiTabla (ID INT, Nombre TEXT, Edad INT);";
    rc = sqlite3_exec(db, createTableSQL, 0, 0, 0);

    if (rc != SQLITE_OK) {
      std::cerr << "Error al crear la tabla: " << sqlite3_errmsg(db) << std::endl;
      sqlite3_close(db);
      return rc;
    }

int opcion;
  while (true) {
    system("cls");
    std::cout << "\t\t    (|   \\                        |        /|/  \\              " << std::endl;
    std::cout << "\t\t     |    | __, _|_  __   ,     __|   _     | __/ __,   ,   _  " << std::endl;
    std::cout << "\t\t    _|    |/  |  |  /  \\_/ \\_  /  |  |/     |   \\/  |  / \\_|/  " << std::endl;
    std::cout << "\t\t   (/\\___/ \\_/|_/|_/\\__/  \\/   \\_/|_/|__/   |(__/\\_/|_/ \\/ |__/  " << std::endl;
    std::cout << "\t\t                                                                  " << std::endl;
    std::cout << "\t\t1. Listar Tablas\n";
    std::cout << "\t\t2. Crear Tabla\n";
    std::cout << "\t\t3. Ver Lista\n";
    std::cout << "\t\t4. Editar Lista\n";
    std::cout << "\t\t5. Salir\n";
    std::cout << "\t\tSeleccione una opcion: ";
    std::cin >> opcion;

    switch (opcion) {
    case 1:
      listarTablas(db);
      break;
    case 2:
      crearTabla(db);
      break;
    case 3:
      mostrarLista(db);
      // Pausa para esperar a que el usuario presione una tecla antes de borrar la pantalla
      std::cout << "Presione una tecla para continuar...";
      std::cin.ignore();
      std::cin.get();
      break;
    case 4:
      menuEditarLista(db);
      break;
    case 5:
      sqlite3_close(db);
      return 0;
    default:
      std::cout << "Opcion no válida. Intente nuevamente.\n";
      break;
    }
  }
}