#include <fstream>
#include <iostream>
#include <vector>
#include <unordered_set>

struct hash_pair {
    size_t operator () (const std::pair<int, int>& p) const {
        return p.first * 1000 + p.second;
    }
};

struct Lab {
    std::vector<std::vector<bool>> oGrid;
    std::pair<int, int> guardPos;
};

Lab ParseLab(std::ifstream& infile) {
    std::vector<std::vector<bool>> oGrid;
    std::pair<int, int> guardPos;

    std::string line;
    int currentLineNum = 0;
    while (std::getline(infile, line)) {
        std::vector<bool> oLine(line.size(), false);
        for (size_t i = 0; i < line.size(); i++) {
            if (line[i] == '.') {
                oLine[i] = false;
            } else if (line[i] == '#') {
                oLine[i] = true;
            } else if (line[i] == '^') {
                guardPos = std::make_pair(currentLineNum, (int)i);
                oLine[i] = false;
            } else {
                std::cout << "Unexpected character during parsing: " << oLine[i] << std::endl;
            }
        }
        oGrid.emplace_back(oLine);
        currentLineNum++;
    }

    return {
        .oGrid = oGrid,
        .guardPos = guardPos,
    };
}

std::pair<int, int> TurnRight(const std::pair<int, int>& dir) {
    // -1,0 -> 0,1
    // 0,1 -> 1,0
    // 1,0 -> 0,-1
    // 0,-1 -> -1,0
    return std::make_pair(dir.second, -dir.first);
}

std::pair<int, int> Move(const std::pair<int, int>& pos, const std::pair<int, int>& dir) {
    return std::make_pair(pos.first + dir.first, pos.second + dir.second);
}

bool IsValidPos(const std::pair<int, int>& pos, int numRows, int numCols) {
    return pos.first >= 0 && pos.first < numRows && pos.second >= 0 && pos.second < numCols;
}

void part1(std::ifstream& infile) {
    Lab lab = ParseLab(infile);

    int numRows = lab.oGrid.size();
    int numCols = lab.oGrid[0].size();
    auto guardPos = lab.guardPos;

    // Up is in the negative direction
    std::pair<int, int> guardDir = std::make_pair(-1,0);
    std::unordered_set<std::pair<int,int>, hash_pair> visited;

    while (IsValidPos(guardPos, numRows, numCols)) {
        visited.insert(guardPos);
        // std::cout << guardPos.first << "," << guardPos.second << std::endl;

        auto nextGuardPos = Move(guardPos, guardDir);
        if (!IsValidPos(nextGuardPos, numRows, numCols)) {
            break;
        }

        if (lab.oGrid[nextGuardPos.first][nextGuardPos.second]) {
            guardDir = TurnRight(guardDir);
            nextGuardPos = guardPos;
        }

        guardPos = nextGuardPos;
    }

    std::cout << "Positions visited: " << visited.size() << std::endl;
}

struct Pose {
    std::pair<int, int> pos;
    std::pair<int, int> dir;

    bool operator == (const Pose& other) const {
        return pos == other.pos && dir == other.dir;
    }

    Pose turnRight() const {
        return Pose{.pos = pos, .dir = TurnRight(dir)};
    }

    Pose moveOne() const {
        return Pose{.pos = Move(pos, dir), .dir = dir};
    }
};

struct hash_pose {
private:
    hash_pair _pairHasher;
public:
    size_t operator () (const Pose& pose) const {
        return _pairHasher(pose.pos) * 1000 + _pairHasher(pose.dir);
    }
};


void PrintGraph(const Pose& blockPose, const std::vector<std::vector<bool>>& oGrid, const std::unordered_set<std::pair<int,int>, hash_pair>& visited, const std::unordered_set<std::pair<int,int>, hash_pair>& blockPath) {
    int numRows = oGrid.size();
    int numCols = oGrid[0].size();

    for (int i = 0; i < numRows; i++) {
        for (int j = 0; j < numCols; j++) {
            auto pos = std::make_pair(i, j);
            char c;
            if (pos == blockPose.pos) {
                c = 'O';
            } else if (blockPath.contains(pos)) {
                c = '-';
            } else if (visited.contains(pos)) {
                c = 'X';
            } else if (oGrid[i][j]) {
                c = '#';
            } else {
                c = '.';
            }
            std::cout << c;
        }
        std::cout << std::endl;
    }
}

bool IsLoop(const std::vector<std::vector<bool>>& oGrid, const Pose& nextPose, const Pose& startPose, std::unordered_set<Pose, hash_pose> visited, bool print) {
    int numRows = oGrid.size();
    int numCols = oGrid[0].size();

    std::unordered_set<std::pair<int,int>, hash_pair> loopPositions;


    // Turn the guardPose to the right to avoid self-hits
    Pose guardPose = startPose.turnRight();
    while (IsValidPos(guardPose.pos, numRows, numCols)) {
        if (visited.contains(guardPose)) {
            if (print) {
                std::unordered_set<std::pair<int, int>, hash_pair> visitedPos;
                for (const auto& pose : visited) {
                    visitedPos.insert(pose.pos);
                }
                PrintGraph(nextPose, oGrid, visitedPos, loopPositions);
            }
            return true;
        }
        visited.insert(guardPose);
        loopPositions.insert(guardPose.pos);
        // std::cout << guardPos.first << "," << guardPos.second << std::endl;

        Pose nextGuardPose = guardPose.moveOne();

        if (!IsValidPos(nextGuardPose.pos, numRows, numCols)) {
            break;
        }

        if (oGrid[nextGuardPose.pos.first][nextGuardPose.pos.second]) {
            nextGuardPose = guardPose.turnRight();
        }

        guardPose = nextGuardPose;
    }

    return false;
}

void part2(std::ifstream& infile) {
    Lab lab = ParseLab(infile);

    int numRows = lab.oGrid.size();
    int numCols = lab.oGrid[0].size();

    // Up is in the negative direction
    Pose guardPose {
        .pos = lab.guardPos,
        .dir = std::make_pair(-1,0)
    };

    std::unordered_set<Pose, hash_pose> visited;
    std::unordered_set<std::pair<int, int>, hash_pair> visitedPos;
    std::unordered_set<std::pair<int, int>, hash_pair> potentialBlocks;

    while (IsValidPos(guardPose.pos, numRows, numCols)) {
        visited.insert(guardPose);
        visitedPos.insert(guardPose.pos);
        // std::cout << guardPos.first << "," << guardPos.second << std::endl;

        Pose nextGuardPose = guardPose.moveOne();

        if (!IsValidPos(nextGuardPose.pos, numRows, numCols)) {
            break;
        }

        if (lab.oGrid[nextGuardPose.pos.first][nextGuardPose.pos.second]) {
            nextGuardPose = guardPose.turnRight();
        } else if (nextGuardPose.pos != lab.guardPos) {
            lab.oGrid[nextGuardPose.pos.first][nextGuardPose.pos.second] = true;
            if (IsLoop(lab.oGrid, nextGuardPose, guardPose, visited, false)) {
                potentialBlocks.insert(nextGuardPose.pos);
                // std::cout << std::endl;
            }
            lab.oGrid[nextGuardPose.pos.first][nextGuardPose.pos.second] = false;
        }

        guardPose = nextGuardPose;
    }

    std::cout << potentialBlocks.contains(lab.guardPos) << std::endl;
    std::cout << "Positions visited: " << visitedPos.size() << std::endl;
    std::cout << "Blocks detected: " << potentialBlocks.size() << std::endl;
}
