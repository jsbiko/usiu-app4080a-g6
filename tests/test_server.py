"""
USIU G6 Server Test Suite
==========================
Comprehensive tests for Flask backend API endpoints, authentication, and database operations.

Tests cover:
- User registration
- User login
- Token verification
- Protected routes
- Password reset
- Logout
- Database integrity
"""

import unittest
import json
import sys
import os

# Add parent and server directories to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
server_dir = os.path.join(parent_dir, 'server')
sys.path.insert(0, parent_dir)
sys.path.insert(0, server_dir)

from app import app, db
from models import User


class TestServerAPI(unittest.TestCase):
    """Test suite for server API endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up test client and database once for all tests"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        cls.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Set up before each test"""
        with app.app_context():
            # Clear all users before each test
            User.query.delete()
            db.session.commit()

    def test_01_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Test',
                'lastName': 'User',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], 'test@example.com')
        print("✅ Test 1: User registration successful")

    def test_02_user_registration_duplicate_email(self):
        """Test registration with duplicate email fails"""
        # Register first user
        self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Test',
                'lastName': 'User',
                'email': 'duplicate@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Try to register with same email
        response = self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Another',
                'lastName': 'User',
                'email': 'duplicate@example.com',
                'password': 'password456'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        print("✅ Test 2: Duplicate email properly rejected")

    def test_03_user_login_success(self):
        """Test successful user login"""
        # Register a user first
        self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Login',
                'lastName': 'Test',
                'email': 'login@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Now login
        response = self.client.post('/api/login',
            data=json.dumps({
                'email': 'login@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        print("✅ Test 3: User login successful")

    def test_04_user_login_wrong_password(self):
        """Test login with wrong password fails"""
        # Register a user
        self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Wrong',
                'lastName': 'Password',
                'email': 'wrongpass@example.com',
                'password': 'correctpassword'
            }),
            content_type='application/json'
        )
        
        # Try to login with wrong password
        response = self.client.post('/api/login',
            data=json.dumps({
                'email': 'wrongpass@example.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
        print("✅ Test 4: Wrong password properly rejected")

    def test_05_user_login_nonexistent_email(self):
        """Test login with non-existent email fails"""
        response = self.client.post('/api/login',
            data=json.dumps({
                'email': 'doesnotexist@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
        print("✅ Test 5: Non-existent email properly rejected")

    def test_06_token_verification(self):
        """Test JWT token verification"""
        # Register and get token
        reg_response = self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Token',
                'lastName': 'Test',
                'email': 'token@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        token = json.loads(reg_response.data)['access_token']
        
        # Verify token
        response = self.client.get('/api/verify-token',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            print(f"   ⚠️  Status code: {response.status_code}")
            print(f"   ⚠️  Response: {response.data.decode()}")
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['valid'])
        print("✅ Test 6: Token verification successful")

    def test_07_protected_route_without_token(self):
        """Test that protected routes require authentication"""
        response = self.client.get('/api/user')
        
        # Should return 401 or redirect to login
        self.assertIn(response.status_code, [401, 422])
        print("✅ Test 7: Protected route blocks unauthenticated access")

    def test_08_protected_route_with_token(self):
        """Test accessing protected route with valid token"""
        # Register and get token
        reg_response = self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Protected',
                'lastName': 'Test',
                'email': 'protected@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        token = json.loads(reg_response.data)['access_token']
        
        # Access protected route
        response = self.client.get('/api/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['user']['email'], 'protected@example.com')
        print("✅ Test 8: Protected route accessible with valid token")

    def test_09_logout_invalidates_token(self):
        """Test that logout properly invalidates token"""
        # Register and get token
        reg_response = self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Logout',
                'lastName': 'Test',
                'email': 'logout@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        token = json.loads(reg_response.data)['access_token']
        
        # Logout
        logout_response = self.client.post('/api/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(logout_response.status_code, 200)
        
        # Try to use token after logout
        response = self.client.get('/api/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Token should be invalid after logout
        self.assertEqual(response.status_code, 401)
        print("✅ Test 9: Logout properly invalidates token")

    def test_10_password_reset_request(self):
        """Test password reset request"""
        # Register a user
        self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Reset',
                'lastName': 'Test',
                'email': 'reset@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Request password reset
        response = self.client.post('/api/forgot-password',
            data=json.dumps({
                'email': 'reset@example.com'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        print("✅ Test 10: Password reset request successful")

    def test_11_database_user_creation(self):
        """Test that users are properly saved to database"""
        with app.app_context():
            # Create user directly in database
            user = User(
                first_name='Database',
                last_name='Test',
                email='database@example.com'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Query user from database
            found_user = User.query.filter_by(email='database@example.com').first()
            
            self.assertIsNotNone(found_user)
            self.assertEqual(found_user.first_name, 'Database')
            self.assertTrue(found_user.check_password('password123'))
            print("✅ Test 11: Database user operations work correctly")

    def test_12_missing_fields_in_registration(self):
        """Test that registration fails with missing required fields"""
        response = self.client.post('/api/register',
            data=json.dumps({
                'firstName': 'Missing',
                # Missing lastName, email, password
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        print("✅ Test 12: Missing fields properly rejected")


def run_tests():
    """Run all tests and display results"""
    print("\n" + "="*60)
    print("USIU G6 SERVER TEST SUITE")
    print("="*60 + "\n")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServerAPI)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
