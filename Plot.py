import os
os.environ["NUMEXPR_MAX_THREADS"] = "16"
import matplotlib.pyplot as plt


def plot_differences(bruteforce_list, jta_list, file):
    if len(bruteforce_list) != len(jta_list):
        raise ValueError("Both lists must have the same length")

    # Compute differences
    differences = [a - b for a, b in zip(bruteforce_list, jta_list)]

    # X-axis: indices from 1 to len(list1)
    x_values = list(range(1, len(bruteforce_list) + 1))

    # Create plot
    plt.figure(figsize=(8, 5))
    plt.plot(x_values, differences, marker='o', color='b', label="Error")
    plt.xlabel("ith pair of Q and E")
    plt.ylabel("Error")
    plt.title("Probability Error")
    plt.legend()
    plt.grid(True)

    # Adjust y-axis scale for maximum precision visibility
    min_diff, max_diff = min(differences), max(differences)
    margin = (max_diff - min_diff) * 0.1 if max_diff != min_diff else 1e-10
    plt.ylim(min_diff - margin, max_diff + margin)

    # Enable scientific notation for small differences
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    # Create a cross-platform directory to save the plot
    file_name = os.path.splitext(os.path.basename(file))[0]
    save_dir = os.path.join(os.getcwd(), "plots")
    os.makedirs(save_dir, exist_ok=True)  # Create folder if it doesn't exist
    save_path = os.path.join(save_dir, f"{file_name}.png")

    # Save the plot
    plt.savefig(save_path, dpi=600)
    plt.close()

    print(f"Plot saved at: {save_path}")


