# mini-CAGE

ARC-Brake 前身实验：用 seccomp 实现最小可用的系统调用沙箱运行时。

## 目录结构

docker-seccomp/gen_seccomp.py — 从 syscall 清单生成 seccomp-bpf JSON profile

docker-seccomp/seccomp-w5.json — W5 基础白名单

docker-seccomp/seccomp-w6.json — W6 版本，82 条 syscall 精简白名单（当前主线）

test.c — 沙箱内测试负载

.gitignore — 排除编译产物、缓存、虚拟机磁盘

## 快速上手

用 Docker 跑沙箱：
docker run --rm --security-opt seccomp=./docker-seccomp/seccomp-w6.json ubuntu:22.04 echo "hello"

验证网络拦截：
docker run --rm --security-opt seccomp=./docker-seccomp/seccomp-w6.json ubuntu:22.04 bash -c "exec 3<>/dev/tcp/127.0.0.1/80"
预期：连接被拒或收到 SIGSYS

重新生成 profile：
cd docker-seccomp && python3 gen_seccomp.py > seccomp-w6.json

## W4-W6 实验记录

W4：跑通 seccomp 最小 demo，确认 ALLOW/ERRNO 行为
W5：从 strace 结果挑出最小集合，写成第一版 JSON
W6：逐条砍到 82 条 syscall，test.c 回归验证通过

## 下一步

- eBPF 审计：把被拦的 syscall 记进 trace pipe
- 对比 seccomp 与 eBPF 观测开销
- 补 test.c 回归用例

## 环境

Ubuntu 24.04 / Docker 24.x+ / Python 3.10+
