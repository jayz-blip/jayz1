// Cloudflare Pages Functions를 사용한 API 프록시
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  
  // 백엔드 API URL (환경 변수에서 가져오기)
  // Cloudflare Pages → Settings → Environment variables에서 BACKEND_URL 설정 필수
  const backendUrl = context.env.BACKEND_URL;
  
  if (!backendUrl) {
    return new Response(JSON.stringify({ 
      error: 'Backend URL not configured',
      message: 'BACKEND_URL environment variable is not set. Please configure it in Cloudflare Pages settings.',
      debug: {
        hasBackendUrl: false,
        envKeys: Object.keys(context.env || {})
      }
    }), {
      status: 500,
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
  
  // API 요청을 백엔드로 프록시
  const path = context.params.path ? `/${context.params.path.join('/')}` : '';
  const apiUrl = `${backendUrl}/api${path}${url.search}`;
  
  try {
    const response = await fetch(apiUrl, {
      method: request.method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: request.method !== 'GET' && request.method !== 'HEAD' ? await request.text() : null,
    });
    
    const data = await response.text();
    
    // Workers에서 오류가 발생한 경우
    if (!response.ok) {
      return new Response(JSON.stringify({ 
        error: 'Backend error',
        status: response.status,
        statusText: response.statusText,
        data: data,
        backendUrl: backendUrl,
        apiUrl: apiUrl
      }), {
        status: response.status,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }
    
    return new Response(data, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Proxy error', 
      message: error.message,
      stack: error.stack,
      backendUrl: backendUrl,
      apiUrl: apiUrl
    }), {
      status: 500,
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
}

