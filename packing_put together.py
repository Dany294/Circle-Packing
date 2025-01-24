import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import scipy as sp
from numba import njit


#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


n = 25 #number of points
num_iter = 100 #number of iterations for the minimization process
n_trials = 10 #number of repetitions for the optimization
initial_m = 10
final_m = 2*10**2

vector_of_ms = np.array(range(initial_m,final_m,40)) #this stores the values of m (m is a power in the optimization process) for the optimization


#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


# A vector of 2n angles is created, this is x_p,y_p; non-constrained
def create_points(n):
    coords = np.zeros(2*n)
    for i in range(n):
        coords[i] =  2 * np.pi *np.random.rand() 
        coords[i + n] = 2 * np.pi *np.random.rand() 
    return coords

# This creates the matrix of distances (symmetric)
@njit
def Distances(points,n): 
    # Matrix of distances
    distances = np.zeros((n,n))
    
    x_p = points[0:n]
    y_p = points[n: 2*n]
    
    for i in range(n):
        for j in range(n):
            distances[i][j] = ( np.sin( x_p[i] ) - np.sin( x_p[j] ) )**2 + ( np.sin( y_p[i] ) - np.sin( y_p[j] ) )**2   #this is distance squared
    return distances

# The energy function as defined by Numerla and Ostregaard: E = sum ( lambda / distance_ij ) ** m
@njit
def Energy(points , m , lambd , n ): 
    E = 0
    delta = 1e-6 #avoids division by zero
    distances = Distances(points,n)
    count = 0
    for i in range( n ):
        for j in range( i + 1 , n ): #this running of indices avoids double counting
            E += ( lambd / ( distances[i][j] + delta ) )**m
            count+=1
    return E

# Picks the lambda from the distances matrix. Lambda is as defined in the paper : Lambda = min(distance_ij)
@njit
def Lambd(distances):
    lambd = 10 #this is arbitrary, just the start
    for i in range( n ):
        for j in range( i + 1 , n ):
            if lambd > distances[i][j]:
                lambd = distances[i][j] #distances are already squared
    return lambd


#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


# Definition of the gradient for the minimization process
@njit
def Gradient( points , m, lambd , n ):
    grad = np.zeros(2*n)
    delta = 1e-6 
    x_p = points[0:n]
    y_p = points[n: 2*n]
    distances = Distances(points,n)
    
    for i in range( n ):
        entry_x = 0
        entry_y = 0
        for j in range( n ):
            if i!=j:
                factor = ( lambd/ (distances[i][j] + delta) ) ** (m+1)
                entry_x += -  m * factor * np.cos( x_p[i] ) * ( np.sin( x_p[i] ) - np.sin( x_p[j] ) ) /lambd 
                entry_y += -  m * factor * np.cos( y_p[i] ) * ( np.sin( y_p[i] ) - np.sin( y_p[j] ) ) /lambd 
        grad[i] = entry_x
        grad[i+n] = entry_y
    return grad

#--------------------------------------------------------------------------------------------

# Minimization process using Truncated Newton Method
def Evolution( n , n_trials , num_iter , vector_of_ms ):
    initial_points = create_points(n)
    best_configuration = [initial_points]
    for i in range(n_trials):
        points = best_configuration[-1]
        for m in vector_of_ms:
            dist = Distances(points,n)
            lambd = Lambd(dist)
            res = sp.optimize.minimize(
                Energy, 
                points, 
                args=(m, lambd,n), 
                method='TNC', 
                jac=Gradient, 
                options={'maxfun': num_iter, 'disp': False})
            result = res.x
            points = result
        best_configuration.append(result)
    final_configuration = best_configuration[-1]
    return final_configuration

result = Evolution(n , n_trials , num_iter , vector_of_ms)


#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


# Picks a vector of 2n components and decomposes it into 2 other vectors, x's and y's
def Separation(points): 
    x = points[0:n]
    y = points[n: 2*n]
    return x,y

# Creates n points out of the vectors of x's and y's 
def Point_assembly(x,y): 
    row = []
    for i in range(len(x)):
        aux = [ x[i] , y[i] ]
        row.append(aux)
    return row

# Computes a vector of distances, this is aimed to work on a vector of points
def distance(new_points):
    distances = []
    new_points = np.array(new_points)
    for i in range(n) : # n is the number of points
        for j in range ( i + 1 , n , 1):
            distance_ij = np.linalg.norm( new_points[i] - new_points[j] )
            distances.append(distance_ij)
    return distances

# Changes vectors of points from the arbitrary coords to the constrained ones
def coord_change(array_with_points): 
    new_points = []
    for point in array_with_points:
        restricted_coords = [ np.sin( point[0] ) , np.sin( point[1] )]
        new_points.append(restricted_coords)
    return np.array( new_points )
    

#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


separated_coords = Separation(result)
Vector_with_points = Point_assembly(separated_coords[0],separated_coords[1])

Constrained_points = coord_change(Vector_with_points)
coordinates = Constrained_points

distances = distance(Constrained_points)
min_distance = min(distances)
radius = min_distance / 2

print("The obtained radius is",radius)

#--------------------------------------------------------------------------------------------

fig, ax = plt.subplots()

# Creates the circles centered at the points of the final configuration
for coord in coordinates:
    circle = plt.Circle((coord[0], coord[1]), radius=radius, fill=False, edgecolor='blue')
    ax.add_patch(circle)

# Limits of the plot
x_coords, y_coords = zip(*coordinates)
x_min, x_max = - radius - 1, radius + 1
y_min, y_max = - radius - 1, radius + 1

# Plots the box containing the circles
rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=False, edgecolor='red', linestyle='--', linewidth=2)
ax.add_patch(rect)

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal', adjustable='datalim')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Packing Configuration')
plt.grid(True)
plt.show()