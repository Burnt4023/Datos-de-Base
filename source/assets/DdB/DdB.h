#ifndef DDB_H
#define DDB_H 
#include <iostream>
#include "..\sqlite3\sqlite3.h"
#include <cstdlib>
#include <string>

void listarTablas(sqlite3 * db) {
  const char * showTablesSQL = "SELECT name FROM sqlite_master WHERE type='table';";
  sqlite3_stmt * stmt;

  if (sqlite3_prepare_v2(db, showTablesSQL, -1, &stmt, 0) == SQLITE_OK) {
    std::cout << "Tablas disponibles:" << std::endl;
    while (sqlite3_step(stmt) == SQLITE_ROW) {
      const unsigned char * tableName = sqlite3_column_text(stmt, 0);
      std::cout << "- " << tableName << std::endl;
    }
  }

  sqlite3_finalize(stmt);
}

void crearTabla(sqlite3 *db) {
  std::string tableName;
  std::cout << "Ingrese el nombre de la nueva tabla: ";
  std::cin >> tableName;

  // Verificar si la tabla ya existe en la base de datos
  const char *checkTableSQL = "SELECT name FROM sqlite_master WHERE type='table' AND name = ?;";
  sqlite3_stmt *stmt;

  if (sqlite3_prepare_v2(db, checkTableSQL, -1, &stmt, 0) == SQLITE_OK) {
    sqlite3_bind_text(stmt, 1, tableName.c_str(), -1, SQLITE_STATIC);

    if (sqlite3_step(stmt) == SQLITE_ROW) {
      std::cout << "La tabla ya existe en la base de datos." << std::endl;
      sqlite3_finalize(stmt);
      return;
    }
  }

  sqlite3_finalize(stmt);

  // Crear la sentencia SQL para crear la nueva tabla
  std::string createTableSQL = "CREATE TABLE IF NOT EXISTS " + tableName + " (ID INT, Nombre TEXT, Edad INT);";
  if (sqlite3_exec(db, createTableSQL.c_str(), 0, 0, 0) == SQLITE_OK) {
    std::cout << "Tabla creada con éxito." << std::endl;
  } else {
    std::cerr << "Error al crear la tabla: " << sqlite3_errmsg(db) << std::endl;
  }
}


void borrarTabla(sqlite3 * db) {
  std::string tableName;
  std::cout << "Ingrese el nombre de la tabla que desea borrar: ";
  std::cin >> tableName;

  // Verificar si la tabla existe en la base de datos
  const char * showTableSQL = "SELECT name FROM sqlite_master WHERE type='table';";
  sqlite3_stmt * stmt;

  if (sqlite3_prepare_v2(db, showTableSQL, -1, &stmt, 0) == SQLITE_OK) {
    bool tableExists = false;
    while (sqlite3_step(stmt) == SQLITE_ROW) {
      const unsigned char * existingTableName = sqlite3_column_text(stmt, 0);
      if (std::string(reinterpret_cast<const char*>(existingTableName)) == tableName) {
        tableExists = true;
        break;
      }
    }

    if (!tableExists) {
      std::cout << "La tabla no existe en la base de datos." << std::endl;
      return;
    }
  }

  sqlite3_finalize(stmt);

  // Crear la sentencia SQL para borrar la tabla
  std::string dropTableSQL = "DROP TABLE IF EXISTS " + tableName + ";";
  if (sqlite3_exec(db, dropTableSQL.c_str(), 0, 0, 0) == SQLITE_OK) {
    std::cout << "Tabla borrada con éxito." << std::endl;
  } else {
    std::cerr << "Error al borrar la tabla: " << sqlite3_errmsg(db) << std::endl;
  }
}

void seleccionarTabla(sqlite3 * db) {
  listarTablas(db);
  std::string tableName;
  std::cout << "Ingrese el nombre de la tabla: ";
  std::cin >> tableName;

  // Verificar si la tabla existe en la base de datos
  const char * showTableSQL = "SELECT name FROM sqlite_master WHERE type='table';";
  sqlite3_stmt * stmt;

  if (sqlite3_prepare_v2(db, showTableSQL, -1, &stmt, 0) == SQLITE_OK) {
    bool tableExists = false;
    while (sqlite3_step(stmt) == SQLITE_ROW) {
      const unsigned char * existingTableName = sqlite3_column_text(stmt, 0);
      if (std::string(reinterpret_cast<const char*>(existingTableName)) == tableName) {
        tableExists = true;
        break;
      }
    }

    if (!tableExists) {
      std::cout << "La tabla no existe en la base de datos." << std::endl;
      return;
    }
  }

  sqlite3_finalize(stmt);

  int opcionTabla;
  while (true) {
    system("cls");
    std::cout << "\t\t    (|   \\                        |        /|/  \\              " << std::endl;
    std::cout << "\t\t     |    | __, _|_  __   ,     __|   _     | __/ __,   ,   _  " << std::endl;
    std::cout << "\t\t    _|    |/  |  |  /  \\_/ \\_  /  |  |/     |   \\/  |  / \\_|/  " << std::endl;
    std::cout << "\t\t   (/\\___/ \\_/|_/|_/\\__/  \\/   \\_/|_/|__/   |(__/\\_/|_/ \\/ |__/  " << std::endl;
    std::cout << "\t\t                                                                  " << std::endl;
    std::cout << "\t\tTabla seleccionada: " << tableName << "\n";
    std::cout << "\t\t1. Mostrar Lista\n";
    std::cout << "\t\t2. Editar Lista\n";
    std::cout << "\t\t3. Atrás\n";
    std::cout << "\t\tSeleccione una opcion: ";
    std::cin >> opcionTabla;

    switch (opcionTabla) {
    case 1:
      // Llama a la función de mostrar lista para la tabla seleccionada
      // Ejemplo: mostrarListaParaTabla(db, tableName);
      std::cout << "Mostrar Lista para la tabla " << tableName << std::endl;
      break;
    case 2:
      // Llama a la función de editar lista para la tabla seleccionada
      // Ejemplo: editarListaParaTabla(db, tableName);
      std::cout << "Editar Lista para la tabla " << tableName << std::endl;
      break;
    case 3:
      return; // Regresar al menú principal
    default:
      std::cout << "Opción no válida. Intente nuevamente." << std::endl;
      break;
    }

    std::cout << "Presione una tecla para continuar...";
    std::cin.ignore();
    std::cin.get();
  }
}

void mostrarLista(sqlite3 * db) {
  const char * selectSQL = "SELECT * FROM MiTabla;";
  sqlite3_stmt * stmt;

  if (sqlite3_prepare_v2(db, selectSQL, -1, & stmt, 0) == SQLITE_OK) {
    while (sqlite3_step(stmt) == SQLITE_ROW) {
      int id = sqlite3_column_int(stmt, 0);
      const unsigned char * nombre = sqlite3_column_text(stmt, 1);
      int edad = sqlite3_column_int(stmt, 2);
      std::cout << "ID: " << id << ", Nombre: " << nombre << ", Edad: " << edad << std::endl;
    }
  }
  sqlite3_finalize(stmt);
}

bool existeID(sqlite3 * db, int id) {
  const char * selectSQL = "SELECT ID FROM MiTabla WHERE ID = ?;";
  sqlite3_stmt * stmt;

  if (sqlite3_prepare_v2(db, selectSQL, -1, & stmt, 0) == SQLITE_OK) {
    sqlite3_bind_int(stmt, 1, id);
    if (sqlite3_step(stmt) == SQLITE_ROW) {
      // El ID ya existe en la base de datos
      sqlite3_finalize(stmt);
      return true;
    }
  }

  sqlite3_finalize(stmt);
  return false; // El ID no existe en la base de datos
}

void agregarRegistro(sqlite3 * db) {
  int id;
  std::string nombre;
  int edad;

  std::cout << "Ingrese el ID: ";
  std::cin >> id;

  // Verificar si el ID ya existe en la base de datos
  if (existeID(db, id)) {
    std::cout << "El ID ingresado ya existe en la base de datos. No se puede repetir." << std::endl;
    std::cout << "Presione una tecla para continuar...";
    std::cin.ignore();
    std::cin.get();
    return;
  }

  std::cout << "Ingrese el nombre: ";
  std::cin >> nombre;
  std::cout << "Ingrese la edad: ";
  std::cin >> edad;

  // Crea la sentencia SQL para insertar el nuevo registro
  std::string insertSQL = "INSERT INTO MiTabla (ID, Nombre, Edad) VALUES (" +
    std::to_string(id) + ", '" + nombre + "', " + std::to_string(edad) + ");";

  if (sqlite3_exec(db, insertSQL.c_str(), 0, 0, 0) == SQLITE_OK) {
    std::cout << "Registro añadido con éxito." << std::endl;
  } else {
    std::cerr << "Error al añadir el registro: " << sqlite3_errmsg(db) << std::endl;
  }

  std::cout << "Presione una tecla para continuar...";
  std::cin.ignore();
  std::cin.get();
}

void editarRegistro(sqlite3 * db) {
  int id;
  std::cout << "Ingrese el ID del registro que desea editar: ";
  std::cin >> id;

  // Verificar si el ID existe en la base de datos
  if (!existeID(db, id)) {
    std::cout << "El ID ingresado no existe en la base de datos." << std::endl;
    std::cout << "Presione una tecla para continuar...";
    std::cin.ignore();
    std::cin.get();
    return;
  }

  int opcion;
  while (true) {
    system("cls"); // Limpiar la pantalla

    std::cout << "Editar Registro - ID: " << id << std::endl;
    std::cout << "Seleccione el atributo que desea sobrescribir:" << std::endl;
    std::cout << "1. Nombre" << std::endl;
    std::cout << "2. Edad" << std::endl;
    std::cout << "0. Atrás" << std::endl;
    std::cout << "Seleccione una opción: ";
    std::cin >> opcion;

    switch (opcion) {
    case 1: {
      std::string nuevoNombre;
      std::cout << "Ingrese el nuevo nombre: ";
      std::cin >> nuevoNombre;

      // Actualizar el nombre en la base de datos
      std::string updateSQL = "UPDATE MiTabla SET Nombre = '" + nuevoNombre + "' WHERE ID = " + std::to_string(id) + ";";
      if (sqlite3_exec(db, updateSQL.c_str(), 0, 0, 0) == SQLITE_OK) {
        std::cout << "Nombre actualizado con éxito." << std::endl;
      } else {
        std::cerr << "Error al actualizar el nombre: " << sqlite3_errmsg(db) << std::endl;
      }
      break;
    }
    case 2: {
      int nuevaEdad;
      std::cout << "Ingrese la nueva edad: ";
      std::cin >> nuevaEdad;

      // Actualizar la edad en la base de datos
      std::string updateSQL = "UPDATE MiTabla SET Edad = " + std::to_string(nuevaEdad) + " WHERE ID = " + std::to_string(id) + ";";
      if (sqlite3_exec(db, updateSQL.c_str(), 0, 0, 0) == SQLITE_OK) {
        std::cout << "Edad actualizada con éxito." << std::endl;
      } else {
        std::cerr << "Error al actualizar la edad: " << sqlite3_errmsg(db) << std::endl;
      }
      break;
    }
    case 0:
      return; // Regresar al menú anterior
    default:
      std::cout << "Opción no válida. Intente nuevamente." << std::endl;
      break;
    }

    std::cout << "Presione una tecla para continuar...";
    std::cin.ignore();
    std::cin.get();
  }
}
void borrarRegistro(sqlite3 * db) {
  int id;
  std::cout << "Ingrese el ID del registro que desea borrar: ";
  std::cin >> id;

  // Verificar si el ID existe en la base de datos
  if (!existeID(db, id)) {
    std::cout << "El ID ingresado no existe en la base de datos." << std::endl;
    std::cout << "Presione una tecla para continuar...";
    std::cin.ignore();
    std::cin.get();
    return;
  }

  // Crear la sentencia SQL para borrar el registro
  std::string deleteSQL = "DELETE FROM MiTabla WHERE ID = " + std::to_string(id) + ";";

  if (sqlite3_exec(db, deleteSQL.c_str(), 0, 0, 0) == SQLITE_OK) {
    std::cout << "Registro borrado con éxito." << std::endl;
  } else {
    std::cerr << "Error al borrar el registro: " << sqlite3_errmsg(db) << std::endl;
  }

  std::cout << "Presione una tecla para continuar...";
  std::cin.ignore();
  std::cin.get();
}

void bombardeenRamanales(sqlite3 * db) {
  std::cout << "¿Está seguro de que desea borrar la base de datos completa? (S/N): ";
  char confirmacion;
  std::cin >> confirmacion;

  if (confirmacion == 'S' || confirmacion == 's') {
    const char * dropTableSQL = "DROP TABLE IF EXISTS MiTabla;";
    if (sqlite3_exec(db, dropTableSQL, 0, 0, 0) == SQLITE_OK) {
      std::cout << "¡La base de datos ha sido borrada por completo!" << std::endl;
    } else {
      std::cerr << "Error al borrar la base de datos: " << sqlite3_errmsg(db) << std::endl;
    }
  } else {
    std::cout << "Operación de borrado cancelada." << std::endl;
  }

  std::cout << "Presione una tecla para continuar...";
  std::cin.ignore();
  std::cin.get();
}
void menuEditarLista(sqlite3 * db) {
  int opcion;
  while (true) {
    system("cls");
    std::cout << "\t\t    (|   \\                        |        /|/  \\              " << std::endl;
    std::cout << "\t\t     |    | __, _|_  __   ,     __|   _     | __/ __,   ,   _  " << std::endl;
    std::cout << "\t\t    _|    |/  |  |  /  \\_/ \\_  /  |  |/     |   \\/  |  / \\_|/  " << std::endl;
    std::cout << "\t\t   (/\\___/ \\_/|_/|_/\\__/  \\/   \\_/|_/|__/   |(__/\\_/|_/ \\/ |__/  " << std::endl;
    std::cout << "\t\t                                                                  " << std::endl;
    std::cout << "\t\tEditar Lista:\n";
    std::cout << "\t\t1. Añadir\n";
    std::cout << "\t\t2. Editar\n";
    std::cout << "\t\t3. Borrar\n";
    std::cout << "\t\t4. Atrás\n";
    std::cout << "\t\tSeleccione una opcion: ";
    std::cin >> opcion;

    switch (opcion) {
    case 1:
      // Llama a la función de añadir un nuevo registro
      agregarRegistro(db);
      break;
    case 2:
      editarRegistro(db);
      break;
    case 3:
      // Menú Borrar
      while (true) {
        system("cls");
        std::cout << "\t\t    (|   \\                        |        /|/  \\              " << std::endl;
        std::cout << "\t\t     |    | __, _|_  __   ,     __|   _     | __/ __,   ,   _  " << std::endl;
        std::cout << "\t\t    _|    |/  |  |  /  \\_/ \\_  /  |  |/     |   \\/  |  / \\_|/  " << std::endl;
        std::cout << "\t\t   (/\\___/ \\_/|_/|_/\\__/  \\/   \\_/|_/|__/   |(__/\\_/|_/ \\/ |__/  " << std::endl;
        std::cout << "\t\t                                                                  " << std::endl;
        std::cout << "\t\tBorrar:\n";
        std::cout << "\t\t1. Borrar Registro\n";
        std::cout << "\t\t2. Bombardeen Ramanales\n";
        std::cout << "\t\t3. Atrás\n";
        std::cout << "\t\tSeleccione una opcion: ";
        std::cin >> opcion;

        switch (opcion) {
        case 1:
          borrarRegistro(db);
          break;
        case 2:
          bombardeenRamanales(db);
          break;
        case 3:
          return; // Regresar al menú principal
        default:
          std::cout << "Opcion no válida. Intente nuevamente.\n";
          std::cout << "Presione una tecla para continuar...";
          std::cin.ignore();
          std::cin.get();
          break;
        }
      }
      break;

      break;
    case 4:
      return; // Regresar al menú principal
    default:
      std::cout << "Opcion no válida. Intente nuevamente.\n";
      std::cout << "Presione una tecla para continuar...";
      std::cin.ignore();
      std::cin.get();
      break;
    }
  }
}





#endif 


