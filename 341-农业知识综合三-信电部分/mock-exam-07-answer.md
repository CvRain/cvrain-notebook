# 341 农业综合知识三（信电）· 模拟卷七 参考答案

## 第一部分 程序设计基础知识（75分）

### 一、填空题（10分）

1. a=**1**, b=**1**, c=**3**（短路求值：a++ 为 0（假），不执行 b++；执行 c++，c 变为 3；a 后自增为 1，b 不变为 1）

2. strlen(s)=**5**, sizeof(s)=**10**（"012\034\0ABC" → '0','1','2', 八进制034对应的字符, '\0' → 5个字符（\0 结束）；数组大小：5 + 1个\0 + 4个"ABC" = 10 字节）

3. `*(a[0] + 1)` = **2**（a[0][1]）；`*(*(a + 2) + 1)` = **6**（a[2][1]）

4. **指向长度为5的整型数组的指针**

5. **文件开头位置**

---

### 二、简答题（15分）

1. **const 三形式**：
   - `const int *p`：指针指向的内容不可修改（指向常量的指针），`*p = 10;` 错误
   - `int *const p`：指针本身不可修改（常量指针），`p = &b;` 错误
   - `const int *const p`：指针和内容都不可修改
   - 场景：`const int *p` 用于函数参数，保证不修改传入数据

2. **内存泄露**：动态分配的内存未被释放，且指针丢失，无法再访问。示例：
   ```c
   void leak() { int *p = malloc(sizeof(int) * 100); } // 忘记 free(p)
   ```
   避免：配对使用 malloc/free，使用工具检测（valgrind），或将资源管理封装在结构中。

3. **函数指针**：指向函数的指针，可用于回调（回调函数）、策略模式、函数表。
   ```c
   int add(int a, int b) { return a + b; }
   int calc(int (*op)(int,int), int x, int y) { return op(x, y); }
   int main() { printf("%d", calc(add, 3, 5)); return 0; } // 输出 8
   ```

4. **#include 区别**：
   - `<>`：先在系统标准头文件路径搜索
   - `""`：先在当前源文件目录搜索，再搜索系统路径
   - 若用户目录下有同名 `stdio.h`，`#include "stdio.h"` 会引用用户的，`<stdio.h>` 仍引系统版本

5. **typedef vs #define**：
   - `typedef` 是编译期类型别名，符合作用域规则
   - `#define` 是预处理文本替换，简单字符串替换
   - 陷阱：`#define PTR int*` → `PTR a, b;` 展开为 `int* a, b;` 只有 a 是指针；`typedef int* PTR;` 则 a 和 b 都是指针

---

### 三、分析题（20分）

1. **F 1 1**（a++为0（假），短路 && 不执行 b++，进入 else 输出 F；最终 a=1, b=1）

2. **6**（while 循环体为空，x 从0到5，当 x=5 时 5<5 不成立但 x++ 已执行，x=6）

3. **2 5**（p=a+2 指向 a[2]=3；p[-1]=a[1]=2；*(a+4)=a[4]=5）

4. **i=0 j=1**（i=0,j=0: i==j,continue; i=0,j=1: 进入 else → goto end 跳出。注意 i 最终为 0，j 为 1）

5. **2 1**（异或交换：a=1,b=2 → a^=b→a=3; b^=a→b=1; a^=b→a=2；交换成功）

6. **5 6**（static n 初始 0，第一次：5+0=5, n=1；第二次：5+1=6, n=2）

7. **e o**（*(s+1)='e'；s[4]='o'）

8. **20 10**（内层块内 x=20 覆盖外层；离开块后恢复外层 x=10）

9. **10**（a[0..4] = {-1,1,3,5,7}；a[2]=3, a[4]=7, 3+7=10）

10. **6 20**（strlen="ABCDEF"=6；sizeof=20，数组声明大小不变）

---

### 四、程序设计题（30分）

**1. 矩阵乘法**

```c
#include <stdio.h>

void matrix_multiply(int A[][3], int B[][2], int C[][2], int m, int n, int p) {
    for (int i = 0; i < m; i++)
        for (int j = 0; j < p; j++) {
            C[i][j] = 0;
            for (int k = 0; k < n; k++)
                C[i][j] += A[i][k] * B[k][j];
        }
}

int main() {
    int A[2][3], B[3][2], C[2][2] = {0};
    printf("输入 2x3 矩阵 A:\n");
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 3; j++) scanf("%d", &A[i][j]);
    printf("输入 3x2 矩阵 B:\n");
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 2; j++) scanf("%d", &B[i][j]);

    matrix_multiply(A, B, C, 2, 3, 2);

    printf("结果矩阵 C:\n");
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) printf("%d ", C[i][j]);
        printf("\n");
    }
    return 0;
}
```

**2. 链表反转**

```c
#include <stdio.h>
#include <stdlib.h>

struct ListNode {
    int val;
    struct ListNode *next;
};

struct ListNode* createList(int arr[], int n) {
    struct ListNode *head = NULL, *tail = NULL;
    for (int i = 0; i < n; i++) {
        struct ListNode *node = malloc(sizeof(struct ListNode));
        node->val = arr[i]; node->next = NULL;
        if (!head) head = tail = node;
        else { tail->next = node; tail = node; }
    }
    return head;
}

struct ListNode* reverseList(struct ListNode *head) {
    struct ListNode *prev = NULL, *curr = head, *next;
    while (curr) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}

void printList(struct ListNode *head) {
    while (head) { printf("%d ", head->val); head = head->next; }
    printf("\n");
}

int main() {
    int arr[100], n = 0, val;
    while (scanf("%d", &val) && val != -1) arr[n++] = val;
    struct ListNode *head = createList(arr, n);
    head = reverseList(head);
    printList(head);
    // 注意：完整程序还需 free 链表
    return 0;
}
```

---

## 第二部分 数据库技术与应用（75分）

### 一、填空题（10分）

1. **{A, B, C, D}**；R.B = S.B **且** R.C = S.C

2. **选择**（Selection）；**投影**（Projection）

3. **UNION 自动去除重复行**，**UNION ALL 保留所有行（含重复）**

4. **脏读**：事务读取了另一个未提交事务修改的数据；**幻读**：事务两次读取之间另一个事务插入了新行，导致第二次读取多了"幻影行"

5. **TRUNCATE TABLE**；**DELETE FROM**；前者**不能**；后者**可以**

---

### 二、简答题（10分）

1. **数据依赖**：关系中属性值之间的约束关系，是数据语义的体现。
   - **函数依赖（FD）**：属性集 X 的一个值唯一确定属性集 Y 的一个值（X→Y）
   - **多值依赖（MVD）**：X 的一个值对应 Y 的一组值，且 Y 的值独立于其他属性（X→→Y）
   - 例：课程→→教材（一门课程有多本参考教材）
   - 多值依赖问题需要通过 **4NF** 解决：消除非平凡的多值依赖，每个决定因素都是超键

2. **两段锁协议（2PL）**：
   - 规则：事务分为加锁（Growing）和解锁（Shrinking）两阶段，加锁阶段不能解锁，解锁阶段不能加锁
   - 保证可串行化：遵守 2PL 的事务调度一定是可串行化的
   - **严格 2PL**：所有排他锁在事务提交后才释放，避免级联回滚（因为未提交数据不被其他事务读取）

---

### 三、操作题（15分）

设有图书借阅管理系统 R, B, L。

**1. 超期未还读者：**
```sql
SELECT R.Rid, R.Rname,
       DATEDIFF(CURDATE(), L.DueDate) AS overdue_days
FROM L JOIN R ON L.Rid = R.Rid
WHERE L.ReturnDate IS NULL AND L.DueDate < CURDATE();
```

**2. 借阅次数前10的书：**
```sql
SELECT B.Bname, B.Author, COUNT(*) AS borrow_count
FROM L JOIN B ON L.Bid = B.Bid
GROUP BY B.Bid, B.Bname, B.Author
ORDER BY borrow_count DESC
LIMIT 10;
```

**3. 借阅>3的读者：**
```sql
SELECT R.Rid, R.Rname, COUNT(*) AS cnt
FROM L JOIN R ON L.Rid = R.Rid
WHERE L.ReturnDate IS NULL
GROUP BY R.Rid, R.Rname
HAVING COUNT(*) > 3;
```

**4. 无借阅的图书：**
```sql
SELECT Bid, Bname FROM B
WHERE NOT EXISTS (SELECT 1 FROM L WHERE L.Bid = B.Bid);
```

**5. 出版社图书统计：**
```sql
SELECT Publisher, COUNT(*) AS total_books, AVG(Price) AS avg_price
FROM B
GROUP BY Publisher
HAVING COUNT(*) > 5;
```

**6. 与"张三"借阅完全相同图书的读者：**
```sql
SELECT R.Rid, R.Rname FROM R
WHERE NOT EXISTS (
    SELECT L.Bid FROM L
    JOIN R AS RZ ON L.Rid = RZ.Rid
    WHERE RZ.Rname = '张三'
    EXCEPT
    SELECT L2.Bid FROM L L2 WHERE L2.Rid = R.Rid
)
AND NOT EXISTS (
    SELECT L2.Bid FROM L L2 WHERE L2.Rid = R.Rid
    EXCEPT
    SELECT L.Bid FROM L JOIN R RZ ON L.Rid = RZ.Rid
    WHERE RZ.Rname = '张三'
)
AND R.Rname != '张三';
```

**7. 还书触发器：**
```sql
DELIMITER //
CREATE TRIGGER trg_return_book
AFTER UPDATE ON L
FOR EACH ROW
BEGIN
    IF NEW.ReturnDate IS NOT NULL AND OLD.ReturnDate IS NULL THEN
        UPDATE B SET Stock = Stock + 1 WHERE Bid = NEW.Bid;
    END IF;
END //
DELIMITER ;
```

---

### 四、分析题（10分）

R(A,B,C,D,E)，F = {AB→C, C→D, D→B, D→E}

**（1）候选键推导**：
- (AB)⁺ = {A,B,C,D,E} = 全属性 → **AB 是候选键**
- (AD)⁺ = {A,D,E,B,C} = 全属性 → **AD 是候选键**
- (AC)⁺ = {A,C,D,B,E} = 全属性 → **AC 是候选键**
- 最终候选键：**AB, AD, AC**（都是极小超键）

**（2）范式判定**：若选 AB 为主键，检查部分依赖：C→D 中 C 不是超键，但 C 有传递性。更关键的是 D→B 中 D 不是超键 → 存在非主属性对候选键的传递依赖 → 最高 **2NF**（因为 D→B 且 D 不是超键）。

**（3）BCNF 分解**：
D→B 违反 BCNF（D 不是超键），分解：
- R1(**D**, B)；R2(**A**, **C**, **D**, E)（含 C→D, D→E, AB/AD/AC 候选键）
- C→D, D→E 中 D 不是超键，继续拆：R21(**C**, D)；R22(**D**, E)；R23(**A**, **C**)
- 最终 BCNF：R1(**D**, B)；R2(**C**, D)；R3(**D**, E)；R4(**A**, C)

---

### 五、设计题（10分）

**课程学习管理系统 E-R 关系模式**：

1. **学生**：Student(**Sno**, Sname, Sex, EnrollYear, Major)
2. **教师**：Teacher(**Tno**, Tname, Title, College)
3. **课程**：Course(**Cno**, Cname, Credit, Hours, Nature, **Tno**) — Tno 外键参照 Teacher
4. **选课**：Enroll(**Sno**, **Cno**, Grade, Comment) — 复合主键，各有外键
5. **先修关系**：Prereq(**Cno**, **PreCno**) — 自参照关系，Cno/PreCno 各参照 Course
6. **考试**：Exam(**ExamID**, **Cno**, ExamName, ExamTime, Location, MaxScore, AvgScore) — Cno 外键

（注：课程性质"必修/选修"和教师"主讲"已在关系模式中体现）

---

### 六、应用题（20分）

**1. 银行转账系统**

（1）查询余额异常的账户：
```sql
SELECT acc_id, cust_name, balance
FROM accounts WHERE balance < 0;
```

（2）每个账户最近5笔交易：
```sql
SELECT acc_id, tx_type, amount, tx_time FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY acc_id ORDER BY tx_time DESC) rn
    FROM transactions
) t WHERE rn <= 5;
```

（3）存储过程 transfer_funds：
```sql
DELIMITER //
CREATE PROCEDURE transfer_funds(
    IN from_acc INT, IN to_acc INT, IN amount DECIMAL(12,2))
BEGIN
    DECLARE from_balance DECIMAL(12,2);
    DECLARE from_exist INT DEFAULT 0;
    DECLARE to_exist INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION ROLLBACK;

    START TRANSACTION;
    SELECT balance INTO from_balance FROM accounts
    WHERE acc_id = from_acc AND status = 'active' FOR UPDATE;
    IF from_balance IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '转出账户不存在或已冻结';
    END IF;
    IF from_balance < amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '余额不足';
    END IF;

    UPDATE accounts SET balance = balance - amount WHERE acc_id = from_acc;
    UPDATE accounts SET balance = balance + amount WHERE acc_id = to_acc;

    INSERT INTO transactions (acc_id, tx_type, amount, status)
    VALUES (from_acc, 'transfer', -amount, 'completed');
    INSERT INTO transactions (acc_id, tx_type, amount, status)
    VALUES (to_acc, 'transfer', amount, 'completed');
    COMMIT;
END //
DELIMITER ;
```

**2. 数据库理论**

（1）索引设计：`CREATE INDEX idx_dno_salary ON employee(dno, salary DESC);`
   - 联合索引先按 dno 过滤，再按 salary 降序，正好匹配 WHERE+ORDER BY 的查询模式，避免 filesort。

（2）**覆盖索引**：查询所需的所有列都在索引中，无需回表查聚集索引。例如 `SELECT dno, salary FROM employee WHERE dno = 5` 配合 `INDEX(dno, salary)` 就是覆盖查询。减少 I/O 因为只需读索引 B+树，不必跳到数据页。

（3）动态备份表结构：
```sql
DELIMITER //
CREATE PROCEDURE backup_table(IN tbl_name VARCHAR(64))
BEGIN
    SET @sql = CONCAT('CREATE TABLE ', tbl_name, '_backup LIKE ', tbl_name);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
```
动态 SQL 的必要性：表名不能在编译时确定，必须用 PREPARE/EXECUTE 在运行时拼接 SQL 字符串。

