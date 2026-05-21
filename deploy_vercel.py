#!/usr/bin/env python
"""
Quick deployment script for Vercel
Run this to deploy your app to Vercel with proper configuration
"""

import os
import sys
import secrets
import subprocess

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        result = subprocess.run(['vercel', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✅ Vercel CLI installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Vercel CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI not installed")
        return False
    except Exception as e:
        print(f"⚠️  Could not check Vercel CLI: {e}")
        return False

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def main():
    print("=" * 60)
    print("🚀 Vercel Deployment Helper")
    print("=" * 60)
    
    # Check if Vercel CLI is installed
    print("\n1️⃣  Checking Vercel CLI...")
    if not check_vercel_cli():
        print("\n💡 Install Vercel CLI first:")
        print("   npm install -g vercel")
        print("\n   Or download from: https://vercel.com/download")
        return False
    
    # Generate secret key
    print("\n2️⃣  Generating SECRET_KEY...")
    secret_key = generate_secret_key()
    print(f"✅ Generated: {secret_key}")
    print("\n⚠️  SAVE THIS KEY! You'll need it for Vercel environment variables")
    
    # Instructions
    print("\n" + "=" * 60)
    print("📋 Deployment Steps")
    print("=" * 60)
    
    print("\n1. Login to Vercel:")
    print("   vercel login")
    
    print("\n2. Set SECRET_KEY environment variable:")
    print("   vercel env add SECRET_KEY production")
    print(f"   Then paste: {secret_key}")
    
    print("\n3. Set FLASK_ENV:")
    print("   vercel env add FLASK_ENV production")
    print("   Then type: production")
    
    print("\n4. Deploy to production:")
    print("   vercel --prod")
    
    print("\n" + "=" * 60)
    print("⚠️  IMPORTANT: Database Considerations")
    print("=" * 60)
    print("\nVercel is serverless - SQLite won't persist between deployments.")
    print("For production, use a cloud database:")
    print("  • Supabase (PostgreSQL) - Free tier available")
    print("  • PlanetScale (MySQL) - Free tier available")
    print("  • Railway (PostgreSQL) - Free tier available")
    print("\nSee VERCEL_DEPLOYMENT.md for detailed database setup.")
    
    print("\n" + "=" * 60)
    print("🚀 Quick Deploy")
    print("=" * 60)
    
    choice = input("\nWould you like to deploy now? (y/n): ").lower().strip()
    
    if choice == 'y':
        print("\n🚀 Deploying to Vercel...")
        try:
            # Check if user is logged in
            result = subprocess.run(['vercel', 'whoami'], 
                                  capture_output=True, 
                                  timeout=10)
            
            if result.returncode != 0:
                print("\n❌ Not logged in to Vercel")
                print("Run: vercel login")
                return False
            
            print("✅ Logged in to Vercel")
            
            # Deploy
            print("\n📦 Starting deployment...")
            subprocess.run(['vercel', '--prod'], timeout=300)
            
            print("\n✅ Deployment initiated!")
            print("\n📝 Remember to set environment variables in Vercel dashboard:")
            print(f"   SECRET_KEY = {secret_key}")
            print("   FLASK_ENV = production")
            
        except subprocess.TimeoutExpired:
            print("\n⚠️  Deployment is taking longer than expected")
            print("   Check Vercel dashboard for status")
        except Exception as e:
            print(f"\n❌ Deployment error: {e}")
            print("\n💡 Try deploying manually:")
            print("   vercel --prod")
    else:
        print("\n📝 Deploy later with: vercel --prod")
    
    print("\n" + "=" * 60)
    print("📖 For detailed instructions, see: VERCEL_DEPLOYMENT.md")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
