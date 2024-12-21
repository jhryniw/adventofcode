#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

namespace {

std::vector<std::vector<int>> ParseReports(std::ifstream& infile) {
    std::vector<std::vector<int>> reports;

    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        std::vector<int> report;

        int a;
        while (iss >> a) {
            report.push_back(a);
        }

        reports.emplace_back(report);
    }

    return reports;
}

bool IsSafePart1(const std::vector<int>& report) {
    bool allIncreasing = true;
    bool allDecreasing = true;
    bool properDiffs = true;
    for (size_t i = 1; i < report.size(); i++) {
        allIncreasing &= report[i] > report[i-1];
        allDecreasing &= report[i] < report[i-1];
        int diff = std::abs(report[i] - report[i-1]);
        properDiffs &= (diff >= 1 && diff <= 3);
    }
    return (allIncreasing || allDecreasing) && properDiffs;
}



bool IsSafeWithSkip(const std::vector<int>& report, int skipIndex) {
    bool allIncreasing = true;
    bool allDecreasing = true;
    bool properDiffs = true;

    constexpr auto increment = [](int idx, int skipIdx) -> int {
        idx++;
        if (idx == skipIdx) {
            idx++;
        }
        return idx;
    };

    int prev = increment(-1, skipIndex);
    int i = increment(0, skipIndex);

    while (i < (int)report.size()) {
        if (i == prev) {
            i = increment(i, skipIndex);
        }

        allIncreasing &= report[i] > report[prev];
        allDecreasing &= report[i] < report[prev];
        int diff = std::abs(report[i] - report[prev]);
        properDiffs &= (diff >= 1 && diff <= 3);

        prev = increment(prev, skipIndex);
        i = increment(i, skipIndex);
    }

    return (allIncreasing || allDecreasing) && properDiffs;
}

bool IsSafePart2(const std::vector<int>& report) {
    bool allIncreasing = true;
    bool allDecreasing = true;
    bool properDiffs = true;

    for (size_t i = 1; i < report.size(); i++) {
        allIncreasing &= report[i] > report[i-1];
        allDecreasing &= report[i] < report[i-1];
        int diff = std::abs(report[i] - report[i-1]);
        properDiffs &= (diff >= 1 && diff <= 3);

        if (!((allIncreasing || allDecreasing) && properDiffs)) {
            if (i == 2) {
                return IsSafeWithSkip(report, 0) || IsSafeWithSkip(report, 1) || IsSafeWithSkip(report, 2);
            } else {
                return IsSafeWithSkip(report, i) || IsSafeWithSkip(report, i-1);
            }
        }
    }

    return (allIncreasing || allDecreasing) && properDiffs;
}

} // namespace

void part1(std::ifstream& infile) {
    auto reports = ParseReports(infile);

    int safe = 0;
    for (const auto& report : reports) {
        if (IsSafePart1(report)) {
            safe++;
        }
    }

    std::cout << "Safe: " << safe << std::endl;
}

void part2(std::ifstream& infile) {
    auto reports = ParseReports(infile);
    int safe = 0;
    for (const auto& report : reports) {
        if (IsSafePart2(report)) {
            safe++;
        }
    }

    std::cout << "Safe: " << safe << std::endl; 
}
