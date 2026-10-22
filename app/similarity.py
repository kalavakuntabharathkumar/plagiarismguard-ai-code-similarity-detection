"""AST normalization and lexical similarity utilities."""
import ast
import re
from collections import Counter
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Normalizer(ast.NodeTransformer):
    """Replace names and literals so renaming variables has less effect."""

    def visit_Name(self, node: ast.Name) -> ast.AST:
        return ast.copy_location(ast.Name(id="VAR", ctx=node.ctx), node)

    def visit_arg(self, node: ast.arg) -> ast.AST:
        node.arg = "ARG"
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        value: Any = node.value
        if isinstance(value, bool):
            node.value = "BOOL"
        elif isinstance(value, (int, float, complex)):
            node.value = 0
        elif isinstance(value, str):
            node.value = "STRING"
        elif value is None:
            node.value = None
        return node


def normalize_python(source: str) -> str:
    """Return normalized AST dump; fall back to token cleanup on parse errors."""
    try:
        tree = ast.parse(source)
        normalized = Normalizer().visit(tree)
        ast.fix_missing_locations(normalized)
        return ast.dump(normalized, include_attributes=False)
    except (SyntaxError, ValueError, TypeError):
        return re.sub(r"\b[A-Za-z_]\w*\b", "ID", source)


def token_frequencies(source: str) -> Counter[str]:
    tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[^\s]", source)
    return Counter(tokens)


def compare_sources(source_a: str, source_b: str) -> dict[str, Any]:
    """Compute a heuristic similarity score from normalized syntax and tokens."""
    normalized_a = normalize_python(source_a)
    normalized_b = normalize_python(source_b)
    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(3, 5))
    try:
        vectors = vectorizer.fit_transform([normalized_a, normalized_b])
        structural = float(cosine_similarity(vectors[0], vectors[1])[0, 0])
    except ValueError:
        structural = 0.0
    token_a, token_b = token_frequencies(source_a), token_frequencies(source_b)
    overlap = sum((token_a & token_b).values())
    total = max(1, sum((token_a | token_b).values()))
    lexical = overlap / total
    score = round((0.75 * structural + 0.25 * lexical) * 100, 2)
    return {
        "similarity_percent": score,
        "structural_similarity_percent": round(structural * 100, 2),
        "lexical_overlap_percent": round(lexical * 100, 2),
        "review_recommended": score >= 70,
        "explanation": "Heuristic similarity signal only; a qualified reviewer must inspect context.",
    }
