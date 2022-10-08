"""
name: rileyounga
date: 10/8/2022
description:
    This program solves nonograms using the union of all valid permutations
license: None
"""
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def image_to_nonogram(image):
    """
    Convert an image to a 2d list of 0's and 1's corresponding to black and white
    portions of the image.
    :param image: 
    :return: 2d list of 0's and 1's
    """
    width, height = image.size
    nonogram = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            if pixel[0] > 230 and pixel[1] > 230 and pixel[2] > 230:
                row.append(0)
            else:
                row.append(1)
        nonogram.append(row)
    return nonogram


def nonogram_decomposer(nonogram):
    """
    Decompose a nonogram into a list of rows and columns
    returns two lists of lists containing the solution
    to the nonogram
    :param nonogram: 2d list of 0's and 1's
    :return: rows, cols
    """
    rows = []
    cols = []
    for row in nonogram:
        rows.append(decompose(row))
    for i in range(len(nonogram[0])):
        col = []
        for row in nonogram:
            col.append(row[i])
        cols.append(decompose(col))
    return rows, cols


def decompose(vector):
    """
    Helper function to decompose a row or column into a list of numbers
    :param vector: 
    :return: list of numbers
    """
    decomposed = []
    count = 0
    for i in range(len(vector)):
        if vector[i] == 1:
            count += 1
        elif vector[i] == 0 and count > 0:
            decomposed.append(count)
            count = 0
    if count > 0:
        decomposed.append(count)
    if len(decomposed) == 0:
        decomposed.append(0)
    return decomposed


def nonogram_solver(rows, cols):
    """
    Solve a nonogram using the union of all valid permutations
    :param rows: 
    :param cols: 
    :return: 2d solved grid
    """
    width = len(cols)
    height = len(rows)
    # create a width by height grid of all 2's
    grid = [[2] * width for i in range(height)]
    while True:
        i = 0
        for row in rows:
            # TODO check if row is solved, if so skip
            grid[i] = permute_union(row, width, grid[i])
            i += 1
        i = 0
        for col in cols:
            col_pos = permute_union(col, height, [x[i] for x in grid])
            for j in range(height):
                grid[j][i] = col_pos[j]
            i += 1
        # plot_grid(grid)
        if check(grid):
            break
    return grid


def permute_union(vector, length, grid_vector):
    """
    Find the union of all valid permutations of the vector in a list
    of length length while taking into account the list of grid_vector 0's and 1's
    :param vector: 
    :param length: 
    :param grid_vector: 
    :return: a function call to union
    """
    vsum = sum(vector)
    raw_perm = raw_permute(length, length - vsum, vsum)
    valid_perm = valid(raw_perm, vector, grid_vector)
    return union(valid_perm)


def raw_permute(length, num_0, num_1):
    """
    Generate all permutations of a list of length: length
    with num_0 0's and num_1 1's
    :param length: 
    :param num_0: 
    :param num_1: 
    :return: 2d list of permutations
    """
    if length == 0:
        return [[]]
    if num_0 == 0:
        return [[1] * length]
    if num_1 == 0:
        return [[0] * length]
    return [[0] + x for x in raw_permute(length - 1, num_0 - 1, num_1)] + [[1] + x for x in
                                                                           raw_permute(length - 1, num_0, num_1 - 1)]


def valid(perm, vector, grid_vector):
    """
    Filter out all permutations that do not match the vector
    and the grid_vector
    :param perm: 
    :param vector: 
    :param grid_vector: 
    :return: 2d list of valid permutations
    """
    permutations = []
    for v in perm:
        j = 0
        # counting keeps track if the previous elements were 1's
        counting = False
        cur_num = vector[j]
        valid_perm = True
        count = 0
        for i in range(len(v)):
            # if it doesn't match the grid_vector
            if v[i] == 1 and grid_vector[i] == 0:
                valid_perm = False
                break
            elif v[i] == 0 and grid_vector[i] == 1:
                valid_perm = False
                break
            # start counting if the current element is 1
            elif v[i] == 1 and not counting:
                counting = True
                count = 1
            elif v[i] == 1 and counting:
                count += 1
                # if you pass the current number in the vector then
                # the permutation is invalid
                if count > cur_num:
                    counting = False
                    valid_perm = False
                    break
            elif v[i] == 0 and counting:
                if count < cur_num:
                    # if the count of 1's so far is less than the current number
                    # in the vector then the permutation is invalid
                    counting = False
                    valid_perm = False
                    break
                else:
                    counting = False
                    j += 1
                    if j < len(vector):
                        cur_num = vector[j]
        if count < cur_num:
            # check again at the end of the permutation
            valid_perm = False
        if j < len(vector) - 1:
            valid_perm = False
        if valid_perm:
            permutations.append(v)
    return permutations


def union(perm):
    """
    Find the union of all permutations in perm
    :param perm: 
    :return: 1d list of the union
    """
    final_list = []
    if len(perm) == 1:
        return perm[0]
    # iterate through every permutation
    # for each element in the permutation check if every permutation
    # has that element in the same position
    # if so add it to the final list
    for i in range(len(perm[0])):
        same = True
        for j in range(1, len(perm)):
            if perm[j][i] != perm[0][i]:
                same = False
                break
        if same:
            final_list.append(perm[0][i])
        else:
            final_list.append(2)
    return final_list


def check(grid):
    """
    Check if the grid is solved
    :param grid: 
    :return: Boolean
    """
    for row in grid:
        for col in row:
            if col == 2:
                return False
    return True


def plot_grid(grid):
    """
    Plot the grid using matplotlib
    :param grid: 
    :return: 
    """
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap='Greys', interpolation='nearest')
    plt.show()


def main():
    image = Image.open('image1.jpg') # enter image name here
    # image.show()
    nonogram = image_to_nonogram(image)
    # plot_grid(nonogram)
    rows, cols = nonogram_decomposer(nonogram)
    # sample 10 x 10 nonogram
    rows_10 = [[2], [2, 1, 1], [4, 2], [2, 2, 4], [8], [9], [9], [7], [1, 1], [2, 2]]
    cols_10 = [[1], [3, 2], [3, 4], [1, 6, 1], [9], [4], [5, 1], [7], [6], [6]]
    # sample 15 x 15 nonogram
    rows_15 = [[8], [2, 2], [1, 1], [3, 3], [1, 11], [1, 11], [13], [11], [9], [3], [1, 5], [8, 1], [1, 3, 3], [7, 1], [11]]
    cols_15 = [[0], [5], [1, 1, 2, 1, 1], [1, 6, 3, 1], [1, 5, 1, 2], [1, 5, 2, 2], [1, 11], [1, 11], [1, 11], [1, 5, 2, 2],
           [1, 5, 2], [2, 6, 1], [1, 5, 1, 1], [5, 3], [1]]
    # sample 20 x 20 nonogram
    rows_20 = [[2], [2], [1], [1, 3, 1], [1, 2, 2, 1], [2, 5, 2, 1], [2, 2, 2, 3], [3, 7, 3], [3, 2, 3, 1], [3, 10, 1],
           [2, 3, 9, 1], [2, 2, 7, 2, 1], [2, 2, 7, 2, 2], [4, 7, 4], [2, 5, 1, 1], [3, 3, 2], [3, 3, 2], [5], [2, 2], [7]]
    cols_20 = [[2], [7], [7], [2, 1], [6], [2, 7], [2, 2, 2, 1], [2, 2, 1, 3, 1, 2], [2, 8, 1, 1], [2, 1, 1, 11, 1],
           [4, 1, 1, 9, 1], [1, 1, 1, 9, 1], [2, 1, 6, 1, 1], [2, 2, 5, 1, 2], [2, 2, 2, 1], [2, 8], [1, 4], [3, 2],
           [3, 2], [7]]
    grid = nonogram_solver(rows_15, cols_15)
    plot_grid(grid)


if __name__ == '__main__':
    main()
