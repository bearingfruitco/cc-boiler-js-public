import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { tcpaVerifications } from '@/lib/db/schema/tcpa';

export async function POST(request: Request) {
  try {
    const { certUrl, apiKey } = await request.json();
    
    if (!certUrl) {
      return NextResponse.json(
        { error: 'Certificate URL is required' },
        { status: 400 }
      );
    }
    
    // Verify with TrustedForm API
    const trustedFormApiKey = apiKey || process.env.TRUSTEDFORM_API_KEY;
    
    if (!trustedFormApiKey) {
      console.error('[TrustedForm] API key not configured');
      return NextResponse.json(
        { error: 'TrustedForm not configured' },
        { status: 500 }
      );
    }
    
    // Call TrustedForm API to verify certificate
    const verifyResponse = await fetch(certUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${trustedFormApiKey}`,
        'Accept': 'application/json'
      }
    });
    
    const verificationData = await verifyResponse.json();
    const isValid = verifyResponse.ok && verificationData.cert;
    
    // Store verification result
    await db.insert(tcpaVerifications).values({
      certificateId: certUrl,
      verifiedAt: new Date(),
      valid: isValid,
      provider: 'trustedform',
      responseData: verificationData,
      errorMessage: isValid ? null : verificationData.message
    });
    
    return NextResponse.json({
      valid: isValid,
      data: isValid ? {
        ip: verificationData.ip,
        browser: verificationData.browser,
        os: verificationData.operating_system,
        timestamp: verificationData.created_at,
        expires: verificationData.expires_at,
        page_url: verificationData.page_url
      } : null,
      error: isValid ? null : verificationData.message
    });
    
  } catch (error) {
    console.error('[TrustedForm] Verification error:', error);
    return NextResponse.json(
      { error: 'Verification failed', valid: false },
      { status: 500 }
    );
  }
}
