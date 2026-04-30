# Adder Selection Document

## Selected Adders

For this project, the two selected baseline adder architectures are:

1. **RCA8 (8-bit Ripple Carry Adder)**
2. **CLA8 (8-bit Carry Lookahead Adder baseline, later optimized into a delay-oriented hybrid form)**

These two adders were chosen because they represent two fundamentally different design philosophies in digital arithmetic:

- RCA emphasizes simplicity and low hardware cost.
- CLA emphasizes speed through faster carry computation.

This makes them ideal candidates for architectural comparison and optimization exploration.

---

## 1. RCA8 – Ripple Carry Adder

### Why RCA8 Was Selected

RCA8 was selected because it is the most basic and widely used adder architecture.  
It serves as an essential reference baseline for evaluating optimization improvements.

### Architectural Characteristics

In an RCA:

- Each bit computes sum and carry sequentially.
- Carry-out from one stage becomes carry-in for the next stage.
- Carry propagation must ripple through all 8 stages.

### Advantages

- Very simple structure
- Low area overhead
- Easy to design and verify

### Disadvantages

- Slow carry propagation
- Delay increases linearly with bit width

### Delay Behavior

Critical path:

```text
c0 → c1 → c2 → c3 → c4 → c5 → c6 → c7 → cout

```

## 2. CLA8 – Carry Lookahead Adder

### Why CLA8 Was Selected
CLA8 was selected because it represents a high-speed adder architecture designed to reduce carry delay. Unlike RCA, CLA computes carries in parallel using propagate and generate logic. This makes CLA an excellent contrast to RCA in timing-performance experiments.

### Architectural Characteristics
CLA computes:
- **Generate**: $g = a \ \& \ b$
- **Propagate**: $p = a \oplus b$

Carries are calculated using lookahead equations such as:
- $c_1 = g_0 + p_0 \cdot c_{in}$
- $c_2 = g_1 + p_1 \cdot g_0 + p_1 \cdot p_0 \cdot c_{in}$
- $c_3 = \dots$

This avoids sequential ripple carry delay.

### Advantages
- **Faster carry computation**: Parallel logic reduces the wait time for higher-order bits.
- **Lower critical path delay**: Significantly improves timing over linear ripple chains.
- **Better timing scalability**: More efficient as bit-width increases.

### Disadvantages
- **More complex logic**: Requires additional gates for the lookahead logic.
- **Larger area cost**: The hardware footprint is noticeably larger than RCA.
- **Higher fan-in gates**: Complexity in synthesis increases due to gate input limitations.

### Optimization Observation
During delay-mode optimization, the original CLA baseline evolved into a **carry-select style hybrid architecture** rather than remaining a pure textbook CLA. 

This indicates that under synthesis optimization, the tool identified a **CSA-like hybrid structure** as more delay-efficient in the given technology library. Thus, the optimized CLA design became a delay-oriented hybrid adder derived from CLA principles.

---

## 3. Architectural Differences Summary

| Feature | RCA8 | CLA8 |
| :--- | :--- | :--- |
| **Carry Method** | Sequential ripple propagation | Parallel lookahead carry computation |
| **Speed** | Slower | Faster |
| **Area** | Smaller | Larger |
| **Complexity** | Low | High |
| **Scalability** | Poor for larger widths | Better for larger widths |

---

## 4. Why These Two Together?

Selecting RCA8 and CLA8 creates a meaningful comparison because:
- **RCA** provides a low-complexity, area-efficient baseline.
- **CLA** provides a high-speed, performance-oriented baseline.

Together, they allow evaluation of:
- **Area vs. delay tradeoffs**: Measuring exactly how much area is traded for speed.
- **Structural optimization behavior**: Seeing how tools manipulate different logic structures.
- **Synthesis transformation**: Observing how a starting architecture dictates the final optimized form.

---

## Conclusion

RCA8 and CLA8 were selected because they represent opposite ends of the adder design spectrum: **RCA** prioritizes simplicity and compactness, while **CLA** prioritizes speed and parallel carry computation. Their contrasting architectures make them ideal for studying optimization tradeoffs in digital adder synthesis.