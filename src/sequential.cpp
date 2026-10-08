#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <climits>

using namespace std;

int main() {
    const long long N = 10000000; // 10 million elements

    vector<int> data(N);

    mt19937 rng(42);
    uniform_int_distribution<int> dist(1, 1000000);

    for (long long i = 0; i < N; i++) {
        data[i] = dist(rng);
    }

    int maxValue = INT_MIN;
    int minValue = INT_MAX;

    auto start = chrono::high_resolution_clock::now();

    for (long long i = 0; i < N; i++) {
        if (data[i] > maxValue)
            maxValue = data[i];

        if (data[i] < minValue)
            minValue = data[i];
    }

    auto end = chrono::high_resolution_clock::now();

    double timeMs =
        chrono::duration<double, milli>(end - start).count();

    cout << "========================================\n";
    cout << " Sequential Maximum/Minimum Search\n";
    cout << "========================================\n";
    cout << "Dataset Size : " << N << " elements\n";
    cout << "Maximum      : " << maxValue << "\n";
    cout << "Minimum      : " << minValue << "\n";
    cout << "Execution Time: " << timeMs << " ms\n";
    cout << "========================================\n";

    return 0;
}
