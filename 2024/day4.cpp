#include <fstream>
#include <iostream>
#include <vector>

bool IsValidCoord(int i, int j, int rows, int cols) {
    return !(i < 0 || j < 0 || i >= rows || j >= cols);
}

int SearchXmasPart1(const std::vector<std::string>& xmasMap, size_t i, size_t j) {
    if (xmasMap[i][j] != 'X') {
        return 0;
    }

    int rows = (int)xmasMap.size();
    int cols = (int)xmasMap[0].length();
    int iStart = (int)i;
    int jStart = (int)j;

    static const std::vector<std::pair<int, int>> ITERATORS = {
        {1,0},{-1,0},{0,1},{0,-1},{1,1},{-1,-1},{1,-1},{-1,1}
    };
    constexpr std::string_view SEARCH_STR = "MAS";
    int numXmasFound = 0;

    for (const auto& it : ITERATORS) {
        if (!IsValidCoord(iStart + (it.first * 3), jStart + (it.second * 3), rows, cols)) {
            continue;
        }

        bool found = true;
        int iCur = iStart;
        int jCur = jStart;

        for (size_t offset = 0; offset < 3; offset++) {
            iCur += it.first;
            jCur += it.second;
            if (xmasMap[iCur][jCur] != SEARCH_STR[offset]) {
                found = false;
                break;
            }
        }

        if (found) {
            numXmasFound += 1;
        }
    }

    return numXmasFound;
}

void part1(std::ifstream& infile) {
    std::vector<std::string> xmasMap;
    std::string line;
    while(std::getline(infile, line)) {
        xmasMap.push_back(line);
    }

    size_t rows = xmasMap.size();
    size_t cols = xmasMap[0].length();
    int numXmas = 0;

    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            if (xmasMap[i][j] == 'X') {
                numXmas += SearchXmasPart1(xmasMap, i, j);
            }
        }
    }

    std::cout << numXmas << std::endl;
}

bool IsX(const std::string& s1, const std::string& s2) {

    return (s1 == "MS" || s1 == "SM") && (s2 == "MS" || s2 == "SM");
}

std::string Make2CharStr(char c1, char c2) {
    std::string str(2, c1);
    str[1] = c2;
    return str;
}

int SearchXmasPart2(const std::vector<std::string>& xmasMap, size_t i, size_t j) {
    if (xmasMap[i][j] != 'A') {
        return 0;
    }

    size_t rows = xmasMap.size();
    size_t cols = xmasMap[0].length();

    // 3x3 bounding box
    if (i < 1 || j < 1 || i >= rows - 1 || j >= cols - 1) {
        return 0;
    }

    int numXmas = 0;

    // Check the diagonals
    std::string d1 = Make2CharStr(xmasMap[i-1][j-1], xmasMap[i+1][j+1]);
    std::string d2 = Make2CharStr(xmasMap[i-1][j+1], xmasMap[i+1][j-1]);
    if (IsX(d1, d2)) {
        numXmas += 1;
    }

    return numXmas;
}

void part2(std::ifstream& infile) {
    std::vector<std::string> xmasMap;
    std::string line;
    while(std::getline(infile, line)) {
        xmasMap.push_back(line);
    }

    size_t rows = xmasMap.size();
    size_t cols = xmasMap[0].length();
    int numXmas = 0;

    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            if (xmasMap[i][j] == 'A') {
                numXmas += SearchXmasPart2(xmasMap, i, j);
            }
        }
    }

    std::cout << numXmas << std::endl;
}
