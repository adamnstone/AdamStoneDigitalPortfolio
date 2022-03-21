#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <stdlib.h>
#include "Transpiler.h"
using namespace std;

string changeExtension(string str, string extension) {
    for (int i = str.length() - 1; i >= 0; --i) {
        if (str[i] == '.') {
            return str.substr(0, i) + extension;
        }
    }
    return str + extension;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        cout << "Error: Please provide input and output files" << endl;
        return 0;
    }
    vector<srting> inputFiles;
    for (int i = 1; i < argc - 1; ++i) {
        inputFiles.push_back(argv[i]);
    }
    string outputFile = argv[argc - 1];
    vector<string> toConvert = {"\🧵", "\👀", "\🔤", "\👉", "\👈", "\⏩", "\🤞", " ", "\n", "\🔧", "\⚙", "\🏁", "\🛑", "\🚪", "\🙅", "\🚫", "\⭕", "\💬", "\➖", "\🔴", "\➕", "\✖️", "\➗", "\🤙", "\🤘", "\👍\👎", "\👄", "\🤜", "\👇", "\😀", "\💯", "\🚦", "\🔁", "\🔃", "\🤷", "\🧺"};
    vector<string> converted = {"string", "#include", "char", ">", "<", "->", ",", " ", "\n", "(", ")", "{", "}", "[", "]", "!", ".", "\"", "-", ";", "+", "*", "/", "&", "=", "bool", "'", ":", "using", "namespace", "%", "do", "for", "while", "try", "catch"};
    Transpiler transpiler(toConvert, converted, true, "", false, false);
    
    for (int i = 0; i < inputFiles.size(); ++i) {
        system("mv " + inputFiles[i] + " " + changeExtension(inputFiles[i], "txt"));
    }
}