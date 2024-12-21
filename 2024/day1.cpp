#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>


enum class InputType { TEST, FULL };

namespace {

int ExtractDayFromProgram(const std::string& progPath) {
    std::filesystem::path progFsPath(progPath);
    std::string progName = progFsPath.stem().string();
    std::string dayPart (progName.begin() + 3, progName.end());
    return std::stoi(dayPart);
}

std::string ToString(InputType inputType) {
    return inputType == InputType::TEST ? "test" : "full";
}

InputType ToInputType(const std::string& s) {
    if (s == "test") {
        return InputType::TEST;
    } else {
        return InputType::FULL;
    }
}

std::filesystem::path InputPath(int day, int part, InputType inputType) {
    std::filesystem::path root = "/root/adventofcode/2024";
    std::string dayPart = "day" + std::to_string(day);
    std::string typePart = ToString(inputType) + ".txt";

    std::string fileName = dayPart;
    if (part == 1 or part == 2) {
        std::string partPart = "part" + std::to_string(part);
        fileName += "_" + partPart;
    }
    fileName += "_" + typePart;

    return root / fileName;
}

std::filesystem::path FindBestPath(int day, int part, InputType inputType) {
    auto pathWithPart = InputPath(day, part, inputType);
    if (std::filesystem::exists(pathWithPart)) {
        return pathWithPart;
    }

    auto pathWithoutPart = InputPath(day, -1, inputType);
    return pathWithoutPart;
}

void part1(std::ifstream& infile) {
    std::vector<int> list1;
    std::vector<int> list2;
    int a,b;

    while (infile >> a >> b) {
        list1.push_back(a);
        list2.push_back(b);
    }

    std::sort(list1.begin(), list1.end());
    std::sort(list2.begin(), list2.end());

    int score = 0;

    for (size_t i = 0; i < list1.size(); i++) {
        int diff = std::abs(list1[i] - list2[i]);
        score += diff;
    }

    std::cout << "Score: " << score << std::endl;
}

void part2(std::ifstream& infile) {
    std::vector<int> listLeft;
    std::unordered_map<int, int> rightCounts;
    int a,b;

    while (infile >> a >> b) {
        listLeft.push_back(a);
        rightCounts[b]++;
    }

    int similarity = 0;

    for (size_t i = 0; i < listLeft.size(); i++) {
        int left = listLeft[i];
        int rightCount = 0;
        if (rightCounts.find(left) != rightCounts.end()) {
            rightCount = rightCounts[left];
        }

        similarity += left * rightCount;
    }

    std::cout << "Similarity: " << similarity << std::endl;
}

} // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Usage: {partNum} {test|prod}" << std::endl;
        return 0;
    }

    int day = ExtractDayFromProgram(std::string(argv[0]));
    int part = std::stoi(argv[1]);
    InputType inputType = ToInputType(std::string(argv[2]));

    std::cout << "Running part" << part << " " << ToString(inputType) << std::endl;
    
    std::filesystem::path infilePath = FindBestPath(day, part, inputType);
    if (!std::filesystem::exists(infilePath)) {
        std::cout << "Could not find input file: " << infilePath.string() << std::endl;
    }

    std::ifstream infile(infilePath);

    if (part == 1) {
        part1(infile);
    } else {
        part2(infile);
    }

    return 0;
}
