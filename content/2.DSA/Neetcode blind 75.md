---
title: Neetcode blind 75
tags: [dsa]
---


https://neetcode.io/practice?tab=blind75

![[Pasted image 20250529121142.png]]




# 206 reverse a linked list
![[Pasted image 20250529123125.png]]


### Method 1 : with the help of stack
```java
class Solution {
    public ListNode reverseList(ListNode head) {
        Stack<Integer> valueStack = new Stack<>();
        while (head != null) {
            valueStack.push(head.val);
            head = head.next;
        }

        ListNode reversedList = new ListNode(Integer.MIN_VALUE);
        ListNode ptr = reversedList;

        while (!valueStack.isEmpty()) {
            ptr.next = new ListNode(valueStack.pop());
            ptr = ptr.next;
        }
        return reversedList.next;
    }
}
```

#### time complexity : o(n), Space complexity o(n)

not that efficient we have to reduce space complexity

### Method 2 (with out using any DS here we can reduse space complexity o(1))


reference : https://youtu.be/3IN0BP9Ni6E?t=521 


```java
class Solution {
    public ListNode reverseList(ListNode head) {

        if (head == null){
            return null;
        }

        if (head.next == null){
            return head;
        }

        ListNode preNode = null;
        ListNode currNode = head;

        while (currNode != null) {
            ListNode nextNode = currNode.next;
            currNode.next = preNode;
            preNode = currNode;
            currNode = nextNode;
        }

        head = preNode;
        return head;
    }
}
```


# 21, Merge 2 Sorted Lists
![[Pasted image 20250530181930.png]]


Method 1: With recursion 

```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        if (list1 == null )return list2;
        if (list2 == null )return list1;

        if (list1.val < list2.val){
            list1.next = mergeTwoLists(list1.next, list2);
            return list1;
        } else {
            list2.next = mergeTwoLists(list1, list2.next);
            return list2;
        }
    }
}
```



# 141. Linked list Cycle


![[Pasted image 20250531233744.png]]


referenec only 3 minutes video : https://www.youtube.com/watch?v=IxXf_7LVGpg


```java
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow=head;
        ListNode fast=head;

        while (fast!=null && fast.next!=null)
        {
            slow = slow.next;
            fast = fast.next.next;
            if(slow==fast)
                return true;
        }
        return false;
}
```

