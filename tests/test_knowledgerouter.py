import pytest
import torch
from knowledgerouter import KnowledgeRouter, create_knowledgerouter

class TestKnowledgeRouter:
    def test_init(self):
        m = KnowledgeRouter(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = KnowledgeRouter(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_knowledgerouter()
        assert isinstance(m, KnowledgeRouter)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
