SEEDS = [
    {
        "Original_Sample": {
            "instruction": "Write a python function to find the maximum difference between two numbers in a given sorted array.",
            "response": "```python\\ndef max_diff(arr):\\n    return arr[-1] - arr[0]\\n```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I should change the key point condition: the sorted array->a given array, while use the same word in other part of the instruction as more as possible.",
            "Do some other change: min-max diff between two numbers->two even numbers.",
            "To generate a brand new output that can complete modified instruction, I will rename the function and variable, and use a different algorithm to implement the modified_instruction",
        ],
        "Modified_Sample": {
            "instruction": "Write a python function to find the maximum difference between even numbers in a given array.",
            "response": "```python\\ndef max_diff_even_numbers(arr):\\n    even_numbers = [num for num in arr if num % 2 == 0]\\n    return max(even_numbers) - min(even_numbers)```",
        },
    },
    {
        "Original_Sample": {
            "instruction": "Write a SQL query to find all the users in a database whose age greater than 25.",
            "response": "```SQL\\nSELECT *\\nFROM users\\nWHERE age > 25;\\n```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I changed the condition from finding users of a certain age to finding a specific demographic (male users) with a different age condition (less than 25 instead of greater than 25), while use the same word in other part of the instruction as more as possible.",
            "The modification also includes a change in the output requested: from a simple query listing users to calculating an aggregate statistic (average age) and a count of users that fit the criteria.",
            "To generate a brand new output that can complete modified instruction, I introduced new SQL functions (AVG() and COUNT()) and adjusted the WHERE clause to include a condition for gender, significantly altering both the query's structure and its purpose.",
        ],
        "Modified_Sample": {
            "instruction": "Write a SQL query to find all the male user's average age and their count in a database whose age less than 25.",
            "response": "```SQL\\nSELECT AVG(age) AS average_age, COUNT(*) AS user_count\\nFROM users\\nWHERE gender = 'male' AND age < 25;```",
        },
        "id": 1,
    },
    {
        "Original_Sample": {
            "instruction": "Write a python function to calculate the factorial of a number using recursion.",
            "response": "```python\\ndef factorial(n):\\n    if n == 1:\\n        return 1\\n    else:\\n        return n * factorial(n-1)\\n```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, the key operational task was changed from calculating a single factorial to calculating the sum of multiple factorials, indicating a shift in the complexity and scope of the problem, while use the same word in other part of the instruction as more as possible.",
            "Instead of using recursion directly, I will use a built-in Python module (math.factorial) to calculate individual factorials within a loop.",
            "To generate a brand new output that can complete modified instruction with changed algorithm structure, I will add a loop to iteratively calculate each factorial up to the given number and accumulate their sum.",
        ],
        "Modified_Sample": {
            "instruction": "Write a python function to calculate the sum of factorials of all numbers up to a given number inclusively.",
            "response": "```python\\nimport math\\n\\ndef sum_of_factorials(n):\\n    total = 0\\n    for i in range(1, n + 1):\\n        total += math.factorial(i)\\n    return total```",
        },
        "id": 2,
    },
    {
        "Original_Sample": {
            "instruction": "Create a JavaScript function that reverses a string.",
            "response": "```javascript\\nfunction reverseString(s) {\\n    return s.split('').reverse().join('');\\n}```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I will change it from manipulating a single string, I should transition from reversing the entire string to reversing each word independently while preserving their sequence, while use the same word in other part of the instruction as more as possible.",
            "Incorporate additional operations to handle the revised focus: splitting the string into words, reversing each word individually, and then reassembling the words into a single string.",
            "To create a tailored output for the modified instruction, I will rename the function to reflect its new purpose, and implement a different approach that applies the reverse operation to each word in the string rather than the string as a whole.",
        ],
        "Modified_Sample": {
            "instruction": "Create a JavaScript function that reverses every word in a string but keeps their order.",
            "response": "```javascript\\nfunction reverseWords(sentence) {\\n    return sentence.split(' ').map(word => word.split('').reverse().join('')).join(' ');\\n}```",
        },
        "id": 3,
    },
    {
        "Original_Sample": {
            "instruction": "Write a C++ program to find the largest number in a list.",
            "response": "```cpp\\n#include <iostream>\\n#include <vector>\\nusing namespace std;\\nint findLargest(vector<int>& nums) {\\n    int largest = nums[0];\\n    for(int num : nums) {\\n        if(num > largest) largest = num;\\n    }\\n    return largest;\\n}```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I will change the key point condition: largest number to the second largest number, while use the same word in other part of the instruction as more as possible.",
            "To achieve the new goal, the list needs to be sorted to easily identify the second largest number, introducing a new method (sorting) not used in the original solution.",
            "To generate a brand new output that can complete modified instruction, I will adjust the function name and the inclusion of the algorithm header (for sort) to reflect the changes in functionality and methodology.",
        ],
        "Modified_Sample": {
            "instruction": "Write a C++ program to find the second largest number in a list.",
            "response": "```cpp\\n#include <iostream>\\n#include <vector>\\n#include <algorithm>\\nusing namespace std;\\nint findSecondLargest(vector<int>& list) {\\n    sort(list.begin(), list.end());\\n    return list[list.size() - 2];\\n}```",
        },
        "id": 4,
    },
    {
        "Original_Sample": {
            "instruction": "Design a SQL query to find the highest salary in a company.",
            "response": "```SQL\\nSELECT MAX(salary) AS HighestSalary\\nFROM employees;```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I will alter the required_variables to find the third highest salary instead of the highest, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I will use a different algorithm from `MAX` in orginal: LIMIT with an offset (2, 1) that allows the query to skip the first two highest salaries and return the next one.",
        ],
        "Modified_Sample": {
            "instruction": "Design a SQL query to find the third highest salary in a company.",
            "response": "```SQL\\nSELECT DISTINCT salary \\nFROM employees \\nORDER BY salary DESC \\nLIMIT 2, 1;```",
        },
        "id": 5,
    },
    {
        "Original_Sample": {
            "instruction": "Develop a function in Python to return whether a number is prime.",
            "response": "```python\\ndef isprime(n):\\n    if n <= 1:\\n        return False\\n    elif n <= 3:\\n        return True\\n    elif n % 2 == 0 or n % 3 == 0:\\n        return False\\n    i = 5\\n    while i * i <= n:\\n        if n % i == 0 or n % (i + 2) == 0:\\n            return False\\n        i += 6\\n    return True```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I should take the orignal functionality as a subprocedure and include a new task: find the next factorial, while use the same word in other part of the instruction as more as possible."
            "The solution introduces an iterative approach that starts from the number immediately after the given number and checks each subsequent number for primality until the next prime is found.",
            "To generate a brand new output that can complete modified instruction, I will use a different algorithm to check primality and rename the function `isprime(n)` to `is_prime(num)`",
        ],
        "Modified_Sample": {
            "instruction": "Develop a function in Python to return the next prime number after a given number.",
            "response": "```python\\ndef next_prime(n):\\n    def is_prime(num):\\n        if num <= 1:\\n            return False\\n        for i in range(2, int(num**0.5) + 1):\\n            if num % i == 0:\\n                return False\\n        return True\\n    next_num = n + 1\\n    while not is_prime(next_num):\\n        next_num += 1\\n    return next_num```",
        },
        "id": 6,
    },
    {
        "Original_Sample": {
            "instruction": "Write a JavaScript function to check if a string is a palindrome.",
            "response": "```javascript\\nfunction isPalindrome(str) {\\n    return str == str.split('').reverse().join('');\\n}```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I will introduces a preprocessing step to clean the string, expanded the original task of checking if a string is a palindrome to include ignoring spaces, punctuation, and case, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I incorporated the use of the replace function with a regular expression (/[^A-Za-z0-9]/g) to remove unwanted characters and the toLowerCase method to standardize the case.",
        ],
        "Modified_Sample": {
            "instruction": "Write a JavaScript function to check if a string is a palindrome, ignoring spaces, punctuation, and case.",
            "response": "```javascript\\nfunction isPalindrome(str) {\\n    let cleaned = str.replace(/[^A-Za-z0-9]/g, '').toLowerCase();\\n    return cleaned == cleaned.split('').reverse().join('');\\n}```",
        },
        "id": 7,
    },
    {
        "Original_Sample": {
            "instruction": "Implement a Python function to find the factorial of a number.",
            "response": "```python\\ndef factorial(n):\\n    if n == 0:\\n        return 1\\n    else:\\n        return n * factorial(n-1)```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I should take the orignal functionality as a subprocedure and include a new task: sum the factorial, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I will use a library function instead of hand-writing function to calculate fractorial, and introduce a loop to sum them all.",
        ],
        "Modified_Sample": {
            "instruction": "Implement a Python function to find the sum of the series 1!+2!+...+n!.",
            "response": "```python\\nimport math\\ndef sum_of_series(n):\\n    return sum(math.factorial(i) for i in range(1, n+1))```",
        },
        "id": 8,
    },
    {
        "Original_Sample": {
            "instruction": "Write a function in Java to reverse an array.",
            "response": "```java\\npublic static void reverseArray(int[] array) {\\n    for(int i = 0; i < array.length / 2; i++) {\\n        int temp = array[i];\\n        array[i] = array[array.length - i - 1];\\n        array[array.length - i - 1] = temp;\\n    }\\n}```",
        },
        "Reasoning": [
            "To modify the instruction slight in wording but significant in meaning, I should change the algorithm relevant to the instruction from reversing array to rotating array, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I will change the function signature from `void reverseArray(int[] array)` to `void rotateArrayByOne(int[] arr)`, and implement a rotation algorithm.",
        ],
        "Modified_Sample": {
            "instruction": "Write a function in Java to cyclically rotate an array by one position to the right.",
            "response": "```java\\npublic static void rotateArrayByOne(int[] arr) {\\n    int last = arr[arr.length - 1];\\n    for(int i = arr.length - 1; i > 0; i--) {\\n        arr[i] = arr[i - 1];\\n    }\\n    arr[0] = last;\\n}```",
        },
        "id": 9,
    },
    {
        "Original_Sample": {
            "instruction": "Implement a C++ function to reverse a string.",
            "response": "```c++\\nvoid reverseString(std::string& str) {\\n    std::reverse(str.begin(), str.end());\\n}```",
        },
        "Reasoning": [
            "To modify the instruction slightly in wording but significantly in meaning, I will change the key object operated in the orignal instruction: from a string to the words within a sentence, while use the same word in other part of the instruction as more as possible.",
            "Furthermore, I will add a new condition: keeping the order of word while changing the letter-order.",
            "To generate a brand new output that can complete modified instruction, I will employ the std::istringstream class to iterate over words in the sentence, utilizes the std::reverse function from the standard library to reverse each word individually, and concatenates these reversed words into a new sentence.",
        ],
        "Modified_Sample": {
            "instruction": "Implement a C++ function to reverse the words in a sentence without changing their order.",
            "response": '```c++\\nvoid reverseWords(std::string &sentence) {\\n    std::istringstream iss(sentence);\\n    std::string word;\\n    std::string reversedSentence = "";\\n    while (iss >> word) {\\n        std::reverse(word.begin(), word.end());\\n        reversedSentence += word + " ";\\n    }\\n    sentence = reversedSentence.substr(0, reversedSentence.length() - 1);\\n}```',
        },
        "id": 10,
    },
    {
        "Original_Sample": {
            "instruction": "Create a Python function that takes a list of numbers and returns a new list with each number squared if it is even, and cubed if it is odd. The function should ignore non-numeric values in the list and maintain the order of the original elements. The function signature should be `def transform_list(input_list: List[Union[int, float]]) -> List[Union[int, float]]`.",
            "response": "```python\\nfrom typing import List, Union\\n\\ndef transform_list(input_list: List[Union[int, float]]) -> List[Union[int, float]]:\\n    return [x**2 if x % 2 == 0 else x**3 for x in input_list if isinstance(x, (int, float))]\\n```",
        },
        "Reasoning": [
            "To modify the instruction slightly in wording but significantly in meaning, I introduces a conditional approach to data processing, expanding the task to not only transform each number in the list based on its parity but also to replace non-numeric values with None, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I incorporated mathematical operations to replace even numbers with their factorial and odd numbers with their Fibonacci equivalent, introducing the use of the math.factorial function and a custom fibonacci function for these calculations.",
        ],
        "Modified_Sample": {
            "instruction": "Create a Python function that takes a list of numbers and returns a new list with each number replaced by its factorial if it is even, and its Fibonacci equivalent if it is odd. Non-numeric values in the list should be replaced by None, and the order of the original elements must be preserved. The function signature should be `def transform_list(input_list: List[Union[int, float]]) -> List[Union[int, float, None]]`.",
            "response": "```python\\nfrom typing import List, Union\\nimport math\\n\\ndef fibonacci(n):\\n    if n <= 1:\\n        return n\\n    else:\\n        return fibonacci(n-1) + fibonacci(n-2)\\n\\ndef transform_list(input_list: List[Union[int, float]]) -> List[Union[int, float, None]]:\\n    new_list = []\\n    for x in input_list:\\n        if isinstance(x, (int, float)):\\n            if x % 2 == 0:\\n                new_list.append(math.factorial(int(x)))\\n            else:\\n                new_list.append(fibonacci(int(x)))\\n        else:\\n            new_list.append(None)\\n    return new_list\\n```",
        },
        "id": 11,
    },
    {
        "Original_Sample": {
            "instruction": "Implement a JavaScript function that takes a string and reverses its characters. The function signature should be `function reverseString(s){ }`.",
            "response": "```javascript\\nfunction reverseString(s) {\\n    return s.split('').reverse().join('');\\n}\\n```",
        },
        "Reasoning": [
            "To modify the instruction slightly in wording but significantly in meaning, I will change the object operated in orignal algorithm and add more condition, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I will change the function signature from `function reverseString(s)` to `function reverseEverySecond(s)` and implement the new algorithm.",
        ],
        "Modified_Sample": {
            "instruction": "Implement a JavaScript function that takes a string and returns a new string with every second character reversed. Non-alphabetic characters should be ignored but kept in their original position. The function signature should be `function reverseEverySecond(s){ }`.",
            "response": "```javascript\\nfunction reverseEverySecond(s) {\\n    let result = s.split('');\\n    let letters = result.filter(char => /[a-zA-Z]/.test(char));\\n    for (let i = 1; i < letters.length; i += 2) {\\n        result[result.indexOf(letters[i])] = letters[letters.length - 1 - ((i - 1) / 2)];\\n    }\\n    return result.join('');\\n}\\n```",
        },
        "id": 13,
    },
    {
        "Original_Sample": {
            "instruction": "Write a SQL query to find all employees who earn more than $50,000. Assume the table is named `employees` and has columns `id`, `name`, and `salary`. The SQL query should use `WHERE` over the salary column.",
            "response": "```sql\\nSELECT * FROM employees WHERE salary > 50000;\\n```",
        },
        "Reasoning": [
            "To modify the instruction slightly in wording but significantly in meaning, I will change the key point condition: `earn more than $50,000` -> `find the top 3 employees with the highest salaries`, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I will use `RANK` as a new algorithm in modified SQL.",
        ],
        "Modified_Sample": {
            "instruction": "Write a SQL query to find the top 3 employees with the highest salaries. Assume the table is named `employees` and has columns `id`, `name`, and `salary`. Include a rank for them based on their salary. The SQL query should use `RANK()` over the salary column.",
            "response": "```sql\\nSELECT id, name, salary, RANK() OVER (ORDER BY salary DESC) as rank FROM employees ORDER BY salary DESC LIMIT 3;\\n```",
        },
        "id": 14,
    },
    {
        "Original_Sample": {
            "instruction": "Write a Java method that takes an array of integers and finds the maximum value. The method signature should be `public static int findMax(int[] array)`.",
            "response": "```java\\npublic static int findMax(int[] array) {\\n    int max = array[0];\\n    for(int i = 1; i < array.length; i++) {\\n        if(array[i] > max) {\\n            max = array[i];\\n        }\\n    }\\n    return max;\\n}```",
        },
        "Reasoning": [
            "To modify the instruction slightly in wording but significantly in meaning, I will change the key point condition: `the maximum value` -> `second maximum value`, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I will change the function signature from `int findMax(int[] array)` to `int findSecondMax(int[] arr)`.",
        ],
        "Modified_Sample": {
            "instruction": "Write a Java method that takes an array of integers and finds the second maximum value. Assume the array has at least two distinct values. The method signature should be `public static int findSecondMax(int[] array)`.",
            "response": "```java\\npublic static int findSecondMax(int[] arr) {\\n    int max = Integer.MIN_VALUE;\\n    int secondMax = Integer.MIN_VALUE;\\n    for(int val : arr) {\\n        if(val > max) {\\n            secondMax = max;\\n            max = val;\\n        } else if(val > secondMax && val != max) {\\n            secondMax = val;\\n        }\\n    }\\n    return secondMax;\\n}```",
        },
        "id": 15,
    },
    {
        "Original_Sample": {
            "instruction": "Develop a C# method that calculates and returns the sum of all even numbers between 1 and 100, inclusive. The method signature should be `public static int SumEvenNumbers()`.",
            "response": "```c#\\npublic static int SumEvenNumbers() {\\n    int sum = 0;\\n    for(int i = 2; i <= 100; i += 2) {\\n        sum += i;\\n    }\\n    return sum;\\n}```",
        },
        "Reasoning": [
            "To modify the instruction slightly in wording but significantly in meaning, I will change the key point condition: `even numbers ` -> `prime numbers`, while use the same word in other part of the instruction as more as possible.",
            "Furthermore, I will ask for a pointed algorithm: Sieve of Eratosthenes algorithm, which will lead to a more different output.",
            "To generate a brand new output that can complete modified instruction, I will implement the new algorithm and change the name of variable from `sum` to `s`.",
        ],
        "Modified_Sample": {
            "instruction": "Develop a C# method that calculates and returns the sum of all prime numbers between 1 and 100, inclusive. Use the Sieve of Eratosthenes algorithm for finding primes. The method signature should be `public static int SumPrimeNumbers()`.",
            "response": "```c#\\npublic static int SumPrimeNumbers() {\\n    bool[] prime = new bool[101];\\n    for(int i = 0; i < prime.Length; i++) prime[i] = true;\\n    for(int p = 2; p*p <= 100; p++) {\\n        if(prime[p] == true) {\\n            for(int i = p*p; i <= 100; i += p) prime[i] = false;\\n        }\\n    }\\n    int s = 0;\\n    for(int i = 2; i <= 100; i++) {\\n        if(prime[i]) s += i;\\n    }\\n    return s;\\n}```",
        },
        "id": 16,
    },
    {
        "Original_Sample": {
            "instruction": "Design a JavaScript function that takes an array of numbers and returns the average. Assume the array is not empty. The function signature should be `function calculateAverage(arr){ }`.",
            "response": "```javascript\\nfunction calculateAverage(array) {\\n    return array.reduce((acc, val) => acc + val, 0) / array.length;\\n}\\n```",
        },
        "Reasoning": [
            "To modify the instruction slightly in wording but significantly in meaning, I will change focus from `average` to `median`, while use the same word in other part of the instruction as more as possible.",
            "To generate a brand new output that can complete modified instruction, I will implement the new algorithm and change the name of variable from `array` to `arr`.",
        ],
        "Modified_Sample": {
            "instruction": "Design a JavaScript function that takes an array of numbers and returns the median. Assume the array is not empty and contains an odd number of elements. The function signature should be `function calculateMedian(arr){ }`.",
            "response": "```javascript\\nfunction calculateMedian(arr) {\\n    arr.sort((a, b) => a - b);\\n    return arr[Math.floor(arr.length / 2)];\\n}\\n```",
        },
        "id": 17,
    },
]
SEEDS_LEN = len(SEEDS)


def format_seeds(seed_ids):
    import json
    formatted_strings = (
        "- Original_Samples:\n"
        "{org}\n"
        "- Reasonings:\n"
        "{reason}\n"
        "- Modified_Samples:\n"
        "{ctf}\n"
    )
    seeds = [SEEDS[i] for i in seed_ids]
    prompt = ""
    for seed in seeds:
        prompt += formatted_strings.format(
            org=json.dumps(seed["Original_Sample"], indent=2),
            reason=json.dumps(seed["Reasoning"], indent=2),
            ctf=json.dumps(seed["Modified_Sample"], indent=2)
        )
    return prompt



if __name__ == "__main__":
    print(format_seeds(range(SEEDS_LEN), check=True))