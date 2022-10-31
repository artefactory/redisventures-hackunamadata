import re
from redis.asyncio import Redis
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import VectorField
from typing import Optional, Pattern

from config.redis_config import INDEX_NAME


class TokenEscaper:
    """
    Escape punctuation within an input string. Taken from RedisOM Python.
    """
    # Characters that RediSearch requires us to escape during queries.
    # Source: https://redis.io/docs/stack/search/reference/escaping/#the-rules-of-text-field-tokenization
    DEFAULT_ESCAPED_CHARS = r"[,.<>{}\[\]\\\"\':;!@#$%^&*()\-+=~\/ ]"

    def __init__(self, escape_chars_re: Optional[Pattern] = None):
        if escape_chars_re:
            self.escaped_chars_re = escape_chars_re
        else:
            self.escaped_chars_re = re.compile(self.DEFAULT_ESCAPED_CHARS)

    def escape(self, value: str) -> str:
        def escape_symbol(match):
            value = match.group(0)
            return f"\\{value}"

        return self.escaped_chars_re.sub(escape_symbol, value)


class SearchIndex:
    """
    SearchIndex is used to wrap and capture all information
    and actions applied to a RediSearch index including creation,
    management, and query construction.
    """
    escaper = TokenEscaper()

    async def create_flat(
        self,
        *fields,
        redis_conn: Redis,
        number_of_vectors: int,
        prefix: str,
        distance_metric: str = 'L2'
    ):
        """
        Create a FLAT aka brute force style index.
        Args:
            redis_conn (Redis): Redis connection object.
            number_of_vectors (int): Count of the number of initial vectors.
            prefix (str): key prefix to use for RediSearch index creation.
            distance_metric (str, optional): Distance metric to use for Vector Search. Defaults to 'L2'.
        """
        vector_field = VectorField(
            "vector",
            "FLAT", {
                "TYPE": "FLOAT32",
                "DIM": 768,
                "DISTANCE_METRIC": distance_metric,
                "INITIAL_CAP": number_of_vectors,
                "BLOCK_SIZE": number_of_vectors
            }
        )
        await self._create(
            *fields,
            vector_field,
            redis_conn=redis_conn,
            prefix=prefix
        )

    async def create_hnsw(
        self,
        *fields,
        redis_conn: Redis,
        number_of_vectors: int,
        prefix: str,
        distance_metric: str = 'COSINE'
    ):
        """
        Create an approximate NN index via HNSW.
        Args:
            redis_conn (Redis): Redis connection object.
            number_of_vectors (int): Count of the number of initial vectors.
            prefix (str): key prefix to use for RediSearch index creation.
            distance_metric (str, optional): Distance metric to use for Vector Search. Defaults to 'COSINE'.
        """
        vector_field = VectorField(
            "vector",
            "HNSW", {
                "TYPE": "FLOAT32",
                "DIM": 768,
                "DISTANCE_METRIC": distance_metric,
                "INITIAL_CAP": number_of_vectors,
            }
        )
        await self._create(
            *fields,
            vector_field,
            redis_conn=redis_conn,
            prefix=prefix
        )

    async def _create(
        self,
        *fields,
        redis_conn: Redis,
        prefix: str
    ):
        await redis_conn.ft(INDEX_NAME).create_index(
            fields=fields,
            definition=IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def process_tags(self, categories: list, years: list) -> str:
        """
        Helper function to process tags data.
        Args:
            categories (list): List of categories.
            years (list): List of years.
        Returns:
            str: RediSearch tag query string.
        """
        tag = "("
        if years:
            years = "|".join([self.escaper.escape(year) for year in years])
            tag += f"(@year:{{{years}}})"
        if categories:
            categories = "|".join([self.escaper.escape(cat) for cat in categories])
            if tag:
                tag += f" (@categories:{{{categories}}})"
            else:
                tag += f"(@categories:{{{categories}}})"
        tag += ")"
        # if no tags are selected
        if len(tag) < 3:
            tag = "*"
        return tag

    def vector_query(
        self,
        categories: list,
        years: list,
        search_type: str = "KNN",
        number_of_results: int = 5
    ) -> Query:
        """
        Create a RediSearch query to perform hybrid vector and tag based searches.
        Args:
            categories (list): List of categories.
            years (list): List of years.
            search_type (str, optional): Style of search. Defaults to "KNN".
            number_of_results (int, optional): How many results to fetch. Defaults to 20.
        Returns:
            Query: RediSearch Query
        """
        tag_query = self.process_tags(categories, years)
        base_query = f'{tag_query}=>[{search_type} {number_of_results} @vector $vec_param AS vector_score]'
        return Query(base_query)\
            .sort_by("vector_score")\
            .paging(0, number_of_results)\
            .return_fields("paper_id", "vector_score")\
            .dialect(2)

    def count_query(
        self,
        years: list,
        categories: list
    ) -> Query:
        """
        Create a RediSearch query to count available documents.
        Args:
            categories (list): List of categories.
            years (list): List of years.
        Returns:
            Query: RediSearch Query
        """
        tag_query = self.process_tags(categories, years)
        return Query(f'{tag_query}')\
            .no_content()\
            .dialect(2)
