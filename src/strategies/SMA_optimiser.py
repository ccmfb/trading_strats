from strategies.SMA import SMA

import pandas as pd

def calculate_pnl(data, short_window: int, long_window: int, initial_cash: float = 1000000) -> float:
    """
    Calculate the profit and loss of the SMA strategy with given parameters.

    Args:
        initial_cash (float): Initial cash available for trading.
        short_window (int): Short window for SMA.
        long_window (int): Long window for SMA.

    Returns:
        float: Final portfolio value after executing the strategy.
    """

    sma_strategy = SMA(short_window, long_window)
    _ = sma_strategy.execute(data)

    pnl = sma_strategy.pnl(initial_cash)

    return pnl


def find_min_hill_climbing(
        data: pd.DataFrame,
        short_window: int, 
        long_window: int,
        step_size: int = 1,
        max_iterations: int = 100,
        ) -> tuple:
    """
    Find the optimal short and long SMA windows using hill climbing.

    Args:
        short_window (int): Initial short window for SMA.
        long_window (int): Initial long window for SMA.
        step_size (int): Step size for hill climbing.
        max_iterations (int): Number of iterations for optimization.

    Returns:
        tuple: Optimal short and long SMA windows.
    """

    print(f"Starting optimization with short_window={short_window}, long_window={long_window}")
    print(f'PnL: {calculate_pnl(data, short_window, long_window):.2f}')
    print('-'*50)

    for _ in range(max_iterations):
        current_pnl = calculate_pnl(data, short_window, long_window)

        # Check neighbors
        neighbors = [
            (short_window + step_size, long_window),
            (short_window - step_size, long_window),
            (short_window, long_window + step_size),
            (short_window, long_window - step_size)
        ]

        best_neighbor = None
        best_pnl = current_pnl

        for neighbor in neighbors:
            pnl = calculate_pnl(data, *neighbor)
            if pnl > best_pnl:
                best_pnl = pnl
                best_neighbor = neighbor

        if best_neighbor is None or best_pnl <= current_pnl:
            print("No better neighbor found, stopping optimization.")
            break

        short_window, long_window = best_neighbor
        short_window = max(1, short_window)
        long_window = max(short_window + 1, long_window)
        print(f"New short_window={short_window}, long_window={long_window}, PnL={best_pnl:.2f}")    

    print('-'*50)
    print(f"Optimized short_window={short_window}, long_window={long_window}")
    print(f'Final PnL: {calculate_pnl(data, short_window, long_window):.2f}')       

    return int(short_window), int(long_window)  


def find_min_hill_climbing_expand(
        data: pd.DataFrame,
        short_window: int, 
        long_window: int,
        max_radius: int = 5,
        ) -> tuple:
    """
    Find the optimal short and long SMA windows using hill climbing.

    Args:
        short_window (int): Initial short window for SMA.
        long_window (int): Initial long window for SMA.
        step_size (int): Step size for hill climbing.
        max_iterations (int): Number of iterations for optimization.

    Returns:
        tuple: Optimal short and long SMA windows.
    """

    print(f"Starting optimization with short_window={short_window}, long_window={long_window}")
    print(f'PnL: {calculate_pnl(data, short_window, long_window):.2f}')
    print('-'*50)

    radius = 1
    while radius <= max_radius:
        current_pnl = calculate_pnl(data, short_window, long_window)

        # hollow square of neighbors
        neighbors = []
        for i in range(-radius, radius + 1):

            if short_window + i <= 0:
                continue

            if i == -radius or i == radius:
                for j in range(-radius, radius + 1):

                    if long_window + j <= short_window + i:
                        continue

                    neighbors.append((short_window + i, long_window + j))

            else:
                if long_window - radius > short_window + i:
                    neighbors.append((short_window + i, long_window - radius))
                    neighbors.append((short_window + i, long_window + radius))
            


        best_neighbor = None
        best_pnl = current_pnl

        for neighbor in neighbors:
            pnl = calculate_pnl(data, *neighbor)
            if pnl > best_pnl:
                best_pnl = pnl
                best_neighbor = neighbor

        if best_neighbor is not None:
            short_window, long_window = best_neighbor
            short_window = max(1, short_window)
            long_window = max(short_window + 1, long_window)
            print(f"Found better neighbor: {best_neighbor} with PnL={best_pnl:.2f}")
        else:
            print(f"No better neighbor found at radius {radius}, increasing radius.")
            radius += 1

    print('-'*50)
    print(f"Optimized short_window={short_window}, long_window={long_window}")
    print(f'Final PnL: {calculate_pnl(data, short_window, long_window):.2f}')       

    return int(short_window), int(long_window)  

