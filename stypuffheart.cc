#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <sstream>
#include <memory>
#include <functional>
#include <algorithm>
#include "localdata.cc"
#include "branch.cc"

using namespace std;

// ============================================================================
// TOKENIZER
// ============================================================================
enum TokenType {
    TOKEN_EOF,
    TOKEN_KEYWORD,      // styp, work, if, when, let, class, func, on, import, export
    TOKEN_IDENTIFIER,   // nomes de variáveis/funções
    TOKEN_STRING,       // "texto"
    TOKEN_NUMBER,       // números
    TOKEN_SYMBOL,       // ( ) { } @ $ : = , | [ ]
    TOKEN_OPERATOR,     // + - * / == != < > <= >=
    TOKEN_DOT,          // .
    TOKEN_COLON,        // :
    TOKEN_SEMICOLON,    // ;
};

struct Token {
    TokenType type;
    string value;
    int line, col;
};

class Tokenizer {
private:
    string source;
    size_t pos;
    int line, col;
    
public:
    Tokenizer(const string& src) : source(src), pos(0), line(1), col(1) {}
    
    vector<Token> tokenize() {
        vector<Token> tokens;
        while (pos < source.length()) {
            skipWhitespace();
            if (pos >= source.length()) break;
            
            char c = source[pos];
            
            if (c == '"') {
                tokens.push_back(readString());
            } else if (isdigit(c)) {
                tokens.push_back(readNumber());
            } else if (isalpha(c) || c == '_') {
                tokens.push_back(readIdentifierOrKeyword());
            } else if (isSymbol(c)) {
                tokens.push_back(readSymbol());
            } else {
                pos++;
                col++;
            }
        }
        tokens.push_back({TOKEN_EOF, "", line, col});
        return tokens;
    }
    
private:
    void skipWhitespace() {
        while (pos < source.length() && isspace(source[pos])) {
            if (source[pos] == '\n') {
                line++;
                col = 1;
            } else {
                col++;
            }
            pos++;
        }
    }
    
    Token readString() {
        int startLine = line, startCol = col;
        pos++; col++;
        string value;
        while (pos < source.length() && source[pos] != '"') {
            if (source[pos] == '\\' && pos + 1 < source.length()) {
                pos++; col++;
                value += source[pos];
            } else {
                value += source[pos];
            }
            pos++; col++;
        }
        if (pos < source.length()) {
            pos++; col++;
        }
        return {TOKEN_STRING, value, startLine, startCol};
    }
    
    Token readNumber() {
        int startLine = line, startCol = col;
        string value;
        while (pos < source.length() && isdigit(source[pos])) {
            value += source[pos];
            pos++; col++;
        }
        return {TOKEN_NUMBER, value, startLine, startCol};
    }
    
    Token readIdentifierOrKeyword() {
        int startLine = line, startCol = col;
        string value;
        while (pos < source.length() && (isalnum(source[pos]) || source[pos] == '_')) {
            value += source[pos];
            pos++; col++;
        }
        
        vector<string> keywords = {"styp", "work", "if", "else", "when", "let", "class", 
                                   "const", "func", "on", "import", "export", "set", "assemble"};
        
        TokenType type = TOKEN_IDENTIFIER;
        for (const auto& kw : keywords) {
            if (value == kw) {
                type = TOKEN_KEYWORD;
                break;
            }
        }
        
        return {type, value, startLine, startCol};
    }
    
    Token readSymbol() {
        int startLine = line, startCol = col;
        char c = source[pos];
        string value(1, c);
        
        pos++; col++;
        
        // Check for two-character operators
        if (pos < source.length()) {
            string two = value + source[pos];
            if (two == "==" || two == "!=" || two == "<=" || two == ">=") {
                pos++; col++;
                return {TOKEN_OPERATOR, two, startLine, startCol};
            }
            if (two == "##") {
                pos++; col++;
                value = two;
            }
        }
        
        if (c == '(' || c == ')' || c == '{' || c == '}' || c == '@' || 
            c == '$' || c == ',' || c == '|' || c == '[' || c == ']') {
            return {TOKEN_SYMBOL, value, startLine, startCol};
        } else if (c == '.') {
            return {TOKEN_DOT, value, startLine, startCol};
        } else if (c == ':') {
            return {TOKEN_COLON, value, startLine, startCol};
        } else if (c == '=') {
            return {TOKEN_OPERATOR, value, startLine, startCol};
        } else if (c == '+' || c == '-' || c == '*' || c == '/') {
            return {TOKEN_OPERATOR, value, startLine, startCol};
        } else if (c == '<' || c == '>') {
            return {TOKEN_OPERATOR, value, startLine, startCol};
        }
        
        return {TOKEN_SYMBOL, value, startLine, startCol};
    }
    
    bool isSymbol(char c) {
        return c == '(' || c == ')' || c == '{' || c == '}' || c == '@' || c == '$' ||
               c == '.' || c == ':' || c == '=' || c == ',' || c == '|' || c == '[' ||
               c == ']' || c == '+' || c == '-' || c == '*' || c == '/' || c == '<' ||
               c == '>' || c == '!';
    }
};

// ============================================================================
// AST NODES
// ============================================================================
struct ASTNode {
    virtual ~ASTNode() = default;
};

struct Program : public ASTNode {
    vector<shared_ptr<ASTNode>> statements;
};

struct CreateStatement : public ASTNode {
    string name;
};

struct VariableDeclaration : public ASTNode {
    string name;
    shared_ptr<ASTNode> value;
};

struct IfStatement : public ASTNode {
    shared_ptr<ASTNode> condition;
    vector<shared_ptr<ASTNode>> thenBranch;
    vector<shared_ptr<ASTNode>> elseBranch;
};

struct FunctionCall : public ASTNode {
    string name;
    vector<shared_ptr<ASTNode>> args;
};

struct Assignment : public ASTNode {
    string target;
    shared_ptr<ASTNode> value;
};

struct EventHandler : public ASTNode {
    string eventType;
    string param;
    vector<shared_ptr<ASTNode>> body;
};

struct ClassDeclaration : public ASTNode {
    string name;
    vector<shared_ptr<ASTNode>> members;
};

struct FunctionDeclaration : public ASTNode {
    string name;
    vector<string> params;
    vector<shared_ptr<ASTNode>> body;
};

struct LiteralValue : public ASTNode {
    string value;
};

struct BinaryOp : public ASTNode {
    string op;  // +, -, *, /, ==, !=, <, >, etc
    shared_ptr<ASTNode> left;
    shared_ptr<ASTNode> right;
};

struct WhileLoop : public ASTNode {
    shared_ptr<ASTNode> condition;
    vector<shared_ptr<ASTNode>> body;
};

struct ForLoop : public ASTNode {
    string variable;
    shared_ptr<ASTNode> start;
    shared_ptr<ASTNode> end;
    vector<shared_ptr<ASTNode>> body;
};

struct ArrayAccess : public ASTNode {
    string arrayName;
    shared_ptr<ASTNode> index;
};

struct WorkStatement : public ASTNode {
    string name;
    vector<shared_ptr<ASTNode>> methods;
};

// ============================================================================
// PARSER
// ============================================================================
class Parser {
private:
    vector<Token> tokens;
    size_t pos;
    
public:
    Parser(const vector<Token>& toks) : tokens(toks), pos(0) {}
    
    shared_ptr<Program> parse() {
        auto program = make_shared<Program>();
        while (!isAtEnd()) {
            auto stmt = parseStatement();
            if (stmt) {
                program->statements.push_back(stmt);
            }
        }
        return program;
    }
    
private:
    shared_ptr<ASTNode> parseStatement() {
        if (check(TOKEN_KEYWORD)) {
            string keyword = current().value;
            
            if (keyword == "styp") {
                advance(); // consume 'styp'
                expect(TOKEN_DOT, ".");
                if (check(TOKEN_IDENTIFIER) && current().value == "create") {
                    advance(); // consume 'create'
                    expect(TOKEN_SYMBOL, "(");
                    string name = expect(TOKEN_STRING, "expected string").value;
                    expect(TOKEN_SYMBOL, ")");
                    auto stmt = make_shared<CreateStatement>();
                    stmt->name = name;
                    return stmt;
                }
            } else if (keyword == "work") {
                advance(); // consume 'work'
                expect(TOKEN_SYMBOL, "(");
                string name = "";
                if (check(TOKEN_STRING)) {
                    name = current().value;
                    advance();
                }
                expect(TOKEN_SYMBOL, ")");
                auto stmt = make_shared<CreateStatement>();
                stmt->name = name;
                return stmt;
            } else if (keyword == "let") {
                advance(); // consume 'let'
                string name = expect(TOKEN_IDENTIFIER, "expected identifier").value;
                expect(TOKEN_OPERATOR, "=");
                auto value = parseExpression();
                auto decl = make_shared<VariableDeclaration>();
                decl->name = name;
                decl->value = value;
                return decl;
            } else if (keyword == "if") {
                advance(); // consume 'if'
                expect(TOKEN_SYMBOL, "(");
                auto condition = parseExpression();
                expect(TOKEN_SYMBOL, ")");
                expect(TOKEN_SYMBOL, "{");
                
                expect(TOKEN_SYMBOL, "(");
                
                vector<string> params;
                while (!check(TOKEN_SYMBOL) || current().value != ")") {
                    params.push_back(expect(TOKEN_IDENTIFIER, "expected parameter").value);
                    if (check(TOKEN_SYMBOL) && current().value == ",") {
                        advance();
                    }
                }
                expect(TOKEN_SYMBOL, ")");
                expect(TOKEN_SYMBOL, "{");
                
                vector<shared_ptr<ASTNode>> body;
                while (!check(TOKEN_SYMBOL) || current().value != "}") {
                    auto stmt = parseStatement();
                    if (stmt) body.push_back(stmt);
                }
                expect(TOKEN_SYMBOL, "}");
                
                auto funcDecl = make_shared<FunctionDeclaration>();
                funcDecl->name = "anonymous";
                funcDecl->params = params;
                funcDecl->body = body;
                return funcDecl;
            } else if (keyword == "when") {
                advance(); // consume 'when'
                expect(TOKEN_SYMBOL, "{");
                vector<shared_ptr<ASTNode>> body;
                while (!check(TOKEN_SYMBOL) || current().value != "}") {
                    auto stmt = parseStatement();
                    if (stmt) body.push_back(stmt);
                }
                expect(TOKEN_SYMBOL, "}");
                // For now, treat when as a regular block
                return nullptrMBOL, "{");
                
                vector<shared_ptr<ASTNode>> body;
                while (!check(TOKEN_SYMBOL) || current().value != "}") {
                    auto stmt = parseStatement();
                    if (stmt) body.push_back(stmt);
                }
                expect(TOKEN_SYMBOL, "}");
                
                auto funcDecl = make_shared<FunctionDeclaration>();
                funcDecl->name = name;
                funcDecl->params = params;
                funcDecl->body = body;
                return funcDecl;
            }
        }
        
        // Try to parse as expression/call
        if (check(TOKEN_IDENTIFIER)) {
            string name = current().value;
            advance();
            
            if (check(TOKEN_SYMBOL) && current().value == "(") {
                advance();
                vector<shared_ptr<ASTNode>> args;
                while (!check(TOKEN_SYMBOL) || current().value != ")") {
                    args.push_back(parseExpression());
                    if (check(TOKEN_SYMBOL) && current().value == ",") {
                        advance();
                    }
                }
                expect(TOKEN_SYMBOL, ")");
                
                auto call = make_shared<FunctionCall>();
                call->name = name;
                call->args = args;
                return call;
            }
        }
        
        return nullptr;
    }
    
    shared_ptr<ASTNode> parseExpression() {
        return parseComparison();
    }
    
    shared_ptr<ASTNode> parseComparison() {
        auto expr = parseAdditive();
        
        while (check(TOKEN_OPERATOR) && (current().value == "==" || current().value == "!=" ||
                                          current().value == "<" || current().value == ">" ||
                                          current().value == "<=" || current().value == ">=")) {
            string op = current().value;
            advance();
            auto right = parseAdditive();
            auto binOp = make_shared<BinaryOp>();
            binOp->op = op;
            binOp->left = expr;
            binOp->right = right;
            expr = binOp;
        }
        
        return expr;
    }
    
    shared_ptr<ASTNode> parseAdditive() {
        auto expr = parseMultiplicative();
        
        while (check(TOKEN_OPERATOR) && (current().value == "+" || current().value == "-")) {
            string op = current().value;
            advance();
            auto right = parseMultiplicative();
            auto binOp = make_shared<BinaryOp>();
            binOp->op = op;
            binOp->left = expr;
            binOp->right = right;
            expr = binOp;
        }
        
        return expr;
    }
    
    shared_ptr<ASTNode> parseMultiplicative() {
        auto expr = parsePrimary();
        
        while (check(TOKEN_OPERATOR) && (current().value == "*" || current().value == "/")) {
            string op = current().value;
            advance();
            auto right = parsePrimary();
            auto binOp = make_shared<BinaryOp>();
            binOp->op = op;
            binOp->left = expr;
            binOp->right = right;
            expr = binOp;
        }
        
        return expr;
    }
    
    shared_ptr<ASTNode> parsePrimary() {
        if (check(TOKEN_STRING)) {
            auto lit = make_shared<LiteralValue>();
            lit->value = current().value;
            advance();
            return lit;
        } else if (check(TOKEN_NUMBER)) {
            auto lit = make_shared<LiteralValue>();
            lit->value = current().value;
            advance();
            return lit;
        } else if (check(TOKEN_IDENTIFIER)) {
            string name = current().value;
            advance();
            
            // Check for array access
            if (check(TOKEN_SYMBOL) && current().value == "[") {
                advance();
                auto index = parseExpression();
                expect(TOKEN_SYMBOL, "]");
                auto arrayAccess = make_shared<ArrayAccess>();
                arrayAccess->arrayName = name;
                arrayAccess->index = index;
                return arrayAccess;
            } else {
                auto lit = make_shared<LiteralValue>();
                lit->value = name;
                return lit;
            }
        } else if (check(TOKEN_SYMBOL) && current().value == "(") {
            advance();
            auto expr = parseExpression();
            expect(TOKEN_SYMBOL, ")");
            return expr;
        }
        return nullptr;
    }
    
    bool check(TokenType type) {
        return !isAtEnd() && current().type == type;
    }
    
    Token advance() {
        if (!isAtEnd()) pos++;
        return tokens[pos - 1];
    }
    
    Token current() {
        return tokens[pos];
    }
    
    bool isAtEnd() {
        return pos >= tokens.size() || current().type == TOKEN_EOF;
    }
    
    Token expect(TokenType type, const string& message) {
        if (!check(type)) {
            cerr << "Parse error: " << message << " at line " << current().line << endl;
        }
        return advance();
    }
};

// ============================================================================
// INTERPRETER/EXECUTOR
// ============================================================================
class StypuffEngine {
public:
    LocalData data;
    map<string, shared_ptr<FunctionDeclaration>> functions;
    
    void execute(const string& source) {
        Tokenizer tokenizer(source);
        auto tokens = tokenizer.tokenize();
        
        Parser parser(tokens);
        auto program = parser.parse();
        
        for (auto& stmt : program->statements) {
            executeStatement(stmt);
        }
    }
    
    void executeStatement(shared_ptr<ASTNode> stmt) {
        if (auto create = dynamic_pointer_cast<CreateStatement>(stmt)) {
            cout << "[Stypuff] Criando objeto: " << create->name << endl;
            data.setVariable(create->name, create->name);
        }
        else if (auto var = dynamic_pointer_cast<VariableDeclaration>(stmt)) {
            auto value = evaluateExpression(var->value);
            data.setVariable(var->name, value);
            cout << "[Stypuff] Variável '" << var->name << "' = " << value << endl;
        }
        else if (auto ifStmt = dynamic_pointer_cast<IfStatement>(stmt)) {
            auto condValue = evaluateExpression(ifStmt->condition);
            if (condValue == "true" || condValue == "1" || condValue == "sim") {
                for (auto& stmt : ifStmt->thenBranch) {
                    executeStatement(stmt);
                }
            } else if (!ifStmt->elseBranch.empty()) {
                for (auto& stmt : ifStmt->elseBranch) {
                    executeStatement(stmt);
                }
            }
        }
        else if (auto call = dynamic_pointer_cast<FunctionCall>(stmt)) {
            cout << "[Stypuff] Chamando função: " << call->name << endl;
            if (call->name == "print" || call->name == "print_ln") {
                for (auto& arg : call->args) {
                    cout << evaluateExpression(arg) << " ";
                }
                if (call->name == "print_ln") cout << endl;
            }
        }
        else if (auto funcDecl = dynamic_pointer_cast<FunctionDeclaration>(stmt)) {
            functions[funcDecl->name] = funcDecl;
            cout << "[Stypuff] Função declarada" << endl;
        }
    }
    
    string evaluateExpression(shared_ptr<ASTNode> expr) {
        if (!expr) return "";
        
        if (auto lit = dynamic_pointer_cast<LiteralValue>(expr)) {
            // Try to get variable value
            if (data.hasVariable(lit->value)) {
                return data.getVariable(lit->value);
            }
            return lit->value;
        }
        else if (auto binOp = dynamic_pointer_cast<BinaryOp>(expr)) {
            return evaluateBinaryOp(binOp);
        }
        else if (auto arrayAccess = dynamic_pointer_cast<ArrayAccess>(expr)) {
            auto indexStr = evaluateExpression(arrayAccess->index);
            try {
                int index = stoi(indexStr);
                return data.getArrayElement(arrayAccess->arrayName, index);
            } catch (...) {
                return "";
            }
        }
        
        return "";
    }
    
    string evaluateBinaryOp(shared_ptr<BinaryOp> op) {
        string left = evaluateExpression(op->left);
        string right = evaluateExpression(op->right);
        
        // Operações aritméticas
        try {
            double lVal = stod(left);
            double rVal = stod(right);
            
            if (op->op == "+") return to_string((int)(lVal + rVal));
            if (op->op == "-") return to_string((int)(lVal - rVal));
            if (op->op == "*") return to_string((int)(lVal * rVal));
            if (op->op == "/") {
                if (rVal == 0) return "ERROR: Division by zero";
                return to_string((int)(lVal / rVal));
            }
        } catch (...) {}
        
        // Comparações
        if (op->op == "==") return (left == right) ? "true" : "false";
        if (op->op == "!=") return (left != right) ? "true" : "false";
        
        try {
            int lVal = stoi(left);
            int rVal = stoi(right);
            if (op->op == "<") return (lVal < rVal) ? "true" : "false";
            if (op->op == ">") return (lVal > rVal) ? "true" : "false";
            if (op->op == "<=") return (lVal <= rVal) ? "true" : "false";
            if (op->op == ">=") return (lVal >= rVal) ? "true" : "false";
        } catch (...) {}
        
        // Concatenação de strings
        if (op->op == "+") return left + right;
        
        return "";
    }
};

// ============================================================================
// MAIN
// ============================================================================
int main() {
    StypuffEngine engine;
    
    string code = R"(
        styp.create("myApp")
        let greeting = "Hello Stypuff"
        func sayHello() {
            let message = "Olá mundo"
        }
    )";
    
    cout << "=== Stypuff Interpreter ===" << endl;
    engine.execute(code);
    
    return 0;
}
