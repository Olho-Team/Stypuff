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
