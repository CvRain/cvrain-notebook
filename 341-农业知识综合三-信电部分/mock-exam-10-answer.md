# 341 农业综合知识三（信电）· 模拟卷十 参考答案

## 第一部分 程序设计基础知识（75分）

### 一、填空题（10分）

1. `a / b` = **2**（整数除法截断）；`(double)a / b` = **2.5**（先转浮点再除）

2. `(p + 3)[-1]` = **3**（(p+3)[-1] = *(p+3-1) = *(p+2) = a[2] = 3）；`*(int*)((char*)p + 8)` = **3**（char 偏移8 字节 = 2个 int，即 a[2] = 3）

3. **函数信号处理**声明（signal 函数：接收 int 信号码和函数指针，返回之前的信号处理函数指针）

4. **数组**（长度为3）；**返回 int 且接受两个 int 参数的函数**

5. EOF = **-1**（通常）；一个 **int** 类型**宏**常量

---

### 二、简答题（15分）

1. **左值/右值**：
   - 左值（lvalue）：标识一块内存位置的表达式，可以出现在赋值左侧（有地址）
   - 右值（rvalue）：临时值，无持久内存地址
   - 可做左值：`a`（变量）, `*p`（解引用）, `++a`（前置自增）——注意 `++a` 返回增加后的左值引用
   - 不可做左值：`a+b`（临时结果）, `a++`（后置自增返回原始值的右值拷贝）

2. **头文件守卫**：防止重复包含的宏机制。除 `#ifndef` 外，还有 `#pragma once`（非标准但广泛支持）。`#pragma once` 更简洁但不可移植；`#ifndef` 完全标准但需保证宏名唯一，且有首次解析整个文件的开销。

3. **printf 返回值**：返回成功输出的字符数（失败返回负数）。
   ```c
   int ret = printf("Hello\n");
   if (ret < 0) fprintf(stderr, "printf failed\n");
   ```

4. **可变参数**：使用 stdarg.h
   - `va_list`：声明参数列表变量
   - `va_start(ap, last)`：初始化 ap 指向第一个可变参数（last 是最后一个固定参数）
   - `va_arg(ap, type)`：依次获取参数
   - `va_end(ap)`：清理

5. **setjmp/longjmp**：非局部跳转，可跨函数栈回退。`setjmp` 保存当前环境，`longjmp` 恢复到保存点。适用场景：深层错误处理和恢复（类似 try/catch）。与 goto 区别：goto 只能在同一函数内跳转；setjmp/longjmp 可跨越多个函数调用。

---

### 三、分析题（20分）

1. **3 6**（x=0: y+=++x→x=1,y=1; x=1→y+=2,y=3; x=2→y+=3,y=6; x=3 退出。输出 3 6）

2. **3 4 1**（p=a+2 指向 a[2]=3；p[-1]=a[1]=4；a[4]=1）

3. **5 4 3 2 1**（递归：先输出 n%10=5，再递归 n/10=1234→4, 123→3, 12→2, 1→1）

4. **12**（对齐：char(1)+3pad=4, int=4, short(2)+2pad=4 → 4+4+4=12。或者按8字节 double 对齐则更大。此处假设默认对齐，char 4 对齐到 int 的 4 字节 → 1+3pad+4+2+2pad = 12）

5. ```
   
   *
   **
   ***
   ```
   （i=0: j==0 break, 输出0个*; i=1: j=0=0个*然后break, 输出0个*; i=2: j=0,break; 等等...不对。重新分析：i=0时j=0→break；i=1时j=0→*, j=1→break；i=2→j=0→*,j=1→*,j=2→break；i=3→j=0→*,j=1→*,j=2→*,j=3→break。
   输出：空行, *, **, ***）

6. **4**（p=arr+4 指向 9；p-2 指向 5；9-5=4）

7. **42**（pp→p→x，**pp=42 即 x=42）

8. **120**（f(5)=5×f(4)=5×4×f(3)=...=5×4×3×2×1=120，depth 变量不影响结果）

9. **10**（s[10]="0123456789"→10个字符填满数组，没有位置放 \0！strlen 会一直读取直到遇到 \0 或越界崩溃。这是**未定义行为**。标准假设下可能是 10 或更多。**答案：未定义行为**）

10. **20 10**（指针实现的原位交换：*pa=30; *pb=10; *pa=20; 输出 20 10）

---

### 四、程序设计题（30分）

**1. 通用快速排序**

```c
#include <stdio.h>
#include <string.h>

void swap_bytes(char *a, char *b, size_t size) {
    char tmp[size];
    memcpy(tmp, a, size); memcpy(a, b, size); memcpy(b, tmp, size);
}

// 插入排序（小数组优化）
void insert_sort(void *base, size_t num, size_t size,
                 int (*cmp)(const void*, const void*)) {
    char *arr = base;
    for (size_t i = 1; i < num; i++)
        for (size_t j = i; j > 0 && cmp(arr + (j-1)*size, arr + j*size) > 0; j--)
            swap_bytes(arr + (j-1)*size, arr + j*size, size);
}

// 三数取中
size_t median_of_three(void *base, size_t lo, size_t hi, size_t size,
                       int (*cmp)(const void*, const void*)) {
    char *arr = base;
    size_t mid = (lo + hi) / 2;
    char *a = arr + lo * size, *b = arr + mid * size, *c = arr + hi * size;
    if (cmp(a, b) > 0) { if (cmp(b, c) > 0) return mid; return cmp(a, c) > 0 ? hi : lo; }
    else { if (cmp(a, c) > 0) return lo; return cmp(b, c) > 0 ? hi : mid; }
}

size_t partition(void *base, size_t lo, size_t hi, size_t size,
                 int (*cmp)(const void*, const void*)) {
    char *arr = base;
    size_t pi = median_of_three(base, lo, hi, size, cmp);
    swap_bytes(arr + pi * size, arr + hi * size, size);
    size_t i = lo;
    for (size_t j = lo; j < hi; j++)
        if (cmp(arr + j*size, arr + hi*size) < 0)
            swap_bytes(arr + i++ * size, arr + j * size, size);
    swap_bytes(arr + i * size, arr + hi * size, size);
    return i;
}

void quick_sort_r(void *base, size_t lo, size_t hi, size_t size,
                  int (*cmp)(const void*, const void*)) {
    if (lo >= hi) return;
    if (hi - lo < 10) { insert_sort(base + lo * size, hi - lo + 1, size, cmp); return; }
    size_t p = partition(base, lo, hi, size, cmp);
    if (p > lo) quick_sort_r(base, lo, p - 1, size, cmp);
    quick_sort_r(base, p + 1, hi, size, cmp);
}

void quick_sort(void *base, size_t num, size_t size,
                int (*cmp)(const void*, const void*)) {
    quick_sort_r(base, 0, num - 1, size, cmp);
}
```

**2. 表达式求值器**（中缀转后缀 + 计算，略——核心思路：Dijkstra双栈算法或经典中缀转后缀栈实现）

核心步骤：
1. 遇到数字：解析完整多位数→输出
2. 遇到左括号：入栈
3. 遇到右括号：弹出栈中运算符直到左括号
4. 遇到运算符：比较优先级，弹出所有>=当前优先级的运算符，当前运算符入栈
5. 后缀求值：数字入栈；运算符弹出两个操作数计算后结果入栈
6. 异常处理：除零（检查除数是否为0）、括号不匹配（结束时栈中应有且仅有左括号）

---

## 第二部分 数据库技术与应用（75分）

### 一、填空题（10分）

1. **"对于所有"**（全称量词）；**S 中的所有值在 R 中都有对应**

2. **m**条（偏移量）开始，返回 **n** 条

3. **重做**已提交事务的修改；**撤销**未提交事务的修改

4. **整数（INT/BIGINT）**类型；**1** 个

5. 每次 SELECT 生成**一个新的快照（Read View）**；只第一次 SELECT 生成**一个快照**

---

### 二、简答题（10分）

1. **完整性 vs 安全性**：
   - **完整性**：防止数据库中存在不合语义的数据，保证数据正确性和一致性。分类：实体完整性（PRIMARY KEY）、参照完整性（FOREIGN KEY）、用户定义完整性（CHECK、NOT NULL）。
   - **安全性**：防止非法用户访问和恶意破坏数据。
   - 联系：都与数据保护相关，但侧重点不同（内部正确 vs 外部非法访问）
   - 示例：
     ```sql
     CREATE TABLE Student (
         Sno INT PRIMARY KEY,                          -- 实体完整性
         Sname VARCHAR(20) NOT NULL,                   -- 用户定义完整性
         Dno INT,                                     -- 参照完整性
         Age INT CHECK (Age >= 0 AND Age <= 120),      -- 用户定义完整性
         FOREIGN KEY (Dno) REFERENCES Dept(Dno)        -- 参照完整性
     );
     ```

2. **存储过程 vs 函数**：
   | 特性 | 存储过程 | 函数（UDF） |
   |------|---------|-----------|
   | 返回值 | 0或多个（OUT参数） | 必须返回一个值 |
   | 调用方式 | CALL proc(...) | SELECT func(...) |
   | 事务 | 可以使用 COMMIT/ROLLBACK | 不能使用事务控制语句 |
   | SQL 中使用 | 不能用于 SELECT 内部 | 可用于 SELECT/WHERE |
   | 适用场景 | 复杂业务逻辑、批量操作 | 简单计算、数据转换 |
   
   存储过程更适合：需要事务控制、多步操作、复杂业务逻辑的批处理场景。

---

### 三、操作题（15分）

设有电影票务系统 T, H, M, S, O。

**1. 从未上映的电影：**
```sql
SELECT Mname, Director FROM M
WHERE NOT EXISTS (SELECT 1 FROM S JOIN H ON S.H_id = H.Hid WHERE S.M_id = M.Mid);
```

**2. 各影院平均上座率：**
```sql
SELECT T.Tname,
       COALESCE(SUM(O.Quantity), 0) * 1.0 / SUM(H.SeatCount) AS occupancy_rate
FROM T
JOIN H ON T.Tid = H.T_id
JOIN S ON H.Hid = S.H_id
LEFT JOIN O ON S.Sid = O.Sid
GROUP BY T.Tid, T.Tname
ORDER BY occupancy_rate DESC;
```

**3. 各类型票房前3电影：**
```sql
SELECT Mtype, Mname, revenue FROM (
    SELECT M.Mtype, M.Mname, COALESCE(SUM(O.TotalPrice), 0) AS revenue,
           RANK() OVER (PARTITION BY M.Mtype ORDER BY COALESCE(SUM(O.TotalPrice), 0) DESC) rk
    FROM M JOIN S ON M.Mid = S.M_id
    JOIN O ON S.Sid = O.Sid AND O.Ostatus = 'paid'
    GROUP BY M.Mtype, M.Mid, M.Mname
) t WHERE rk <= 3;
```

**4. 取消订单金额占比：**
```sql
SELECT SUM(CASE WHEN Ostatus = 'cancelled' THEN TotalPrice ELSE 0 END) /
       NULLIF(SUM(TotalPrice), 0) AS cancel_ratio FROM O;
```

**5. 2026年6月IMAX有余票场次：**
```sql
SELECT M.Mname, S.ShowTime, S.Price, S.RemainSeats
FROM S JOIN M ON S.M_id = M.Mid
JOIN H ON S.H_id = H.Hid
WHERE H.Htype = 'IMAX' AND S.RemainSeats > 0
AND YEAR(S.ShowTime) = 2026 AND MONTH(S.ShowTime) = 6;
```

**6. 至少购买5次且每次>=2张的用户：**
```sql
SELECT Uid FROM O
WHERE Quantity >= 2
GROUP BY Uid
HAVING COUNT(*) >= 5;
```

**7. 购票触发器：**
```sql
DELIMITER //
CREATE TRIGGER trg_after_order
BEFORE INSERT ON O
FOR EACH ROW
BEGIN
    DECLARE remain INT;
    IF NEW.Ostatus = 'paid' THEN
        SELECT RemainSeats INTO remain FROM S WHERE Sid = NEW.Sid;
        IF remain < NEW.Quantity THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '余票不足';
        ELSE
            UPDATE S SET RemainSeats = RemainSeats - NEW.Quantity WHERE Sid = NEW.Sid;
        END IF;
    END IF;
END //
DELIMITER ;
```

---

### 四、分析题（10分）

R(A,B,C,D,E,F,G,H)，F = {AB→C, C→D, D→E, E→F, F→G, G→H, H→AB}

**（1）候选键**：循环依赖形成闭环，所有属性可以互相推导：
- (AB)⁺ = {AB,C,D,E,F,G,H} → **AB 候选键**
- (H)⁺ = {H,AB,C,D,E,F,G} → **H 候选键**
- (G)⁺ = {G,H,AB,C,D,E,F} → **G 候选键**
- 同理：**F, E, D, C 都是候选键**（通过传递链和闭环）
- 最终候选键：**AB, C, D, E, F, G, H 中的极小集**。AB 和各个单属性都互为推导，7个单属性各是候选键的话 AB 不是极小。检查：(AB) 去掉 A → B⁺={B} 不全 → A不冗余；去掉 B → A⁺={A} 不全。但 C→D→E→F→G→H→AB→C，闭环。所以极小超键为**各单属性 C, D, E, F, G, H**，以及**二属性 AB**（AB 中任一个都不能独立决定另一个）。

**（2）范式判定**：所有属性都是主属性（每个单属性都是候选键！），所以不存在非主属性的部分/传递依赖。但需要判断 BCNF：AB→C 中 AB 是超键 ✓；C→D 中 C 是超键（C 是候选键）✓；D→E 中 D 是超键 ✓... 所有 FD 的决定因素都是候选键 → **R ∈ BCNF**（也是 3NF, 2NF, 1NF）。

**（3）分解**：R 已是 BCNF，无需分解。或者可说：R 本身就是最优的 3NF/BCNF 模式。

---

### 五、设计题（10分）

**毕设管理系统关系模式**：

1. **学生**：Student(**Sno**, Sname, Major, Class, Phone, Email)
2. **教师**：Teacher(**Tno**, Tname, Title, College, ResearchArea)
3. **毕设题目**：Topic(**TopicID**, Tname, Ttype, Source, Description, Skills, MaxStudents, **Tno**) — Tno 外键参照 Teacher
4. **选题**：Selection(**Sno**, **TopicID**, SelectTime, Status) — Sno 外键参照 Student，TopicID 外键参照 Topic（Status: '待审核'/'已通过'/'已拒绝'）
5. **指导记录**：Guidance(**GID**, **Sno**, **Tno**, Date, Summary, Plan) — Sno/Tno 外键
6. **答辩**：Defense(**DefenseID**, **Sno**, DefenseTime, Location, Score, Comment) — Sno 外键对照 Student

---

### 六、应用题（20分）

**1. 社交平台帖子管理**

（1）从未发过帖的用户：
```sql
SELECT uname, reg_time FROM users
WHERE NOT EXISTS (SELECT 1 FROM posts WHERE posts.uid = users.uid);
```

（2）获赞前10用户：
```sql
SELECT u.uname, SUM(p.likes) AS total_likes
FROM users u JOIN posts p ON u.uid = p.uid
GROUP BY u.uid, u.uname
ORDER BY total_likes DESC LIMIT 10;
```

（3）存储过程 hot_posts：
```sql
DELIMITER //
CREATE PROCEDURE hot_posts(IN n INT)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_pid, v_likes, v_comments INT;
    DECLARE v_summary VARCHAR(55);
    DECLARE cur CURSOR FOR
        SELECT pid, LEFT(content, 50), likes, comments
        FROM posts
        WHERE post_time > DATE_SUB(NOW(), INTERVAL 7 DAY) AND likes > 100
        ORDER BY likes DESC LIMIT n;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_pid, v_summary, v_likes, v_comments;
        IF done THEN LEAVE read_loop; END IF;
        SELECT v_pid AS '帖子编号', v_summary AS '内容摘要', v_likes AS '点赞', v_comments AS '评论';
    END LOOP;
    CLOSE cur;
END //
DELIMITER ;
```

**2. 数据库优化**

（1）**索引合并优化（Index Merge）**：MySQL 同时使用多个索引来处理查询，对结果取交集（Intersection）或并集（Union）。适用于单个索引选择性不足但多个索引组合能有效过滤的场景。EXPLAIN type=index_merge 表示优化器用了多个索引。

（2）**聚簇索引 vs 二级索引**：
   - 聚簇索引：数据按索引顺序物理存储（InnoDB 的数据即按主键 B+树组织），叶子节点存整行数据
   - 二级索引：叶子节点存索引列值和对应的主键值，需**回表**查完整行
   - 自增主键优势：新数据总是追加到末尾，减少页分裂和碎片；聚簇索引页填充率高

（3）**2亿订单表优化**：
   - 索引优化：`CREATE INDEX idx_uid_time ON orders(uid, order_time DESC);` 覆盖查询
   - 可考虑按 uid 哈希分表（如 uid % 64 取模分 64 表），将数据和索引分散到多张表
   - ORDER BY 优化：利用联合索引的有序性避免 filesort
   - 读写分离：历史订单读从库，实时订单写主库

