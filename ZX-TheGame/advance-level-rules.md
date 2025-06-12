# Advance Level Walkthroughs (Spoiler Alert!)

Below are the optimal steps for each level in the ZX-calculus simplification game. Use them as hints or a full guide to master the rules efficiently.

---

## 🧩 Level 1: The Simple Identity

**Initial Diagram:**  
`W(0) -- Z(1, φ=0.00π) -- W(2)`

**Optimal Moves (1):**
1. Choose **Rule 2** (Identity Rule).
2. Enter ID of spider: `1`

**Result:**  
`W(0) -- W(2)` ✅ **(Win!)**

---

## 🧩 Level 2: Fusing Spiders

**Initial Diagram:**  
`W(0) -- Z(1, φ=1.00π) -- Z(2, φ=1.00π) -- W(3)`

**Optimal Moves (2):**
1. Choose **Rule 1** (Spider Fusion).
   - Enter ID of first spider: `1`
   - Enter ID of second spider: `2`  
   _(Diagram becomes: `W(0) -- Z(1, φ=2.00π) -- W(3)` → Note: `2.00π ≡ 0.00π`)_

2. Choose **Rule 2** (Identity Rule).
   - Enter ID of spider: `1`

**Result:**  
`W(0) -- W(3)` ✅ **(Win!)**

---

## 🧩 Level 3: Hadamard Challenges

**Initial Diagram:**  
`W(0) -- Z(1, φ=0.00π) -- H(2) -- X(3, φ=0.00π) -- H(4) -- W(5)`

**Optimal Moves (4):**

1. Choose **Rule 3** (Hadamard Color Change).
   - Enter ID of Hadamard node: `2`
   - Enter ID of connected spider: `1`  
   _(Diagram becomes: `W(0) -- X(1, φ=0.00π) -- X(3, φ=0.00π) -- H(4) -- W(5)`)_

2. Choose **Rule 1** (Spider Fusion).
   - Enter ID of first spider: `1`
   - Enter ID of second spider: `3`  
   _(Diagram becomes: `W(0) -- X(1, φ=0.00π) -- H(4) -- W(5)`)_

3. Choose **Rule 3** (Hadamard Color Change).
   - Enter ID of Hadamard node: `4`
   - Enter ID of connected spider: `1`  
   _(Diagram becomes: `W(0) -- Z(1, φ=0.00π) -- W(5)`)_

4. Choose **Rule 2** (Identity Rule).
   - Enter ID of spider: `1`

**Result:**  
`W(0) -- W(5)` ✅ **(Win!)**

---

🎮 Enjoy playing and mastering the basics of ZX-calculus simplification through interactive gameplay and logical reasoning!
