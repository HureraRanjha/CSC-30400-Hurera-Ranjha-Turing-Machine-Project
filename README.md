# CSC-30400-Hurera-Ranjha-Turing-Machine-Project

**Author:** Hurera Ranjha  
**EMPLID:** 24418873  

### 📎 Submission Note for Professor
Please refer to the following files in my GitHub repository for all components of the project:

- **[TM1d-24418873.txt](TM1d-24418873.txt)** — Custom Turing Machine decider description  
- **[TM1-24418873.txt](TM1-24418873.txt)** — Tape input file  
- **[results-TM1-24418873.txt](results-TM1-24418873.txt)** — Computation trace/output  
- **[TM1d-24418873.pdf](TM1d-24418873.pdf)** — TM1 decider documentation  
- **[TM2-24418873.pdf](TM2-24418873.pdf)** — TM2 machine documentation  
- **[readme-24418873.pdf](readme-24418873.pdf)** — Full project write-up  


## 📌 Overview
This project is a **multi-tape Turing Machine simulator** written in Python.  
It loads two input files:

1. **Machine Description File** — specifies the TM name, number of tapes, max steps, alphabets, states, and transitions.  
2. **Tape File** — contains the test inputs to run through the machine.

The simulator then parses both files, initializes the tapes, applies transitions step-by-step, and outputs a full trace including:  
- Step number  
- Rule number
- Tape head positions  
- Current state  
- Symbols read  
- Symbols written  
- Head movement (L/R/S)  
- Final Accept/Reject status  

Repository link:  
https://github.com/HureraRanjha/CSC-30400-Hurera-Ranjha-Turing-Machine-Project

---

## 🚀 How to Run the Program

### 1. Verify Python 3 is installed
```bash
python --version
```
### 2. Navigate to the project directory
```bash
cd CSC-30400-Hurera-Ranjha-Turing-Machine-Project
```
### 3. Run the simulator with
```bash
python TM-24418873.py <machine_file> <tape_file>
```




