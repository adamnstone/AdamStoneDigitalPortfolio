#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdlib.h>
using namespace std;

const string transpilerCppText = "#include <iostream>\n#include <fstream>\n#include <string>\n#include <vector>\n#include <map>\n#include <stdio.h>\n#include \"Transpiler.h\"\nusing namespace std;\n\nTranspiler::Transpiler(vector<string> toConvert, vector<string> converted, bool ignoreUnrecognizedStatements, string joinStatements, bool ignoreInDoubleQuotes, bool ignoreInSingleQuotes) {\n    if (toConvert.size() != converted.size()) {\n        cout << \"Error: vector<string> 'toConvert' and vector<string> 'converted' not the same length\" << endl;\n        throw exception();\n    }\n    ignoreUnrecognized = ignoreUnrecognizedStatements;\n    joinStatements = joinStatements;\n    ignoreDoubleQuotes = ignoreInDoubleQuotes;\n    ignoreSingleQuotes = ignoreInSingleQuotes;\n    setToConvert(toConvert);\n    setConverted(converted);\n};\n\nvoid Transpiler::setToConvert(vector<string> items) {\n    toConvert = items;\n};\n\nvoid Transpiler::setConverted(vector<string> items) {\n    converted = items;\n};\n\nstring Transpiler::join(vector<string> arr, string joiner) {\n    string fin = \"\";\n    for (int i = 0; i < arr.size(); ++i) {\n        fin += arr[i];\n        if (i != arr.size() - 1) {\n            fin += joiner;\n        }\n    }\n    return fin;\n}\n\nstring Transpiler::transpileTo(string input) {\n    vector<string> output;\n    bool inDoubleQuotes = false;\n    bool inSingleQuotes = false;\n    for (int i = 0; i < input.length(); ++i) {\n        bool found = false;\n        bool prevIsSlash = false;\n        if (i != 0) {\n            prevIsSlash = input[i-1] == '\\\\';\n        }\n        if (!prevIsSlash) {\n            if (input[i] == '\"' && ignoreDoubleQuotes && !inSingleQuotes) {\n                inDoubleQuotes = !inDoubleQuotes;\n                for (int j = 0; j < toConvert.size(); ++j) {\n                    if (toConvert[j] == \"\\\"\") {\n                        output.push_back(converted[j]);\n                    }\n                }\n            }\n            if (input[i] == '\\'' && ignoreSingleQuotes && !inDoubleQuotes) {\n                inSingleQuotes = !inSingleQuotes;\n                for (int j = 0; j < toConvert.size(); ++j) {\n                    if (toConvert[j] == \"'\") {\n                        output.push_back(converted[j]);\n                    }\n                }\n            }\n        }\n        if (!inDoubleQuotes && !inSingleQuotes) {\n            int longestIndex = -1;\n            int longestLength = 0;\n            for (int j = 0; j < toConvert.size(); ++j) {\n                if (toConvert[j] == input.substr(i, toConvert[j].length())) {\n                    if (toConvert[j].length() > longestLength) {\n                        longestLength = toConvert[j].length();\n                        longestIndex = j;\n                    }\n                }\n            }\n            if (longestIndex != -1) {\n                output.push_back(converted[longestIndex]);\n                found = true;\n                i += toConvert[longestIndex].length()-1;\n            }\n        }\n        else {\n            output.push_back(string(1, input[i]));\n        }\n        if (!inDoubleQuotes && !inSingleQuotes) {\n            if (!found && !ignoreUnrecognized) {\n                cout << ignoreUnrecognized << endl;\n                string error = \"Error: Statement Not Found at Index \";\n                error += to_string(i);\n                throw exception();\n            }\n            else if (!found) {\n                output.push_back(string(1, input[i]));\n            }\n        }\n    }\n    return join(output, joinStatements);\n}\n\nstring Transpiler::transpileFrom(string input) {\n    vector<string> output;\n    bool inDoubleQuotes = false;\n    bool inSingleQuotes = false;\n    for (int i = 0; i < input.length(); ++i) {\n        bool found = false;\n        bool prevIsSlash = false;\n        if (i != 0) {\n            prevIsSlash = input[i-1] == '\\\\';\n        }\n        if (!prevIsSlash) {\n            if (input[i] == '\"' && ignoreDoubleQuotes && !inSingleQuotes) {\n                inDoubleQuotes = !inDoubleQuotes;\n                for (int j = 0; j < converted.size(); ++j) {\n                    if (converted[j] == \"\\\"\") {\n                        output.push_back(toConvert[j]);\n                    }\n                }\n            }\n            if (input[i] == '\\'' && ignoreSingleQuotes && !inDoubleQuotes) {\n                inSingleQuotes = !inSingleQuotes;\n                for (int j = 0; j < converted.size(); ++j) {\n                    if (converted[j] == \"'\") {\n                        output.push_back(toConvert[j]);\n                    }\n                }\n            }\n        }\n        if (!inDoubleQuotes && !inSingleQuotes) {\n            int longestIndex = -1;\n            int longestLength = 0;\n            for (int j = 0; j < converted.size(); ++j) {\n                if (converted[j] == input.substr(i, converted[j].length())) {\n                    if (converted[j].length() > longestLength) {\n                        longestLength = converted[j].length();\n                        longestIndex = j;\n                    }\n                }\n            }\n            if (longestIndex != -1) {\n                output.push_back(toConvert[longestIndex]);\n                found = true;\n                i += converted[longestIndex].length()-1;\n            }\n        }\n        else {\n            output.push_back(string(1, input[i]));\n        }\n        if (!inDoubleQuotes && !inSingleQuotes) {\n            if (!found && !ignoreUnrecognized) {\n                cout << ignoreUnrecognized << endl;\n                string error = \"Error: Statement Not Found at Index \";\n                error += to_string(i);\n                throw exception();\n            }\n            else if (!found) {\n                output.push_back(string(1, input[i]));\n            }\n        }\n    }\n    return join(output, joinStatements);\n}\n\nstring Transpiler::transpileToFromFile(string inputFile) {\n    string line;\n    string allContent = \"\";\n    ifstream file (inputFile);\n    if (!file.is_open()) {\n        cout << \"Unable to open file\" << endl;\n        throw exception();\n    }\n    while (getline(file, line)) {\n        allContent += line + '\\n';\n    }\n    file.close();\n    allContent.erase(prev(allContent.end()));\n\n    return transpileTo(allContent);\n};\n\nstring Transpiler::transpileFromFromFile(string inputFile) {\n    string line;\n    string allContent = \"\";\n    ifstream file (inputFile);\n    if (!file.is_open()) {\n        cout << \"Unable to open file\" << endl;\n        throw exception();\n    }\n    while (getline(file, line)) {\n        allContent += line + '\\n';\n    }\n    file.close();\n    allContent.erase(prev(allContent.end()));\n\n    return transpileFrom(allContent);\n};";
const string transpilerHeaderText = "#include <iostream>\n#include <fstream>\n#include <string>\n#include <vector>\n#include <map>\n#include <stdio.h>\nusing namespace std;\n\nclass Transpiler {\n    vector<string> toConvert;\n    vector<string> converted;\n    bool ignoreUnrecognized;\n    string joinStatements;\n    bool ignoreDoubleQuotes;\n    bool ignoreSingleQuotes;\n    void setToConvert(vector<string>);\n    void setConverted(vector<string>);\n    string join(vector<string>, string);\npublic:\n    Transpiler(vector<string>, vector<string>, bool, string, bool, bool);\n    string transpileTo(string);\n    string transpileFrom(string);\n    string transpileToFromFile(string);\n    string transpileFromFromFile(string);\n};";

bool fileExists(const char *fileName)
{
    ifstream infile(fileName);
    return infile.good();
}

string getTemporaryFile() {
    string name = "a";
    while (fileExists(&(name + ".cpp")[0])) {
        name += "a";
    }
    return name + ".cpp";
}

vector<string> getStatements(string str) {
    vector<string> statements;
    string current = "";
    bool isInQuotes = false;
    for (int i = 0; i < str.length(); ++i) {
        bool prevIsSlash = false;
        if (i != 0) {
            prevIsSlash = str[i - 1] == '\\';
        }
        if (str[i] == '"' && !prevIsSlash) {
            isInQuotes = !isInQuotes;
            i += 1;
            if (!isInQuotes) {
                statements.push_back(current);
                current = "";
            }
        }
        if (isInQuotes) {
            current += string(1, str[i]);
        }
    }
    return statements;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Error: Please Provide a .tdsn File" << endl;
        throw exception();
    }
    bool noDelete = false;
    if (argc >= 3) {
        if (string(argv[2]) == "--nodelete") {
            noDelete = true;
        }
    }
    string designFile = argv[1];

    string line;
    vector<string> lines;
    ifstream file (designFile);
    string title;
    bool createdTitle = false;
    if (!file.is_open()) {
        cout << "Unable to open file" << endl;
        throw exception();
    }
    while (getline(file, line)) {
        if (!createdTitle) {
            title = line;
            createdTitle = true;
        }
        else {
            lines.push_back(line);
        }
    }
    file.close();

    cout << "Creating \"" << title << "\"" << endl << endl;

    string before;
    string after;
    bool useSingleQuotes = false;
    bool useDoubleQuotes = false;
    bool hasRunCommand = false;
    string runCommand;
    string setupCode = "";
    string cleanupCode = "";
    bool ignoreUnrecognized = true;
    for (int i = 0; i < lines.size(); ++i) {
        for (int j = 0; j < lines[i].length(); ++j) {
            if (lines[i].substr(j, 6) == "BEFORE") {
                before = lines[i].substr(j+6, lines[i].length()-(j+6));
                break;
            }
            else if (lines[i].substr(j, 5) == "AFTER") {
                after = lines[i].substr(j+5, lines[i].length()-(j+5));
                break;
            }
            else if (lines[i].substr(j, 17) == "USE SINGLE QUOTES") {
                string sub = lines[i].substr(j+17, lines[i].length()-(j+17));
                useSingleQuotes = sub.find("YES") != string::npos;
                break;
            }
            else if (lines[i].substr(j, 17) == "USE DOUBLE QUOTES") {
                string sub = lines[i].substr(j+17, lines[i].length()-(j+17));
                useDoubleQuotes = sub.find("YES") != string::npos;
                break;
            }
            else if (lines[i].substr(j, 31) == "IGNORE UNRECOGNIZED STATEMENTS") {
                string sub = lines[i].substr(j+31, lines[i].length()-(j+31));
                ignoreUnrecognized = sub.find("YES") != string::npos;
                break;
            }
            else if (lines[i].substr(j, 11) == "RUN COMMAND") {
                string sub = lines[i].substr(j+11, lines[i].length()-(j+11));
                for (int k = 0; k < sub.length(); ++k) {
                    if (sub[k] == '"') {
                        for (int l = k + 1; l < sub.length(); ++l) {
                            if (sub[l-1] != '\\' && sub[l] == '"') {
                                hasRunCommand = true;
                                runCommand = sub.substr(k + 1, l-(k+1));
                                break;
                            }
                        }
                    }
                }
                break;
            }
            else if (lines[i].substr(j, 10) == "SETUP CODE") {
                string sub = lines[i].substr(j+10, lines[i].length()-(j+10));
                for (int k = 0; k < sub.length(); ++k) {
                    if (sub[k] == '"') {
                        for (int l = k + 1; l < sub.length(); ++l) {
                            if (sub[l-1] != '\\' && sub[l] == '"') {
                                setupCode = sub.substr(k + 1, l-(k+1));
                                break;
                            }
                        }
                    }
                }
                break;
            }
            else if (lines[i].substr(j, 12) == "CLEANUP CODE") {
                string sub = lines[i].substr(j+12, lines[i].length()-(j+12));
                for (int k = 0; k < sub.length(); ++k) {
                    if (sub[k] == '"') {
                        for (int l = k + 1; l < sub.length(); ++l) {
                            if (sub[l-1] != '\\' && sub[l] == '"') {
                                cleanupCode = sub.substr(k + 1, l-(k+1));
                                break;
                            }
                        }
                    }
                }
                break;
            }
        }
    }

    vector<string> beforeStatements = getStatements(before);
    vector<string> afterStatements = getStatements(after);

    if (beforeStatements.size() != afterStatements.size()) {
        cout << "Error: BEFORE and AFTER not the Same Length" << endl;
        throw exception();
    }

    for (int i = 0; i < beforeStatements.size(); ++i) {
        cout << "BEFORE: " << beforeStatements[i] << endl;
    }


    for (int i = 0; i < afterStatements.size(); ++i) {
        cout << "AFTER: " << afterStatements[i] << endl;
    }

    cout << "Using Double Quotes: " << useDoubleQuotes << endl;
    cout << "Using Single Quotes: " << useSingleQuotes << endl;
    cout << "Ignore Unrecognized Statements: " << ignoreUnrecognized << endl;

    if (hasRunCommand) {
        cout << "Run Command: " << runCommand << endl;
    }

    cout << "Setup Code: " << setupCode << endl;
    cout << "Cleanup Code: " << cleanupCode << endl;

    string outputText = "#include <stdlib.h>\n#include <iostream>\n#include <string>\n#include <vector>\n#include \"Transpiler.h\"\nusing namespace std;\nint main(int argc, char** argv){if (argc < 4) {cout << \"Must Include to/from and a input and output file\" << endl; throw exception();}";
    outputText += "vector<string> t = {";
    for (int i = 0; i < beforeStatements.size(); ++i) {
        outputText += "\"" + beforeStatements[i] + "\"";
        if (i != beforeStatements.size() - 1) {
            outputText += ",";
        }
    }
    outputText += "};";
    outputText += "vector<string> c = {";
    for (int i = 0; i < afterStatements.size(); ++i) {
        outputText += "\"" + afterStatements[i] + "\"";
        if (i != afterStatements.size() - 1) {
            outputText += ",";
        }
    }
    outputText += "};";
    outputText += "Transpiler transpiler(t, c, ";
    if (ignoreUnrecognized) {
        outputText += "true";
    }
    else {
        outputText += "false";
    }
    outputText += ", \"\", ";
    if (useDoubleQuotes) {
        outputText += "true,";
    }
    else {
        outputText += "false,";
    }
    if (useSingleQuotes) {
        outputText += "true";
    }
    else {
        outputText += "false";
    }
    outputText += "); string final;";
    outputText += "if (string(argv[1]).substr(0,2) == \"to\") {final = transpiler.transpileToFromFile(argv[2]);}";
    outputText += "else if (string(argv[1]).substr(0,4) == \"from\") {final = transpiler.transpileFromFromFile(argv[2]);}";
    outputText += "string setupCode = \"\";";
    outputText += "if (string(argv[1]).substr(0, 2) == \"to\") {";
    outputText += "setupCode = \"";
    outputText += setupCode;
    outputText += "\";";
    outputText += "}";
    outputText += "string cleanupCode = \"\";";
    outputText += "if (string(argv[1]).substr(0, 2) == \"to\") {";
    outputText += "cleanupCode = \"";
    outputText += cleanupCode;
    outputText += "\";";
    outputText += "}";
    outputText += "ofstream myfile;myfile.open(argv[3]);myfile<<setupCode;myfile<<final;myfile<<cleanupCode;myfile.close();string finalFile = argv[3];";
    outputText += "if (string(argv[1]).substr(0,2) == \"to\") {";
    if (hasRunCommand) {
        string finalRunCommand = "";
        for (int i = 0; i < runCommand.length(); ++i) {
            if (runCommand.substr(i, 4) == "FILE") {
                finalRunCommand += "\"+finalFile+\"";
                i += 3;
                continue;
            }
            else {
                finalRunCommand += string(1, runCommand[i]);
            }
        }
        int prev = 0;
        for (int i = 0; i <= finalRunCommand.length(); ++i) {
            if (finalRunCommand[i] == ';' || i == finalRunCommand.length()) {
                string com = finalRunCommand.substr(prev, i-prev);
                outputText += "string com";
                outputText += to_string(i);
                outputText += " = \"" + com + "\";";
                outputText += "system(&";
                outputText += "com";
                outputText += to_string(i);
                outputText += "[0]);";
                prev = i + 1;
                i++;
            }
        }
        
    }
    outputText += "}";
    outputText += "return 0;}";
    ofstream myfile;
    string f = getTemporaryFile();
    myfile.open(f);
    myfile << outputText;
    myfile.close();
    myfile.open("Transpiler.cpp");
    myfile << transpilerCppText;
    myfile.close();
    myfile.open("Transpiler.h");
    myfile << transpilerHeaderText;
    myfile.close();
    string command = "g++ " + f + " Transpiler.cpp -o \"" + title + "\"";
    system(&command[0]);
    if (!noDelete) {
        remove(&f[0]);
        remove("Transpiler.cpp");
        remove("Transpiler.h");
    }
    return 0;
}