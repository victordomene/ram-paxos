---
title: RAM-ified Part-Time Parliament
author:
- name: Victor Domene
  email: victordomene@college.harvard.edu
- name: Gabriel Guimaraes
  email: gabrielguimaraes@college.harvard.edu
- name: Brian Arroyo
  email: brianarroyo@college.harvard.edu
date: May 6th, 2016
fontsize: 12pt
geometry: margin=3cm
toc: true
linestretch: 1.2
documentclass: article
numbersections: true
abstract: |
  With the rise of persistent memory technologies [2], it is possible that 
  in the near future we will have RAM-speed access with byte-granularity persistence.
  In this project, we seek to measure the performance differences between
  a Paxos implementation that uses disks as its *ledger* [1], and another that
  simply uses RAM. This may provide some insight into new applications of Paxos,
  where the algorithm may be ignored due to its low performance. This paper
  describes our implementation of the Paxos algorithm in Python (which, on its own right,
  deserves a great deal of attention) and presents benchmarking information on
  several workloads designed to stress the ledgers. (XXX CONCLUDE BY ADDING A
  VERY BRIEF SUMMARY OF OUR FINDINGS).
---

\newpage

# Introduction

# Paxos Implementation

## Initial Design: Messaging System

### Using Google's gRPC

### Using our own RDTP (Real Data Transfer Protocol)

## Alternative Designs

### Using gRPC in a better way

## Final Design

# Workloads

## Workload A

## Workload B

# Benchmarks

# References
