#Trips for Wednesday, January 3, 2024
import pickle

matrix = [[0, 36, 18, 18, 17, 4, 28, 43, 45, 22, 34, 3, 41, 44, 37, 34, 38, 35, 6, 43, 17, 4, 8, 36, 46, 46, 41, 36, 16, 38, 38, 36, 10, 18, 3, 17, 44, 45, 10, 17, 28, 16, 20, 45, 47, 5, 4, 36, 8, 28, 18, 7, 6, 28, 46, 42, 33, 36, 43, 17, 35, 18, 3, 17, 17], [37, 0, 29, 26, 45, 34, 45, 60, 62, 28, 39, 34, 64, 61, 60, 5, 39, 52, 33, 60, 27, 34, 31, 6, 69, 63, 64, 53, 28, 55, 54, 53, 31, 29, 34, 28, 61, 62, 28, 26, 45, 27, 30, 62, 70, 35, 35, 4, 31, 46, 28, 32, 34, 47, 63, 65, 5, 52, 60, 46, 4, 26, 34, 29, 29], [15, 28, 0, 7, 25, 13, 33, 48, 50, 9, 25, 13, 46, 49, 42, 27, 29, 40, 12, 47, 3, 13, 10, 27, 51, 51, 46, 40, 2, 43, 42, 41, 10, 2, 13, 2, 49, 50, 7, 5, 33, 2, 5, 50, 52, 14, 13, 27, 13, 33, 5, 11, 13, 32, 50, 47, 24, 40, 48, 25, 28, 9, 13, 3, 3], [17, 26, 7, 0, 26, 15, 35, 50, 51, 6, 23, 15, 43, 51, 39, 25, 27, 42, 14, 49, 6, 15, 12, 24, 48, 53, 43, 42, 7, 45, 44, 43, 12, 7, 15, 8, 51, 52, 9, 9, 35, 7, 5, 52, 49, 16, 15, 25, 15, 35, 5, 13, 15, 34, 52, 44, 22, 42, 50, 26, 26, 2, 15, 9, 9], [16, 45, 25, 25, 0, 16, 38, 46, 47, 22, 44, 17, 34, 50, 30, 43, 48, 44, 19, 48, 26, 17, 20, 44, 39, 46, 34, 45, 26, 47, 46, 45, 20, 25, 17, 24, 47, 49, 20, 26, 38, 26, 24, 50, 40, 16, 17, 44, 19, 36, 26, 20, 19, 35, 50, 35, 42, 44, 46, 3, 44, 27, 17, 24, 24], [4, 34, 16, 16, 17, 0, 26, 41, 43, 20, 32, 4, 41, 42, 37, 32, 36, 33, 4, 41, 15, 3, 6, 34, 46, 44, 41, 34, 14, 36, 35, 34, 11, 15, 4, 15, 42, 43, 11, 14, 26, 14, 18, 43, 46, 6, 5, 34, 6, 26, 16, 6, 4, 25, 43, 42, 31, 33, 41, 17, 33, 16, 4, 14, 15], [30, 46, 36, 35, 38, 27, 0, 23, 25, 40, 52, 30, 63, 24, 59, 44, 56, 19, 28, 23, 35, 28, 29, 47, 68, 26, 63, 19, 34, 22, 21, 20, 33, 35, 30, 35, 24, 25, 30, 34, 0, 34, 38, 25, 68, 30, 30, 47, 27, 4, 36, 29, 27, 5, 26, 64, 44, 19, 23, 35, 45, 36, 30, 34, 35], [44, 61, 50, 50, 46, 41, 23, 0, 2, 54, 66, 44, 71, 7, 67, 59, 70, 22, 43, 6, 49, 43, 43, 61, 76, 4, 71, 21, 48, 20, 26, 22, 47, 50, 44, 49, 5, 6, 45, 48, 23, 49, 52, 8, 76, 44, 44, 61, 42, 24, 50, 44, 42, 24, 8, 72, 59, 23, 0, 43, 60, 50, 44, 48, 49], [46, 62, 52, 52, 47, 43, 25, 3, 0, 56, 68, 46, 72, 9, 69, 61, 72, 24, 45, 7, 51, 45, 45, 63, 77, 5, 72, 23, 50, 22, 28, 24, 49, 52, 46, 51, 6, 8, 47, 50, 25, 51, 54, 9, 78, 46, 46, 63, 44, 26, 52, 46, 44, 26, 9, 73, 61, 25, 3, 45, 62, 52, 46, 50, 51], [22, 28, 9, 6, 23, 19, 39, 54, 56, 0, 25, 19, 40, 55, 36, 27, 29, 46, 19, 54, 9, 19, 16, 26, 45, 57, 40, 47, 10, 49, 48, 47, 16, 9, 19, 9, 55, 56, 14, 12, 39, 9, 6, 56, 46, 20, 20, 27, 20, 39, 7, 17, 19, 38, 57, 41, 24, 46, 54, 23, 28, 7, 19, 11, 11], [34, 39, 26, 22, 45, 32, 52, 67, 68, 25, 0, 32, 48, 68, 44, 39, 6, 59, 31, 66, 24, 32, 29, 38, 53, 70, 48, 59, 24, 61, 61, 60, 29, 26, 32, 25, 68, 69, 26, 25, 52, 23, 27, 69, 53, 33, 32, 39, 32, 52, 25, 30, 32, 51, 69, 48, 35, 59, 67, 45, 40, 23, 32, 26, 26], [3, 34, 16, 16, 17, 4, 28, 43, 45, 20, 32, 0, 41, 44, 37, 32, 36, 35, 3, 43, 15, 3, 5, 34, 46, 46, 41, 36, 14, 38, 37, 36, 8, 15, 0, 15, 44, 45, 8, 15, 28, 14, 18, 45, 46, 3, 1, 34, 8, 28, 16, 5, 6, 27, 45, 42, 31, 35, 43, 17, 33, 16, 0, 14, 15], [41, 65, 46, 43, 34, 41, 63, 71, 72, 40, 48, 41, 0, 74, 12, 64, 52, 69, 44, 73, 47, 42, 44, 63, 13, 71, 3, 69, 47, 72, 71, 70, 45, 46, 41, 46, 72, 73, 44, 49, 63, 47, 43, 75, 12, 41, 42, 63, 44, 61, 45, 45, 44, 60, 75, 8, 61, 69, 71, 34, 65, 45, 41, 50, 50], [45, 61, 51, 51, 49, 42, 24, 7, 9, 55, 67, 45, 74, 0, 71, 60, 71, 23, 43, 3, 50, 43, 44, 62, 79, 6, 74, 22, 49, 21, 27, 23, 48, 51, 45, 50, 4, 4, 46, 49, 24, 49, 53, 3, 80, 45, 45, 62, 43, 24, 51, 44, 43, 25, 5, 75, 59, 24, 7, 47, 60, 51, 45, 49, 50], [37, 60, 41, 39, 30, 37, 59, 67, 69, 36, 44, 37, 12, 71, 0, 60, 48, 65, 40, 69, 43, 38, 40, 59, 17, 68, 12, 65, 43, 67, 67, 65, 41, 42, 37, 42, 68, 70, 40, 45, 59, 43, 39, 71, 17, 37, 38, 59, 40, 58, 41, 41, 40, 57, 71, 12, 57, 65, 67, 30, 61, 41, 37, 44, 44], [35, 6, 29, 26, 44, 32, 44, 59, 61, 28, 39, 33, 64, 60, 60, 0, 39, 51, 32, 59, 27, 33, 30, 4, 69, 62, 64, 51, 27, 54, 53, 52, 30, 29, 33, 28, 60, 61, 27, 25, 44, 27, 30, 61, 70, 34, 33, 7, 30, 45, 28, 31, 33, 46, 61, 65, 5, 51, 59, 44, 3, 26, 33, 29, 28], [37, 40, 29, 25, 48, 35, 55, 69, 71, 28, 7, 35, 51, 70, 47, 40, 0, 62, 34, 69, 27, 34, 32, 39, 56, 72, 51, 62, 27, 64, 64, 62, 31, 29, 35, 28, 70, 72, 29, 28, 55, 26, 30, 71, 56, 36, 35, 40, 35, 55, 28, 32, 35, 54, 72, 51, 36, 62, 69, 48, 41, 25, 35, 28, 29], [36, 52, 42, 42, 45, 33, 19, 22, 24, 46, 58, 36, 69, 23, 65, 50, 62, 0, 34, 22, 41, 35, 35, 53, 74, 25, 69, 3, 40, 4, 7, 2, 39, 42, 36, 41, 23, 24, 37, 40, 19, 40, 44, 24, 75, 36, 36, 53, 34, 20, 42, 36, 34, 20, 25, 70, 50, 4, 22, 45, 51, 42, 36, 40, 41], [5, 33, 15, 15, 19, 4, 27, 42, 44, 19, 31, 4, 43, 43, 39, 31, 35, 34, 0, 42, 14, 3, 5, 33, 48, 45, 43, 34, 13, 37, 36, 35, 10, 15, 4, 14, 43, 44, 10, 13, 27, 13, 17, 44, 49, 6, 5, 33, 7, 27, 15, 4, 5, 26, 44, 44, 30, 34, 42, 19, 32, 15, 4, 13, 14], [44, 60, 50, 50, 48, 41, 22, 5, 7, 54, 66, 44, 73, 4, 69, 58, 70, 22, 42, 0, 49, 42, 43, 61, 78, 4, 73, 21, 48, 20, 25, 22, 47, 49, 44, 49, 2, 5, 44, 48, 22, 48, 52, 4, 78, 44, 44, 61, 42, 23, 50, 43, 41, 24, 5, 74, 58, 23, 5, 45, 59, 50, 44, 48, 49], [16, 27, 3, 6, 26, 14, 34, 49, 50, 9, 24, 14, 46, 50, 42, 26, 27, 41, 13, 48, 0, 14, 11, 25, 51, 52, 46, 41, 3, 43, 43, 42, 11, 4, 14, 3, 50, 51, 8, 7, 34, 1, 5, 50, 52, 15, 14, 26, 14, 34, 4, 12, 14, 33, 51, 47, 23, 41, 49, 27, 27, 7, 14, 5, 4], [4, 34, 16, 15, 17, 3, 27, 42, 44, 19, 31, 3, 41, 43, 37, 32, 35, 34, 3, 42, 14, 0, 6, 33, 46, 45, 41, 34, 13, 37, 36, 35, 10, 15, 3, 14, 43, 44, 10, 13, 27, 14, 17, 44, 47, 5, 3, 33, 7, 27, 16, 5, 4, 26, 44, 42, 31, 34, 42, 17, 33, 16, 3, 14, 14], [7, 32, 13, 13, 20, 6, 28, 43, 45, 17, 29, 5, 44, 44, 41, 30, 33, 35, 5, 43, 12, 5, 0, 31, 49, 46, 44, 36, 11, 38, 37, 36, 8, 13, 5, 12, 44, 45, 7, 11, 28, 12, 15, 45, 50, 7, 5, 31, 8, 28, 13, 3, 7, 27, 45, 45, 29, 35, 43, 20, 31, 13, 5, 12, 12], [37, 6, 28, 25, 46, 34, 46, 61, 62, 27, 39, 34, 64, 62, 60, 5, 39, 53, 34, 60, 27, 34, 32, 0, 69, 64, 64, 53, 27, 55, 55, 53, 31, 29, 34, 28, 62, 63, 29, 26, 46, 26, 29, 62, 69, 36, 35, 6, 31, 46, 27, 32, 35, 47, 63, 65, 5, 53, 61, 46, 5, 26, 34, 28, 28], [46, 70, 51, 48, 40, 46, 68, 76, 78, 45, 54, 46, 14, 80, 17, 69, 57, 74, 49, 78, 52, 47, 50, 69, 0, 77, 14, 74, 52, 77, 76, 75, 50, 51, 46, 52, 77, 79, 50, 55, 68, 52, 48, 80, 14, 46, 47, 69, 49, 67, 50, 50, 49, 66, 80, 8, 66, 74, 76, 39, 70, 50, 46, 55, 55], [47, 63, 53, 53, 46, 44, 26, 4, 5, 57, 69, 47, 71, 6, 67, 62, 73, 25, 46, 4, 52, 46, 46, 64, 76, 0, 71, 24, 51, 23, 29, 25, 50, 53, 47, 52, 3, 5, 48, 51, 26, 52, 55, 6, 76, 47, 47, 64, 45, 27, 54, 47, 45, 27, 6, 72, 62, 26, 4, 43, 63, 53, 47, 52, 52], [42, 66, 47, 44, 35, 42, 64, 72, 74, 41, 49, 42, 4, 76, 13, 65, 53, 70, 45, 74, 48, 43, 45, 64, 13, 72, 0, 70, 48, 73, 72, 71, 46, 47, 42, 47, 73, 75, 45, 51, 64, 48, 44, 76, 14, 42, 43, 65, 45, 63, 46, 46, 45, 62, 76, 9, 62, 70, 72, 35, 66, 46, 42, 51, 51], [36, 52, 42, 42, 45, 33, 19, 21, 23, 46, 58, 36, 69, 22, 65, 50, 62, 3, 34, 21, 41, 34, 35, 53, 74, 24, 69, 0, 40, 4, 6, 2, 39, 42, 36, 41, 22, 23, 36, 40, 19, 40, 44, 23, 74, 36, 36, 53, 34, 19, 42, 35, 33, 20, 23, 70, 50, 3, 21, 45, 51, 42, 36, 40, 41], [15, 28, 4, 8, 26, 13, 33, 48, 50, 10, 25, 13, 47, 49, 43, 27, 29, 40, 12, 48, 3, 13, 10, 27, 52, 51, 47, 40, 0, 43, 42, 41, 10, 3, 13, 3, 49, 50, 8, 5, 33, 2, 6, 50, 53, 14, 13, 27, 13, 33, 6, 11, 13, 32, 50, 48, 24, 40, 48, 26, 28, 9, 13, 5, 4], [38, 55, 45, 44, 47, 36, 21, 20, 22, 49, 61, 38, 71, 21, 68, 53, 64, 4, 37, 20, 43, 37, 37, 55, 76, 23, 71, 4, 42, 0, 9, 4, 41, 44, 38, 43, 21, 23, 39, 42, 21, 43, 47, 22, 77, 38, 38, 55, 36, 22, 45, 38, 36, 23, 23, 72, 53, 6, 20, 47, 54, 45, 38, 43, 43], [38, 54, 44, 44, 47, 35, 21, 26, 27, 48, 60, 38, 71, 27, 67, 53, 64, 7, 36, 25, 43, 37, 37, 55, 76, 29, 71, 7, 42, 9, 0, 7, 41, 44, 38, 43, 27, 28, 39, 42, 21, 42, 46, 28, 77, 38, 38, 55, 36, 22, 44, 38, 36, 22, 28, 72, 53, 6, 26, 47, 53, 44, 38, 42, 43], [36, 53, 42, 42, 45, 33, 19, 22, 24, 46, 58, 36, 69, 23, 65, 51, 62, 2, 35, 21, 41, 35, 35, 53, 74, 25, 69, 1, 40, 4, 7, 0, 39, 42, 36, 41, 23, 24, 37, 40, 19, 41, 44, 24, 75, 36, 36, 53, 34, 20, 43, 36, 34, 21, 24, 70, 51, 3, 22, 45, 52, 43, 36, 41, 41], [10, 30, 12, 12, 20, 10, 30, 45, 47, 16, 28, 8, 44, 46, 40, 29, 32, 37, 10, 44, 11, 10, 7, 30, 49, 48, 44, 37, 10, 40, 39, 38, 0, 11, 8, 11, 46, 47, 3, 9, 30, 10, 14, 47, 50, 8, 8, 30, 10, 30, 12, 8, 10, 29, 47, 45, 27, 37, 45, 20, 30, 12, 8, 11, 11], [16, 29, 2, 7, 25, 14, 34, 49, 51, 9, 26, 14, 46, 50, 42, 28, 30, 41, 13, 48, 4, 14, 11, 28, 51, 52, 46, 41, 3, 44, 43, 42, 11, 0, 14, 2, 50, 51, 8, 6, 34, 3, 5, 51, 52, 15, 14, 28, 14, 34, 5, 12, 14, 33, 51, 47, 25, 41, 49, 25, 29, 9, 14, 4, 4], [3, 34, 16, 16, 17, 4, 28, 43, 45, 20, 32, 0, 41, 44, 37, 32, 36, 35, 3, 43, 15, 3, 5, 34, 46, 46, 41, 36, 14, 38, 37, 36, 8, 15, 0, 15, 44, 45, 8, 15, 28, 14, 18, 45, 46, 3, 1, 34, 8, 28, 16, 5, 6, 27, 45, 42, 31, 35, 43, 17, 33, 16, 0, 14, 15], [15, 29, 3, 8, 24, 13, 33, 48, 50, 9, 25, 13, 46, 49, 42, 27, 29, 40, 12, 48, 3, 13, 10, 27, 51, 51, 46, 41, 2, 43, 42, 41, 11, 3, 13, 0, 49, 50, 8, 5, 33, 2, 5, 50, 52, 14, 13, 27, 13, 33, 5, 11, 13, 32, 50, 47, 24, 40, 48, 24, 28, 9, 13, 2, 2], [45, 61, 51, 50, 47, 42, 23, 5, 6, 55, 67, 44, 72, 4, 69, 59, 70, 23, 43, 2, 50, 43, 44, 62, 77, 4, 72, 21, 49, 21, 26, 23, 48, 50, 44, 49, 0, 4, 45, 48, 23, 49, 53, 4, 78, 45, 45, 62, 42, 24, 51, 44, 42, 25, 5, 73, 59, 24, 5, 45, 60, 51, 44, 49, 49], [46, 62, 52, 52, 48, 43, 25, 6, 8, 56, 68, 46, 74, 4, 70, 61, 72, 24, 44, 5, 51, 45, 45, 63, 79, 5, 73, 23, 50, 22, 28, 24, 49, 52, 46, 51, 5, 0, 47, 50, 25, 50, 54, 4, 79, 46, 46, 63, 44, 25, 52, 46, 44, 26, 3, 74, 61, 25, 6, 46, 62, 52, 46, 50, 51], [10, 28, 10, 9, 20, 10, 29, 44, 46, 14, 26, 8, 44, 45, 40, 26, 29, 36, 9, 44, 9, 9, 7, 28, 49, 47, 44, 37, 8, 39, 39, 37, 3, 9, 8, 8, 45, 46, 0, 7, 29, 8, 12, 46, 50, 8, 8, 28, 10, 29, 10, 8, 9, 29, 47, 45, 25, 37, 44, 20, 27, 10, 8, 9, 9], [16, 26, 8, 9, 27, 14, 34, 48, 50, 12, 25, 14, 50, 49, 46, 25, 29, 41, 13, 48, 7, 13, 11, 26, 55, 51, 50, 41, 6, 43, 43, 41, 10, 7, 14, 7, 49, 51, 7, 0, 34, 6, 10, 50, 55, 15, 14, 26, 14, 34, 9, 11, 14, 33, 51, 51, 23, 41, 48, 27, 26, 10, 14, 7, 7], [30, 46, 36, 35, 38, 27, 0, 23, 25, 40, 52, 30, 63, 24, 59, 44, 56, 19, 28, 23, 35, 28, 29, 47, 68, 26, 63, 19, 34, 22, 21, 20, 33, 35, 30, 35, 24, 25, 30, 34, 0, 34, 38, 25, 68, 30, 30, 47, 27, 4, 36, 29, 27, 5, 26, 64, 44, 19, 23, 35, 45, 36, 30, 34, 35], [16, 27, 4, 7, 26, 14, 33, 48, 50, 10, 24, 14, 47, 49, 43, 26, 27, 41, 13, 48, 1, 13, 11, 25, 52, 51, 47, 41, 2, 43, 43, 41, 10, 4, 14, 2, 49, 50, 8, 6, 33, 0, 5, 50, 53, 15, 14, 26, 14, 33, 4, 11, 13, 33, 51, 48, 23, 41, 48, 26, 27, 7, 14, 4, 4], [19, 29, 5, 5, 24, 17, 37, 52, 54, 5, 27, 17, 43, 53, 39, 29, 31, 44, 17, 52, 5, 17, 14, 28, 48, 55, 43, 45, 6, 47, 46, 45, 14, 5, 17, 6, 53, 54, 12, 9, 37, 5, 0, 54, 49, 17, 18, 28, 18, 37, 4, 15, 17, 36, 55, 44, 26, 44, 52, 24, 30, 7, 17, 8, 7], [45, 62, 52, 51, 50, 43, 24, 7, 9, 56, 68, 45, 75, 3, 71, 60, 71, 24, 44, 4, 50, 44, 45, 63, 80, 6, 75, 22, 49, 22, 27, 24, 48, 51, 45, 50, 4, 5, 46, 49, 24, 50, 54, 0, 80, 46, 45, 63, 43, 25, 52, 45, 43, 26, 5, 75, 60, 25, 7, 47, 61, 52, 45, 50, 50], [46, 70, 51, 48, 40, 46, 68, 76, 78, 46, 54, 46, 11, 80, 17, 69, 58, 74, 49, 78, 52, 47, 50, 69, 13, 77, 13, 74, 52, 77, 76, 75, 50, 51, 46, 52, 77, 79, 50, 55, 68, 52, 49, 80, 0, 46, 47, 69, 49, 67, 50, 50, 49, 66, 80, 14, 66, 74, 76, 39, 70, 50, 46, 55, 55], [4, 35, 17, 17, 16, 6, 28, 43, 45, 20, 33, 3, 40, 44, 36, 34, 37, 35, 6, 43, 17, 5, 7, 35, 45, 46, 40, 36, 15, 38, 37, 36, 8, 17, 3, 15, 44, 45, 8, 14, 28, 15, 17, 45, 46, 0, 4, 35, 10, 28, 17, 7, 8, 28, 46, 41, 32, 35, 43, 16, 35, 17, 3, 14, 14], [4, 35, 16, 16, 18, 5, 28, 43, 45, 20, 32, 2, 42, 44, 38, 33, 36, 36, 4, 43, 15, 4, 5, 34, 47, 46, 42, 36, 14, 38, 38, 36, 9, 16, 2, 15, 44, 45, 8, 15, 28, 15, 18, 45, 47, 4, 0, 34, 8, 28, 16, 5, 7, 28, 46, 43, 32, 36, 43, 18, 34, 16, 2, 14, 15], [37, 3, 28, 25, 46, 34, 46, 62, 64, 27, 38, 34, 64, 63, 60, 6, 39, 54, 34, 62, 26, 34, 32, 6, 69, 65, 64, 54, 27, 56, 56, 54, 31, 29, 34, 28, 63, 64, 29, 26, 46, 26, 29, 64, 69, 36, 35, 0, 31, 47, 27, 32, 34, 48, 64, 65, 4, 54, 62, 46, 5, 26, 34, 28, 28], [9, 31, 16, 15, 20, 6, 27, 42, 44, 19, 31, 8, 44, 43, 40, 29, 35, 34, 7, 41, 14, 7, 8, 31, 49, 45, 44, 34, 13, 37, 36, 35, 12, 15, 8, 14, 43, 44, 10, 13, 27, 14, 17, 44, 50, 10, 9, 31, 0, 27, 16, 8, 6, 26, 44, 45, 28, 34, 42, 20, 30, 16, 8, 14, 14], [29, 47, 35, 35, 36, 26, 4, 24, 26, 39, 51, 29, 61, 25, 58, 45, 55, 20, 27, 24, 34, 28, 28, 47, 66, 27, 61, 20, 33, 22, 22, 20, 32, 35, 29, 34, 25, 26, 30, 33, 4, 33, 37, 26, 67, 29, 29, 47, 27, 0, 35, 29, 27, 3, 26, 62, 45, 20, 24, 34, 46, 35, 29, 33, 34], [18, 28, 4, 5, 26, 16, 36, 50, 52, 8, 25, 16, 45, 51, 41, 27, 29, 43, 15, 50, 4, 15, 13, 27, 50, 53, 45, 43, 5, 45, 45, 43, 12, 5, 16, 5, 51, 53, 10, 9, 36, 4, 4, 52, 51, 17, 16, 27, 16, 36, 0, 13, 16, 35, 53, 46, 25, 43, 50, 26, 28, 6, 16, 7, 6], [7, 32, 14, 13, 20, 6, 28, 43, 45, 18, 30, 5, 44, 44, 40, 30, 33, 35, 4, 43, 12, 5, 3, 31, 49, 46, 44, 36, 11, 38, 37, 36, 8, 13, 5, 12, 44, 45, 8, 11, 28, 12, 16, 45, 50, 6, 5, 31, 8, 28, 14, 0, 7, 27, 45, 45, 29, 35, 43, 20, 31, 14, 5, 12, 12], [6, 34, 16, 16, 19, 4, 26, 41, 43, 20, 32, 6, 43, 42, 40, 33, 36, 33, 5, 41, 15, 4, 7, 34, 48, 44, 43, 34, 14, 36, 36, 34, 12, 16, 6, 15, 42, 43, 11, 14, 26, 14, 18, 43, 49, 8, 7, 34, 6, 26, 16, 7, 0, 26, 44, 44, 31, 34, 41, 19, 33, 16, 6, 14, 15], [28, 47, 34, 34, 35, 25, 5, 25, 27, 38, 50, 28, 60, 26, 57, 46, 54, 20, 27, 24, 33, 27, 27, 48, 66, 28, 60, 21, 32, 23, 23, 21, 31, 34, 28, 33, 26, 27, 29, 32, 5, 33, 36, 27, 66, 28, 28, 48, 26, 3, 35, 28, 26, 0, 27, 61, 46, 21, 25, 33, 47, 35, 28, 33, 33], [46, 62, 52, 52, 50, 43, 25, 7, 9, 56, 68, 46, 75, 4, 71, 61, 72, 24, 44, 5, 51, 45, 45, 63, 80, 6, 75, 23, 50, 22, 28, 24, 49, 52, 46, 51, 5, 3, 47, 50, 25, 50, 54, 5, 80, 46, 46, 63, 44, 25, 52, 46, 44, 26, 0, 75, 61, 25, 7, 47, 62, 52, 46, 50, 51], [42, 66, 47, 44, 36, 42, 64, 72, 74, 42, 50, 42, 10, 76, 13, 65, 53, 70, 45, 74, 48, 43, 46, 65, 8, 73, 10, 70, 48, 73, 72, 71, 46, 47, 42, 48, 73, 75, 46, 51, 64, 48, 45, 76, 14, 42, 43, 65, 45, 63, 46, 46, 45, 62, 76, 0, 62, 70, 72, 35, 66, 46, 42, 51, 51], [34, 5, 25, 22, 43, 31, 44, 59, 61, 24, 35, 31, 61, 60, 57, 5, 36, 51, 31, 59, 23, 31, 29, 4, 66, 62, 61, 51, 24, 54, 53, 52, 28, 26, 31, 25, 60, 61, 26, 23, 44, 23, 26, 61, 66, 33, 32, 4, 28, 45, 24, 29, 31, 45, 61, 62, 0, 51, 59, 43, 6, 23, 31, 25, 25], [36, 52, 42, 41, 44, 33, 18, 23, 25, 46, 58, 35, 69, 24, 65, 50, 62, 4, 34, 23, 41, 34, 35, 53, 74, 26, 69, 3, 40, 6, 6, 3, 39, 41, 35, 40, 24, 25, 36, 39, 18, 40, 44, 25, 74, 36, 36, 53, 33, 19, 42, 35, 33, 20, 25, 69, 50, 0, 23, 45, 51, 42, 35, 40, 40], [44, 61, 50, 50, 46, 41, 23, 0, 2, 54, 66, 44, 71, 7, 67, 59, 70, 22, 43, 6, 49, 43, 43, 61, 76, 4, 71, 21, 48, 20, 26, 22, 47, 50, 44, 49, 5, 6, 45, 48, 23, 49, 52, 8, 76, 44, 44, 61, 42, 24, 50, 44, 42, 24, 8, 72, 59, 23, 0, 43, 60, 50, 44, 48, 49], [17, 45, 25, 26, 4, 17, 36, 44, 45, 23, 45, 17, 34, 47, 30, 43, 48, 44, 19, 46, 27, 17, 20, 44, 39, 44, 34, 45, 27, 47, 47, 45, 20, 25, 17, 24, 45, 46, 20, 27, 36, 26, 24, 48, 40, 17, 18, 45, 20, 34, 26, 20, 19, 33, 48, 35, 42, 45, 44, 0, 44, 27, 17, 24, 24], [36, 4, 30, 26, 45, 33, 45, 60, 62, 28, 40, 34, 65, 61, 61, 3, 40, 52, 33, 60, 28, 34, 31, 5, 70, 63, 65, 52, 28, 55, 54, 53, 30, 30, 34, 29, 61, 62, 28, 26, 45, 27, 30, 62, 71, 35, 34, 6, 31, 46, 29, 32, 34, 46, 62, 66, 6, 52, 60, 45, 0, 27, 34, 30, 29], [17, 26, 8, 2, 27, 15, 35, 50, 52, 7, 23, 15, 44, 51, 40, 25, 27, 42, 14, 49, 7, 15, 12, 25, 49, 53, 44, 42, 7, 45, 44, 43, 12, 8, 15, 8, 51, 52, 9, 9, 35, 7, 7, 52, 50, 16, 15, 25, 15, 35, 6, 13, 15, 34, 52, 45, 22, 42, 50, 27, 26, 0, 15, 9, 10], [3, 34, 16, 16, 17, 4, 28, 43, 45, 20, 32, 0, 41, 44, 37, 32, 36, 35, 3, 43, 15, 3, 5, 34, 46, 46, 41, 36, 14, 38, 37, 36, 8, 15, 0, 15, 44, 45, 8, 15, 28, 14, 18, 45, 46, 3, 1, 34, 8, 28, 16, 5, 6, 27, 45, 42, 31, 35, 43, 17, 33, 16, 0, 14, 15], [16, 30, 4, 10, 24, 14, 34, 49, 50, 11, 26, 14, 48, 50, 44, 28, 30, 41, 13, 48, 4, 14, 11, 28, 53, 52, 48, 41, 4, 43, 43, 42, 11, 4, 14, 2, 50, 51, 8, 7, 34, 4, 7, 50, 53, 15, 14, 28, 14, 34, 7, 12, 14, 33, 51, 48, 25, 41, 49, 25, 29, 10, 14, 0, 2], [15, 28, 3, 8, 25, 13, 33, 48, 49, 10, 25, 13, 47, 49, 43, 26, 28, 40, 12, 47, 3, 13, 10, 26, 52, 51, 47, 40, 2, 43, 42, 41, 10, 3, 13, 1, 49, 50, 7, 5, 33, 3, 6, 50, 53, 14, 13, 27, 13, 33, 5, 11, 13, 32, 50, 48, 24, 40, 48, 25, 27, 9, 13, 3, 0]]

locations = [(-119.7955506, 36.3080387), (-119.5704632, 36.0942314), (-119.6554101, 36.3303066), (-119.6237299, 36.3380492), 
                         (-119.8490873, 36.4255948), (-119.8008192, 36.2977343), (-120.1022328, 36.1966597), (-120.3398708, 36.15156), 
                         (-120.3398121, 36.149349), (-119.6327801, 36.3612236), (-119.2913175, 36.3157652), (-119.7862348, 36.30631839999999), 
                         (-119.7631925, 36.7798332), (-120.357745, 36.133279), (-119.7929501, 36.7359653), (-119.5853202, 36.1067755), (-119.3117487, 36.2989252), 
                         (-120.129451, 36.0078362), (-119.783814, 36.3011433), (-120.3524123, 36.1382284), (-119.6484623, 36.3284855), (-119.7916385, 36.301749), 
                         (-119.7692494, 36.3008697), (-119.5764424, 36.1191005), (-119.7622379, 36.83903420000001), (-120.3505544, 36.1487252), (-119.7721444, 36.7832302), 
                         (-120.1317068, 36.0037319), (-119.6546605, 36.3267851), (-120.1415864, 36.0080062), (-120.1098246, 35.9891839), (-120.130624, 36.00523), (-119.7267228, 36.3059747), 
                         (-119.6565933, 36.3308329), (-119.7862348, 36.30631839999999), (-119.6582146, 36.3281217), (-120.356004, 36.14118930000001), (-120.3663847, 36.1397778), (-119.7153425, 36.3137698), 
                         (-119.6572954, 36.31528), (-120.1022328, 36.1966597), (-119.651048, 36.3272593), (-119.6485127, 36.3470397), (-120.3631648, 36.1303214), (-119.6625151, 36.8407241), (-119.7838819, 36.3164792), 
                         (-119.7831582, 36.3057842), (-119.5625239, 36.099222), (-119.7870479, 36.2765953), (-120.1025408, 36.2064141), (-119.6452757, 36.33657669999999), (-119.7732526, 36.3035439), (-119.7947591, 36.2908911), (-120.1024922, 36.2116704), 
                         (-120.3670827, 36.1353988), (-119.7810098, 36.8203357), (-119.5628077, 36.1127417), (-120.1233378, 36.0029657), (-120.3398708, 36.15156), (-119.8607957, 36.4287451), (-119.5803378, 36.1001729), (-119.6247834, 36.3311775), (-119.7862348, 36.30631839999999), 
                         (-119.6657674, 36.3270161), (-119.6599664, 36.3273481)]

def main():
    #Load the matrix into a pickle file
    with open('matrix.pkl', 'wb') as file:
        pickle.dump(matrix, file)

    #Load locations into a pickle file
    with open('locations.pkl', 'wb') as file:
        pickle.dump(locations, file)

    # Load the matrix from the binary file
    # with open('matrix.pkl', 'rb') as file:
    #     loaded_matrix = pickle.load(file)
        
if __name__ == '__main__':
    main()
