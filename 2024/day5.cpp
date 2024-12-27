#include <algorithm>
#include <deque>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

struct Page {
    std::unordered_set<int> mustBeBefore;
    std::unordered_set<int> mustBeAfter;
};

std::unordered_map<int, Page> ParsePages(std::ifstream& infile) {
    std::unordered_map<int, Page> pages;

    std::string line;
    while (std::getline(infile, line)) {
        if (line == "") {
            break;
        }

        int pageBefore, pageAfter;
        char sep;
        std::istringstream iss(line);
        iss >> pageBefore;
        iss >> sep;
        iss >> pageAfter;

        pages[pageBefore].mustBeBefore.insert(pageAfter);
        pages[pageAfter].mustBeAfter.insert(pageBefore);
    }

    return pages;
}

std::vector<std::vector<int>> ParseUpdates(std::ifstream& infile) {
    std::vector<std::vector<int>> updates;
    std::string line;

    while (std::getline(infile, line)) {
        std::vector<int> update;
        int page;
        char sep;
        std::istringstream iss(line);
        while (iss >> page) {
            update.push_back(page);
            if (!iss.eof()) {
                iss >> sep;
            }
        }
        updates.emplace_back(update);
    }

    return updates;
}

bool IsValidUpdate(const std::vector<int>& update, const std::unordered_map<int, Page>& pages) {
    std::unordered_set<int> prefix;
    std::unordered_set<int> postfix(update.begin(), update.end());

    for (int page : update) {
        postfix.erase(page);
        if (auto pageIt = pages.find(page); pageIt != pages.end()) {
            // Cannot be before any pages it must be after
            for (int pageThatMustBeBefore : pageIt->second.mustBeAfter) {
                if (postfix.find(pageThatMustBeBefore) != postfix.end()) {
                    return false;
                }
            }

            // Cannot be after any pages it must be before
            for (int pageThatMustBeAfter : pageIt->second.mustBeBefore) {
                if (prefix.find(pageThatMustBeAfter) != prefix.end()) {
                    return false;
                }
            }
        }
        prefix.insert(page);
    }

    return true;
}

void part1(std::ifstream& infile) {
    auto pages = ParsePages(infile);
    auto updates = ParseUpdates(infile);

    int validUpdates = 0;
    int sumMiddleNums = 0;

    for (const auto& update : updates) {
        if (IsValidUpdate(update, pages)) {
            if (update.size() % 2 == 0) {
                std::cout << "Got even sized update..." << std::endl;
            }
            sumMiddleNums += update[update.size() / 2];
            validUpdates += 1;
        }
    }

    std::cout << "Valid Updates: " << validUpdates << std::endl;
    std::cout << "Sum Middle: " << sumMiddleNums << std::endl;
}

std::vector<int> FixUpdate(const std::vector<int>& update, const std::unordered_map<int, Page>& pages) {
    std::unordered_map<int, Page> updatePageMap;
    for (int page : update) {
        if (const auto pageIt = pages.find(page); pageIt != pages.end()) {
            Page pageCopy;
            for (int p : update) {
                if (pageIt->second.mustBeAfter.find(p) != pageIt->second.mustBeAfter.end()) {
                    pageCopy.mustBeAfter.emplace(p);
                }
            }
            updatePageMap[page] = pageCopy;
        } else {
            updatePageMap[page] = Page();
        }
    }

    // Use topological sort procedure
    std::vector<int> fixedUpdate;
    std::deque<int> pageQ(update.begin(), update.end());

    while (!pageQ.empty()) {
        int page = pageQ.front();
        pageQ.pop_front();
        
        if (updatePageMap[page].mustBeAfter.empty()) {
            fixedUpdate.push_back(page);
            updatePageMap.erase(page);
            for (auto& pageIt : updatePageMap) {
                pageIt.second.mustBeAfter.erase(page);
            }
        } else {
            pageQ.push_back(page);
        }
    }

    return fixedUpdate;
}

void part2(std::ifstream& infile) {
    auto pages = ParsePages(infile);
    auto updates = ParseUpdates(infile);

    int invalidUpdates = 0;
    int sumMiddleNums = 0;

    for (const auto& update : updates) {
        if (!IsValidUpdate(update, pages)) {
            auto fixed = FixUpdate(update, pages);
            for (int p : fixed) {
                std::cout << p << " ";
            }
            std::cout << std::endl;

            if (fixed.size() % 2 == 0) {
                std::cout << "Got even sized update..." << std::endl;
            }
            sumMiddleNums += fixed[fixed.size() / 2];
            invalidUpdates += 1;
        }
    }

    std::cout << "Valid Updates: " << invalidUpdates << std::endl;
    std::cout << "Sum Middle: " << sumMiddleNums << std::endl;
}
