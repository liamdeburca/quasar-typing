"""Test emcee type validation using pydantic TypeAdapter."""

import pytest
from pydantic import TypeAdapter, ValidationError

try:
    import emcee
    from emcee import EnsembleSampler, backends, moves
except ImportError:
    pytest.skip("emcee not installed", allow_module_level=True)

from quasar_typing.emcee import (
    BackendType,
    EnsembleSamplerType,
    HDFBackendType,
    MoveType,
)


class TestMoveTypeValid:
    """Tests for valid Move inputs."""

    def test_move_de_valid(self, move_de):
        """DEMove instance should pass validation."""
        adapter = TypeAdapter(MoveType)
        result = adapter.validate_python(move_de)
        assert isinstance(result, moves.Move)
        assert isinstance(result, moves.DEMove)

    def test_move_de_snooker_valid(self, move_de_snooker):
        """DESnookerMove instance should pass validation."""
        adapter = TypeAdapter(MoveType)
        result = adapter.validate_python(move_de_snooker)
        assert isinstance(result, moves.Move)
        assert isinstance(result, moves.DESnookerMove)

    def test_move_stretch_valid(self, move_stretch):
        """StretchMove instance should pass validation."""
        adapter = TypeAdapter(MoveType)
        result = adapter.validate_python(move_stretch)
        assert isinstance(result, moves.Move)
        assert isinstance(result, moves.StretchMove)

    def test_move_maintains_identity(self, move_de):
        """Validated Move should be the same object."""
        adapter = TypeAdapter(MoveType)
        result = adapter.validate_python(move_de)
        assert result is move_de


class TestMoveTypeInvalid:
    """Tests for invalid Move inputs."""

    def test_move_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(MoveType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_move_rejects_dict(self):
        """Plain dict should raise validation error."""
        adapter = TypeAdapter(MoveType)
        with pytest.raises(ValidationError):
            adapter.validate_python({})

    def test_move_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(MoveType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a move")

    def test_move_rejects_integer(self):
        """Integer should raise validation error."""
        adapter = TypeAdapter(MoveType)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)


class TestEnsembleSamplerTypeValid:
    """Tests for valid EnsembleSampler inputs."""

    def test_ensemble_sampler_basic_valid(self, ensemble_sampler_basic):
        """Basic EnsembleSampler should pass validation."""
        adapter = TypeAdapter(EnsembleSamplerType)
        result = adapter.validate_python(ensemble_sampler_basic)
        assert isinstance(result, EnsembleSampler)

    def test_ensemble_sampler_with_backend_valid(self, ensemble_sampler_with_backend):
        """EnsembleSampler with backend should pass validation."""
        adapter = TypeAdapter(EnsembleSamplerType)
        result = adapter.validate_python(ensemble_sampler_with_backend)
        assert isinstance(result, EnsembleSampler)
        assert result.backend is not None

    def test_ensemble_sampler_with_moves_valid(self, ensemble_sampler_with_moves):
        """EnsembleSampler with custom moves should pass validation."""
        adapter = TypeAdapter(EnsembleSamplerType)
        result = adapter.validate_python(ensemble_sampler_with_moves)
        assert isinstance(result, EnsembleSampler)

    def test_ensemble_sampler_maintains_identity(self, ensemble_sampler_basic):
        """Validated EnsembleSampler should be the same object."""
        adapter = TypeAdapter(EnsembleSamplerType)
        result = adapter.validate_python(ensemble_sampler_basic)
        assert result is ensemble_sampler_basic

    def test_ensemble_sampler_has_attributes(self, ensemble_sampler_basic):
        """Validated EnsembleSampler should have expected attributes."""
        adapter = TypeAdapter(EnsembleSamplerType)
        result = adapter.validate_python(ensemble_sampler_basic)
        assert hasattr(result, 'nwalkers')
        assert hasattr(result, 'ndim')
        assert result.nwalkers == 32
        assert result.ndim == 3


class TestEnsembleSamplerTypeInvalid:
    """Tests for invalid EnsembleSampler inputs."""

    def test_ensemble_sampler_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(EnsembleSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_ensemble_sampler_rejects_dict(self):
        """Plain dict should raise validation error."""
        adapter = TypeAdapter(EnsembleSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"nwalkers": 32, "ndim": 3})

    def test_ensemble_sampler_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(EnsembleSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a sampler")

    def test_ensemble_sampler_rejects_move(self, move_de):
        """Move object should raise validation error."""
        adapter = TypeAdapter(EnsembleSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python(move_de)


class TestBackendTypeValid:
    """Tests for valid Backend inputs."""

    def test_backend_memory_valid(self, backend_memory):
        """Memory Backend should pass validation."""
        adapter = TypeAdapter(BackendType)
        result = adapter.validate_python(backend_memory)
        assert isinstance(result, backends.Backend)

    def test_backend_hdf5_valid(self, backend_hdf5):
        """HDF5 Backend should pass validation."""
        adapter = TypeAdapter(BackendType)
        result = adapter.validate_python(backend_hdf5)
        assert isinstance(result, backends.Backend)

    def test_backend_maintains_identity(self, backend_memory):
        """Validated Backend should be the same object."""
        adapter = TypeAdapter(BackendType)
        result = adapter.validate_python(backend_memory)
        assert result is backend_memory

    def test_backend_has_attributes(self, backend_memory):
        """Validated Backend should have expected attributes."""
        adapter = TypeAdapter(BackendType)
        result = adapter.validate_python(backend_memory)
        assert hasattr(result, 'ndim')
        assert hasattr(result, 'nwalkers')


class TestBackendTypeInvalid:
    """Tests for invalid Backend inputs."""

    def test_backend_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(BackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_backend_rejects_dict(self):
        """Plain dict should raise validation error."""
        adapter = TypeAdapter(BackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"ndim": 3, "nwalkers": 16})

    def test_backend_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(BackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a backend")

    def test_backend_rejects_sampler(self, ensemble_sampler_basic):
        """EnsembleSampler should raise validation error."""
        adapter = TypeAdapter(BackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python(ensemble_sampler_basic)


class TestHDFBackendTypeValid:
    """Tests for valid HDFBackend inputs."""

    def test_hdf_backend_valid(self, backend_hdf5):
        """HDFBackend instance should pass validation."""
        adapter = TypeAdapter(HDFBackendType)
        result = adapter.validate_python(backend_hdf5)
        assert isinstance(result, backends.HDFBackend)

    def test_hdf_backend_maintains_identity(self, backend_hdf5):
        """Validated HDFBackend should be the same object."""
        adapter = TypeAdapter(HDFBackendType)
        result = adapter.validate_python(backend_hdf5)
        assert result is backend_hdf5


class TestHDFBackendTypeInvalid:
    """Tests for invalid HDFBackend inputs."""

    def test_hdf_backend_rejects_memory_backend(self, backend_memory):
        """Memory Backend should raise validation error."""
        adapter = TypeAdapter(HDFBackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python(backend_memory)

    def test_hdf_backend_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(HDFBackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_hdf_backend_rejects_dict(self):
        """Plain dict should raise validation error."""
        adapter = TypeAdapter(HDFBackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"name": "test"})

    def test_hdf_backend_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(HDFBackendType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not an hdf backend")


class TestIntegration:
    """Integration tests for multiple types."""

    def test_sampler_accepts_move(self, ensemble_sampler_basic, move_de):
        """Test that sampler and move types work in context."""
        adapter_sampler = TypeAdapter(EnsembleSamplerType)
        adapter_move = TypeAdapter(MoveType)
        
        validated_sampler = adapter_sampler.validate_python(ensemble_sampler_basic)
        validated_move = adapter_move.validate_python(move_de)
        
        assert isinstance(validated_sampler, EnsembleSampler)
        assert isinstance(validated_move, moves.Move)

    def test_sampler_accepts_backend(self, ensemble_sampler_with_backend, backend_memory):
        """Test that sampler and backend types work in context."""
        adapter_sampler = TypeAdapter(EnsembleSamplerType)
        adapter_backend = TypeAdapter(BackendType)
        
        validated_sampler = adapter_sampler.validate_python(ensemble_sampler_with_backend)
        validated_backend = adapter_backend.validate_python(backend_memory)
        
        assert isinstance(validated_sampler, EnsembleSampler)
        assert isinstance(validated_backend, backends.Backend)
