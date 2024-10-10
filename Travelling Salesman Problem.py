from functools import lru_cache

def solve_tsp(start):
    cities = 'abcdef'
    if start not in cities: return None, None, "Invalid starting city"
    
    dist = {('a','b'):10, ('a','f'):6, ('b','c'):19, ('b','e'):10, ('b','f'):15,
            ('c','d'):22, ('d','e'):5, ('e','f'):12}
    dist.update({(j,i):v for (i,j),v in dist.items()})
    
    idx = {c:i for i,c in enumerate(cities)}
    start_idx = idx[start]
    
    @lru_cache(None)
    def dp(mask, pos):
        if mask == (1 << len(cities)) - 1:
            return dist.get((cities[pos], start), float('inf'))
        return min((dist.get((cities[pos], cities[i]), float('inf')) + 
                   dp(mask | (1 << i), i) for i in range(len(cities)) 
                   if not mask & (1 << i)), default=float('inf'))
    
    def get_path():
        path, mask, pos = [start], 1 << start_idx, start_idx
        for _ in range(len(cities) - 1):
            pos = min(((i, dist.get((cities[pos], cities[i]), float('inf')) + 
                     dp(mask | (1 << i), i)) for i in range(len(cities)) 
                     if not mask & (1 << i)), key=lambda x: x[1])[0]
            path.append(cities[pos])
            mask |= 1 << pos
        return path + [start]

    min_cost = dp(1 << start_idx, start_idx)
    if min_cost == float('inf'): return None, None, "No valid route found"
    
    return get_path(), min_cost, None

def main():
    while True:
        print("\nWelcome to the Traveling Salesman Problem Solver!")
        print("This program finds the shortest route to visit all cities.")
        print("Available cities: a, b, c, d, e, f")
        start_city = input("Please enter your starting city: ").lower()
        
        route, distance, error = solve_tsp(start_city)
        
        if error:
            print(f"Error: {error}")
        else:
            print(f"\nBest route starting from city {start_city}:")
            print(" -> ".join(route))
            print(f"Total distance: {distance}")
        
        continue_choice = input("\nWould you like to try another city? (yes/no): ").lower()
        if continue_choice != 'yes' and continue_choice != 'y':
            print("Thank you for using the TSP Solver. Goodbye!")
            break 

if __name__ == "__main__":
    main()