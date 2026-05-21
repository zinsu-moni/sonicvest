#!/usr/bin/env python3
"""
Test GTR Pay API response simulation
"""

def simulate_gtr_response():
    """Simulate what GTR Pay might be returning"""
    
    # Common response scenarios
    scenarios = [
        # Scenario 1: Success with proper structure
        {"code": "200", "data": {"payUrl": "https://pay.gtrpay.com/xyz123", "tradeNo": "TR123"}},
        
        # Scenario 2: Success message only (likely the problematic one)
        {"message": "success"},
        
        # Scenario 3: Success status only
        {"status": "success"},
        
        # Scenario 4: Code 200 but no data
        {"code": "200"},
        
        # Scenario 5: Different structure
        {"payUrl": "https://pay.gtrpay.com/direct123", "tradeNo": "TR456"}
    ]
    
    print("Testing different GTR Pay response scenarios:")
    print("=" * 50)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {scenario}")
        
        # Simulate our response handling logic
        if isinstance(scenario, dict):
            # Case 1: Standard success response with data structure
            if (scenario.get('code') == '200' or scenario.get('code') == 200) and 'data' in scenario:
                payment_data = scenario['data']
                if 'payUrl' in payment_data:
                    result = {
                        'success': True,
                        'payment_url': payment_data['payUrl'],
                        'trade_no': payment_data.get('tradeNo', 'REF123'),
                        'reference': 'REF123'
                    }
                    print(f"✅ Result: {result}")
                    continue
            
            # Case 2: Direct success response with payment URL
            elif 'payUrl' in scenario:
                result = {
                    'success': True,
                    'payment_url': scenario['payUrl'],
                    'trade_no': scenario.get('tradeNo', 'REF123'),
                    'reference': 'REF123'
                }
                print(f"✅ Result: {result}")
                continue
            
            # Case 3: Success message but no payment URL - this is likely the issue
            elif (scenario.get('message') == 'success' or 
                  scenario.get('status') == 'success' or
                  str(scenario.get('code')) == '200'):
                print(f"⚠️ GTR Pay returned success but no payment URL")
                result = {
                    'success': False,
                    'message': 'GTR Pay API returned success but no payment URL. Please check your merchant configuration.'
                }
                print(f"❌ Result: {result}")
                continue
            
            # Case 4: Error response
            else:
                error_msg = (scenario.get('msg') or 
                           scenario.get('message') or 
                           scenario.get('error') or 
                           f'Unknown error from payment gateway. Response: {scenario}')
                
                # Avoid recursive error messages
                if error_msg == 'success':
                    error_msg = 'GTR Pay returned "success" but payment creation failed. Please check configuration.'
                
                result = {
                    'success': False,
                    'message': error_msg
                }
                print(f"❌ Result: {result}")

if __name__ == "__main__":
    simulate_gtr_response()
