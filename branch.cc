#pragma once

#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <functional>

using namespace std;

// ============================================================================
// FLOW CONTROL (Branches)
// ============================================================================
// Controla fluxo: if/else, when, loops, event handlers

class FlowControl {
public:
    
    // ========== Condições ==========
    static bool evaluateCondition(const string& left, const string& op, const string& right) {
        // Converter para números se possível
        try {
            int lValue = stoi(left);
            int rValue = stoi(right);
            
            if (op == "==") return lValue == rValue;
            if (op == "!=") return lValue != rValue;
            if (op == "<")  return lValue < rValue;
            if (op == ">")  return lValue > rValue;
            if (op == "<=") return lValue <= rValue;
            if (op == ">=") return lValue >= rValue;
        } catch (...) {
            // Comparação de strings
            if (op == "==") return left == right;
            if (op == "!=") return left != right;
        }
        return false;
    }
    
    // ========== Verificadores de Evento ==========
    static bool isMouseKeyPressed(const string& key) {
        // Simulação de verificação de eventos
        // Em uma implementação real, isso verificaria estado de entrada
        return false;
    }
    
    static bool isKeyPressed(const string& key) {
        // Simulação de verificação de teclado
        return false;
    }
    
    // ========== Gerenciador de Eventos ==========
    struct Event {
        string type;        // "mousekeypressed", "keypressed", "onclick", etc
        string parameter;   // qual botão, qual tecla, etc
        string target;      // alvo do evento
    };
    
    struct EventListener {
        string eventType;
        string param;
        string callbackFunction;
    };
    
private:
    static vector<EventListener> listeners;
    
public:
    static void addEventListener(const string& eventType, const string& param, const string& callback) {
        listeners.push_back({eventType, param, callback});
    }
    
    static void removeEventListener(const string& eventType, const string& param) {
        listeners.erase(
            remove_if(listeners.begin(), listeners.end(),
                     [&](const EventListener& l) { 
                         return l.eventType == eventType && l.param == param; 
                     }),
            listeners.end()
        );
    }
    
    static vector<EventListener> getListeners(const string& eventType) {
        vector<EventListener> result;
        for (const auto& listener : listeners) {
            if (listener.eventType == eventType) {
                result.push_back(listener);
            }
        }
        return result;
    }
    
    // ========== Execução Condicional ==========
    static void executeIfStatement(bool condition, vector<function<void()>>& thenBranch,
                                   vector<function<void()>>& elseBranch) {
        if (condition) {
            for (auto& stmt : thenBranch) {
                stmt();
            }
        } else {
            for (auto& stmt : elseBranch) {
                stmt();
            }
        }
    }
    
    // ========== When (Switch/Case) ==========
    struct WhenCase {
        string value;
        vector<function<void()>> body;
    };
    
    static void executeWhenStatement(const string& value, const vector<WhenCase>& cases,
                                     const vector<function<void()>>& defaultCase) {
        for (const auto& caseItem : cases) {
            if (caseItem.value == value) {
                for (const auto& stmt : caseItem.body) {
                    stmt();
                }
                return;
            }
        }
        // Execute default
        for (const auto& stmt : defaultCase) {
            stmt();
        }
    }
    
    // ========== Loop Detection ==========
    static bool isEventLoop(const string& eventType) {
        return eventType == "on";
    }
    
    static vector<string> parseEventCondition(const string& eventStr) {
        // Parse: "if(event == $mousekeypressed("click"))"
        vector<string> parts;
        // TODO: Implementar parsing
        return parts;
    }
};

// Definição estática do vetor de listeners
vector<FlowControl::EventListener> FlowControl::listeners;
