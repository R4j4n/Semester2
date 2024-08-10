def merge(nums1, m, num2, n):
    x, y = m - 1, n - 1

    for p in range(m + n - 1, -1, -1):
        if y < 0:
            break
        if x >= 0 and nums1[x] > num2[y]:
            nums1[p] = nums1[x]
            x -= 1
        else:
            nums1[p] = num2[y]
            y -= 1

    return nums1


nums1 = [1, 2, 3, 0, 0, 0]
nums2 = [2, 5, 6]
m, n = 3, 3

print(merge(nums1, m, nums2, n))
