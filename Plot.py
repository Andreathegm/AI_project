import os
os.environ["NUMEXPR_MAX_THREADS"] = "16"
import matplotlib.pyplot as plt


def plot_differences(bruteforce_list, jta_list, file, iterations):
    if len(bruteforce_list) != len(jta_list):
        raise ValueError("Both lists must have the same length")

    if not bruteforce_list:  # Evita errori con liste vuote
        raise ValueError("Input lists cannot be empty")

    differences = [abs(a - b) for a, b in zip(bruteforce_list, jta_list)]

    x_values = list(range(1, len(bruteforce_list) + 1))

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, differences, marker='o', color='b', label="Error", linestyle='None')
    plt.xlabel("ith pair of Q,E")
    plt.ylabel(f"Mean error (n = {iterations})")
    plt.title(f"Probability mean error for {os.path.splitext(os.path.basename(file))[0]}.bif")
    plt.grid(True)

    plt.xticks(x_values, x_values)  # Mostra solo numeri interi

    min_diff, max_diff = min(differences), max(differences)
    margin = max(abs(min_diff), abs(max_diff)) * 0.1 if max_diff != min_diff else 1e-10
    plt.ylim(min_diff - margin, max_diff + margin)

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    save_dir = os.path.join(os.getcwd(), "plots")
    os.makedirs(save_dir, exist_ok=True)  # Create folder if it doesn't exist
    file_name = os.path.splitext(os.path.basename(file))[0]
    save_path = os.path.join(save_dir, f"{file_name}.png")

    plt.savefig(save_path, dpi=600)
    plt.close()

    print(f"✅ Plot saved at: {os.path.abspath(save_path)}")  # Mostra il path assoluto


def save_values_to_text(bruteforce_list, jta_list, file, iterations, formattedQs,formattedEvidences):
    # Create a cross-platform directory to save the text file
    file_name = os.path.splitext(os.path.basename(file))[0]
    save_dir = os.path.join(os.getcwd(), "results")
    os.makedirs(save_dir, exist_ok=True)  # Create folder if it doesn't exist
    save_path = os.path.join(save_dir, f"{file_name}.txt")

    # Save the values
    with open(save_path, 'w') as f:
        f.write(f"Results for {file_name}.bif\n\n")
        if iterations != 1:
            f.write("Mean value for each pair of Q,E\n\n")
        for i, (bf, jta) in enumerate(zip(bruteforce_list, jta_list), start=1):
            f.write(f"brute force--> P({formattedQs[i-1]}|{formattedEvidences[i-1]}) : {bf}\n")
            f.write(f"JTA--> P({formattedQs[i-1]}|{formattedEvidences[i-1]}) : {jta}\n")
            print("\n")

    print(f"Results saved at: {save_path}")
