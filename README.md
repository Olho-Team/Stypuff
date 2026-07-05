# 🔥 Stypuff Programming Language

Um interpretador de linguagem de programação criado em C++ baseado na especificação Stypuff.

## 📁 Estrutura do Projeto

```
stypuffheart.cc  - Núcleo do interpretador (Tokenizer, Parser, Executor)
localdata.cc     - Gerenciador de variáveis, objetos e arrays
branch.cc        - Controle de fluxo e eventos
codelist.txt     - Lista de código/especificação Stypuff
examples.styp    - Exemplos de programas em Stypuff
tests.cc         - Suite de testes
README.md        - Este arquivo
```

## 🚀 Como Compilar e Executar

### Windows (PowerShell/CMD)
```bash
# Compilar o interpretador
g++ -std=c++17 -o stypuff stypuffheart.cc

# Executar
.\stypuff
```

### Linux/Mac
```bash
# Compilar
g++ -std=c++17 -o stypuff stypuffheart.cc

# Executar
./stypuff
```

### Alternativa: Executar via wrapper (recomendado para desenvolvimento)
O repositório inclui um wrapper `bin/stypuff` que executará o binário C++ se estiver disponível (em `build/stypuff`) ou o interpretador Python (`stypuff_interpreter.py`) como fallback.

Para usar:
```bash
./bin/stypuff
```

### Instalar como package Python
Para instalar localmente como um package Python e ter o comando `stypuff` disponível:
```bash
pip install .
```

Para instalar em modo de desenvolvimento:
```bash
pip install -e .
```

Depois disso, execute o interpretador com:
```bash
stypuff
```

### Publicar no PyPI
Esse projeto já possui um workflow GitHub Actions em `.github/workflows/publish-python.yml`.
Ele publica automaticamente na criação de um release, usando o segredo `PYPI_API_TOKEN` no repositório.

### Compilar e Rodar Testes
```bash
# Compilar testes
g++ -std=c++17 -o tests tests.cc

# Executar
.\tests  (Windows)
./tests  (Linux/Mac)
```

## 📝 Sintaxe Stypuff

### Criação de Aplicação
```stypuff
styp.create("nomeApp")
work("nomeApp").eventboxNew
```

### Variáveis
```stypuff
let variavel = valor
const constante = valor
let numero = 42
let texto = "Olá"
```

### Operações Aritméticas
```stypuff
let resultado = 10 + 5    # Soma
let resultado = 10 - 5    # Subtração
let resultado = 10 * 5    # Multiplicação
let resultado = 10 / 5    # Divisão
```

### Condicionais
```stypuff
if(condicao) {
    # código
}

if(condicao) {
    # código if
} else {
    # código else
}
```

### Funções
```stypuff
func() {
    # corpo da função
}

func(param1, param2) {
    # função com parâmetros
}
```

### Arrays
```stypuff
let styp.array("lista") = 
@array("lista")[0]
@array("lista")[1]
```

### Dados/Objetos
```stypuff
set @data("player") = {}
set @data("player") = "name" = "Miguel"
set @variable("score") = 100
```

### Controle de Eventos
```stypuff
# Eventos de mouse/teclado
if(event == $mousekeypressed("click")) {
    # ação
}

if(event == $keypressed("Enter")) {
    # ação
}

# Listeners de eventos
on @variable(""):: $itsDisplaying("") {
    # ação quando variável está visível
}

on @variable(""):: $itsNotDisplaying("") {
    # ação quando variável está oculta
}
```

### Módulos
```stypuff
import "utils"
import "helpers"

export minhaFuncao()
```

### Recursos Mitológicos
```stypuff
assemble = mythicControl

mythicControl.##Response() {
    @eletronicData("estado") = "processado"
}

mythicControl.##CallResponse() {
    # processar resposta
}

# Acessar dados eletrônicos, imagens e dados Stypuff
@eletronicData()
@image()
@stypuffData()
```

## 💡 Exemplos

### Exemplo 1: Olá Mundo
```stypuff
styp.create("helloApp")
let greeting = "Olá, Mundo!"
print(greeting)
```

### Exemplo 2: Calculadora
```stypuff
styp.create("calculator")
let num1 = 10
let num2 = 5

let soma = num1 + num2
let produto = num1 * num2

print(soma)
print(produto)
```

### Exemplo 3: Gerenciamento de Dados
```stypuff
styp.create("dataApp")

let nome = "Miguel"
let score = 9999

@data("jogador") = {}
set @data("jogador") = "name" = "Herói"
set @data("jogador") = "level" = 10
set @data("jogador") = "health" = 100
```

### Exemplo 4: Lógica Condicional
```stypuff
styp.create("ifExample")

let idade = 18

if(idade == 18) {
    print("Você tem 18 anos!")
}

if(idade > 21) {
    print("Maior de idade!")
} else {
    print("Menor de idade!")
}
```

## 🔧 Componentes Principais

### Tokenizer
Converte o código-fonte em tokens:
- Palavras-chave: `styp`, `work`, `if`, `let`, `func`, etc
- Identificadores: nomes de variáveis e funções
- Strings: `"texto entre aspas"`
- Números: `123`, `42`
- Símbolos: `(){}@$:=,|[]`
- Operadores: `+ - * / == != < > <= >=`

### Parser
Constrói uma Árvore de Sintaxe Abstrata (AST):
- Statements: criação, declarações, condicionais
- Expressions: valores literais, operações binárias, acessos a arrays
- Funções: declarações e chamadas

### Executor (StypuffEngine)
Interpreta e executa o AST:
- Gerencia variáveis e dados
- Avalia expressões aritméticas e lógicas
- Executa fluxo de controle
- Gerencia funções e eventos

### LocalData
Gerencia estado da aplicação:
- Variáveis simples (chave-valor)
- Objetos/Dados complexos (aninhados)
- Arrays com acesso por índice
- Métodos de get/set/has/delete

### FlowControl
Controla fluxo de execução:
- Avaliação de condições
- Gerenciamento de eventos
- Execução condicional
- Listeners de eventos

## 🎯 Features Implementadas

✅ Tokenizer completo
✅ Parser com suporte a expressões
✅ Operações aritméticas (+, -, *, /)
✅ Comparações (==, !=, <, >, <=, >=)
✅ Variáveis e constantes
✅ Arrays com índice
✅ Objetos/Dados complexos
✅ Funções
✅ Condicionais (if/else)
✅ Eventos e listeners
✅ Gerenciamento de estado
✅ Print/Output

## 📈 Features Futuras

⬜ Loops (while, for)
⬜ Switch/Case (when)
⬜ Try/Catch para tratamento de erros
⬜ Closures e funções anônimas
⬜ Destruturaçao de objetos
⬜ Spread operator
⬜ Async/await
⬜ Classes com herança
⬜ Tipos customizados
⬜ Pattern matching
⬜ Integração com sistemas externos
⬜ Otimizações de performance

## 🐛 Troubleshooting

### Erro de compilação
- Certifique-se de usar C++17 ou superior: `g++ -std=c++17`
- Verifique que todos os includes estão no mesmo diretório

### Código não executa
- Verifique a sintaxe no seu programa Stypuff
- Veja os exemplos em `examples.styp`

### Variáveis não funcionam
- Use `let` antes de declarar variáveis
- Use `@variable()` para acessar do gerenciador de dados

## 📚 Referências

- Especificação completa: `codelist.txt`
- Exemplos: `examples.styp`
- Testes: `tests.cc`

## 👨‍💻 Autor

Criado como interpretador educacional para a linguagem Stypuff.

## 📄 Licença

Libre para uso educacional e pessoal.

---

**Divirta-se programando em Stypuff!** 🚀✨
