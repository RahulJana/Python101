# Normalization

1. Ref 1: https://www.youtube.com/watch?v=bqhQ2LWBheQ

## Methods of Normalization


### 🔹 1. **Min-Max Normalization (Rescaling)**

* **Formula**:

  $$
  X_{\text{norm}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}}
  $$
* **Range**: Scales data to a specific range, usually $[0, 1]$.
* **Use case**: When you know the **min and max** values and the data **doesn’t have significant outliers**.
* **Common in**: Deep learning, computer vision, neural networks.

---

### 🔹 2. **Z-Score Normalization (Standardization)**

* **Formula**:

  $$
  X_{\text{std}} = \frac{X - \mu}{\sigma}
  $$

  where $\mu$ = mean, $\sigma$ = standard deviation
* **Range**: Not fixed (can be negative or greater than 1), but mean becomes 0 and standard deviation becomes 1.
* **Use case**: When data follows a **Gaussian distribution** or contains **outliers**.
* **Common in**: General ML models like regression, SVM, logistic regression.

---

### 🔹 3. **Max Abs Scaling**

* **Formula**:

  $$
  X_{\text{scaled}} = \frac{X}{|X_{\max}|}
  $$
* **Range**: $[-1, 1]$
* **Use case**: When data is already **centered at zero** and you want to preserve sparsity (e.g. sparse data like text vectors).
* **Common in**: NLP tasks, large sparse matrices.

---

### 🔹 4. **Decimal Scaling Normalization**

* **Formula**:

  $$
  X_{\text{scaled}} = \frac{X}{10^j}
  $$

  where $j$ is the smallest integer such that the **max absolute value** of $X_{\text{scaled}}$ is less than 1.
* **Use case**: Simple datasets with well-understood magnitude.
* **Rarely used** in practice today, more theoretical or academic.

---

### 🔹 5. **Robust Scaling (Using IQR)**

* **Formula**:

  $$
  X_{\text{scaled}} = \frac{X - \text{median}}{\text{IQR}}
  $$

  where IQR = Interquartile Range = Q3 - Q1
* **Range**: Not fixed, but resistant to outliers.
* **Use case**: When data has **many outliers** and you want a **robust** method.
* **Common in**: Real-world messy datasets (e.g. finance, sensor data).

---

### 🔹 6. **Unit Vector Normalization (L2 or L1 Normalization)**

* **Formula (L2)**:

  $$
  X_{\text{norm}} = \frac{X}{\|X\|_2}
  $$

  where $\|X\|_2 = \sqrt{x_1^2 + x_2^2 + \dots + x_n^2}$
* **Use case**: When you want to scale features as vectors with unit length (e.g., in **text classification**, **cosine similarity**).
* **Common in**: NLP, information retrieval, recommendation systems.

---

### 📊 Comparison Table

| Method           | Range       | Sensitive to Outliers? | Suitable For                 |
| ---------------- | ----------- | ---------------------- | ---------------------------- |
| Min-Max          | \[0, 1]     | Yes                    | Bounded data, image data     |
| Z-Score          | \~\[-3, 3]  | No                     | Normal-distributed features  |
| Max Abs          | \[-1, 1]    | Yes                    | Sparse, zero-centered data   |
| Decimal Scaling  | \[-1, 1]    | Yes                    | Simple numerical data        |
| Robust Scaling   | Varies      | No                     | Data with many outliers      |
| Unit Vector (L2) | Unit length | Yes                    | Text/vector similarity tasks |



## Normalization vs Standardazation

### 🔹 What is Feature Scaling?

* A **preprocessing step** in machine learning used to ensure that all features are on a similar scale.
* Prevents **one feature from dominating** others due to different value ranges.
* Commonly used before training models like neural networks or regression algorithms.

---

### 🔹 Why Feature Scaling is Needed:

* Features like **interest rate**, **employment score**, and **S\&P 500 index** can have drastically different ranges.
* For example:

  * Interest rates: 1.5–3
  * Employment score: 40–70
  * S\&P 500: 1800–3000
* Without scaling, these differences can bias machine learning models.

---

### 🔹 Normalization

* **Objective**: Scale data to a **\[0, 1]** range.
* Also called **Min-Max Scaling**.
* **Formula**:

  $$
  X_{\text{norm}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}}
  $$
* Example:

  * A value of 2206 scaled between a min of 1800 and a max of 3000 becomes ≈ 0.338.
  * Minimum becomes 0, maximum becomes 1.

**Key Points:**

* Used when the **distribution is unknown** or **not Gaussian**.
* Common in **neural networks** and **deep learning**.

---

### 🔹 Standardization

* **Objective**: Transform data to have **mean = 0** and **standard deviation = 1**.

* Also called **Z-score normalization**.

* **Formula**:

  $$
  X_{\text{std}} = \frac{X - \mu}{\sigma}
  $$

  where:

  * $\mu$: mean
  * $\sigma$: standard deviation

* Example:

  * A value of 2206 with mean 2319 and std dev 193 becomes ≈ -0.583.
  * Mean becomes 0, standard deviation becomes 1.
  * Minimum and maximum values can vary (e.g., -2.67 to +3.5), not restricted like normalization.

**Key Points:**

* Better for data with a **Gaussian (normal) distribution**.
* More robust when **outliers** are present.

---

### 🔹 When to Use Which?

| Situation                                                                           | Use Normalization | Use Standardization |
| ----------------------------------------------------------------------------------- | ----------------- | ------------------- |
| Data distribution is unknown or not Gaussian                                        | ✅                 | ❌                   |
| Data follows Gaussian distribution                                                  | ❌                 | ✅                   |
| You have outliers                                                                   | ❌                 | ✅                   |
| Algorithm needs gradient descent (e.g. neural networks, linear/logistic regression) | ✅                 | ✅                   |
| Tree-based or distance-based models (e.g. KNN, SVM, decision trees, XGBoost)        | ❌ (optional)      | ❌ (optional)        |

---

### 🔹 Algorithms that **require scaling**:

* Linear Regression
* Logistic Regression
* Neural Networks (ANNs, DNNs)
* Any algorithm using **gradient descent**

### 🔹 Algorithms that **do not require scaling**:

* Decision Trees
* Random Forests
* XGBoost
* K-Nearest Neighbors (can optionally benefit from scaling)
* SVM (when kernel is used)
