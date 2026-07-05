# 🔧 GUIA DE INSTALAÇÃO - Stypuff

## Problema: Compiladores/Interpretadores não instalados

Seu sistema não tem os compiladores necessários. Aqui estão as soluções:

---

## 📦 Opção 1: Instalar MinGW-w64 (Recomendado para Windows)

### Passo 1: Baixar MinGW-w64
1. Visite: https://www.mingw-w64.org/
2. Clique em "Downloads"
3. Baixe a versão mais recente (x86_64)

### Passo 2: Instalar
1. Execute o instalador
2. Configure:
   - Architecture: x86_64
   - Threads: posix
   - Exception handling: seh

### Passo 3: Adicionar ao PATH
1. Pressione `Win + X` → "Configurações"
2. Vá para "Variáveis de ambiente"
3. Edite a variável "Path"
4. Adicione: `C:\Program Files\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64\bin`

### Passo 4: Compilar Stypuff
```bash
cd "c:\Users\Miguel Massola\Downloads\Stypuff"
g++ -std=c++17 -o stypuff stypuffheart.cc
.\stypuff
```

---

## 📦 Opção 2: Instalar Python (Alternativa Mais Rápida)

### Windows
1. Visite: https://www.python.org/downloads/
2. Baixe Python 3.10+
3. **IMPORTANTE**: Marque "Add Python to PATH"
4. Instale

### Após instalar
```bash
cd "c:\Users\Miguel Massola\Downloads\Stypuff"
python stypuff_interpreter.py
```

---

## 📦 Opção 3: Instalar Visual Studio Community (Completo)

1. Visite: https://visualstudio.microsoft.com/downloads/
2. Baixe "Visual Studio Community"
3. Na instalação, selecione "Desktop development with C++"
4. Após instalar, abra "Developer Command Prompt for Visual Studio"
5. Compile:
```bash
cd "c:\Users\Miguel Massola\Downloads\Stypuff"
cl /std:latest stypuffheart.cc
stypuffheart.exe
```

---

## 🚀 Opção 4: Usar Repl.it ou OnlineGDB (Sem Instalar)

### Repl.it (Recomendado)
1. Visite: https://replit.com
2. Crie nova repl C++
3. Copie o conteúdo de `stypuffheart.cc`
4. Execute online

### OnlineGDB
1. Visite: https://www.onlinegdb.com
2. Selecione C++ na linguagem
3. Cole o código
4. Compile e execute

---

## ⚡ Teste Rápido (Sem Compilador)

Se você só quer **entender como funciona** sem compilar:

1. Abra [examples.styp](examples.styp) para ver exemplos
2. Leia o código em [stypuffheart.cc](stypuffheart.cc)
3. Veja a documentação em [README.md](README.md)

---

## ✅ Verificar Instalação

### MinGW/g++
```bash
g++ --version
```
Deve mostrar a versão do g++

### Python
```bash
python --version
```
Deve mostrar Python 3.x.x

### Visual Studio
```bash
cl
```
Deve reconhecer o comando

---

## 🎯 Próximos Passos Após Instalar

1. **Compilar C++**:
   ```bash
   g++ -std=c++17 -o stypuff stypuffheart.cc
   .\stypuff
   ```

2. **Rodar Testes C++**:
   ```bash
   g++ -std=c++17 -o tests tests.cc
   .\tests
   ```

3. **Executar Interpretador Python**:
   ```bash
   python stypuff_interpreter.py
   ```

---

## 🐛 Troubleshooting

### "g++ não é reconhecido"
- Abra um **novo** terminal PowerShell/CMD após instalar
- Verifique o PATH (veja Opção 3, Passo 3)
- Reinicie o computador

### "cl não é reconhecido"
- Abra "Developer Command Prompt for Visual Studio" (não PowerShell)
- Ou adicione o caminho do VC++ ao PATH

### "python não é reconhecido"
- Reinstale Python marcando "Add Python to PATH"
- Reinicie o computador

---

## 📚 Recursos Adicionais

- **GCC Online Compiler**: https://www.onlinegdb.com/
- **Python Docs**: https://docs.python.org/3/
- **C++ Reference**: https://cppreference.com/

---

## ❓ Perguntas?

Veja os arquivos:
- [README.md](README.md) - Documentação completa
- [examples.styp](examples.styp) - Exemplos de código
- [codelist.txt](codelist.txt) - Especificação da linguagem

**Qualquer dúvida, releia este guia ou consulte as referências acima!** 🚀
