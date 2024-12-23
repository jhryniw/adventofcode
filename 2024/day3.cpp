#include <fstream>
#include <iostream>
#include <regex>
#include <sstream>

namespace {

std::string ParseProgram(std::ifstream& infile) {
    std::ostringstream ss;

    // Note: eliminates newlines, but this doesn't matter
    while (!infile.eof()) {
        std::string line;
        infile >> line;
        ss << line << '\n';
    }

    return ss.str();
}

} // namespace

void part1(std::ifstream& infile) {
    std::string program = ParseProgram(infile);
    std::cout << program << std::endl;

    std::regex mulMatcher("mul\\((\\d+),(\\d+)\\)");
    std::smatch sm;

    int total = 0;

    while(true) {
        std::regex_search(program, sm, mulMatcher);
        if (sm.empty()) {
            break;
        }

        int left = std::stoi(sm[1]);
        int right = std::stoi(sm[2]);

        if (left < 1000 && right < 1000) {   
            total += left * right;
        }

        std::cout << sm.str() << " " << left * right << std::endl;

        program = sm.suffix();
    }

    std::cout << "Total: " << total << std::endl;
}

void part2(std::ifstream& infile) {
    std::string program = ParseProgram(infile);
    std::cout << program << std::endl;

    std::regex mulMatcher("mul\\((\\d+),(\\d+)\\)|do\\(\\)|don't\\(\\)");
    std::smatch sm;

    int total = 0;
    bool shouldDo = true;

    while(true) {
        std::regex_search(program, sm, mulMatcher);
        if (sm.empty()) {
            break;
        }
        
        std::string matchStr = sm.str();
        if (matchStr.rfind("don", 0) == 0) {
            shouldDo = false;
        } else if (matchStr.rfind("do", 0) == 0) {
            shouldDo = true;
        } else {
            int left = std::stoi(sm[1]);
            int right = std::stoi(sm[2]);

            if (shouldDo && left < 1000 && right < 1000) {   
                total += left * right;
            }

            std::cout << sm.str() << " " << left * right << " " << (shouldDo ? "do" : "dont") << std::endl;
        }

        program = sm.suffix();
    }

    std::cout << "Total: " << total << std::endl;
}
