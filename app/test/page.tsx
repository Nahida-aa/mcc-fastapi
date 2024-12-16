import React from 'react'

// 从服务器接收的 access_token
const accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik5haGlkYS1hYSIsInNjb3BlcyI6W10sImV4cCI6MTczNDc4MDc3OX0.not6SX55YBSbZo0ei8Uq_nl7jBs3sJStMx4vjVq_BTc";

// 解码 JWT 以获取过期时间
function parseJwt(token: string) {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  return JSON.parse(jsonPayload);
}

const decodedToken = parseJwt(accessToken);
const expTimestamp = decodedToken.exp * 1000; // 将秒转换为毫秒

// // 设置 access_token 的 Cookie 过期时间
const accessTokenExpires = new Date(expTimestamp).toUTCString();
// document.cookie = `access_token=${accessToken}; expires=${accessTokenExpires}; path=/; secure; HttpOnly`;

export default function testPage() {
  return (
    <main>
      <pre>
        decodedToken: {JSON.stringify(decodedToken, null, 2)}
      </pre>
      <pre>
        expTimestamp: {expTimestamp},
        accessTokenExpires: {accessTokenExpires}
      </pre>
    </main>
  )
}
