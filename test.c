#include <seccomp.h>
#include <unistd.h>

int main() {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);

    // 放行必要的系统调用
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);

    seccomp_load(ctx);

    // 用最底层的 write 打印，避开 printf 的底层坑
    const char *msg = "hello，我还在\n";
    write(1, msg, 13);

    // 尝试执行 ls（ls 内部会被拦，符合预期）
    execlp("/bin/ls", "ls", NULL);

    // 兜底退出
    _exit(0);
}

