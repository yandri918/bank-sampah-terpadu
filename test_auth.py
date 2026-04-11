from modules import auth_db, auth_service
import os

def test_auth_flow():
    print("Testing Authentication Logic...")
    
    # Clean up old DB for testing if exists
    if os.path.exists("users.db"):
        # os.remove("users.db") # Risky in prod, but okay for dev verification if needed. 
        # Better: just use a unique email for testing
        pass

    auth_db.init_db()
    
    test_email = "test_auto@agrisensa.com"
    test_pass = "securepass123"
    test_name = "Automated Tester"
    
    # 1. Register
    print(f"1. Registering user: {test_email}...")
    success, msg = auth_service.register(test_email, test_pass, test_name)
    print(f"   Result: {success} ({msg})")
    
    # 2. Login Success
    print("2. Testing Correct Login...")
    # Mocking st.session_state for the service call
    class MockSessionState(dict):
        def __init__(self):
            self.update({'logged_in': False, 'user_info': {}})
            
    import streamlit as st
    if not hasattr(st, 'session_state'):
        st.session_state = MockSessionState()
        
    login_success = auth_service.login(test_email, test_pass)
    print(f"   Login Result: {login_success}")
    assert login_success == True, "Login should succeed"
    assert st.session_state['logged_in'] == True
    assert st.session_state['user_info']['email'] == test_email
    
    # 3. Login Fail
    print("3. Testing Incorrect Password...")
    login_fail = auth_service.login(test_email, "wrongpass")
    print(f"   Login Result: {login_fail}")
    assert login_fail == False, "Login should fail"
    
    print("\nAuthentication Backend Verified! ✅")

if __name__ == "__main__":
    test_auth_flow()
