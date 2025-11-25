# Test Suite

## Test Files

- `test_server.py` - Backend API tests 
- `test_integration.py` - End-to-end workflow tests 
- `run_all_tests.py` - Test runner for all tests

## How to run the tests

#### Install Dependencies (Required)

```bash
cd server
pip install -r requirements.txt
```

### Option 1: Run individual tests 

```bash
cd tests

# Run server tests 
python test_server.py

# Run integration tests 
python test_integration.py

# Or run both together with the runner
python run_all_tests.py --server --integration
```

## Test Coverage

### Server Tests

- ✅ User registration
- ✅ User login
- ✅ Token verification
- ✅ Protected route access
- ✅ User logout
- ✅ Password reset flow
- ✅ Database operations
- ✅ Error handling (duplicate email, wrong password, missing fields)

### Integration Tests

- ✅ Complete user registration → login → protected access flow
- ✅ Logout → blocked access → re-authentication flow
- ✅ Full password reset workflow
- ✅ Invalid credentials handling

### Client Tests

- ✅ Homepage loads
- ✅ Navigation menu exists
- ✅ Login page accessible
- ✅ Signup page accessible
- ✅ Contact page accessible
- ✅ Mobile menu toggle exists
- ✅ Form validation attributes
- ✅ Protected pages exist
- ✅ CSS stylesheets loaded
- ✅ JavaScript files loaded
