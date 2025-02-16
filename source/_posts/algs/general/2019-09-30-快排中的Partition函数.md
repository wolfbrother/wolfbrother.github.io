---
dtindex: 2019-09-30快排中的Pa
title: 快排中的Partition函数
categories: 刷题
tags:  [partition]
author: wolfbrother
date: 2019-09-30 
---

### 快排算法与partition函数

#### 快排算法的递归形式：

```python
def quicksort(nums, l, r):
    if l >= r:
        return
    k = partition(nums, l, r)
    quicksort(nums, l, k - 1)
    quicksort(nums, k + 1, r)
```

#### 快排算法的非递归形式

+ 使用了栈

```python
def quicksort(nums, l, r):
    stack = [(l, r)]
    while len(stack) > 0:
        l, r = stack.pop(-1)
        if l >= r:
            continue
        ix = partition3(nums, l, r)
        stack.append((ix+1, r))
        stack.append((l, ix-1))
```

#### partition函数

其中partition函数输入参数是一个数组nums和两个位置索引`l`和`r`，输出为位置索引k。需要满足：

+ $l\le k \le r$
+ $nums[l..k-1]\le nums[k]$ 且$nums[k+1..r]\ge nums[k]$

而一般的partition函数的实现不仅能够满足上述两个条件，还会更严格，如把第二个条件中的其中一个等号去掉：

+ $nums[l..k-1] < nums[k]$ 且$nums[k+1..r]\ge nums[k]$

不但能够用来排序，还能做其它事情。

### Partition函数实现：

如下版本返回值k，均满足$nums[l..k-1] < nums[k]$ 且$nums[k+1..r]\ge nums[k]$

#### 单向扫描

+ `for`循环遍历基准元素左侧所有元素，里指针s所指元素及其左侧元素都是小于最右侧基准元素`nums[r]`。
+ 出了`for`循环，s再前进一位，所指元素与基准元素对调，以确保最终的列表里其右侧元素均大于等于其所指元素。
+ `for`循环里以指针`i`为核心，其向右遍历，如果小于基准元素，则替换以大于等于基准元素。

```python
def partition(nums, l, r):
    s = l - 1
    for i in range(l, r):
        if nums[i] < nums[r]:
            s += 1
            if s != i:
                nums[s], nums[i] = nums[i], nums[s]
    s += 1
    nums[s], nums[r] = nums[r], nums[s]
    return s
```

#### 双向扫描

+ 双重while循环出来，后有`i==j`且`nums[l..i-1]<x`，`nums[i+1..r]>=x`。
  + 然后根据`nums[i]`与x的大小关系，分三种情况处理，并决定返回值：
    ```python
    if nums[i] > x: 
        nums[i], nums[r] = x, nums[i]
    elif nums[i] < x: 
        i += 1
        if nums[i] > x:
            nums[i], nums[r] = x, nums[i] 
    ```
+ 返回值i必然大于等于l，小于等于r，quicksort根据其划分的子问题规模必然小于原问题。

```python
def partition3(nums, l, r):
    x = nums[r]
    i, j = l, r-1
    while i < j: 
        while nums[i] < x and i < j: # 循环终止时i满足nums[i]>=x或者i==j
            i += 1
        while nums[j] >= x and i < j: # 循环终止时j满足nums[j]<x或者i==j
            j -= 1
        if j > i: # 说明必有nums[i]>=x且nums[j]<x，需要调换二者位置
            nums[i], nums[j] = nums[j], nums[i]

    if nums[i] < x: 
        i += 1
    nums[i], nums[r] = x, nums[i] 
    return i
```

### partition函数的应用


#### LeetCode215. 数组中的第K个最大元素

+ 第K大，就是第L-K+1个最小元素。

```python
class Solution(object):
    def findKthLargest(self, nums, k):

        if len(nums) == 0 or k <= 0 or k > len(nums):
            return None
        i, j = 0, len(nums)-1
        k = len(nums) - k
        while True:
            ix = partition(nums, i, j)
            if ix == k:
                return nums[ix]
            elif ix < k:
                i = ix + 1
            else:
                j = ix - 1
```

#### 剑指29-最小的K个数

用快排的partition方法来找到第k大的数，那么该数以及其左侧k-1个数一起，就是最小的k个数。

```python
class Solution:
    def GetLeastNumbers_Solution(self, tinput, k):
        if tinput is None or len(tinput) < k or k <= 0:
            return []
        s, t = 0, len(tinput)-1
        while True:
            ix = partition(tinput, s, t)
            if ix == k -1:
                return sorted(tinput[:k])
            elif ix > k -1:
                t = ix -1
            else:
                s = ix + 1
```

#### 剑指28-数组中出现次数超过一半的数字

+ 快排的partition函数能够以某个数为基准，将数组内元素按大小分为小于该数和大于等于该数两部分。可以用来将数组分成前k个较小值和其余的值两部分，方法是迭代，将partition函数的输入区间向k和拢。
+ 而出现次数超过一半的数，排序之后肯定会在下标`len(numbers)>>1`上出现，因此用partition函数找到该数，然后检查其是否满足条件即可。
+ 每次迭代使得partition的输出更接近`len(numbers)>>1`这个下标，直到二者相等。如果有出现次数超过一半的数，则必然是该下标的元素。究竟是不是，也要检查一番才能确定。
+ 注意：虽然partition的输出下标左侧的元素肯定要小于该下标所指的元素，但最终`len(numbers)>>1`这个下标左侧的元素却是小于等于该下标所指元素。只是由`while True`循环里对`s`和`t`的更新方式导致的。

```python
class Solution:
    def MoreThanHalfNum_Solution(self, numbers):  
        def checkMoreThanHalf(num, numbers):
            half = (len(numbers)>>1)+1 # 一半加一
            for n in numbers:
                if n == num:
                    half -= 1
            return half <= 0
        if len(numbers) == 0:
            return 0
        s, t = 0, len(numbers)-1
        mid = len(numbers)>>1
        while True:
            ix = partition(numbers, s, t) 
            if ix > mid:
                t = ix - 1
            elif ix < mid: 
                s = ix + 1
            else:
                break
        num = numbers[mid]
        return num if checkMoreThanHalf(num, numbers) else 0
```
