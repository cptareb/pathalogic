def list_strip(data_list, target_value):
    start = 0
    end = len(data_list)

    # Move start index forward while target is matched
    while start < end and data_list[start] == target_value:
        start += 1

    # Move end index backward while target is matched
    while end > start and data_list[end - 1] == target_value:
        end -= 1

    # Return the stripped slice
    return data_list[start:end]