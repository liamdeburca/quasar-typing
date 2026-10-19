import cachetools
import pytest
from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError

from quasar_typing.cachetools import CacheType, LRUCacheType


class TestCacheType:
    """Tests for CacheType - cachetools.Cache validation"""

    def test_cache_type_accepts_cache_instance(self):
        """CacheType accepts cachetools.Cache instance."""
        cache = cachetools.Cache(maxsize=10)
        adapter = TypeAdapter(CacheType)
        result = adapter.validate_python(cache)
        assert isinstance(result, cachetools.Cache)
        assert result is cache

    def test_cache_type_accepts_lru_cache(self):
        """CacheType accepts cachetools.LRUCache (subclass of Cache)."""
        lru = cachetools.LRUCache(maxsize=10)
        adapter = TypeAdapter(CacheType)
        result = adapter.validate_python(lru)
        assert isinstance(result, cachetools.Cache)
        assert result is lru

    def test_cache_type_accepts_ttl_cache(self):
        """CacheType accepts cachetools.TTLCache (subclass of Cache)."""
        ttl = cachetools.TTLCache(maxsize=10, ttl=60)
        adapter = TypeAdapter(CacheType)
        result = adapter.validate_python(ttl)
        assert isinstance(result, cachetools.Cache)
        assert result is ttl

    def test_cache_type_accepts_fifo_cache(self):
        """CacheType accepts cachetools.FIFOCache (subclass of Cache)."""
        fifo = cachetools.FIFOCache(maxsize=10)
        adapter = TypeAdapter(CacheType)
        result = adapter.validate_python(fifo)
        assert isinstance(result, cachetools.Cache)
        assert result is fifo

    def test_cache_type_accepts_rr_cache(self):
        """CacheType accepts cachetools.RRCache (subclass of Cache)."""
        rr = cachetools.RRCache(maxsize=10)
        adapter = TypeAdapter(CacheType)
        result = adapter.validate_python(rr)
        assert isinstance(result, cachetools.Cache)
        assert result is rr

    def test_cache_type_rejects_none(self):
        """CacheType rejects None."""
        adapter = TypeAdapter(CacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_cache_type_rejects_string(self):
        """CacheType rejects string."""
        adapter = TypeAdapter(CacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a cache")

    def test_cache_type_rejects_int(self):
        """CacheType rejects integer."""
        adapter = TypeAdapter(CacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)

    def test_cache_type_rejects_dict(self):
        """CacheType rejects dict."""
        adapter = TypeAdapter(CacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"key": "value"})

    def test_cache_type_rejects_list(self):
        """CacheType rejects list."""
        adapter = TypeAdapter(CacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python([1, 2, 3])

    def test_cache_type_in_pydantic_model(self):
        """CacheType can be used in Pydantic model."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cache: CacheType

        cache = cachetools.Cache(maxsize=10)
        config = Config(cache=cache)
        assert config.cache is cache

    def test_cache_type_multiple_instances(self):
        """Multiple CacheType instances are independently valid."""
        adapter = TypeAdapter(CacheType)
        cache1 = cachetools.Cache(maxsize=5)
        cache2 = cachetools.LRUCache(maxsize=10)
        
        result1 = adapter.validate_python(cache1)
        result2 = adapter.validate_python(cache2)
        
        assert result1 is cache1
        assert result2 is cache2
        assert result1 is not result2

    def test_cache_type_passthrough(self):
        """Validated cache is the same instance (passthrough)."""
        adapter = TypeAdapter(CacheType)
        cache = cachetools.Cache(maxsize=10)
        result = adapter.validate_python(cache)
        assert result is cache

    def test_cache_type_with_data(self):
        """CacheType accepts cache with data."""
        cache = cachetools.Cache(maxsize=10)
        cache["key1"] = "value1"
        cache["key2"] = "value2"
        
        adapter = TypeAdapter(CacheType)
        result = adapter.validate_python(cache)
        assert result["key1"] == "value1"
        assert result["key2"] == "value2"

    def test_cache_type_different_maxsizes(self):
        """CacheType accepts caches with different maxsizes."""
        adapter = TypeAdapter(CacheType)
        
        cache1 = cachetools.Cache(maxsize=1)
        cache10 = cachetools.Cache(maxsize=10)
        cache100 = cachetools.Cache(maxsize=100)
        
        assert adapter.validate_python(cache1) is cache1
        assert adapter.validate_python(cache10) is cache10
        assert adapter.validate_python(cache100) is cache100


class TestLRUCacheType:
    """Tests for LRUCacheType - cachetools.LRUCache validation"""

    def test_lru_cache_accepts_lru_cache_instance(self):
        """LRUCacheType accepts cachetools.LRUCache instance."""
        lru = cachetools.LRUCache(maxsize=10)
        adapter = TypeAdapter(LRUCacheType)
        result = adapter.validate_python(lru)
        assert isinstance(result, cachetools.LRUCache)
        assert result is lru

    def test_lru_cache_rejects_base_cache(self):
        """LRUCacheType rejects base cachetools.Cache (not LRU)."""
        cache = cachetools.Cache(maxsize=10)
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(cache)

    def test_lru_cache_rejects_ttl_cache(self):
        """LRUCacheType rejects cachetools.TTLCache."""
        ttl = cachetools.TTLCache(maxsize=10, ttl=60)
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(ttl)

    def test_lru_cache_rejects_fifo_cache(self):
        """LRUCacheType rejects cachetools.FIFOCache."""
        fifo = cachetools.FIFOCache(maxsize=10)
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(fifo)

    def test_lru_cache_rejects_rr_cache(self):
        """LRUCacheType rejects cachetools.RRCache."""
        rr = cachetools.RRCache(maxsize=10)
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(rr)

    def test_lru_cache_rejects_none(self):
        """LRUCacheType rejects None."""
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_lru_cache_rejects_string(self):
        """LRUCacheType rejects string."""
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a cache")

    def test_lru_cache_rejects_int(self):
        """LRUCacheType rejects integer."""
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)

    def test_lru_cache_rejects_dict(self):
        """LRUCacheType rejects dict."""
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"key": "value"})

    def test_lru_cache_rejects_list(self):
        """LRUCacheType rejects list."""
        adapter = TypeAdapter(LRUCacheType)
        with pytest.raises(ValidationError):
            adapter.validate_python([1, 2, 3])

    def test_lru_cache_in_pydantic_model(self):
        """LRUCacheType can be used in Pydantic model."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cache: LRUCacheType

        lru = cachetools.LRUCache(maxsize=10)
        config = Config(cache=lru)
        assert config.cache is lru

    def test_lru_cache_multiple_instances(self):
        """Multiple LRUCacheType instances are independently valid."""
        adapter = TypeAdapter(LRUCacheType)
        lru1 = cachetools.LRUCache(maxsize=5)
        lru2 = cachetools.LRUCache(maxsize=10)
        
        result1 = adapter.validate_python(lru1)
        result2 = adapter.validate_python(lru2)
        
        assert result1 is lru1
        assert result2 is lru2
        assert result1 is not result2

    def test_lru_cache_passthrough(self):
        """Validated LRU cache is the same instance (passthrough)."""
        adapter = TypeAdapter(LRUCacheType)
        lru = cachetools.LRUCache(maxsize=10)
        result = adapter.validate_python(lru)
        assert result is lru

    def test_lru_cache_with_data(self):
        """LRUCacheType accepts cache with data."""
        lru = cachetools.LRUCache(maxsize=10)
        lru["key1"] = "value1"
        lru["key2"] = "value2"
        
        adapter = TypeAdapter(LRUCacheType)
        result = adapter.validate_python(lru)
        assert result["key1"] == "value1"
        assert result["key2"] == "value2"

    def test_lru_cache_different_maxsizes(self):
        """LRUCacheType accepts caches with different maxsizes."""
        adapter = TypeAdapter(LRUCacheType)
        
        lru1 = cachetools.LRUCache(maxsize=1)
        lru10 = cachetools.LRUCache(maxsize=10)
        lru100 = cachetools.LRUCache(maxsize=100)
        
        assert adapter.validate_python(lru1) is lru1
        assert adapter.validate_python(lru10) is lru10
        assert adapter.validate_python(lru100) is lru100

    def test_lru_cache_eviction(self):
        """LRUCacheType correctly evicts least recently used items."""
        lru = cachetools.LRUCache(maxsize=3)
        lru["a"] = 1
        lru["b"] = 2
        lru["c"] = 3
        lru["d"] = 4  # Should evict "a"
        
        adapter = TypeAdapter(LRUCacheType)
        result = adapter.validate_python(lru)
        
        assert "a" not in result
        assert "b" in result
        assert "c" in result
        assert "d" in result


class TestCacheTypeInModels:
    """Tests for CacheType and LRUCacheType in Pydantic models"""

    def test_model_with_cache_and_lru_cache(self):
        """Model with both CacheType and LRUCacheType fields."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cache: CacheType
            lru: LRUCacheType

        cache = cachetools.Cache(maxsize=10)
        lru = cachetools.LRUCache(maxsize=20)
        
        config = Config(cache=cache, lru=lru)
        assert config.cache is cache
        assert config.lru is lru

    def test_model_with_multiple_caches(self):
        """Model with multiple cache fields."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cache1: CacheType
            cache2: CacheType
            lru1: LRUCacheType
            lru2: LRUCacheType

        cache1 = cachetools.Cache(maxsize=5)
        cache2 = cachetools.Cache(maxsize=10)
        lru1 = cachetools.LRUCache(maxsize=15)
        lru2 = cachetools.LRUCache(maxsize=20)
        
        config = Config(cache1=cache1, cache2=cache2, lru1=lru1, lru2=lru2)
        assert config.cache1 is cache1
        assert config.cache2 is cache2
        assert config.lru1 is lru1
        assert config.lru2 is lru2

    def test_model_with_optional_cache(self):
        """Model with optional cache field."""
        from typing import Optional
        
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cache: Optional[CacheType] = None

        # With cache
        cache = cachetools.Cache(maxsize=10)
        config_with_cache = Config(cache=cache)
        assert config_with_cache.cache is cache

        # Without cache
        config_without_cache = Config()
        assert config_without_cache.cache is None

    def test_model_cache_field_validation_error(self):
        """Model cache field validation error."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cache: CacheType

        with pytest.raises(ValidationError):
            Config(cache="not a cache")

    def test_model_lru_field_validation_error(self):
        """Model LRU field validation error (base Cache rejected)."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            lru: LRUCacheType

        cache = cachetools.Cache(maxsize=10)
        with pytest.raises(ValidationError):
            Config(lru=cache)
