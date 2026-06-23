# 341 农业综合知识三（信电）· 模拟卷九 参考答案

## 第一部分 程序设计基础知识（75分）

### 一、填空题（10分）

1. `sizeof(++a)` = **4**（sizeof 是编译期操作符，不会求值，++a 不被执行），a 的值 = **5**（不变）

2. `sizeof(p)` = **8**（64位指针，或32位为4），`sizeof(*p)` = **1**（char 类型 1 字节）

3. `a[1][2]` = **5**（{3,4,5} 第二行初始化完整，下标2=5）；`a[2][1]` = **0**（{6} 只初始化 a[2][0]，其余为 0）

4. **8**（union 大小为最大成员的大小，double 通常 8 字节）

5. n 表示**要拷贝的字节数**；返回值是**dest 的指针**

---

### 二、简答题（15分）

1. **序列点**：程序中所有副作用（side effect）必须完成的点，表达式求值在此点之前的副作用保证在此点之后可见。`i = i++ + ++i;` 在同一个表达式中两次修改 i（多次修改和读取之间无序列点），违反 C 标准规定 → **未定义行为**。

2. **malloc/calloc/realloc**：
   - `malloc(size)`：分配未初始化的内存
   - `calloc(n, size)`：分配并清零 n×size 字节
   - `realloc(ptr, size)`：调整已分配内存大小
   - 注意：realloc 可能返回新地址，需用临时变量接收以防失败丢失原指针
   - 内存泄露：`int *p = malloc(100); p = malloc(200);` 第一次分配的内存未释放

3. **副作用**：表达式求值过程中改变了程序状态（修改变量值、I/O 等）。产生副作用的操作：赋值（=）、++、--、函数调用（printf）。纯函数式编程通过不可变数据和无副作用函数来避免。

4. **restrict**：告知编译器某指针是访问其所指向数据的唯一方式，两个 restrict 指针不会指向重叠区域。用于优化（如 memcpy 比 memmove 更快），编译器可假设无别名进行向量化。

5. **变长数组 VLA**：`int n; scanf("%d", &n); int arr[n];` 数组大小在运行时确定。限制：不能用于全局/静态，不能在结构体中，不支持初始化器。C11 中变为可选是因为 VLA 实现复杂且有栈溢出风险。

---

### 三、分析题（20分）

1. **-1 0 0**（a--为 0（假），短路 && 不执行 b--；a 后自减为 -1，b=0 不变，r=0）

2. **7 15**（a[0]=1；a[1]=1×2+1=3；a[2]=3×2+1=7；a[3]=7×2+1=15）

3. ```
   123
    23
     3
   ```
   （j<i 时输出空格，否则输出 j）

4. **6**（p 遍历到 \0，p-s=6，即字符串长度）

5. **0 1 2**（x++ → 输出 0, x=1；输出 1；++x → x=2, 输出 2）

6. **5 3**（a 为 2×3 矩阵；`*(*a+4)=*((int*)a+4)=5`；`*(a[1]-1)=*((int*)a+2)=3`——按行存储：{1,2,3,4,5,6}，a[1] 指向 4，a[1]-1 指向 3）

7. **3 5**（a[0]+0=1; a[1]+1=2; a[2]+2=3; a[3]+3=4; a[4]+4=5。a[2]=3, a[4]=5）

8. **13**（fib(7)=13：0,1,1,2,3,5,8,13（第0项0，第7项13））

9. **4 3**（异或交换：a=3,b=4→ a=7, b=3, a=4；输出 4 3）

10. **8 6**（sizeof(p)=指针大小8；sizeof(s)=字符数组大小6（含 \0））

---

### 四、程序设计题（30分）

**1. 埃拉托斯特尼筛法**

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sieve(int n, int *prime_count, int *primes) {
    char *is_prime = malloc(n + 1);
    memset(is_prime, 1, n + 1);
    is_prime[0] = is_prime[1] = 0;
    for (int i = 2; i * i <= n; i++)
        if (is_prime[i])
            for (int j = i * i; j <= n; j += i)
                is_prime[j] = 0;
    int cnt = 0;
    for (int i = 2; i <= n; i++)
        if (is_prime[i]) primes[cnt++] = i;
    *prime_count = cnt;
    free(is_prime);
}

int main() {
    int n;
    scanf("%d", &n);
    int *primes = malloc(n * sizeof(int));
    int cnt;
    sieve(n, &cnt, primes);
    for (int i = 0; i < cnt; i++) {
        printf("%d ", primes[i]);
        if ((i + 1) % 8 == 0) printf("\n");
    }
    printf("\n共 %d 个素数\n", cnt);
    free(primes);
    return 0;
}
```

**2. 动态扩容栈**

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int top;
    int capacity;
} Stack;

Stack* createStack(int cap) {
    Stack *s = malloc(sizeof(Stack));
    s->data = malloc(cap * sizeof(int));
    s->top = -1;
    s->capacity = cap;
    return s;
}

void push(Stack *s, int val) {
    if (s->top + 1 == s->capacity) {
        s->capacity *= 2;
        s->data = realloc(s->data, s->capacity * sizeof(int));
    }
    s->data[++s->top] = val;
}

int pop(Stack *s) {
    if (s->top == -1) { printf("栈空\n"); return -1; }
    return s->data[s->top--];
}

int top(Stack *s) {
    if (s->top == -1) { printf("栈空\n"); return -1; }
    return s->data[s->top];
}

int isEmpty(Stack *s) { return s->top == -1; }

void freeStack(Stack *s) { free(s->data); free(s); }

int main() {
    Stack *s = createStack(4);
    int val;
    while (scanf("%d", &val) && val != -1) push(s, val);
    while (!isEmpty(s)) printf("%d ", pop(s));
    printf("\n");
    freeStack(s);
    return 0;
}
```

---

## 第二部分 数据库技术与应用（75分）

### 一、填空题（10分）

1. **U（全集）**；**U（全集）**

2. **ASC（升序）**；**IS NULL** 或 **ORDER BY col IS NULL, col**

3. **授予权限**；**撤销权限**

4. **先写日志（WAL, Write-Ahead Logging）**

5. **间隙锁（Gap Lock）**（InnoDB 的 Next-Key Lock 机制）

---

### 二、简答题（10分）

1. **概念设计 vs 逻辑设计**：
   - **概念设计**：产出 E-R 图，描述实体、属性和联系，独立于 DBMS。以学生选课为例：学生(学号,姓名)、课程(编号,名称)、选课(成绩) 三个实体及它们之间的联系。
   - **逻辑设计**：E-R 图转关系模式。多对多联系→独立关系表（选课表）；一元联系→自参照（课程先修）；三元联系→独立表（含三个外键）
   - E-R 图转换规则：实体→表，1:1联系→合并或外键，1:N联系→N方加外键，M:N联系→新建联系表

2. **事务持久性**：事务一旦提交，其修改就永久保存，即使系统崩溃也不丢失。InnoDB 通过 **redo log（重做日志）** 保证：提交前先将修改写入 redo log，崩溃恢复时重做已提交但未写入数据文件的事务。**双写缓冲（doublewrite buffer）**：InnoDB 先将脏页写入共享表空间的 doublewrite buffer，再写入实际数据文件。如果写入数据文件时发生部分写故障，可以从 doublewrite buffer 恢复完整页，避免页损坏。

---

### 三、操作题（15分）

设有科研管理系统 P, T, PI, Paper。

**1. 经费>100万且进行中的项目：**
```sql
SELECT Pno, Pname FROM P
WHERE Budget > 1000000 AND Status = '进行中';
```

**2. 教师参与项目总经费>50万：**
```sql
SELECT T.Tno, T.Tname, COUNT(PI.Pno) AS proj_cnt,
       SUM(P.Budget) AS total_budget
FROM T JOIN PI ON T.Tno = PI.Tno
JOIN P ON PI.Pno = P.Pno
GROUP BY T.Tno, T.Tname
HAVING SUM(P.Budget) > 500000;
```

**3. 无论文的项目：**
```sql
SELECT Pno, Pname, Ptype FROM P
WHERE NOT EXISTS (SELECT 1 FROM Paper WHERE Paper.Pno = P.Pno);
```

**4. 在所有项目中都是负责人的教师：**
```sql
SELECT Tno FROM PI
GROUP BY Tno
HAVING COUNT(*) = SUM(CASE WHEN Role = '负责人' THEN 1 ELSE 0 END);
```

**5. 合作最多的教师对：**
```sql
SELECT p1.Tno, p2.Tno, COUNT(*) AS co_papers FROM PI p1
JOIN PI p2 ON p1.Pno = p2.Pno AND p1.Tno < p2.Tno
GROUP BY p1.Tno, p2.Tno
ORDER BY co_papers DESC LIMIT 1;
```

**6. 项目汇总视图：**
```sql
CREATE VIEW v_project_summary AS
SELECT P.Pno, P.Pname,
       (SELECT T.Tname FROM PI JOIN T ON PI.Tno = T.Tno
        WHERE PI.Pno = P.Pno AND PI.Role = '负责人' LIMIT 1) AS leader,
       COUNT(DISTINCT PI.Tno) AS member_cnt,
       COALESCE(SUM(PI.Hours), 0) AS total_hours,
       COUNT(DISTINCT Paper.PaperId) AS paper_cnt
FROM P
LEFT JOIN PI ON P.Pno = PI.Pno
LEFT JOIN Paper ON P.Pno = Paper.Pno
GROUP BY P.Pno, P.Pname;
```

**7. 检查负责人的触发器：**
```sql
DELIMITER //
CREATE TRIGGER trg_check_budget
BEFORE INSERT ON PI
FOR EACH ROW
BEGIN
    IF NEW.Role = '负责人' AND EXISTS (
        SELECT 1 FROM PI WHERE Pno = NEW.Pno AND Role = '负责人'
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '该项目已有负责人';
    END IF;
END //
DELIMITER ;
```

---

### 四、分析题（10分）

R(A,B,C,D,E,F,G)，F = {A→B, B→C, C→D, D→A, AE→F, BF→G}

**（1）候选键**：
- (AE)⁺：A→B→C→D→A (回环，{A,B,C,D})，AE→F，缺 G。还需 BF→G：已含 B→G → {A,B,C,D,E,F,G} → **AE 是候选键**
- (BE)⁺：B→C→D→A→B，BE→? 直接有 BF→G 需 F，AE→F 需 AE。缺... 检查：(BE)⁺ = {B,E,C,D,A,F,G} = 全属性 → **BE 也是候选键**（B→C→D→A, 有 A,E→F, B,F→G）
- (DE)⁺ = {D,E,A,B,C,F,G} = 全属性 → **DE 候选键**
- (CE)⁺ = {C,E,D,A,B,F,G} = 全属性 → **CE 候选键**
- 最终候选键：**AE, BE, CE, DE**（含 E 且含 A/B/C/D 之一）

**（2）范式判定**：检查每个 FD 的决定因素是否超键：A→B（A不是超键）、B→C（不是）、C→D（不是）、D→A（不是）→ 决定性非主属性对候选键的传递依赖 → 最高 **1NF**。

**（3）BCNF 分解**：按 FD 逐个分解非 BCNF 模式：
- 取 A→B：R1(**A**, B)；R2(**A**, C, D, E, F, G)
- R2 中 B→C：R21(**B**, C)；R22(**A**, B, D, E, F, G)
- 继续... BCNF 分解：R1(**A**, B)；R2(**B**, C)；R3(**C**, D)；R4(**D**, A)；R5(**A**, **E**, F)；R6(**B**, **F**, G)

---

### 五、设计题（10分）

**会议室预订管理系统关系模式**：

1. **会议室**：Room(**RID**, Rname, Floor, Capacity)
2. **会议室设备**：RoomDevice(**RID**, **Device**) — 多值属性单独建表
3. **员工**：Employee(**EID**, Ename, DeptID, Position, Phone)
4. **部门**：Dept(**DeptID**, Dname, Location, **MgrEID**) — MgrEID 外键参照 Employee
5. **预订**：Booking(**BID**, **RID**, **BookerEID**, Date, StartTime, EndTime, Topic, AttendeeCount) — RID/BookerEID 外键
6. **参会者**：Attendee(**BID**, **EID**, Status) — 记录出席状态（'已确认'/'待确认'/'已拒绝'）
7. **使用反馈**：Feedback(**FID**, **BID**, Rating, Comment, FeedbackTime) — BID 外键

---

### 六、应用题（20分）

**1. 库存管理系统**

（1）低于最低库存的商品：
```sql
SELECT p.pid, p.pname, i.quantity, w.wname
FROM inventory i
JOIN products p ON i.pid = p.pid
JOIN warehouses w ON i.wid = w.wid
WHERE i.quantity < i.min_qty;
```

（2）各仓库库存金额前3：
```sql
SELECT wname, pname, stock_value FROM (
    SELECT w.wname, p.pname, i.quantity * p.unit_price AS stock_value,
           RANK() OVER (PARTITION BY i.wid ORDER BY i.quantity * p.unit_price DESC) rk
    FROM inventory i
    JOIN products p ON i.pid = p.pid
    JOIN warehouses w ON i.wid = w.wid
) t WHERE rk <= 3;
```

（3）存储过程 restock_report：
```sql
DELIMITER //
CREATE PROCEDURE restock_report(IN p_wid INT)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_pname VARCHAR(50);
    DECLARE v_qty, v_min, v_max, v_need INT;
    DECLARE cur CURSOR FOR
        SELECT p.pname, i.quantity, i.min_qty, i.max_qty,
               i.max_qty - i.quantity AS need
        FROM inventory i JOIN products p ON i.pid = p.pid
        WHERE i.wid = p_wid AND i.quantity < i.min_qty
        ORDER BY need DESC;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_pname, v_qty, v_min, v_max, v_need;
        IF done THEN LEAVE read_loop; END IF;
        SELECT CONCAT(v_pname, '：当前库存 ', v_qty, '，需补货 ', v_need, ' 件') AS report;
    END LOOP;
    CLOSE cur;
END //
DELIMITER ;
```

**2. 数据库优化**

（1）**慢查询**：执行时间超过阈值的 SQL。开启：`SET GLOBAL slow_query_log = ON; SET long_query_time = 2;`。优化方向：加索引、优化 SQL 写法、调整表结构、升级硬件、使用缓存。

（2）**EXPLAIN**：
   - `type`：访问类型，从好到差：system > const > eq_ref > ref > range > index > ALL
   - `key`：实际使用的索引
   - `rows`：预估扫描行数
   - `Extra`：额外信息（Using index=覆盖索引, Using filesort=需排序, Using temporary=需临时表）

（3）**读写分离方案**：
   - 应用层：使用数据源路由（如 Spring AbstractRoutingDataSource），根据 SQL 类型切换数据源
   - 中间件：使用 MySQL Proxy、ProxySQL、MyCat 等
   - 主从延迟问题：对实时性要求高的读走主库；使用半同步复制减少延迟；业务上容忍一定延迟；通过版本号或时间戳检测数据新鲜度

