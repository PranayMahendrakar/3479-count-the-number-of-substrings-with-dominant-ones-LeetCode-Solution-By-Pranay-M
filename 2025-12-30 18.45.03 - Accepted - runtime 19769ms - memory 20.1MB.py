class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        n = len(s)
        result = 0
        
        # Precompute prefix sum of ones
        ones_prefix = [0] * (n + 1)
        for i in range(n):
            ones_prefix[i + 1] = ones_prefix[i] + (1 if s[i] == '1' else 0)
        
        # For each number of zeros z from 0 to sqrt(n)
        # We need ones >= z^2, i.e., ones >= z*z
        # Total length = ones + z, so ones = length - z
        # Condition: length - z >= z*z => length >= z*z + z
        
        for z in range(int(n**0.5) + 2):
            # Find all substrings with exactly z zeros
            zero_positions = [-1]  # positions where zeros occur (add -1 as boundary)
            for i in range(n):
                if s[i] == '0':
                    zero_positions.append(i)
            zero_positions.append(n)  # add n as boundary
            
            if z == 0:
                # Count substrings with all ones
                # For each consecutive sequence of ones
                i = 0
                while i < n:
                    if s[i] == '1':
                        j = i
                        while j < n and s[j] == '1':
                            j += 1
                        length = j - i
                        result += length * (length + 1) // 2
                        i = j
                    else:
                        i += 1
            else:
                # For exactly z zeros, iterate through all combinations
                m = len(zero_positions)
                for i in range(1, m - z):
                    # zeros are at indices i to i+z-1 in zero_positions
                    left_zero = zero_positions[i]
                    right_zero = zero_positions[i + z - 1]
                    
                    # Left boundary: must include left_zero, can start from zero_positions[i-1]+1
                    # Right boundary: must include right_zero, can end at zero_positions[i+z]-1
                    
                    min_left = zero_positions[i - 1] + 1
                    max_right = zero_positions[i + z] - 1
                    
                    # For substring [l, r], length = r - l + 1
                    # ones = length - z = r - l + 1 - z
                    # Need: ones >= z*z => r - l + 1 - z >= z*z => r - l + 1 >= z*z + z
                    min_length = z * z + z
                    
                    # l ranges from min_left to left_zero
                    # r ranges from right_zero to max_right
                    # length = r - l + 1 >= min_length => r >= l + min_length - 1
                    
                    for l in range(min_left, left_zero + 1):
                        # r >= max(right_zero, l + min_length - 1) and r <= max_right
                        r_min = max(right_zero, l + min_length - 1)
                        if r_min <= max_right:
                            result += max_right - r_min + 1
        
        return result