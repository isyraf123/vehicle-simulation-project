#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <string>
#include <algorithm>
#include <sstream>

using namespace std;

const double AIR_DENSITY = 1.20;
const double AIR_VISCOSITY = 1.81e-5;
const double FUEL_DENSITY = 0.74;
const double HEATING_VALUE = 44000000.0;
const double GRAVITY = 9.81;
const double ROLLING_RESISTANCE_COEFF = 0.015;

class Vehicle {
private:
    double mass;
    double width;
    double height;
    double length;
    double efficiency;
    double frontalArea;
    
public:
    Vehicle(double m, double w, double h, double l, double eff) {
        mass = m;
        width = w;
        height = h;
        length = l;
        efficiency = eff;
        frontalArea = w * h;
    }
    
    double getMass() const { return mass; }
    double getWidth() const { return width; }
    double getHeight() const { return height; }
    double getLength() const { return length; }
    double getEfficiency() const { return efficiency; }
    double getFrontalArea() const { return frontalArea; }
    
    void displayInfo() const {
        cout << "Vehicle Mass: " << mass << " kg" << endl;
        cout << "Dimensions: " << width << "m x " << height << "m x " << length << "m" << endl;
        cout << "Frontal Area: " << frontalArea << " m^2" << endl;
        cout << "Engine Efficiency: " << efficiency * 100 << "%" << endl;
    }
};

struct SimulationData {
    double time;
    double speed;
    double acceleration;
    double drag;
    double rollingResistance;
    double slopeResistance;
    double totalResistance;
    double fuel;
    double cumulativeFuel;
    double reynolds;
    double cd;
    double altitude;
    double slope;
};

void printLine() {
    cout << "==========================================================" << endl;
}

void printTitle() {
    printLine();
    cout << "   ADVANCED ROAD VEHICLE DYNAMICS & FUEL SIMULATION" << endl;
    printLine();
}

double getInput(string prompt) {
    double value;
    cout << prompt;
    cin >> value;
    return value;
}

int getIntInput(string prompt) {
    int value;
    cout << prompt;
    cin >> value;
    return value;
}

double calculateReynolds(double velocity, double length) {
    return (AIR_DENSITY * velocity * length) / AIR_VISCOSITY;
}

double calculateCdFromReynolds(double Re) {
    if (Re < 2e6) return 0.38;
    else if (Re < 3e6) return 0.35;
    else if (Re < 4e6) return 0.32;
    else return 0.30;
}

double calculateAerodynamicDrag(double Cd, double area, double velocity) {
    return 0.5 * AIR_DENSITY * Cd * area * velocity * velocity;
}

double calculateRollingResistance(double mass, double angle) {
    return ROLLING_RESISTANCE_COEFF * mass * GRAVITY * cos(angle);
}

double calculateSlopeResistance(double mass, double angle) {
    return mass * GRAVITY * sin(angle);
}

double calculateWork(double force, double distance) {
    return force * distance;
}

double calculateFuelEnergy(double work, double efficiency) {
    return work / efficiency;
}

double calculateFuelMass(double energy) {
    return energy / HEATING_VALUE;
}

double calculateFuelVolume(double mass) {
    return mass / FUEL_DENSITY;
}

double getTerrainSlope(int scenario, double currentTime, double totalTime) {
    double angle = 0.0;
    
    if (scenario == 1) {
        angle = 0.0;
    } else if (scenario == 2) {
        if (currentTime < totalTime * 0.25) {
            angle = 0.02;
        } else if (currentTime < totalTime * 0.5) {
            angle = 0.0;
        } else if (currentTime < totalTime * 0.75) {
            angle = -0.02;
        } else {
            angle = 0.0;
        }
    } else if (scenario == 3) {
        angle = 0.03 * sin(2 * M_PI * currentTime / (totalTime / 3));
    }
    
    return angle;
}

double getSpeedProfile(int scenario, int step, int totalSteps, double baseSpeed) {
    double speed = baseSpeed;
    double progress = static_cast<double>(step) / totalSteps;
    
    if (scenario == 1) {
        if (step < totalSteps * 0.2) {
            speed = baseSpeed * (0.3 + 0.7 * progress * 5);
        } else if (step < totalSteps * 0.8) {
            speed = baseSpeed;
        } else {
            speed = baseSpeed * (1.0 - (progress - 0.8) * 5);
        }
    } else if (scenario == 2) {
        if (step < totalSteps / 2) {
            speed += 0.02 * step;
        } else {
            speed += 0.02 * (totalSteps / 2) - 0.02 * (step - totalSteps / 2);
        }
    } else if (scenario == 3) {
        speed = baseSpeed * (1.0 + 0.3 * sin(4 * M_PI * progress));
    }
    
    if (speed < 1.0) speed = 1.0;
    return speed;
}

void displayScenarioMenu() {
    printLine();
    cout << "SELECT DRIVING SCENARIO:" << endl;
    cout << "1. Urban Driving (Stop-and-go traffic)" << endl;
    cout << "2. Highway Driving (Acceleration/Deceleration)" << endl;
    cout << "3. Sport Driving (Variable speed)" << endl;
    printLine();
}

void displayInputSummary(const Vehicle& vehicle, double distance, double speed, int scenario) {
    printLine();
    cout << "INPUT SUMMARY" << endl;
    printLine();
    vehicle.displayInfo();
    cout << "Travel Distance: " << distance << " km" << endl;
    cout << "Initial Speed: " << speed << " km/h" << endl;
    cout << "Scenario: " << scenario << endl;
    printLine();
}

vector<SimulationData> runSimulation(const Vehicle& vehicle, double distanceKm, 
                                     double speedKmh, int scenario) {
    vector<SimulationData> results;
    
    double speed = speedKmh * 1000.0 / 3600.0;
    double distance = distanceKm * 1000.0;
    double dt = 1.0;
    double totalTime = distance / speed;
    int steps = static_cast<int>(totalTime);
    
    double cumulativeFuel = 0.0;
    double altitude = 0.0;
    double previousSpeed = speed;
    
    printLine();
    cout << "SIMULATION RUNNING..." << endl;
    cout << "Total Steps: " << steps << endl;
    printLine();
    
    for (int i = 0; i < steps; i++) {
        SimulationData data;
        
        speed = getSpeedProfile(scenario, i, steps, speedKmh * 1000.0 / 3600.0);
        
        double currentTime = i * dt;
        double slopeAngle = getTerrainSlope(scenario, currentTime, totalTime);
        
        data.time = currentTime;
        data.speed = speed;
        data.acceleration = (speed - previousSpeed) / dt;
        data.slope = slopeAngle;
        
        double Re = calculateReynolds(speed, vehicle.getLength());
        double Cd = calculateCdFromReynolds(Re);
        
        double Fd = calculateAerodynamicDrag(Cd, vehicle.getFrontalArea(), speed);
        double Fr = calculateRollingResistance(vehicle.getMass(), slopeAngle);
        double Fs = calculateSlopeResistance(vehicle.getMass(), slopeAngle);
        
        data.drag = Fd;
        data.rollingResistance = Fr;
        data.slopeResistance = Fs;
        data.totalResistance = Fd + Fr + Fs;
        data.reynolds = Re;
        data.cd = Cd;
        
        double dx = speed * dt;
        altitude += dx * sin(slopeAngle);
        data.altitude = altitude;
        
        double totalForce = data.totalResistance;
        if (data.acceleration > 0) {
            totalForce += vehicle.getMass() * data.acceleration;
        }
        
        double W = calculateWork(totalForce, dx);
        double E = calculateFuelEnergy(W, vehicle.getEfficiency());
        double fuelMass = calculateFuelMass(E);
        double fuelVolume = calculateFuelVolume(fuelMass);
        
        data.fuel = fuelVolume;
        cumulativeFuel += fuelVolume;
        data.cumulativeFuel = cumulativeFuel;
        
        results.push_back(data);
        
        previousSpeed = speed;
        
        if (i % 5000 == 0 || i == steps - 1) {
            cout << "Progress: " << (i * 100 / steps) << "% | ";
            cout << "Time: " << currentTime << "s | ";
            cout << "Speed: " << speed << "m/s" << endl;
        }
    }
    
    printLine();
    cout << "SIMULATION COMPLETED" << endl;
    printLine();
    
    return results;
}

void saveResultsToCSV(const vector<SimulationData>& results, int scenario) {
    stringstream filename;
    filename << "vehicle_simulation_scenario_" << scenario << ".csv";
    
    ofstream file(filename.str());
    
    file << "time,speed,acceleration,drag,rolling_resistance,slope_resistance,";
    file << "total_resistance,fuel,cumulative_fuel,reynolds,cd,altitude,slope\n";
    
    for (size_t i = 0; i < results.size(); i++) {
        file << results[i].time << ",";
        file << results[i].speed << ",";
        file << results[i].acceleration << ",";
        file << results[i].drag << ",";
        file << results[i].rollingResistance << ",";
        file << results[i].slopeResistance << ",";
        file << results[i].totalResistance << ",";
        file << results[i].fuel << ",";
        file << results[i].cumulativeFuel << ",";
        file << results[i].reynolds << ",";
        file << results[i].cd << ",";
        file << results[i].altitude << ",";
        file << results[i].slope << "\n";
    }
    
    file.close();
    cout << "Results saved to: " << filename.str() << endl;
}

void calculateAndDisplayStatistics(const vector<SimulationData>& results) {
    printLine();
    cout << "SIMULATION STATISTICS" << endl;
    printLine();
    
    double totalFuel = results.back().cumulativeFuel;
    double totalDistance = 0.0;
    double maxSpeed = 0.0;
    double avgSpeed = 0.0;
    double maxDrag = 0.0;
    double avgDrag = 0.0;
    double maxAltitude = results[0].altitude;
    double minAltitude = results[0].altitude;
    
    for (size_t i = 0; i < results.size(); i++) {
        if (i > 0) {
            totalDistance += results[i].speed * (results[i].time - results[i-1].time);
        }
        
        avgSpeed += results[i].speed;
        avgDrag += results[i].drag;
        
        if (results[i].speed > maxSpeed) maxSpeed = results[i].speed;
        if (results[i].drag > maxDrag) maxDrag = results[i].drag;
        if (results[i].altitude > maxAltitude) maxAltitude = results[i].altitude;
        if (results[i].altitude < minAltitude) minAltitude = results[i].altitude;
    }
    
    avgSpeed /= results.size();
    avgDrag /= results.size();
    
    double fuelPer100km = (totalFuel / totalDistance) * 100000.0;
    
    cout << "Total Fuel Consumed: " << totalFuel << " L" << endl;
    cout << "Fuel per 100km: " << fuelPer100km << " L/100km" << endl;
    cout << "Total Distance: " << totalDistance / 1000.0 << " km" << endl;
    cout << "Average Speed: " << avgSpeed << " m/s (" << avgSpeed * 3.6 << " km/h)" << endl;
    cout << "Maximum Speed: " << maxSpeed << " m/s (" << maxSpeed * 3.6 << " km/h)" << endl;
    cout << "Average Drag Force: " << avgDrag << " N" << endl;
    cout << "Maximum Drag Force: " << maxDrag << " N" << endl;
    cout << "Maximum Altitude: " << maxAltitude << " m" << endl;
    cout << "Minimum Altitude: " << minAltitude << " m" << endl;
    cout << "Altitude Change: " << (maxAltitude - minAltitude) << " m" << endl;
    printLine();
}

bool validateInput(double value, double min, double max, string name) {
    if (value < min || value > max) {
        cout << "ERROR: " << name << " must be between " << min << " and " << max << endl;
        return false;
    }
    return true;
}

int main() {
    cout << fixed << setprecision(5);
    
    printTitle();
    
    cout << "Enter Vehicle Parameters:" << endl;
    printLine();
    
    double mass = getInput("Vehicle mass (kg) [500-5000]: ");
    if (!validateInput(mass, 500, 5000, "Mass")) return 1;
    
    double width = getInput("Vehicle width (m) [1.0-3.0]: ");
    if (!validateInput(width, 1.0, 3.0, "Width")) return 1;
    
    double height = getInput("Vehicle height (m) [1.0-3.0]: ");
    if (!validateInput(height, 1.0, 3.0, "Height")) return 1;
    
    double length = getInput("Vehicle length (m) [2.0-8.0]: ");
    if (!validateInput(length, 2.0, 8.0, "Length")) return 1;
    
    double efficiency = getInput("Engine efficiency [0.1-0.5]: ");
    if (!validateInput(efficiency, 0.1, 0.5, "Efficiency")) return 1;
    
    Vehicle vehicle(mass, width, height, length, efficiency);
    
    printLine();
    cout << "Enter Trip Parameters:" << endl;
    printLine();
    
    double distanceKm = getInput("Travel distance (km) [1-500]: ");
    if (!validateInput(distanceKm, 1, 500, "Distance")) return 1;
    
    double speedKmh = getInput("Initial speed (km/h) [10-200]: ");
    if (!validateInput(speedKmh, 10, 200, "Speed")) return 1;
    
    displayScenarioMenu();
    int scenario = getIntInput("Choose scenario (1-3): ");
    if (scenario < 1 || scenario > 3) {
        cout << "Invalid scenario selection!" << endl;
        return 1;
    }
    
    displayInputSummary(vehicle, distanceKm, speedKmh, scenario);
    
    cout << "Confirm and start simulation? (1 = Yes, 0 = No): ";
    int confirm;
    cin >> confirm;
    
    if (confirm != 1) {
        cout << "Simulation cancelled." << endl;
        return 0;
    }
    
    vector<SimulationData> results = runSimulation(vehicle, distanceKm, speedKmh, scenario);
    
    calculateAndDisplayStatistics(results);
    
    saveResultsToCSV(results, scenario);
    
    printLine();
    cout << "Run another scenario? (1 = Yes, 0 = No): ";
    int runAgain;
    cin >> runAgain;
    
    if (runAgain == 1) {
        cout << "\nPlease run the program again for another scenario.\n";
    }
    
    printLine();
    cout << "PROGRAM TERMINATED SUCCESSFULLY" << endl;
    printLine();
    
    return 0;
}