#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

// Incluir o interpretador
#include "stypuffheart.cc"

int main() {
    StypuffEngine engine;
    
    cout << "╔════════════════════════════════════════════════════════════╗" << endl;
    cout << "║           STYPUFF Programming Language v1.0              ║" << endl;
    cout << "║                  Interactive Interpreter                 ║" << endl;
    cout << "╚════════════════════════════════════════════════════════════╝" << endl << endl;
    
    // TESTE 1: Hello World
    cout << "\n--- TESTE 1: Olá Mundo ---" << endl;
    string code1 = R"(
        styp.create("helloApp")
        let greeting = "Olá, Mundo!"
    )";
    engine.execute(code1);
    
    // TESTE 2: Operações Aritméticas
    cout << "\n--- TESTE 2: Operações Aritméticas ---" << endl;
    string code2 = R"(
        styp.create("calculator")
        let num1 = 10
        let num2 = 5
        let soma = num1 + num2
        let subtracao = num1 - num2
        let multiplicacao = num1 * num2
        let divisao = num1 / num2
    )";
    engine.execute(code2);
    
    // TESTE 3: Condicionais
    cout << "\n--- TESTE 3: Condicionais ---" << endl;
    string code3 = R"(
        styp.create("ifExample")
        let idade = 18
        if(idade == 18) {
            print("Você tem 18 anos!")
        }
    )";
    engine.execute(code3);
    
    // TESTE 4: Comparações
    cout << "\n--- TESTE 4: Comparações ---" << endl;
    string code4 = R"(
        styp.create("comparisonTest")
        let valor = 42
        print(valor)
    )";
    engine.execute(code4);
    
    // TESTE 5: Arrays e Dados
    cout << "\n--- TESTE 5: Gerenciador de Dados ---" << endl;
    StypuffEngine engine5;
    engine5.data.setVariable("nome", "Miguel");
    engine5.data.setVariable("score", "9999");
    engine5.data.createArray("numeros");
    engine5.data.pushToArray("numeros", "10");
    engine5.data.pushToArray("numeros", "20");
    engine5.data.pushToArray("numeros", "30");
    
    cout << "Variável 'nome': " << engine5.data.getVariable("nome") << endl;
    cout << "Variável 'score': " << engine5.data.getVariable("score") << endl;
    cout << "Array[0]: " << engine5.data.getArrayElement("numeros", 0) << endl;
    cout << "Array[1]: " << engine5.data.getArrayElement("numeros", 1) << endl;
    cout << "Array[2]: " << engine5.data.getArrayElement("numeros", 2) << endl;
    cout << "Tamanho do Array: " << engine5.data.getArraySize("numeros") << endl;
    
    // TESTE 6: Objetos/Dados Complexos
    cout << "\n--- TESTE 6: Objetos/Dados Complexos ---" << endl;
    StypuffEngine engine6;
    engine6.data.createData("player");
    engine6.data.setDataField("player", "name", "Herói");
    engine6.data.setDataField("player", "level", "10");
    engine6.data.setDataField("player", "health", "100");
    engine6.data.setDataField("player", "mana", "50");
    
    cout << "Player Name: " << engine6.data.getDataField("player", "name") << endl;
    cout << "Player Level: " << engine6.data.getDataField("player", "level") << endl;
    cout << "Player Health: " << engine6.data.getDataField("player", "health") << endl;
    cout << "Player Mana: " << engine6.data.getDataField("player", "mana") << endl;
    
    cout << "\n╔════════════════════════════════════════════════════════════╗" << endl;
    cout << "║                  Testes Concluídos!                      ║" << endl;
    cout << "╚════════════════════════════════════════════════════════════╝" << endl;
    
    return 0;
}
