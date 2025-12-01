
#include <sqlite3.h>
#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <unordered_set>
#include <unordered_map>
#include <chrono>
#include <numeric>
#include <cassert>
#include <cctype>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <io.h>
#include <fcntl.h>
#include <locale>
#endif

//std::wstring_convert<std::codecvt_utf8<char32_t>, char32_t> converter;
// 全局数据
std::vector<std::string> questions;
std::vector<std::string> answers;

// 使用 char32_t 表示 Unicode 码点
std::unordered_map<char32_t, std::set<int>> charToQuestions;
std::vector<std::unordered_set<char32_t>> questionSets;


std::u32string utf8_to_utf32(const std::string& utf8) {
    std::u32string result;
    size_t i = 0;
    while (i < utf8.size()) {
        unsigned char c = static_cast<unsigned char>(utf8[i]);
        char32_t cp;

        if ((c & 0x80) == 0) { // ASCII
            cp = c;
            i += 1;
        }
        else if ((c & 0xE0) == 0xC0) { // 2-byte
            if (i + 1 >= utf8.size()) break;
            cp = ((c & 0x1F) << 6) | (static_cast<unsigned char>(utf8[i + 1]) & 0x3F);
            i += 2;
        }
        else if ((c & 0xF0) == 0xE0) { // 3-byte (most Chinese)
            if (i + 2 >= utf8.size()) break;
            cp = ((c & 0x0F) << 12) |
                ((static_cast<unsigned char>(utf8[i + 1]) & 0x3F) << 6) |
                ((static_cast<unsigned char>(utf8[i + 2]) & 0x3F));
            i += 3;
        }
        else if ((c & 0xF8) == 0xF0) { // 4-byte
            if (i + 3 >= utf8.size()) break;
            cp = ((c & 0x07) << 18) |
                ((static_cast<unsigned char>(utf8[i + 1]) & 0x3F) << 12) |
                ((static_cast<unsigned char>(utf8[i + 2]) & 0x3F) << 6) |
                ((static_cast<unsigned char>(utf8[i + 3]) & 0x3F));
            i += 4;
        }
        else {
            // Invalid UTF-8: skip
            ++i;
            continue;
        }

        // Skip surrogate code points (invalid in UTF-32)
        if (cp >= 0xD800 && cp <= 0xDFFF) continue;
        // Valid Unicode range
        if (cp <= 0x10FFFF) {
            result.push_back(cp);
        }
    }
    return result;
}

class Timer {
public:
    std::chrono::steady_clock::time_point start;

    Timer() : start(std::chrono::steady_clock::now()) {}

    ~Timer() {
        auto end = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::printf( "用时%.2fs\n",duration.count() / 1'000'000.0);
    }
};

static int callback(void* /*data*/, int argc, char** argv, char** azColName) {
    std::string q, a;
    for (int i = 0; i < argc; i++) {
        const char* value = argv[i] ? argv[i] : "";
        const char* key = azColName[i];
        if (std::strcmp(key, "question") == 0) {
            q = value;
        }
        else if (std::strcmp(key, "answer") == 0) {
            a = value;
        }
    }
    if (!q.empty() || !a.empty()) { // 即使一方为空也保留（可选）
        questions.emplace_back(std::move(q));
        answers.emplace_back(std::move(a));
    }
    return 0;
}

// 返回匹配的答案索引，失败返回 -1
static int answer_fast(const std::string& input) {
    Timer timer;
    if (questions.empty()) return -1;

    auto u32input = utf8_to_utf32(input);
    if (u32input.empty()) return -1;

    std::unordered_set<char32_t> qSet(u32input.begin(), u32input.end());
    std::set<int> candidateIndices;

    // 倒排索引收集候选
    for (char32_t c : qSet) {
        auto it = charToQuestions.find(c);
        if (it != charToQuestions.end()) {
            candidateIndices.insert(it->second.begin(), it->second.end());
        }
    }

    std::vector<int> candidates;
    if (candidateIndices.empty()) {
        // 回退到全集
        candidates.resize(questions.size());
        std::iota(candidates.begin(), candidates.end(), 0);
    }
    else {
        candidates.assign(candidateIndices.begin(), candidateIndices.end());
    }

    float maxSim = -1.0f;
    int bestIdx = 0;
    size_t qLen = qSet.size();

    for (int idx : candidates) {
        const auto& qSetI = questionSets[idx];
        if (qSetI.empty()) continue;

        size_t inter = 0;
        for (char32_t c : qSet) {
            if (qSetI.count(c)) ++inter;
        }
        size_t uni = qLen + qSetI.size() - inter;
        float sim = (uni > 0) ? static_cast<float>(inter) / static_cast<float>(uni) : 0.0f;

        if (sim > maxSim) {
            maxSim = sim;
            bestIdx = idx;
        }
    }

    if (maxSim < 0.1f) {
        std::printf("阿巴阿巴\n");
        return -1;
    }

    return bestIdx;
}

int main(int argc, char* argv[]) {

#ifdef _WIN32
    // 步骤 1: 设置控制台代码页为 UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    // 步骤 2: 设置 C/C++ 运行时 locale 为 UTF-8
    std::setlocale(LC_ALL, ".utf8");

    // 正确做法：保持 byte stream，靠 SetConsoleOutputCP + setlocale 即可
#endif
    {
        Timer t;
        sqlite3* db = nullptr;
        char* zErrMsg = nullptr;
        const char* query = "SELECT question, answer FROM g ORDER BY rowid";

        int rc = sqlite3_open("dataset.db", &db);
        if (rc != SQLITE_OK) {
            std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << "\n";
            sqlite3_close(db);
            return 1;
        }

        rc = sqlite3_exec(db, query, callback, nullptr, &zErrMsg);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error: " << zErrMsg << "\n";
            sqlite3_free(zErrMsg);
            sqlite3_close(db);
            return 1;
        }

        sqlite3_close(db);

        // 校验数据一致性
        assert(questions.size() == answers.size());
        std::printf( "加载了%d个问答对\n ",(int)questions.size());

        //std::cout << r;
        // 预计算字符集和倒排索引
        for (size_t i = 0; i < questions.size(); ++i) {
            auto u32q = utf8_to_utf32(questions[i]);
            std::unordered_set<char32_t> s(u32q.begin(), u32q.end());
            questionSets.emplace_back(std::move(s));
            for (char32_t c : s) {
                charToQuestions[c].insert(static_cast<int>(i));
            }
        }
    }

    std::string q;
    std::printf("TinyLangJaccard-Swiftness-Sqlite-C++测试.\n");
    std::printf( "数据集:https://modelscope.cn/datasets/qiaojiedongfeng/qiaojiedongfeng\n");

    while (std::printf("请输入问题 ") && std::getline(std::cin, q)) {
        // 支持退出命令
        if (q == "quit" || q == "exit") break;

        if (q.empty()) {
            std::printf("请输入问题。\n");
            continue;
        }

        int result = answer_fast(q);
        if (result >= 0 && result < static_cast<int>(answers.size())) {
            std::cout << answers[result] << '\n';
        }
        else {
            std::printf("我不太明白您的意思...\n");
        }
    }

    return 0;
}