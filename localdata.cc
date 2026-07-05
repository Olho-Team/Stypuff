#pragma once

#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <memory>

using namespace std;

// ============================================================================
// LOCAL DATA MANAGER
// ============================================================================
// Gerencia variáveis, dados e estado local do Stypuff

class LocalData {
private:
    map<string, string> variables;          // Armazenar variáveis simples
    map<string, map<string, string>> objects; // Armazenar objetos/dados complexos
    map<string, vector<string>> arrays;     // Armazenar arrays
    
public:
    // ========== Variáveis ==========
    void setVariable(const string& name, const string& value) {
        variables[name] = value;
    }
    
    string getVariable(const string& name) {
        if (variables.find(name) != variables.end()) {
            return variables[name];
        }
        return "";
    }
    
    bool hasVariable(const string& name) {
        return variables.find(name) != variables.end();
    }
    
    void deleteVariable(const string& name) {
        variables.erase(name);
    }
    
    // ========== Dados (Objetos) ==========
    void createData(const string& name) {
        objects[name] = map<string, string>();
    }
    
    void setDataField(const string& objectName, const string& fieldName, const string& value) {
        if (objects.find(objectName) == objects.end()) {
            objects[objectName] = map<string, string>();
        }
        objects[objectName][fieldName] = value;
    }
    
    string getDataField(const string& objectName, const string& fieldName) {
        if (objects.find(objectName) != objects.end()) {
            auto& obj = objects[objectName];
            if (obj.find(fieldName) != obj.end()) {
                return obj[fieldName];
            }
        }
        return "";
    }
    
    bool hasDataField(const string& objectName, const string& fieldName) {
        if (objects.find(objectName) != objects.end()) {
            return objects[objectName].find(fieldName) != objects[objectName].end();
        }
        return false;
    }
    
    // ========== Arrays ==========
    void createArray(const string& name) {
        arrays[name] = vector<string>();
    }
    
    void pushToArray(const string& name, const string& value) {
        if (arrays.find(name) == arrays.end()) {
            arrays[name] = vector<string>();
        }
        arrays[name].push_back(value);
    }
    
    string getArrayElement(const string& name, int index) {
        if (arrays.find(name) != arrays.end()) {
            auto& arr = arrays[name];
            if (index >= 0 && index < (int)arr.size()) {
                return arr[index];
            }
        }
        return "";
    }
    
    int getArraySize(const string& name) {
        if (arrays.find(name) != arrays.end()) {
            return arrays[name].size();
        }
        return 0;
    }
    
    void setArrayElement(const string& name, int index, const string& value) {
        if (arrays.find(name) != arrays.end()) {
            auto& arr = arrays[name];
            if (index >= 0 && index < (int)arr.size()) {
                arr[index] = value;
            }
        }
    }
    
    // ========== Limpeza ==========
    void clear() {
        variables.clear();
        objects.clear();
        arrays.clear();
    }
    
    void printVariables() {
        cout << "\n=== Variáveis ===" << endl;
        for (const auto& var : variables) {
            cout << var.first << " = " << var.second << endl;
        }
    }
    
    void printObjects() {
        cout << "\n=== Objetos/Dados ===" << endl;
        for (const auto& obj : objects) {
            cout << obj.first << " { ";
            for (const auto& field : obj.second) {
                cout << field.first << ": " << field.second << ", ";
            }
            cout << "}" << endl;
        }
    }
    
    void printArrays() {
        cout << "\n=== Arrays ===" << endl;
        for (const auto& arr : arrays) {
            cout << arr.first << " = [ ";
            for (const auto& elem : arr.second) {
                cout << elem << ", ";
            }
            cout << "]" << endl;
        }
    }
};
