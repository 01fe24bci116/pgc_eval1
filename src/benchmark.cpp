#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <climits>
#include <fstream>
#include <cmath>
#include <omp.h>

using namespace std;

double runParallel(const vector<int>& data, int threads, int& maxValue, int& minValue) {
    omp_set_num_threads(threads);

    maxValue = INT_MIN;
    minValue = INT_MAX;

    auto start = chrono::high_resolution_clock::now();

    #pragma omp parallel for reduction(max:maxValue) reduction(min:minValue)
    for (long long i = 0; i < (long long)data.size(); i++) {
        if (data[i] > maxValue)
            maxValue = data[i];

        if (data[i] < minValue)
            minValue = data[i];
    }

    auto end = chrono::high_resolution_clock::now();

    return chrono::duration<double, milli>(end - start).count();
}

double runSequential(const vector<int>& data, int& maxValue, int& minValue) {
    maxValue = INT_MIN;
    minValue = INT_MAX;

    auto start = chrono::high_resolution_clock::now();

    for (long long i = 0; i < (long long)data.size(); i++) {
        if (data[i] > maxValue)
            maxValue = data[i];

        if (data[i] < minValue)
            minValue = data[i];
    }

    auto end = chrono::high_resolution_clock::now();

    return chrono::duration<double, milli>(end - start).count();
}

double calculateMean(const vector<double>& values) {
    double sum = 0.0;

    for (double value : values)
        sum += value;

    return sum / values.size();
}

double calculateStdDev(const vector<double>& values, double mean) {
    double sum = 0.0;

    for (double value : values)
        sum += (value - mean) * (value - mean);

    return sqrt(sum / values.size());
}

int main() {

    const int RUNS = 5;

    vector<long long> datasetSizes = {
        10000000,
        50000000,
        100000000,
        200000000
    };

    vector<int> threadCounts = {1, 2, 4, 8, 16};

    ofstream csv("results\\benchmark.csv");

    csv << "DatasetSize,Threads,Type,AverageTimeMs,StdDevMs,Maximum,Minimum\n";

    mt19937 rng(42);
    uniform_int_distribution<int> dist(1, 1000000);

    cout << "====================================================\n";
    cout << " OpenMP Maximum/Minimum Benchmark\n";
    cout << " Averaged over " << RUNS << " runs\n";
    cout << "====================================================\n";

    for (long long N : datasetSizes) {

        cout << "\nDataset Size: " << N << " elements\n";

        vector<int> data(N);

        for (long long i = 0; i < N; i++) {
            data[i] = dist(rng);
        }

        int maxValue = INT_MIN;
        int minValue = INT_MAX;

        vector<double> sequentialTimes;

        for (int run = 0; run < RUNS; run++) {
            sequentialTimes.push_back(
                runSequential(data, maxValue, minValue)
            );
        }

        double sequentialMean =
            calculateMean(sequentialTimes);

        double sequentialStd =
            calculateStdDev(sequentialTimes, sequentialMean);

        cout << "Sequential: "
             << sequentialMean
             << " ms (SD: "
             << sequentialStd
             << ")\n";

        csv << N << ",1,Sequential,"
            << sequentialMean << ","
            << sequentialStd << ","
            << maxValue << ","
            << minValue << "\n";

        for (int threads : threadCounts) {

            vector<double> parallelTimes;

            for (int run = 0; run < RUNS; run++) {

                parallelTimes.push_back(
                    runParallel(
                        data,
                        threads,
                        maxValue,
                        minValue
                    )
                );
            }

            double mean =
                calculateMean(parallelTimes);

            double stdDev =
                calculateStdDev(parallelTimes, mean);

            cout << "Threads " << threads
                 << ": "
                 << mean
                 << " ms (SD: "
                 << stdDev
                 << ")\n";

            csv << N << ","
                << threads
                << ",OpenMP,"
                << mean
                << ","
                << stdDev
                << ","
                << maxValue
                << ","
                << minValue
                << "\n";
        }

        cout << "----------------------------------------------------\n";
    }

    csv.close();

    cout << "\n====================================================\n";
    cout << " Benchmark completed successfully.\n";
    cout << " Results saved to: results\\benchmark.csv\n";
    cout << "====================================================\n";

    return 0;
}
