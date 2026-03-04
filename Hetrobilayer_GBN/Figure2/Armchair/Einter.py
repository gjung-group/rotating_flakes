import numpy as np

data_directory = "*************************************/Peratom"

data_parameters = {
    "AA": {
        "filename": "energy100.dat",
        "E_substrate": -904484.306789182,
        "E_flake": -405946.404924603,
        "num_atoms": 60901
    },
}

for key, params in data_parameters.items():
    filename = params["filename"]
    E_substrate = params["E_substrate"]
    E_flake = params["E_flake"]
    num_atoms = params["num_atoms"]
    file_path = f"{data_directory}/{filename}"

    try:
        data = np.genfromtxt(file_path)

        if data.ndim == 1:
            print(f"Data in {filename} is one-dimensional; please check the file format.")
            continue

        twist = data[:, 0]
        total_energy = data[:, 1]

        E_inter = total_energy - E_substrate - E_flake
        E_inter_per_atom = E_inter / (2 * num_atoms)

        result_data = np.column_stack((twist, E_inter_per_atom))

        output_filename = f"{data_directory}/E_inter_{filename}"
        np.savetxt(output_filename, result_data, fmt="%.6f", comments="")
        print(f"Calculated E_inter per atom and saved to {output_filename}")

    except IOError:
        print(f"Error: File '{filename}' not found or could not be read.")
    except Exception as e:
        print(f"An error occurred with file '{filename}': {e}")

