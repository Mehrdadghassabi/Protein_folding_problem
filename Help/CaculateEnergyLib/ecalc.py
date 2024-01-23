# Module for energy calculation algorithm
import numpy as np
import math as math

# First, computes the leftmost all-by-all sum in the given formula, including the flag 
# function implemented by a mask matrix, to compute the Van-der-Waals energy.
def vdw(df):
    # Pull out and format arrays to convert to processed matrices.
    x = np.array(df["X"]).astype(float)
    y = np.array(df["Y"]).astype(float)
    z = np.array(df["Z"]).astype(float)
    sigma = np.array(df["Sigma"]).astype(float)
    epsilon = np.array(df["Epsilon"]).astype(float)
    charge = np.array(df["Charge"]).astype(float)
    combined = np.array(df["Combined"])
    
    # Returns a euclidean distance matrix between all pairs of atoms given the X, 
    # Y, and Z coordinates for each atom.
    def distance(x=x, y=y, z=z):
        x_matrix = np.subtract.outer(x, x).T
        y_matrix = np.subtract.outer(y, y).T
        z_matrix = np.subtract.outer(z, z).T
        distance_matrix = np.sqrt(np.square(x_matrix) 
                                  + np.square(y_matrix) 
                                  + np.square(z_matrix))
        return distance_matrix

    # Returns a symmetrical matrix of the sigma value. 
    def sigma(sigma=sigma):
        sigma_matrix = np.add.outer(sigma, sigma)
        sigma_matrix = np.divide(sigma, 2)
        return sigma_matrix

    # Returns a simmetrical matrix of the epsilon value for all pairs of atoms. 
    def epsilon(epsilon=epsilon):
        epsilon_matrix = np.multiply.outer(epsilon,epsilon)
        epsilon_matrix = np.sqrt(epsilon)
        return epsilon_matrix

    # Returns an element-wise multiplication matrix of the electrostatic charge for all pairs of atoms
    def charge(charge=charge):
        charge_matrix = np.multiply.outer(charge,charge)
        return charge_matrix
    
    # Returns a matrix where each index of the input dataframe is paired with
    # each element of the "Combined" column to insert zeros into a TRUE matrix, 
    # creating a mask matrix.
    def mask(df):
        nrow = df.shape[0]
        mask_matrix = np.full((nrow, nrow), 1)
        for i in range(nrow):
            x = combined[i]
            if x:
                for j in range(len(x)):
                    y = x[j]
                    mask_matrix[i,y] = 0
        return mask_matrix
    
    # Combine each sub matrix and process with the flag operator
    sigma_div_dist = np.divide(sigma(), distance())
    charge_div_dist = np.divide(charge(), distance())
    # Combine each subcalculation
    part1 = np.multiply(epsilon(), 
                    (np.power(sigma_div_dist, 12.0) - 
                     np.multiply(np.power(sigma_div_dist, 6.0), 2.0)))
    part2 = np.multiply(charge_div_dist, 
                        (1.0 / (4.0 * math.pi * 8.8541878128E-12 * 4.0)))
    flag = mask(df)
    vdw_matrix = part1 + part2
    # Apply the flag operator using the mask matrix.
    vdw_processed = np.multiply(flag, vdw_matrix)
    # Since the matrix is symmetrical along the diagonal k=0, make all values including the diagonal zero to count all pairs once.
    vdw_trimmed = np.triu(vdw_processed, k=1)
    # Return this correctly zeroed matrix.
    return vdw_trimmed
    
# Returns the solvation energy as a sum of the element-wise product of the
# approximate atomic solvation parameter and accessable surface area.
def solvation(df):
    asa = np.array(df["R"]).astype(float)
    asp = np.array(df["ASP"]).astype(float)
    const = (0.2 * 4.0 * math.pi)
    asa = np.square(asa + 1.4).astype(float)
    asa = np.multiply(asa, const)
    solvation = np.multiply(asa, asp)
    return solvation

# Currently computes the energy of one input protein object. Full implementation will 
# take a list of protein objects and output a properly formatted text file. 
def energy(df):
    with np.errstate(divide='ignore', invalid='ignore'):
        # Calculate histogram
        vdw_energies = vdw(df)
        solvation_energies = solvation(df)
        # Protein energy is the sum of Van-der-Waals and Solvation energies/
        energy = np.sum(vdw_energies) + np.sum(solvation_energies)
        # Convert the vdw matrix into a 1d list of numbers to visualize the distribution of energies using histograms. 
        vdw_energies = np.triu_indices(len(vdw_energies), 1)
        return energy, vdw_energies, solvation_energies