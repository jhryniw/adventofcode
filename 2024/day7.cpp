#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

struct Calibration {
    std::vector<int> nums;
    long long result = 0;
};

std::vector<Calibration> ParseCalibrations(std::ifstream& infile) {
    std::vector<Calibration> cals;

    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        Calibration cal;
        char colonSink;
        iss >> cal.result;
        iss >> colonSink;

        int num = 0;
        while (iss >> num) {
            cal.nums.emplace_back(num);
        }
        cals.emplace_back(cal);
    }

    return cals;
}

bool dfs1(const std::vector<int>& nums, long long result, size_t index, long long current) {
    if (index >= nums.size()) {
        return current == result;
    }
    return dfs1(nums, result, index+1, current + nums[index]) || 
           dfs1(nums, result, index+1, current * nums[index]);
}

void part1(std::ifstream& infile) {
    std::vector<Calibration> cals = ParseCalibrations(infile);

    long long total = 0;
    for (const Calibration& cal : cals) {
        if (dfs1(cal.nums, cal.result, 1, cal.nums[0])) {
            total += cal.result;
        }
    }

    std::cout << std::endl;
    std::cout << total << std::endl;
}

long long combineDigits(long long a, long long b) {
    int bPowerOfTen = 0;
    long long bCopy = b;
    while (bCopy > 0) {
        bCopy /= 10;
        bPowerOfTen++;
    }

    return (a * std::pow(10, bPowerOfTen)) + b;
}

bool dfs2(const std::vector<int>& nums, long long result, size_t index, long long current) {
    if (index >= nums.size()) {
        return current == result;
    }
    return dfs2(nums, result, index+1, current + nums[index]) || 
           dfs2(nums, result, index+1, current * nums[index]) ||
           dfs2(nums, result, index+1, combineDigits(current, nums[index]));
}

void part2(std::ifstream& infile) {
    std::vector<Calibration> cals = ParseCalibrations(infile);

    long long total = 0;
    for (const Calibration& cal : cals) {
        if (dfs2(cal.nums, cal.result, 1, cal.nums[0])) {
            total += cal.result;
        }
    }

    std::cout << total << std::endl;
}
