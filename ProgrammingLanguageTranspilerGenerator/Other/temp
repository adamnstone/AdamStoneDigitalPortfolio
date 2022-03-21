#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <stdio.h>
#include "Transpiler.h"
using namespace std;

Transpiler::Transpiler(vector<string> toConvert, vector<string> converted, bool ignoreUnrecognizedStatements, string joinStatements, bool ignoreInDoubleQuotes, bool ignoreInSingleQuotes) {
    if (toConvert.size() != converted.size()) {
        cout << "Error: vector<string> 'toConvert' and vector<string> 'converted' not the same length" << endl;
        throw exception();
    }
    ignoreUnrecognized = ignoreUnrecognizedStatements;
    joinStatements = joinStatements;
    ignoreDoubleQuotes = ignoreInDoubleQuotes;
    ignoreSingleQuotes = ignoreInSingleQuotes;
    setToConvert(toConvert);
    setConverted(converted);
};

void Transpiler::setToConvert(vector<string> items) {
    toConvert = items;
};

void Transpiler::setConverted(vector<string> items) {
    converted = items;
};

string Transpiler::join(vector<string> arr, string joiner) {
    string fin = "";
    for (int i = 0; i < arr.size(); ++i) {
        fin += arr[i];
        if (i != arr.size() - 1) {
            fin += joiner;
        }
    }
    return fin;
}

string Transpiler::transpileTo(string input) {
    vector<string> output;
    bool inDoubleQuotes = false;
    bool inSingleQuotes = false;
    for (int i = 0; i < input.length(); ++i) {
        bool found = false;
        bool prevIsSlash = false;
        if (i != 0) {
            prevIsSlash = input[i-1] == '\\';
        }
        if (!prevIsSlash) {
            if (input[i] == '"' && ignoreDoubleQuotes && !inSingleQuotes) {
                inDoubleQuotes = !inDoubleQuotes;
                for (int j = 0; j < toConvert.size(); ++j) {
                    if (toConvert[j] == "\"") {
                        output.push_back(converted[j]);
                    }
                }
            }
            if (input[i] == '\'' && ignoreSingleQuotes && !inDoubleQuotes) {
                inSingleQuotes = !inSingleQuotes;
                for (int j = 0; j < toConvert.size(); ++j) {
                    if (toConvert[j] == "'") {
                        output.push_back(converted[j]);
                    }
                }
            }
        }
        if (!inDoubleQuotes && !inSingleQuotes) {
            int longestIndex = -1;
            int longestLength = 0;
            for (int j = 0; j < toConvert.size(); ++j) {
                if (toConvert[j] == input.substr(i, toConvert[j].length())) {
                    if (toConvert[j].length() > longestLength) {
                        longestLength = toConvert[j].length();
                        longestIndex = j;
                    }
                }
            }
            if (longestIndex != -1) {
                output.push_back(converted[longestIndex]);
                found = true;
                i += toConvert[longestIndex].length()-1;
            }
        }
        else {
            output.push_back(string(1, input[i]));
        }
        if (!inDoubleQuotes && !inSingleQuotes) {
            if (!found && !ignoreUnrecognized) {
                cout << ignoreUnrecognized << endl;
                string error = "Error: Statement Not Found at Index ";
                error += to_string(i);
                throw exception();
            }
            else if (!found) {
                output.push_back(string(1, input[i]));
            }
        }
    }
    return join(output, joinStatements);
}

string Transpiler::transpileFrom(string input) {
    vector<string> output;
    bool inDoubleQuotes = false;
    bool inSingleQuotes = false;
    for (int i = 0; i < input.length(); ++i) {
        bool found = false;
        bool prevIsSlash = false;
        if (i != 0) {
            prevIsSlash = input[i-1] == '\\';
        }
        if (!prevIsSlash) {
            if (input[i] == '"' && ignoreDoubleQuotes && !inSingleQuotes) {
                inDoubleQuotes = !inDoubleQuotes;
                for (int j = 0; j < converted.size(); ++j) {
                    if (converted[j] == "\"") {
                        output.push_back(toConvert[j]);
                    }
                }
            }
            if (input[i] == '\'' && ignoreSingleQuotes && !inDoubleQuotes) {
                inSingleQuotes = !inSingleQuotes;
                for (int j = 0; j < converted.size(); ++j) {
                    if (converted[j] == "'") {
                        output.push_back(toConvert[j]);
                    }
                }
            }
        }
        if (!inDoubleQuotes && !inSingleQuotes) {
            int longestIndex = -1;
            int longestLength = 0;
            for (int j = 0; j < converted.size(); ++j) {
                if (converted[j] == input.substr(i, converted[j].length())) {
                    if (converted[j].length() > longestLength) {
                        longestLength = converted[j].length();
                        longestIndex = j;
                    }
                }
            }
            if (longestIndex != -1) {
                output.push_back(toConvert[longestIndex]);
                found = true;
                i += converted[longestIndex].length()-1;
            }
        }
        else {
            output.push_back(string(1, input[i]));
        }
        if (!inDoubleQuotes && !inSingleQuotes) {
            if (!found && !ignoreUnrecognized) {
                cout << ignoreUnrecognized << endl;
                string error = "Error: Statement Not Found at Index ";
                error += to_string(i);
                throw exception();
            }
            else if (!found) {
                output.push_back(string(1, input[i]));
            }
        }
    }
    return join(output, joinStatements);
}

string Transpiler::transpileToFromFile(string inputFile) {
    string line;
    string allContent = "";
    ifstream file (inputFile);
    if (!file.is_open()) {
        cout << "Unable to open file" << endl;
        throw exception();
    }
    while (getline(file, line)) {
        allContent += line + '\n';
    }
    file.close();
    allContent.erase(prev(allContent.end()));

    return transpileTo(allContent);
};

string Transpiler::transpileFromFromFile(string inputFile) {
    string line;
    string allContent = "";
    ifstream file (inputFile);
    if (!file.is_open()) {
        cout << "Unable to open file" << endl;
        throw exception();
    }
    while (getline(file, line)) {
        allContent += line + '\n';
    }
    file.close();
    allContent.erase(prev(allContent.end()));

    return transpileFrom(allContent);
};