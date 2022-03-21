#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <stdio.h>
using namespace std;

class Transpiler {
    vector<string> toConvert;
    vector<string> converted;
    bool ignoreUnrecognized;
    string joinStatements;
    bool ignoreDoubleQuotes;
    bool ignoreSingleQuotes;
    void setToConvert(vector<string>);
    void setConverted(vector<string>);
    string join(vector<string>, string);
public:
    Transpiler(vector<string>, vector<string>, bool, string, bool, bool);
    string transpileTo(string);
    string transpileFrom(string);
    string transpileToFromFile(string);
    string transpileFromFromFile(string);
};