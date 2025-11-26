// Cloudflare Pages Functions를 사용한 API 프록시
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  
  // 백엔드 API URL (환경 변수에서 가져오거나 직접 설정)
  // Cloudflare Pages → Settings → Environment variables에서 BACKEND_URL 설정
  const backendUrl = context.env.BACKEND_URL || 'http://localhost:8000';
  
  if (!context.env.BACKEND_URL) {
    console.warn('BACKEND_URL 환경 변수가 설정되지 않았습니다. 기본값을 사용합니다.');
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
    return new Response(JSON.stringify({ error: 'Proxy error', message: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

