# BENCHMARKING


Testing with `ab` tool:

```
ab -n 1000 -c 5 -s 2 -l -H 'Approov-Token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJleHAiOjE0Nzc4MzY4MDAsImlzcyI6IkxVQSAtIEFwcHJvb3YgVG9rZW4gQ2hlY2tlciJ9.ZNmv054qZJC6KIvK-Ycfq6mXV1Qm\-vWRzYB49UU94A0' http://example.com:8000/approov-token-protected

```

and the result:

```
This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking example.com (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        nginx/1.17.3
Server Hostname:        example.com
Server Port:            8000

Document Path:          /approov-token-protected
Document Length:        Variable

Concurrency Level:      5
Time taken for tests:   12.537 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      332000 bytes
HTML transferred:       179000 bytes
Requests per second:    79.76 [#/sec] (mean)
Time per request:       62.686 [ms] (mean)
Time per request:       12.537 [ms] (mean, across all concurrent requests)
Transfer rate:          25.86 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       28   30   2.3     30      53
Processing:    30   32   2.0     32      56
Waiting:       30   32   1.8     32      54
Total:         58   62   3.2     62      87

Percentage of the requests served within a certain time (ms)
  50%     62
  66%     62
  75%     63
  80%     63
  90%     64
  95%     67
  98%     73
  99%     79
 100%     87 (longest request)
 ```

The AWS `t2.micro` instance:

```
$ hostnamectl
   Static hostname: ip-999-0-0-0.eu-west-1.compute.internal
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 0c18f62af54604
           Boot ID: 9d15cb4e81da0a
    Virtualization: xen
  Operating System: Amazon Linux 2
       CPE OS Name: cpe:2.3:o:amazon:amazon_linux:2
            Kernel: Linux 4.14.114-105.126.amzn2.x86_64
      Architecture: x86-64
```

CPU:

```
$ lscpu
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              1
On-line CPU(s) list: 0
Thread(s) per core:  1
Core(s) per socket:  1
Socket(s):           1
NUMA node(s):        1
Vendor ID:           GenuineIntel
CPU family:          6
Model:               63
Model name:          Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz
Stepping:            2
CPU MHz:             2400.188
BogoMIPS:            4800.07
Hypervisor vendor:   Xen
Virtualization type: full
L1d cache:           32K
L1i cache:           32K
L2 cache:            256K
L3 cache:            30720K
NUMA node0 CPU(s):   0
Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology cpuid pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm cpuid_fault invpcid_single pti fsgsbase bmi1 avx2 smep bmi2 erms invpcid xsaveopt
```

MEMORY:

```
free -mt
              total        used        free      shared  buff/cache   available
Mem:            983         603         120           1         259         233
Swap:             0           0           0
Total:          983         603         120
```
