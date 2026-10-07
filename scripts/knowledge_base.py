"""
AIToolCrux 知识库 - 向量数据库管理
用Chroma存储所有重要决策、SOP、踩坑经验，AI执行前先检索相关上下文，解决"失忆"问题。

用法：
  from scripts.knowledge_base import KnowledgeBase
  kb = KnowledgeBase()
  kb.add("决策", "迁移到Cloudflare Pages因为Vercel免费额度用完", {"date": "2026-10-02", "category": "infrastructure"})
  results = kb.search("如何修复tools路由503", n=5)
"""
import os
import json
from datetime import datetime

try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("[WARN] chromadb未安装，知识库功能不可用。运行: pip install chromadb")


class KnowledgeBase:
    """向量数据库知识库，存储决策、SOP、经验、踩坑记录"""

    def __init__(self, persist_dir=None):
        if not CHROMA_AVAILABLE:
            self.client = None
            self.collection = None
            return

        if persist_dir is None:
            persist_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "iteration_center", "knowledge_base"
            )
        os.makedirs(persist_dir, exist_ok=True)
        self.persist_dir = persist_dir

        self.client = chromadb.PersistentClient(path=persist_dir)

        # 使用默认embedding函数（all-MiniLM-L6-v2，本地运行，不需要API key）
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        # 创建/获取集合
        self.collection = self.client.get_or_create_collection(
            name="aitoolcrux_knowledge",
            embedding_function=self.embedding_fn,
            metadata={"description": "AIToolCrux项目知识库，存储决策、SOP、经验、踩坑记录"}
        )

    def add(self, doc_type, content, metadata=None):
        """
        添加一条知识到向量数据库

        Args:
            doc_type: 类型（决策/SOP/经验/踩坑/工具/报告）
            content: 内容文本
            metadata: 额外元数据（date, category, source等）
        """
        if not self.collection:
            print("[WARN] 知识库未初始化")
            return None

        if metadata is None:
            metadata = {}

        metadata["doc_type"] = doc_type
        metadata["created_at"] = datetime.now().isoformat()

        # 生成唯一ID
        doc_id = f"{doc_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{abs(hash(content)) % 10000}"

        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return doc_id

    def search(self, query, n=5, doc_type=None):
        """
        语义搜索相关知识

        Args:
            query: 搜索查询
            n: 返回结果数量
            doc_type: 可选，按类型过滤

        Returns:
            list of dict: [{"content": ..., "metadata": ..., "distance": ...}]
        """
        if not self.collection:
            return []

        where = {"doc_type": doc_type} if doc_type else None

        results = self.collection.query(
            query_texts=[query],
            n_results=n,
            where=where
        )

        output = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                output.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                })
        return output

    def get_context_for_task(self, task_description, n=5):
        """
        为某个任务获取相关上下文（AI执行前调用）

        Args:
            task_description: 任务描述
            n: 返回结果数量

        Returns:
            str: 格式化的上下文文本
        """
        results = self.search(task_description, n=n)
        if not results:
            return "（无相关历史上下文）"

        context_parts = ["【相关历史上下文】"]
        for i, r in enumerate(results, 1):
            doc_type = r["metadata"].get("doc_type", "未知")
            date = r["metadata"].get("created_at", "未知")[:10]
            context_parts.append(f"\n{i}. [{doc_type}] ({date})\n   {r['content'][:300]}")
        return "\n".join(context_parts)

    def stats(self):
        """获取知识库统计"""
        if not self.collection:
            return {"status": "未初始化"}
        count = self.collection.count()
        return {
            "status": "正常",
            "total_documents": count,
            "persist_dir": self.persist_dir
        }

    def import_from_commander_learning(self, md_path):
        """从指挥官学习笔记导入历史经验"""
        if not os.path.exists(md_path):
            print(f"[WARN] 文件不存在: {md_path}")
            return 0

        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 简单按章节分割
        sections = content.split("## ")
        count = 0
        for section in sections[1:]:  # 跳过第一个空段
            lines = section.strip().split("\n")
            if not lines:
                continue
            title = lines[0].strip()
            body = "\n".join(lines[1:]).strip()
            if len(body) > 20:  # 只导入有实质内容的
                self.add("经验", f"【{title}】\n{body}", {"source": "commander_learning.md"})
                count += 1
        return count


# 命令行使用
if __name__ == "__main__":
    import sys

    kb = KnowledgeBase()
    print("知识库状态:", kb.stats())

    if len(sys.argv) > 1 and sys.argv[1] == "import":
        # 导入指挥官学习笔记
        md_path = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"
        count = kb.import_from_commander_learning(md_path)
        print(f"导入了 {count} 条经验")

    elif len(sys.argv) > 1 and sys.argv[1] == "search":
        query = " ".join(sys.argv[2:])
        results = kb.search(query, n=5)
        print(f"\n搜索: {query}\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['metadata'].get('doc_type', '?')}] (距离: {r['distance']:.4f})")
            print(f"   {r['content'][:200]}")
            print()

    else:
        print("用法:")
        print("  python knowledge_base.py import          # 导入指挥官学习笔记")
        print("  python knowledge_base.py search <查询>   # 语义搜索")
        print("  python knowledge_base.py                 # 查看状态")
