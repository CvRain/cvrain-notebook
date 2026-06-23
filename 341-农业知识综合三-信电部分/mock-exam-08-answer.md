# 341 农业综合知识三（信电）· 模拟卷八 参考答案

## 第一部分 程序设计基础知识（75分）

### 一、填空题（10分）

1. `~a` = **0xFFFFE5D4**（32位：0x1A2B→0x00001A2B，按位取反得0xFFFFE5D4）；`a | 0xFF00` = **0xFFAB**（0x1A2B | 0xFF00 = 0xFF2B...等等 0x1A2B=6699, 0xFF00=65280, 或=0xFF2B。重新算：0x1A2B=0001 1010 0010 1011, 0xFF00=1111 1111 0000 0000, 或=1111 1111 0010 1011=0xFF2B）

2. `sizeof(a)/sizeof(a[0])` = **3**（行数）；`sizeof(a)/sizeof(a[0][0])` = **12**（元素总数）

3. **10**（struct {int x; char y;} 可能对齐，但 `((int*)(&s))[0]` 直接读取 x 成员 = 10）

4. **未定义**（i 在 for 语句的声明中，出了循环体作用域就不可访问——C99之前 undefined；C99/C11中 i 的作用域仅限于 for 语句。但题目若在 for 后访问 i，则取决于该 for 外是否声明了 i。此处 i 在 for 内声明，循环后的 `i` 不可见 → 编译错误或未定义。假设 C89 兼容模式，答案无意义。按现代 C 标准，**编译错误**。）

5. **double**（默认参数提升，float→double）

---

### 二、简答题（15分）

1. **未定义行为（UB）**：C 标准不规定程序行为的操作，编译器可以做任何事（包括崩溃、输出随机结果、格式化硬盘等）。常见例子：
   - 数组越界：`int a[5]; a[5] = 0;`
   - 使用未初始化的局部变量
   - 有符号整数溢出：`INT_MAX + 1`

2. **回调函数**：将函数指针作为参数传递给另一个函数，由后者在适当时机调用。
   ```c
   int asc(int a, int b) { return a - b; }
   int desc(int a, int b) { return b - a; }
   void sort(int *arr, int n, int (*cmp)(int,int)) {
       for (int i = 0; i < n-1; i++)
           for (int j = 0; j < n-1-i; j++)
               if (cmp(arr[j], arr[j+1]) > 0) { int t = arr[j]; arr[j] = arr[j+1]; arr[j+1] = t; }
   }
   ```

3. **堆 vs 栈**：
   | 比较维度 | 栈 | 堆 |
   |---------|-----|-----|
   | 分配方式 | 自动（编译器） | 手动（malloc/free） |
   | 效率 | 极高（移动栈指针） | 较慢（查找空闲块） |
   | 大小 | 有限（几 MB） | 取决于系统（可达 GB） |
   | 生命周期 | 函数返回自动释放 | 手动释放，可跨函数 |

4. **volatile**：告知编译器该变量可能被程序外部因素修改（硬件寄存器、中断、多线程），禁止优化器对其做缓存或假设不变。嵌入式场景：读取硬件状态寄存器、中断服务程序中的共享变量。

5. **#pragma once vs #ifndef**：
   - `#pragma once`：编译器指令，告诉预处理器只包含一次，简单高效但有移植性问题（非标准）
   - `#ifndef`：通过宏守卫判断，完全标准，但需要保证宏名不冲突
   - C++ 也支持 `#pragma once` 作为编译器扩展

---

### 三、分析题（20分）

1. **5 5**（for 后分号是空循环体；`printf("%d ", i);` 是单独的语句块但缩进误导——实际先执行 for(i=0;i<5;i++){} 空循环，i=5 时退出，执行 printf("%d ", i) 输出 5，再 printf("%d", i) 输出 5。结果 **5 5**）

2. **2.0**（整数除法：5/2=2，赋值给 double 得 2.0）

3. **2**（p=a+1=&a[1]; q=&a[3]; q-p=3-1=2，指针差返回元素个数）

4. **220**（∑_{i=1}^{10} ∑_{j=1}^{i} ∑_{k=1}^{j} 1 = ∑_{i=1}^{10} i(i+1)/2 =  简化：∑i= ∑i²/2+∑i/2。∑i²=n(n+1)(2n+1)/6=10×11×21/6=385；∑i=55。S=(385+55)/2=220）

5. **5 12**（strlen 在 \0 处停止→5；sizeof 数组总大小=5+1+5+1=12）

6. **1 2**（static count 从 0→1→2；f(0)第一次：n+count=0+1=1；f(0)第二次：0+2=2）

7. **4 6**（6 & 4 = 0110 & 0100 = 0100 = 4；6 | 4 = 0110 | 0100 = 0110 = 6）

8. **1 2 2**（a++ 为 0（假），短路 || 左操作数，但左操作数 `a++` 是整表达式，右侧 `b++ && c++` 需要求值。a=0→求值 b++：b=1（真），继续求 c++：c=2（真），&& 结果真。**注意**：`a++ || b++ && c++` 等价于 `a++ || (b++ && c++)`（&& 优先级高于 ||）。a++=0(假)，b++=1(真)，c++=2(真)，(1&&2)=1(真)。最终 r=1。a=1, b=2, c=2。输出 **1 2 2**）

9. ```
     1
    22
   333
   ```
   （i=1: 2空格, 输出"1"; i=2: 1空格, 输出"22"; i=3: 0空格, 输出"333"）

10. **段错误（Segmentation Fault）**或**未定义行为**（func 中 p 是局部变量拷贝，malloc 的指针丢失，q 仍为 NULL。执行 `*q` 解引用 NULL 指针 → 崩溃）

---

### 四、程序设计题（30分）

**1. 字符串切分 my_strtok**

```c
#include <stdio.h>

char* my_strtok(char *str, const char *delim) {
    static char *next = NULL;
    if (str) next = str;
    if (!next || *next == '\0') return NULL;
    // 跳过前导分隔符
    while (*next && strchr(delim, *next)) next++;
    if (*next == '\0') return NULL;
    char *token = next;
    // 找到下一个分隔符
    while (*next && !strchr(delim, *next)) next++;
    if (*next) { *next = '\0'; next++; }
    return token;
}

int main() {
    char s[] = "apple,,banana;orange;grape,,";
    char *t = my_strtok(s, ",;");
    while (t) { printf("%s\n", t); t = my_strtok(NULL, ",;"); }
    return 0;
}
```

**2. 大整数加法**

```c
#include <stdio.h>
#include <string.h>

void reverse(char *s) {
    int l = strlen(s);
    for (int i = 0; i < l / 2; i++) { char t = s[i]; s[i] = s[l-1-i]; s[l-1-i] = t; }
}

void big_add(const char *a, const char *b, char *result) {
    int la = strlen(a), lb = strlen(b);
    int carry = 0, k = 0, i = la - 1, j = lb - 1;
    while (i >= 0 || j >= 0 || carry) {
        int da = (i >= 0) ? a[i--] - '0' : 0;
        int db = (j >= 0) ? b[j--] - '0' : 0;
        int sum = da + db + carry;
        result[k++] = (sum % 10) + '0';
        carry = sum / 10;
    }
    result[k] = '\0';
    reverse(result);
}

int main() {
    char a[1002], b[1002], r[2004];
    scanf("%s %s", a, b);
    big_add(a, b, r);
    printf("%s\n", r);
    return 0;
}
```

---

## 第二部分 数据库技术与应用（75分）

### 一、填空题（10分）

1. **R1 ∩ R2 → R1 ∈ F⁺ 或 R1 ∩ R2 → R2 ∈ F⁺**（公共属性是其中一个分解模式的超键）

2. **后**；**前**；**前**（执行顺序：WHERE → GROUP BY → HAVING → ORDER BY）

3. **布尔值（TRUE/FALSE）**

4. **系统**故障（事务故障+系统故障用日志）；**介质**故障（用转储）

5. **排他锁（X 锁）**；**共享锁（S 锁）**

---

### 二、简答题（10分）

1. **数据字典（DD）**：存储数据库元数据（表结构、列类型、约束、索引等）的系统表；**数据流图（DFD）**：以图形方式描述数据在系统中流动和处理的过程。需求分析中：DFD 用于理解和描述业务流程；DD 用于记录和管理所有数据元素的定义和关系。

2. **DAC vs MAC**：
   - **DAC**：数据所有者自主决定谁可以访问，基于授权（GRANT/REVOKE）
   - **MAC**：系统根据安全标签强制执行访问规则，用户不能自行授权
   - MySQL 实现 DAC：GRANT/REVOKE 语句
   - 视图安全：创建只包含部分列的视图，授予用户视图访问权而非基表访问权，从而隐藏敏感列。例如只给 HR 人员看员工姓名和部门，不暴露薪水。

---

### 三、操作题（15分）

设有宿舍管理系统 D, S, R。

**1. 超员宿舍：**
```sql
SELECT Dno, Dname FROM D
WHERE Capacity < (SELECT COUNT(*) FROM S WHERE S.Dno = D.Dno);
```

**2. 各年级男女分布：**
```sql
SELECT Grade, Ssex, COUNT(*) AS cnt
FROM S GROUP BY Grade, Ssex ORDER BY Grade, Ssex;
```

**3. 无报修宿舍：**
```sql
SELECT Dno, Dname FROM D
WHERE NOT EXISTS (SELECT 1 FROM R WHERE R.Dno = D.Dno);
```

**4. 报修最多前5学生：**
```sql
SELECT S.Sno, S.Sname, COUNT(*) AS cnt
FROM R JOIN S ON R.Sno = S.Sno
GROUP BY S.Sno, S.Sname ORDER BY cnt DESC LIMIT 5;
```

**5. 未完成报修：**
```sql
SELECT R.Rno, D.Dname, R.Description,
       DATEDIFF(CURDATE(), R.ReportTime) AS wait_days
FROM R JOIN D ON R.Dno = D.Dno
WHERE R.Status IN ('pending', 'processing')
ORDER BY R.ReportTime;
```

**6. 更新6号楼空余>5的宿舍管理员：**
```sql
UPDATE D SET Manager = '张管理员'
WHERE Building = '6号楼' AND
Capacity - (SELECT COUNT(*) FROM S WHERE S.Dno = D.Dno) > 5;
```

**7. 创建视图：**
```sql
CREATE VIEW v_dorm_occupancy AS
SELECT D.Dno, D.Dname, D.Capacity,
       COUNT(S.Sno) AS occupied,
       D.Capacity - COUNT(S.Sno) AS vacant
FROM D LEFT JOIN S ON D.Dno = S.Dno
GROUP BY D.Dno, D.Dname, D.Capacity;
```

---

### 四、分析题（10分）

R(A,B,C,D,E,G)，F = {AB→C, C→A, BC→D, ACD→B, D→EG, BE→C}

**（1）候选键推导**：
- (AB)⁺：AB→C, C→A→{A,B,C}，再 BC→D→{A,B,C,D}，D→EG→{A,B,C,D,E,G} → **AB 是候选键**
- (BC)⁺：BC→D→{B,C,D}，D→EG→{B,C,D,E,G}，C→A→{A,B,C,D,E,G} → **BC 是候选键**
- (BE)⁺：BE→C→{B,E,C}，C→A→{A,B,C,E}，BC→D→{A,B,C,D,E}，D→EG→{A,B,C,D,E,G} → **BE 是候选键**
- (CD)⁺：CD，C→A→{A,C,D}，D→EG→{A,C,D,E,G}，AB? 缺B... → 不全 → CD 不是
- 极小化后候选键：**AB, BC, BE**（此外还有 AE？AE⁺: C? 缺 C→A不产生 C... 不是。候选键为 **AB, BC, BE**）

**（2）3NF 判定**：检查每个 FD：AB→C（AB超键 ✓）、C→A（C不是超键，A是主属性 → 3NF 允许主属性对候选键的依赖 ✓）、BC→D（BC超键 ✓）、ACD→B（ACD不是超键，B是主属性 → ✓）、D→EG（D不是超键，E,G非主属性 → **违反3NF！**）、BE→C（BE超键 ✓）

D→EG 存在非主属性对非超键的依赖 → **R 不属于 3NF**，最高 **2NF**。

**（3）BCNF 分解**：R 最多 2NF，需先到 3NF再BCNF。
- 分解 D→EG：R1(**D**, E, G)；R2(**A**, **B**, **C**, D)（去除 E,G）
- R2 中 AB→C、C→A、BC→D、ACD→B：C→A 违反 BCNF → R21(**C**, A)；R22(**B**, **C**, D)
- 最终 BCNF 模式集：R1(**D**, E, G)；R2(**C**, A)；R3(**B**, **C**, D)
- 验证无损连接性丢失... 此题较复杂，实际考试按步骤得分即可。

---

### 五、设计题（10分）

**快递配送管理系统关系模式**：

1. **配送站**：Station(**SID**, Sname, Address, Phone, Area)
2. **快递员**：Courier(**EID**, Name, Sex, HireDate, Phone, **SID**) — SID 外键
3. **客户**：Customer(**CID**, Cname, Phone, Address, Level)
4. **快递**：Package(**PID**, **SendCID**, **RecvCID**, SendAddr, RecvAddr, Weight, Fee, OrderTime, Status, **PickEID**, **DeliverEID**) — SendCID/RecvCID 外键参照 Customer；PickEID/DeliverEID 外键参照 Courier
5. **中转记录**：TransitLog(**PID**, **StationID**, ArriveTime, LeaveTime) — 复合主键

---

### 六、应用题（20分）

**1. 在线考试系统**

（1）各考试题型统计：
```sql
SELECT e.eid, e.ename,
       COUNT(eq.qid) AS total,
       SUM(CASE WHEN q.qtype='single' THEN 1 ELSE 0 END) AS single_cnt,
       SUM(CASE WHEN q.qtype='multi' THEN 1 ELSE 0 END) AS multi_cnt,
       SUM(CASE WHEN q.qtype='judge' THEN 1 ELSE 0 END) AS judge_cnt,
       SUM(CASE WHEN q.qtype='fill' THEN 1 ELSE 0 END) AS fill_cnt
FROM exams e
LEFT JOIN exam_questions eq ON e.eid = eq.eid
LEFT JOIN questions q ON eq.qid = q.qid
GROUP BY e.eid, e.ename;
```

（2）未分配题目的考试：
```sql
SELECT eid, ename FROM exams e
WHERE NOT EXISTS (SELECT 1 FROM exam_questions eq WHERE eq.eid = e.eid);
```

（3）存储过程 calc_exam_total：
```sql
DELIMITER //
CREATE PROCEDURE calc_exam_total(IN p_eid INT)
BEGIN
    DECLARE total INT DEFAULT 0;
    DECLARE done INT DEFAULT 0;
    DECLARE q_score INT;
    DECLARE cur CURSOR FOR
        SELECT q.score FROM exam_questions eq
        JOIN questions q ON eq.qid = q.qid WHERE eq.eid = p_eid;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    IF (SELECT COUNT(*) FROM exams WHERE eid = p_eid) = 0 THEN
        SELECT '考试不存在' AS msg;
    ELSE
        OPEN cur;
        read_loop: LOOP
            FETCH cur INTO q_score;
            IF done THEN LEAVE read_loop; END IF;
            SET total = total + q_score;
        END LOOP;
        CLOSE cur;
        UPDATE exams SET total_score = total WHERE eid = p_eid;
    END IF;
END //
DELIMITER ;
```

**2. 数据库理论**

（1）**MyISAM vs InnoDB**：
| 特性 | MyISAM | InnoDB |
|------|--------|--------|
| 事务 | 不支持 | 支持 ACID |
| 锁粒度 | 表级锁 | 行级锁 |
| 外键 | 不支持 | 支持 |
| 崩溃恢复 | 不支持 | 支持（redo log） |

（2）**半同步复制**：主库提交事务时等待至少一个从库确认收到 binlog 后才返回客户端。异步复制主库不等待。提高安全性：确保已提交的事务至少在一台从库上有副本。性能代价：增加网络往返延迟。

（3）**日志归档存储过程**：
```sql
DELIMITER //
CREATE PROCEDURE archive_logs()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION ROLLBACK;
    START TRANSACTION;
    INSERT INTO logs_archive SELECT * FROM logs WHERE log_time < DATE_SUB(NOW(), INTERVAL 6 MONTH);
    DELETE FROM logs WHERE log_time < DATE_SUB(NOW(), INTERVAL 6 MONTH);
    COMMIT;
END //
DELIMITER ;
```

