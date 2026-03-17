# Embedding 向量嵌入

获取给定输入的向量表示，可以轻松被机器学习模型和算法使用。

## 什么是嵌入向量？

嵌入向量是浮点数的向量（列表），用于衡量文本字符串的相关性。两个向量之间的距离衡量它们的相关性：小距离表示高相关性，大距离表示低相关性。

嵌入通常用于：
- **搜索** - 结果按与查询字符串的相关性排序
- **聚类** - 文本字符串按相似性分组
- **推荐** - 推荐具有相关文本字符串的项目
- **异常检测** - 识别相关性较低的异常值
- **分类** - 文本字符串按其最相似的标签分类

## 快速开始

### 安装 SDK

```bash
pip install openai
```

### 基础示例

> 请确保将 `$MODELVERSE_API_KEY` 替换为您自己的 API Key，获取 [API Key](https://console.ucloud.cn/modelverse/experience/api-keys)。

<!-- tabs:start -->
#### ** Python **

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_MODELVERSE_API_KEY",
    base_url="https://api.modelverse.cn/v1"
)

response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-large"
)

print(response.data[0].embedding)
```

#### ** curl **

```bash
curl https://api.modelverse.cn/v1/embeddings \
  -H "Authorization: Bearer $MODELVERSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Your text string goes here",
    "model": "text-embedding-3-large"
  }'
```
<!-- tabs:end -->

响应包含嵌入向量（浮点数列表）以及一些附加元数据。您可以提取嵌入向量，将其保存在向量数据库中，并用于许多不同的用例。

## API 参考

**POST** `https://api.modelverse.cn/v1/embeddings`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| input | string 或 array | 是 | 要嵌入的输入文本，编码为字符串或 token 数组。要在单个请求中嵌入多个输入，请传递字符串数组。输入不得超过 8192 个 token，不能为空字符串。单个请求中所有输入的 token 总和最多为 300,000 个。 |
| model | string | 是 | 要使用的模型 ID，如 `text-embedding-3-large`。 |
| dimensions | integer | 否 | 生成的输出嵌入向量应具有的维度数。仅在 text-embedding-3 及更高版本的模型中支持。 |
| encoding_format | string | 否 | 返回嵌入向量的格式。可以是 `float` 或 `base64`。默认值：`float` |

### 响应示例

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.0023064255, -0.009327292, ..., -0.0028842222],
      "index": 0
    }
  ],
  "model": "text-embedding-3-large",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| embedding | array | 嵌入向量，是一个浮点数列表。向量的长度取决于模型。 |
| index | integer | 嵌入在嵌入列表中的索引。 |
| object | string | 对象类型，始终为 "embedding"。 |

## 嵌入模型

| 模型 | 默认维度 | 最大输入 | MTEB 评估性能 |
|------|---------|---------|--------------|
| text-embedding-3-large | 3072 | 8192 | 64.6% |
| text-embedding-ada-002 | 1536 | 8192 | 61.0% |

## 降低嵌入维度

使用较大的嵌入向量通常成本更高，消耗更多的计算、内存和存储。您可以通过传入 `dimensions` 参数来缩短嵌入维度，而不会丢失嵌入的概念表示属性。

例如，`text-embedding-3-large` 嵌入可以缩短到 256 维，同时仍然优于 1536 维的 `text-embedding-ada-002`。

<!-- tabs:start -->
#### ** Python **

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_MODELVERSE_API_KEY",
    base_url="https://api.modelverse.cn/v1"
)

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="Testing 123",
    dimensions=256  # 指定输出维度
)

print(response.data[0].embedding)
```

#### ** curl **

```bash
curl https://api.modelverse.cn/v1/embeddings \
  -H "Authorization: Bearer $MODELVERSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Testing 123",
    "model": "text-embedding-3-large",
    "dimensions": 256
  }'
```
<!-- tabs:end -->

### 手动归一化维度

如果需要手动截断并归一化嵌入向量：

```python
from openai import OpenAI
import numpy as np

client = OpenAI(
    api_key="YOUR_MODELVERSE_API_KEY",
    base_url="https://api.modelverse.cn/v1"
)

def normalize_l2(x):
    x = np.array(x)
    if x.ndim == 1:
        norm = np.linalg.norm(x)
        if norm == 0:
            return x
        return x / norm
    else:
        norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
        return np.where(norm == 0, x, x / norm)

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="Testing 123",
    encoding_format="float"
)

cut_dim = response.data[0].embedding[:256]
norm_dim = normalize_l2(cut_dim)
print(norm_dim)
```

## 使用场景

### 1. 文本搜索

使用查询的嵌入向量和每个文档之间的余弦相似度，返回得分最高的文档。

```python
from openai import OpenAI
import numpy as np

client = OpenAI(
    api_key="YOUR_MODELVERSE_API_KEY",
    base_url="https://api.modelverse.cn/v1"
)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_embedding(text, model="text-embedding-3-large"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def search_documents(documents, query, n=3):
    query_embedding = get_embedding(query)
    
    results = []
    for doc in documents:
        doc_embedding = get_embedding(doc)
        similarity = cosine_similarity(query_embedding, doc_embedding)
        results.append((doc, similarity))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:n]

# 示例
documents = ["Python 是一种编程语言", "机器学习很有趣", "今天天气很好"]
results = search_documents(documents, "编程")
print(results)
```

### 2. 基于嵌入的问答

将相关文档放入模型的上下文窗口中进行问答。

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_MODELVERSE_API_KEY",
    base_url="https://api.modelverse.cn/v1"
)

# 假设已通过嵌入搜索找到相关文章
relevant_article = "2022年冬季奥运会冰壶金牌由..."

query = f"""使用以下文章回答问题。如果找不到答案，请写"我不知道。"

文章：
\"\"\"
{relevant_article}
\"\"\"

问题：哪些运动员在 2022 年冬季奥运会上获得了冰壶金牌？
"""

response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': '你回答有关 2022 年冬季奥运会的问题。'},
        {'role': 'user', 'content': query},
    ],
    model="gpt-4o",
    temperature=0,
)

print(response.choices[0].message.content)
```

### 3. 聚类分析

使用嵌入向量对文本进行聚类分组。

```python
import numpy as np
from sklearn.cluster import KMeans

# 假设 embeddings 是已获取的嵌入向量列表
embeddings = [...]  # 从 API 获取的嵌入向量

matrix = np.vstack(embeddings)
n_clusters = 4

kmeans = KMeans(
    n_clusters=n_clusters,
    init='k-means++',
    random_state=42
)
kmeans.fit(matrix)

# 每个文本的聚类标签
labels = kmeans.labels_
```

### 4. 推荐系统

基于嵌入向量的相似度进行推荐。

```python
from openai import OpenAI
import numpy as np

client = OpenAI(
    api_key="YOUR_MODELVERSE_API_KEY",
    base_url="https://api.modelverse.cn/v1"
)

def get_embedding(text, model="text-embedding-3-large"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def recommend_similar(items, source_index, n=3):
    """返回与源项目最相似的 n 个项目"""
    embeddings = [get_embedding(item) for item in items]
    source_embedding = embeddings[source_index]
    
    similarities = []
    for i, emb in enumerate(embeddings):
        if i != source_index:
            sim = np.dot(source_embedding, emb)
            similarities.append((i, items[i], sim))
    
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:n]
```

### 5. 零样本分类

无需训练数据，使用嵌入进行分类。

```python
from openai import OpenAI
import numpy as np

client = OpenAI(
    api_key="YOUR_MODELVERSE_API_KEY",
    base_url="https://api.modelverse.cn/v1"
)

def get_embedding(text, model="text-embedding-3-large"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def classify_text(text, labels):
    text_embedding = get_embedding(text)
    label_embeddings = [get_embedding(label) for label in labels]
    
    similarities = [cosine_similarity(text_embedding, le) for le in label_embeddings]
    best_index = np.argmax(similarities)
    return labels[best_index]

# 示例
labels = ["positive", "negative", "neutral"]
result = classify_text("这个产品太棒了！", labels)
print(result)  # 输出: positive
```

## 常见问题

### 如何计算字符串的 token 数量？

使用 OpenAI 的分词器 [`tiktoken`](https://github.com/openai/tiktoken)：

```python
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """返回文本字符串中的 token 数量。"""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

print(num_tokens_from_string("tiktoken is great!"))  # 输出: 4
```

> 对于第三代嵌入模型（如 `text-embedding-3-large`），使用 `cl100k_base` 编码。

### 如何快速检索 K 个最近的嵌入向量？

为了快速搜索大量向量，建议您使用向量数据库，如：
- AI 数据库（参考文档：[AI数据库](https://docs.ucloud.cn/aidb/README)）
- pgvector (参考文档：[PostgreSQL](https://docs.ucloud.cn/upgsql/README))

### 应该使用哪个距离函数？

推荐使用**余弦相似度**。OpenAI 嵌入已归一化为长度 1，这意味着：
- 余弦相似度可以仅使用点积计算，速度更快
- 余弦相似度和欧几里得距离将产生相同的排名
