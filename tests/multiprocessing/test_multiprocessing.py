import pytest
import multiprocessing
from multiprocessing import Pool
from pydantic import BaseModel, ValidationError, ConfigDict, TypeAdapter

from quasar_typing.multiprocessing import PoolType


# Module-level function for pickling (required for multiprocessing)
def _square(x):
    """Simple square function for pool testing."""
    return x * x


class TestPoolType:
    """Tests for PoolType - multiprocessing.pool.Pool validation"""

    def test_pool_type_accepts_pool_instance(self):
        """PoolType accepts multiprocessing.Pool instance."""
        with Pool(processes=2) as pool:
            adapter = TypeAdapter(PoolType)
            result = adapter.validate_python(pool)
            assert isinstance(result, multiprocessing.pool.Pool)
            assert result is pool

    def test_pool_type_accepts_pool_with_single_process(self):
        """PoolType accepts Pool with single process."""
        with Pool(processes=1) as pool:
            adapter = TypeAdapter(PoolType)
            result = adapter.validate_python(pool)
            assert isinstance(result, multiprocessing.pool.Pool)
            assert result is pool

    def test_pool_type_accepts_pool_with_multiple_processes(self):
        """PoolType accepts Pool with multiple processes."""
        with Pool(processes=4) as pool:
            adapter = TypeAdapter(PoolType)
            result = adapter.validate_python(pool)
            assert isinstance(result, multiprocessing.pool.Pool)
            assert result is pool

    def test_pool_type_rejects_none(self):
        """PoolType rejects None."""
        adapter = TypeAdapter(PoolType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_pool_type_rejects_string(self):
        """PoolType rejects string."""
        adapter = TypeAdapter(PoolType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a pool")

    def test_pool_type_rejects_int(self):
        """PoolType rejects integer."""
        adapter = TypeAdapter(PoolType)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)

    def test_pool_type_rejects_dict(self):
        """PoolType rejects dict."""
        adapter = TypeAdapter(PoolType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"key": "value"})

    def test_pool_type_rejects_list(self):
        """PoolType rejects list."""
        adapter = TypeAdapter(PoolType)
        with pytest.raises(ValidationError):
            adapter.validate_python([1, 2, 3])

    def test_pool_type_rejects_queue(self):
        """PoolType rejects multiprocessing.Queue."""
        queue = multiprocessing.Queue()
        adapter = TypeAdapter(PoolType)
        try:
            with pytest.raises(ValidationError):
                adapter.validate_python(queue)
        finally:
            queue.close()
            queue.join_thread()

    def test_pool_type_rejects_process(self):
        """PoolType rejects multiprocessing.Process."""
        process = multiprocessing.Process(target=lambda: None)
        adapter = TypeAdapter(PoolType)
        with pytest.raises(ValidationError):
            adapter.validate_python(process)

    def test_pool_type_rejects_manager(self):
        """PoolType rejects multiprocessing.Manager."""
        manager = multiprocessing.Manager()
        adapter = TypeAdapter(PoolType)
        try:
            with pytest.raises(ValidationError):
                adapter.validate_python(manager)
        finally:
            manager.shutdown()

    def test_pool_type_in_pydantic_model(self):
        """PoolType can be used in Pydantic model."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            pool: PoolType

        with Pool(processes=2) as pool:
            config = Config(pool=pool)
            assert config.pool is pool
            assert isinstance(config.pool, multiprocessing.pool.Pool)

    def test_pool_type_multiple_instances(self):
        """Multiple PoolType instances are independently valid."""
        adapter = TypeAdapter(PoolType)
        with Pool(processes=2) as pool1:
            with Pool(processes=4) as pool2:
                result1 = adapter.validate_python(pool1)
                result2 = adapter.validate_python(pool2)
                assert result1 is pool1
                assert result2 is pool2
                assert result1 is not result2

    def test_pool_type_passthrough(self):
        """Validated pool is the same instance (passthrough)."""
        with Pool(processes=2) as pool:
            adapter = TypeAdapter(PoolType)
            result = adapter.validate_python(pool)
            assert result is pool

    def test_pool_type_different_maxsizes(self):
        """PoolType accepts pools with different process counts."""
        adapter = TypeAdapter(PoolType)
        with Pool(processes=1) as pool1:
            with Pool(processes=2) as pool2:
                with Pool(processes=8) as pool8:
                    assert adapter.validate_python(pool1) is pool1
                    assert adapter.validate_python(pool2) is pool2
                    assert adapter.validate_python(pool8) is pool8

    def test_pool_type_with_work(self):
        """PoolType accepts pool that has been used for work."""
        with Pool(processes=2) as pool:
            # Use the pool for some work
            results = pool.map(_square, [1, 2, 3])
            assert results == [1, 4, 9]
            
            # Now validate it
            adapter = TypeAdapter(PoolType)
            result = adapter.validate_python(pool)
            assert result is pool


class TestPoolTypeInModels:
    """Tests for PoolType in Pydantic models"""

    def test_model_with_pool_field(self):
        """Model with PoolType field."""
        class WorkerConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            pool: PoolType

        with Pool(processes=4) as pool:
            config = WorkerConfig(pool=pool)
            assert config.pool is pool

    def test_model_with_multiple_pools(self):
        """Model with multiple pool fields."""
        class MultiPoolConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            computation_pool: PoolType
            io_pool: PoolType

        with Pool(processes=4) as pool1:
            with Pool(processes=2) as pool2:
                config = MultiPoolConfig(
                    computation_pool=pool1,
                    io_pool=pool2
                )
                assert config.computation_pool is pool1
                assert config.io_pool is pool2
                assert config.computation_pool is not config.io_pool

    def test_model_with_optional_pool(self):
        """Model with optional pool field."""
        from typing import Optional

        class OptionalPoolConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            pool: Optional[PoolType] = None

        # With pool
        with Pool(processes=2) as pool:
            config_with_pool = OptionalPoolConfig(pool=pool)
            assert config_with_pool.pool is pool

        # Without pool
        config_without_pool = OptionalPoolConfig()
        assert config_without_pool.pool is None

    def test_model_pool_field_validation_error(self):
        """Model pool field validation error."""
        class WorkerConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            pool: PoolType

        with pytest.raises(ValidationError):
            WorkerConfig(pool="not a pool")

    def test_model_pool_field_validation_error_with_queue(self):
        """Model pool field rejects Queue."""
        class WorkerConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            pool: PoolType

        queue = multiprocessing.Queue()
        try:
            with pytest.raises(ValidationError):
                WorkerConfig(pool=queue)
        finally:
            queue.close()
            queue.join_thread()

    def test_nested_model_with_pool(self):
        """Nested model with pool field."""
        class PoolConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            pool: PoolType

        class ApplicationConfig(BaseModel):
            name: str
            worker: PoolConfig

        with Pool(processes=4) as pool:
            config = ApplicationConfig(
                name="my_app",
                worker=PoolConfig(pool=pool)
            )
            assert config.worker.pool is pool
            assert config.name == "my_app"


class TestPoolTypeBasics:
    """Basic validation tests for PoolType"""

    def test_pool_type_instance_check(self):
        """Verify Pool is instance of multiprocessing.pool.Pool."""
        with Pool(processes=2) as pool:
            assert isinstance(pool, multiprocessing.pool.Pool)

    def test_pool_type_different_from_other_multiprocessing_objects(self):
        """Pool is distinctly different from other multiprocessing objects."""
        with Pool(processes=2) as pool:
            queue = multiprocessing.Queue()
            try:
                assert isinstance(pool, multiprocessing.pool.Pool)
                assert not isinstance(queue, multiprocessing.pool.Pool)
            finally:
                queue.close()
                queue.join_thread()

    def test_pool_type_state_after_validation(self):
        """Pool state is unchanged after validation."""
        with Pool(processes=2) as pool:
            # Add some data to track
            pool_id_before = id(pool)
            
            adapter = TypeAdapter(PoolType)
            result = adapter.validate_python(pool)
            
            pool_id_after = id(pool)
            
            # Same object
            assert pool_id_before == pool_id_after
            assert result is pool
