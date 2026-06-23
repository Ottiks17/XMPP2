"""Tests for REST API endpoints."""
import pytest
import json
from unittest.mock import MagicMock, patch
from flask import Flask

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rest_server import RESTServer, RateLimiter


class TestRateLimiter:
    """Rate limiter tests."""
    
    def test_rate_limiter_allows_requests_under_limit(self):
        """Test that rate limiter allows requests under the limit."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        ip = "127.0.0.1"
        
        for i in range(5):
            assert limiter.is_allowed(ip) is True
        
        # 6th request should be denied
        assert limiter.is_allowed(ip) is False
    
    def test_rate_limiter_resets_after_window(self):
        """Test that rate limiter resets after window expires."""
        limiter = RateLimiter(max_requests=2, window_seconds=1)
        ip = "127.0.0.1"
        
        assert limiter.is_allowed(ip) is True
        assert limiter.is_allowed(ip) is True
        assert limiter.is_allowed(ip) is False
        
        import time
        time.sleep(1.1)
        
        # After window, should allow again
        assert limiter.is_allowed(ip) is True
    
    def test_rate_limiter_different_ips(self):
        """Test that rate limiter tracks different IPs separately."""
        limiter = RateLimiter(max_requests=2, window_seconds=60)
        
        ip1 = "127.0.0.1"
        ip2 = "192.168.1.1"
        
        assert limiter.is_allowed(ip1) is True
        assert limiter.is_allowed(ip1) is True
        assert limiter.is_allowed(ip1) is False
        
        # ip2 should still have allowance
        assert limiter.is_allowed(ip2) is True


class TestRESTServer:
    """REST Server tests."""
    
    @pytest.fixture
    def rest_server(self):
        """Create a test REST server."""
        config = {
            'rest_api': {
                'host': '127.0.0.1',
                'port': 8080,
                'endpoint': '/send_message',
                'api_key': 'test-key',
                'allow_get': False,
            },
            'kafka': {
                'enabled': False,
            },
        }
        
        def mock_log_callback(msg, level):
            print(f"[{level}] {msg}")
        
        server = RESTServer(config, message_handler=None, log_callback=mock_log_callback)
        return server
    
    @pytest.fixture
    def client(self, rest_server):
        """Create a Flask test client."""
        return rest_server.app.test_client()
    
    def test_health_check(self, client):
        """Test /health endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json == {"status": "running"}
    
    def test_send_message_without_api_key(self, client):
        """Test /send_message without API key (should fail)."""
        data = {"to": "user@domain", "message": "test"}
        response = client.post('/send_message', json=data)
        assert response.status_code == 401
        assert "Unauthorized" in response.json["error"]
    
    def test_send_message_with_invalid_api_key(self, client):
        """Test /send_message with invalid API key."""
        data = {"to": "user@domain", "message": "test"}
        headers = {"X-API-Key": "invalid-key"}
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code == 401
    
    def test_send_message_missing_fields(self, client):
        """Test /send_message with missing fields."""
        data = {"to": "user@domain"}
        headers = {"X-API-Key": "test-key"}
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code == 400
        assert "Missing" in response.json["error"]
    
    def test_send_message_empty_message(self, client):
        """Test /send_message with empty message."""
        data = {"to": "user@domain", "message": ""}
        headers = {"X-API-Key": "test-key"}
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code == 400
    
    def test_send_message_too_long_message(self, client):
        """Test /send_message with message exceeding 256 chars."""
        data = {"to": "user@domain", "message": "x" * 300}
        headers = {"X-API-Key": "test-key"}
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code == 400
        assert "exceeds" in response.json["error"].lower()
    
    def test_send_message_no_handler(self, client):
        """Test /send_message with no message handler."""
        data = {"to": "user@domain", "message": "test"}
        headers = {"X-API-Key": "test-key"}
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code == 500
        assert "not configured" in response.json["error"].lower()
    
    def test_send_message_with_handler(self, rest_server, client):
        """Test /send_message with a working handler."""
        def mock_handler(to_user, message):
            return True
        
        rest_server.message_handler = mock_handler
        
        data = {"to": "user@domain", "message": "test"}
        headers = {"X-API-Key": "test-key"}
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code == 200
        assert response.json["status"] == "success"
    
    def test_rate_limiting(self, client):
        """Test that rate limiting works."""
        def mock_handler(to_user, message):
            return True
        
        # Mock the rate limiter to have a low limit
        client.application.rate_limiter.max_requests = 1
        
        data = {"to": "user@domain", "message": "test"}
        headers = {"X-API-Key": "test-key"}
        
        # First request should succeed
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code in [200, 500]  # Could be 500 due to no handler
        
        # Second request should be rate limited
        response = client.post('/send_message', json=data, headers=headers)
        assert response.status_code == 429
        assert "Too many requests" in response.json["error"]
    
    def test_security_headers(self, client):
        """Test that security headers are present."""
        response = client.get('/health')
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
