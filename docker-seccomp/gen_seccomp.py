#!/usr/bin/env python3
import json

ALLOW = [
    # 基础 IO / 文件（含 runc 常用）
    "read","write","open","openat","openat2","close","close_range",
    "fstat","fstatat","newfstatat","lseek","statx",
    "fcntl","dup","dup2","dup3","pipe","pipe2","ioctl",
    "access","getcwd",
    # 目录遍历（本次关键：ls / 触发 readdir）
    "readdir","getdents","getdents64",
    # 目录 / 路径
    "chdir","fchdir",
    # fs / proc 探测 + 重新打开（runc 查 mount id / proc magiclink）
    "statfs","fstatfs","fsmount","fsconfig","fsopen","fsmove",
    "reopen","reopenat",
    "mount","umount","umount2",
    # 进程 / 执行
    "execve","execveat","clone","clone3","fork",
    "exit","exit_group","wait4","kill","tkill","tgkill",
    # 用户 / 权限（setup user / setgroups / cap）
    "setgroups","getgroups","setuid","setgid","setreuid","setregid",
    "capget","capset",
    # 内存 / 调度 / 信号
    "mmap","mprotect","mremap","munmap","brk",
    "rt_sigreturn","rt_sigaction","rt_sigprocmask","sigaltstack",
    "sched_yield","nanosleep","futex","getcpu",
    # 基础标识 / 运行时常需
    "arch_prctl","getpid","getuid","getgid","geteuid","getegid",
    "getppid","gettid","set_tid_address","set_robust_list",
    "uname","sysinfo","prctl"
]

policy = {
    "defaultAction": "SCMP_ACT_ERRNO",
    "syscalls": [{"names": ALLOW, "action": "SCMP_ACT_ALLOW"}]
}

with open("seccomp-w6.json","w") as f:
    json.dump(policy, f, indent=2)

print("生成完成: seccomp-w6.json (放行", len(ALLOW), "个 syscall)")
