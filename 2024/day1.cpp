#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>

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
