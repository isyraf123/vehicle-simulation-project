import csv
import math
import statistics
import matplotlib.pyplot as plt
import os
from matplotlib.gridspec import GridSpec

class SimulationData:
    def __init__(self):
        self.time = []
        self.speed = []
        self.acceleration = []
        self.drag = []
        self.rolling_resistance = []
        self.slope_resistance = []
        self.total_resistance = []
        self.fuel = []
        self.cumulative_fuel = []
        self.reynolds = []
        self.cd = []
        self.altitude = []
        self.slope = []
        
    def add_row(self, row):
        self.time.append(float(row[0]))
        self.speed.append(float(row[1]))
        self.acceleration.append(float(row[2]))
        self.drag.append(float(row[3]))
        self.rolling_resistance.append(float(row[4]))
        self.slope_resistance.append(float(row[5]))
        self.total_resistance.append(float(row[6]))
        self.fuel.append(float(row[7]))
        self.cumulative_fuel.append(float(row[8]))
        self.reynolds.append(float(row[9]))
        self.cd.append(float(row[10]))
        self.altitude.append(float(row[11]))
        self.slope.append(float(row[12]))
    
    def get_size(self):
        return len(self.time)

def print_separator():
    print("=" * 70)

def print_header(title):
    print_separator()
    print(f"  {title}")
    print_separator()

def load_csv_file(filename):
    data = SimulationData()
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                data.add_row(row)
        print(f"Successfully loaded {data.get_size()} data points from {filename}")
        return data
    except FileNotFoundError:
        print(f"ERROR: File {filename} not found.")
        return None

def calculate_basic_statistics(values):
    if len(values) == 0:
        return None
    stats = {
        'mean': statistics.mean(values),
        'median': statistics.median(values),
        'std': statistics.stdev(values) if len(values) > 1 else 0,
        'min': min(values),
        'max': max(values),
        'range': max(values) - min(values)
    }
    return stats

def calculate_total_distance(speed, time):
    distance = 0.0
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        distance += speed[i] * dt
    return distance

def calculate_average_fuel_consumption(cumulative_fuel, distance):
    if distance == 0:
        return 0
    total_fuel = cumulative_fuel[-1] if cumulative_fuel else 0
    return (total_fuel / distance) * 100000.0

def calculate_energy_efficiency(cumulative_fuel, distance):
    FUEL_ENERGY_DENSITY = 32.4
    if distance == 0 or not cumulative_fuel:
        return 0
    total_energy = cumulative_fuel[-1] * FUEL_ENERGY_DENSITY
    return distance / total_energy

def calculate_cost_estimation(cumulative_fuel, fuel_price_per_liter=1.5):
    if not cumulative_fuel:
        return 0
    return cumulative_fuel[-1] * fuel_price_per_liter

def calculate_co2_emissions(cumulative_fuel):
    CO2_PER_LITER = 2.31
    if not cumulative_fuel:
        return 0
    return cumulative_fuel[-1] * CO2_PER_LITER

def find_peak_consumption_period(fuel, time, window_size=100):
    if len(fuel) < window_size:
        return None
    
    max_consumption = 0
    max_index = 0
    
    for i in range(len(fuel) - window_size):
        window_consumption = sum(fuel[i:i+window_size])
        if window_consumption > max_consumption:
            max_consumption = window_consumption
            max_index = i
    
    return {
        'start_time': time[max_index],
        'end_time': time[max_index + window_size],
        'consumption': max_consumption
    }

def calculate_acceleration_metrics(acceleration):
    positive_acc = [a for a in acceleration if a > 0]
    negative_acc = [a for a in acceleration if a < 0]
    
    return {
        'avg_acceleration': statistics.mean(positive_acc) if positive_acc else 0,
        'avg_deceleration': statistics.mean(negative_acc) if negative_acc else 0,
        'max_acceleration': max(acceleration) if acceleration else 0,
        'max_deceleration': min(acceleration) if acceleration else 0
    }

def calculate_resistance_breakdown(drag, rolling, slope):
    total_drag = sum(drag)
    total_rolling = sum(rolling)
    total_slope = sum(abs(s) for s in slope)
    total = total_drag + total_rolling + total_slope
    
    if total == 0:
        return None
    
    return {
        'drag_percentage': (total_drag / total) * 100,
        'rolling_percentage': (total_rolling / total) * 100,
        'slope_percentage': (total_slope / total) * 100
    }

def calculate_correlation(x, y):
    if len(x) != len(y) or len(x) == 0:
        return 0
    
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
    denominator_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
    denominator_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))
    
    if denominator_x == 0 or denominator_y == 0:
        return 0
    
    return numerator / (math.sqrt(denominator_x) * math.sqrt(denominator_y))

def print_detailed_statistics(data):
    print_header("DETAILED STATISTICAL ANALYSIS")
    
    distance = calculate_total_distance(data.speed, data.time)
    
    print(f"\nDistance & Fuel Metrics:")
    print(f"  Total Distance: {distance / 1000:.3f} km")
    print(f"  Total Fuel Used: {data.cumulative_fuel[-1]:.3f} L")
    print(f"  Fuel Consumption: {calculate_average_fuel_consumption(data.cumulative_fuel, distance):.3f} L/100km")
    print(f"  Energy Efficiency: {calculate_energy_efficiency(data.cumulative_fuel, distance):.3f} km/MJ")
    print(f"  Estimated Cost: ${calculate_cost_estimation(data.cumulative_fuel):.2f}")
    print(f"  CO2 Emissions: {calculate_co2_emissions(data.cumulative_fuel):.3f} kg")
    
    speed_stats = calculate_basic_statistics(data.speed)
    print(f"\nSpeed Statistics (m/s):")
    print(f"  Mean: {speed_stats['mean']:.3f}")
    print(f"  Median: {speed_stats['median']:.3f}")
    print(f"  Std Dev: {speed_stats['std']:.3f}")
    print(f"  Min: {speed_stats['min']:.3f}")
    print(f"  Max: {speed_stats['max']:.3f}")
    
    acc_metrics = calculate_acceleration_metrics(data.acceleration)
    print(f"\nAcceleration Metrics (m/s²):")
    print(f"  Avg Acceleration: {acc_metrics['avg_acceleration']:.3f}")
    print(f"  Avg Deceleration: {acc_metrics['avg_deceleration']:.3f}")
    print(f"  Max Acceleration: {acc_metrics['max_acceleration']:.3f}")
    print(f"  Max Deceleration: {acc_metrics['max_deceleration']:.3f}")
    
    drag_stats = calculate_basic_statistics(data.drag)
    print(f"\nAerodynamic Drag Statistics (N):")
    print(f"  Mean: {drag_stats['mean']:.3f}")
    print(f"  Max: {drag_stats['max']:.3f}")
    print(f"  Std Dev: {drag_stats['std']:.3f}")
    
    reynolds_stats = calculate_basic_statistics(data.reynolds)
    print(f"\nReynolds Number Statistics:")
    print(f"  Mean: {reynolds_stats['mean']:.0f}")
    print(f"  Min: {reynolds_stats['min']:.0f}")
    print(f"  Max: {reynolds_stats['max']:.0f}")
    
    resistance_breakdown = calculate_resistance_breakdown(
        data.drag, data.rolling_resistance, data.slope_resistance
    )
    if resistance_breakdown:
        print(f"\nResistance Force Breakdown:")
        print(f"  Aerodynamic Drag: {resistance_breakdown['drag_percentage']:.1f}%")
        print(f"  Rolling Resistance: {resistance_breakdown['rolling_percentage']:.1f}%")
        print(f"  Slope Resistance: {resistance_breakdown['slope_percentage']:.1f}%")
    
    altitude_stats = calculate_basic_statistics(data.altitude)
    print(f"\nAltitude Profile (m):")
    print(f"  Max Elevation: {altitude_stats['max']:.2f}")
    print(f"  Min Elevation: {altitude_stats['min']:.2f}")
    print(f"  Elevation Change: {altitude_stats['range']:.2f}")
    
    peak_period = find_peak_consumption_period(data.fuel, data.time)
    if peak_period:
        print(f"\nPeak Consumption Period:")
        print(f"  Time Range: {peak_period['start_time']:.0f}s - {peak_period['end_time']:.0f}s")
        print(f"  Consumption: {peak_period['consumption']:.5f} L")
    
    print_separator()

def print_correlation_analysis(data):
    print_header("CORRELATION ANALYSIS")
    
    corr_speed_fuel = calculate_correlation(data.speed, data.fuel)
    corr_speed_drag = calculate_correlation(data.speed, data.drag)
    corr_reynolds_cd = calculate_correlation(data.reynolds, data.cd)
    corr_slope_fuel = calculate_correlation(data.slope, data.fuel)
    
    print(f"\nCorrelation Coefficients:")
    print(f"  Speed vs Fuel Consumption: {corr_speed_fuel:.3f}")
    print(f"  Speed vs Drag Force: {corr_speed_drag:.3f}")
    print(f"  Reynolds Number vs Cd: {corr_reynolds_cd:.3f}")
    print(f"  Slope vs Fuel Consumption: {corr_slope_fuel:.3f}")
    
    print(f"\nInterpretation:")
    if abs(corr_speed_fuel) > 0.7:
        print(f"  Strong correlation between speed and fuel consumption")
    if abs(corr_speed_drag) > 0.9:
        print(f"  Very strong correlation between speed and drag (expected)")
    if abs(corr_slope_fuel) > 0.5:
        print(f"  Moderate correlation between terrain slope and fuel use")
    
    print_separator()

def plot_comprehensive_analysis(data, scenario_name):
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(4, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(data.time, data.speed, 'b-', linewidth=1)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Speed (m/s)")
    ax1.set_title("Speed Profile")
    ax1.grid(True, alpha=0.3)
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(data.time, data.cumulative_fuel, 'r-', linewidth=1)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Cumulative Fuel (L)")
    ax2.set_title("Cumulative Fuel Consumption")
    ax2.grid(True, alpha=0.3)
    
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(data.time, data.drag, 'g-', linewidth=1, label='Aerodynamic')
    ax3.plot(data.time, data.rolling_resistance, 'orange', linewidth=1, label='Rolling')
    ax3.plot(data.time, [abs(s) for s in data.slope_resistance], 'purple', linewidth=1, label='Slope')
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Force (N)")
    ax3.set_title("Resistance Forces")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.plot(data.time, data.acceleration, 'b-', linewidth=1)
    ax4.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Acceleration (m/s²)")
    ax4.set_title("Acceleration Profile")
    ax4.grid(True, alpha=0.3)
    
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.plot(data.reynolds, data.cd, 'r.', markersize=1)
    ax5.set_xlabel("Reynolds Number")
    ax5.set_ylabel("Drag Coefficient")
    ax5.set_title("Cd vs Reynolds Number")
    ax5.grid(True, alpha=0.3)
    
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.plot(data.time, data.altitude, 'brown', linewidth=1)
    ax6.set_xlabel("Time (s)")
    ax6.set_ylabel("Altitude (m)")
    ax6.set_title("Altitude Profile")
    ax6.grid(True, alpha=0.3)
    
    ax7 = fig.add_subplot(gs[2, 0])
    ax7.hist(data.speed, bins=30, color='blue', alpha=0.7, edgecolor='black')
    ax7.set_xlabel("Speed (m/s)")
    ax7.set_ylabel("Frequency")
    ax7.set_title("Speed Distribution")
    ax7.grid(True, alpha=0.3)
    
    ax8 = fig.add_subplot(gs[2, 1])
    ax8.plot(data.speed, data.fuel, 'g.', markersize=1)
    ax8.set_xlabel("Speed (m/s)")
    ax8.set_ylabel("Fuel per Step (L)")
    ax8.set_title("Fuel Consumption vs Speed")
    ax8.grid(True, alpha=0.3)
    
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.hist(data.reynolds, bins=30, color='red', alpha=0.7, edgecolor='black')
    ax9.set_xlabel("Reynolds Number")
    ax9.set_ylabel("Frequency")
    ax9.set_title("Reynolds Number Distribution")
    ax9.grid(True, alpha=0.3)
    
    ax10 = fig.add_subplot(gs[3, 0])
    ax10.plot(data.time, data.total_resistance, 'purple', linewidth=1)
    ax10.set_xlabel("Time (s)")
    ax10.set_ylabel("Total Resistance (N)")
    ax10.set_title("Total Resistance Force")
    ax10.grid(True, alpha=0.3)
    
    ax11 = fig.add_subplot(gs[3, 1])
    resistance_breakdown = calculate_resistance_breakdown(
        data.drag, data.rolling_resistance, data.slope_resistance
    )
    if resistance_breakdown:
        labels = ['Aerodynamic', 'Rolling', 'Slope']
        sizes = [
            resistance_breakdown['drag_percentage'],
            resistance_breakdown['rolling_percentage'],
            resistance_breakdown['slope_percentage']
        ]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        ax11.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax11.set_title("Resistance Force Breakdown")
    
    ax12 = fig.add_subplot(gs[3, 2])
    speed_kmh = [s * 3.6 for s in data.speed]
    fuel_per_100km = []
    window = 100
    for i in range(len(data.fuel) - window):
        window_fuel = sum(data.fuel[i:i+window])
        window_distance = sum(data.speed[i:i+window]) * window / 100000.0
        if window_distance > 0:
            fuel_per_100km.append(window_fuel / window_distance)
        else:
            fuel_per_100km.append(0)
    
    if fuel_per_100km:
        ax12.plot(range(len(fuel_per_100km)), fuel_per_100km, 'b-', linewidth=1)
        ax12.set_xlabel("Time Window")
        ax12.set_ylabel("L/100km")
        ax12.set_title("Rolling Fuel Consumption")
        ax12.grid(True, alpha=0.3)
    
    fig.suptitle(f"Comprehensive Analysis - {scenario_name}", fontsize=16, fontweight='bold')
    plt.savefig(f"analysis_{scenario_name}.png", dpi=150, bbox_inches='tight')
    print(f"Comprehensive plot saved as: analysis_{scenario_name}.png")

def compare_scenarios():
    scenarios = []
    scenario_names = []
    
    for i in range(1, 4):
        filename = f"vehicle_simulation_scenario_{i}.csv"
        if os.path.exists(filename):
            data = load_csv_file(filename)
            if data:
                scenarios.append(data)
                scenario_names.append(f"Scenario {i}")
    
    if len(scenarios) < 2:
        print("Not enough scenarios to compare. Need at least 2 CSV files.")
        return
    
    print_header("SCENARIO COMPARISON")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    for i, data in enumerate(scenarios):
        axes[0, 0].plot(data.time, data.speed, label=scenario_names[i], linewidth=1)
    axes[0, 0].set_xlabel("Time (s)")
    axes[0, 0].set_ylabel("Speed (m/s)")
    axes[0, 0].set_title("Speed Comparison")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    for i, data in enumerate(scenarios):
        axes[0, 1].plot(data.time, data.cumulative_fuel, label=scenario_names[i], linewidth=1)
    axes[0, 1].set_xlabel("Time (s)")
    axes[0, 1].set_ylabel("Cumulative Fuel (L)")
    axes[0, 1].set_title("Fuel Consumption Comparison")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    for i, data in enumerate(scenarios):
        axes[1, 0].plot(data.time, data.drag, label=scenario_names[i], linewidth=1)
    axes[1, 0].set_xlabel("Time (s)")
    axes[1, 0].set_ylabel("Drag Force (N)")
    axes[1, 0].set_title("Drag Force Comparison")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    fuel_totals = [data.cumulative_fuel[-1] for data in scenarios]
    axes[1, 1].bar(scenario_names, fuel_totals, color=['blue', 'red', 'green'][:len(scenarios)])
    axes[1, 1].set_ylabel("Total Fuel (L)")
    axes[1, 1].set_title("Total Fuel Comparison")
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("scenario_comparison.png", dpi=150, bbox_inches='tight')
    print("Scenario comparison saved as: scenario_comparison.png")
    
    print("\nComparative Statistics:")
    for i, data in enumerate(scenarios):
        distance = calculate_total_distance(data.speed, data.time)
        fuel_consumption = calculate_average_fuel_consumption(data.cumulative_fuel, distance)
        print(f"\n{scenario_names[i]}:")
        print(f"  Total Fuel: {data.cumulative_fuel[-1]:.3f} L")
        print(f"  Fuel per 100km: {fuel_consumption:.3f} L/100km")
        print(f"  Distance: {distance / 1000:.3f} km")
        print(f"  Avg Speed: {statistics.mean(data.speed):.3f} m/s")
    
    print_separator()

def export_summary_report(data, scenario_name):
    filename = f"summary_report_{scenario_name}.txt"
    with open(filename, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write(f"SIMULATION SUMMARY REPORT - {scenario_name}\n")
        f.write("=" * 70 + "\n\n")
        
        distance = calculate_total_distance(data.speed, data.time)
        f.write(f"Total Distance: {distance / 1000:.3f} km\n")
        f.write(f"Total Fuel Used: {data.cumulative_fuel[-1]:.3f} L\n")
        f.write(f"Fuel Consumption: {calculate_average_fuel_consumption(data.cumulative_fuel, distance):.3f} L/100km\n")
        f.write(f"Estimated Cost: ${calculate_cost_estimation(data.cumulative_fuel):.2f}\n")
        f.write(f"CO2 Emissions: {calculate_co2_emissions(data.cumulative_fuel):.3f} kg\n\n")
        
        speed_stats = calculate_basic_statistics(data.speed)
        f.write(f"Average Speed: {speed_stats['mean']:.3f} m/s\n")
        f.write(f"Maximum Speed: {speed_stats['max']:.3f} m/s\n\n")
        
        f.write("Analysis completed successfully.\n")
    
    print(f"Summary report exported to: {filename}")

def main():
    print_header("ADVANCED VEHICLE SIMULATION ANALYSIS")
    
    scenario_files = []
    for i in range(1, 4):
        filename = f"vehicle_simulation_scenario_{i}.csv"
        if os.path.exists(filename):
            scenario_files.append((filename, f"Scenario_{i}"))
    
    if not scenario_files:
        print("ERROR: No simulation CSV files found.")
        print("Please run the C++ simulation first.")
        return
    
    print(f"\nFound {len(scenario_files)} scenario file(s)")
    
    for filename, scenario_name in scenario_files:
        print(f"\n{'=' * 70}")
        print(f"Processing: {filename}")
        print('=' * 70)
        
        data = load_csv_file(filename)
        if data is None:
            continue
        
        print_detailed_statistics(data)
        print_correlation_analysis(data)
        plot_comprehensive_analysis(data, scenario_name)
        export_summary_report(data, scenario_name)
    
    if len(scenario_files) > 1:
        compare_scenarios()
    
    plt.show()
    
    print_header("ANALYSIS COMPLETE")
    print("All plots and reports have been generated.")
    print("Check your working directory for output files.")

if __name__ == "__main__":
    main()