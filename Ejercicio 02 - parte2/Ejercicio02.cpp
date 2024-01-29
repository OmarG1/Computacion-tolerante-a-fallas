#include <iostream>

// Alumno: Gomez Quintero Omar Federico

/*
Esta es una forma de mostrar el como se realiza el manejo de errores utilizando en este caso la estructura try catch.
Aplicando esta estructura  en una funcion que realiza una division si esta recibe como denominador 0 el throw le mandara un mensaje al entrar al catch
mostrando "Error: El denominador es 0"

Otra forma para manejar errores es aplicando lo conocido como "metodo con codigo de retorno", el cual es implementado por los desarrolladores, este consiste en retornar un valor el cual nos permita identificar
el error si no se cumplio lo esperado que en este caso como retorno es 0 y si nos genera esto significa que ahi se encuentra el error


*/

double dividir(int numerador, int denominador) {
    try {
        if (denominador == 0) {
            throw std::runtime_error("Error: El denominador es 0.");
        }
        return numerador / denominador;
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return 0.0; 
    }
}

int main() {
    int numerador, denominador, numerador2, denominador2;

    std::cout << "Ingrese el numerador: ";
    std::cin >> numerador;

    std::cout << "Ingrese el denominador: ";
    std::cin >> denominador;

    std::cout << "Ingrese el numerador: ";
    std::cin >> numerador2;

    std::cout << "Ingrese el denominador: ";
    std::cin >> denominador2;

    double resultado = dividir(numerador, denominador);

    // si es igual al valor que se asigno para identificar el error en este caso 0 mostrara el mensaje de que hubo un error en caso contrario realiza el funcionamiento correcto
    if (resultado != 0.0) {
        std::cout << "Resultado: " << resultado << std::endl;
    } else {
        std::cout << "Hubo un error al realizar la division." << std::endl;
    }

    double resultado2 = dividir(numerador2, denominador2);

    if (resultado2 != 0.0) {
        std::cout << "Resultado: " << resultado2 << std::endl;
    } else {
        std::cout << "Hubo un error al realizar la division." << std::endl;
    }

    return 0;
}