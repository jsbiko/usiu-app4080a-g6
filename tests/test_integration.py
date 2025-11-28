"""
USIU G6 Integration Test Suite
================================
End-to-end tests that verify complete user flows across client and server.

Tests complete workflows:
- Registration → Login → Access protected pages
- Logout → Verify access revoked
- Password reset flow
- Form submissions
"""

import unittest
import json
import time
import sys
import os

# Add parent and server directories to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
server_dir = os.path.join(parent_dir, 'server')
sys.path.insert(0, parent_dir)
sys.path.insert(0, server_dir)

from app import app, db
from models import User


class TestIntegrationFlows(unittest.TestCase):
    """Integration tests for complete user workflows"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        cls.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Clear database before each test"""
        with app.app_context():
            User.query.delete()
            db.session.commit()

    def test_01_complete_registration_and_login_flow(self):
        """Test: User registers → logs in → accesses protected resources"""
        print("\n▶️  Testing complete registration and login flow...")
        
        # Step 1: Register new user
        reg_response = self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Integration',
                'lastName': 'User',
                'email': 'integration@example.com',
                'password': 'secure123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(reg_response.status_code, 201)
        reg_data = json.loads(reg_response.data)
        self.assertIn('access_token', reg_data)
        print("  ✓ Step 1: User registered successfully")
        
        # Step 2: Login with credentials
        login_response = self.client.post('/api/login',
            data=json.dumps({
                'email': 'integration@example.com',
                'password': 'secure123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(login_response.status_code, 200)
        login_data = json.loads(login_response.data)
        token = login_data['access_token']
        print("  ✓ Step 2: User logged in successfully")
        
        # Step 3: Access protected user endpoint
        user_response = self.client.get('/api/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(user_response.status_code, 200)
        user_data = json.loads(user_response.data)
        self.assertEqual(user_data['user']['email'], 'integration@example.com')
        self.assertEqual(user_data['user']['firstName'], 'Integration')
        print("  ✓ Step 3: Protected resource accessed successfully")
        
        # Step 4: Verify token
        verify_response = self.client.get('/api/verify-token',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(verify_response.status_code, 200)
        print("  ✓ Step 4: Token verified successfully")
        
        print("✅ Complete flow passed!\n")

    def test_02_logout_and_reauth_flow(self):
        """Test: User logs in → logs out → cannot access protected → logs in again"""
        print("\n▶️  Testing logout and re-authentication flow...")
        
        # Step 1: Register and login
        self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Logout',
                'lastName': 'Test',
                'email': 'logout@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        login_response = self.client.post('/api/login',
            data=json.dumps({
                'email': 'logout@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        token = json.loads(login_response.data)['access_token']
        print("  ✓ Step 1: User logged in")
        
        # Step 2: Access protected resource (should work)
        response = self.client.get('/api/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)
        print("  ✓ Step 2: Protected resource accessible")
        
        # Step 3: Logout
        logout_response = self.client.post('/api/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(logout_response.status_code, 200)
        print("  ✓ Step 3: User logged out")
        
        # Step 4: Try to access protected resource (should fail)
        response = self.client.get('/api/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 401)
        print("  ✓ Step 4: Protected resource blocked after logout")
        
        # Step 5: Login again
        relogin_response = self.client.post('/api/login',
            data=json.dumps({
                'email': 'logout@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        new_token = json.loads(relogin_response.data)['access_token']
        
        # Step 6: Access protected resource with new token
        response = self.client.get('/api/user',
            headers={'Authorization': f'Bearer {new_token}'}
        )
        self.assertEqual(response.status_code, 200)
        print("  ✓ Step 5: Re-authentication successful")
        
        print("✅ Logout and reauth flow passed!\n")

    def test_03_password_reset_flow(self):
        """Test: User requests password reset → receives token → can reset"""
        print("\n▶️  Testing password reset flow...")
        
        # Step 1: Register user
        self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Reset',
                'lastName': 'Test',
                'email': 'resetflow@example.com',
                'password': 'oldpassword'
            }),
            content_type='application/json'
        )
        print("  ✓ Step 1: User registered")
        
        # Step 2: Request password reset
        reset_request = self.client.post('/api/forgot-password',
            data=json.dumps({
                'email': 'resetflow@example.com'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(reset_request.status_code, 200)
        print("  ✓ Step 2: Password reset requested")
        
        # Step 3: Get reset token from database
        with app.app_context():
            user = User.query.filter_by(email='resetflow@example.com').first()
            reset_token = user.reset_token
            self.assertIsNotNone(reset_token)
        print("  ✓ Step 3: Reset token generated")
        
        # Step 4: Reset password
        reset_response = self.client.post('/api/reset-password',
            data=json.dumps({
                'token': reset_token,
                'newPassword': 'newpassword123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(reset_response.status_code, 200)
        print("  ✓ Step 4: Password reset successfully")
        
        # Step 5: Try to login with old password (should fail)
        old_login = self.client.post('/api/login',
            data=json.dumps({
                'email': 'resetflow@example.com',
                'password': 'oldpassword'
            }),
            content_type='application/json'
        )
        self.assertEqual(old_login.status_code, 401)
        print("  ✓ Step 5: Old password rejected")
        
        # Step 6: Login with new password (should work)
        new_login = self.client.post('/api/login',
            data=json.dumps({
                'email': 'resetflow@example.com',
                'password': 'newpassword123'
            }),
            content_type='application/json'
        )
        self.assertEqual(new_login.status_code, 200)
        print("  ✓ Step 6: New password works")
        
        print("✅ Password reset flow passed!\n")

    def test_04_invalid_credentials_flow(self):
        """Test: User tries various invalid login attempts"""
        print("\n▶️  Testing invalid credentials handling...")
        
        # Register user
        self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Valid',
                'lastName': 'User',
                'email': 'valid@example.com',
                'password': 'correctpassword'
            }),
            content_type='application/json'
        )
        
        # Test 1: Wrong password
        response1 = self.client.post('/api/login',
            data=json.dumps({
                'email': 'valid@example.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 401)
        print("  ✓ Wrong password rejected")
        
        # Test 2: Non-existent email
        response2 = self.client.post('/api/login',
            data=json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'anypassword'
            }),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 401)
        print("  ✓ Non-existent email rejected")
        
        # Test 3: Empty password
        response3 = self.client.post('/api/login',
            data=json.dumps({
                'email': 'valid@example.com',
                'password': ''
            }),
            content_type='application/json'
        )
        self.assertIn(response3.status_code, [400, 401])
        print("  ✓ Empty password rejected")
        
        # Test 4: Valid credentials still work
        response4 = self.client.post('/api/login',
            data=json.dumps({
                'email': 'valid@example.com',
                'password': 'correctpassword'
            }),
            content_type='application/json'
        )
        self.assertEqual(response4.status_code, 200)
        print("  ✓ Valid credentials still work")
        
        print("✅ Invalid credentials handling passed!\n")


def run_integration_tests():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("USIU G6 INTEGRATION TEST SUITE")
    print("="*60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegrationFlows)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("INTEGRATION TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1)
