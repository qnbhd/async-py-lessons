def average_cor():
    nums_count, nums_sum, nums_average = 0, 0, None
    while True:
        try:
            current_num = yield nums_average
        except StopIteration:
            pass
        else:
            nums_sum += current_num
            nums_count += 1
            nums_average = round(nums_sum / nums_count, 2)

