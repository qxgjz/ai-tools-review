import { NextRequest, NextResponse } from 'next/server';
import { JWT } from 'google-auth-library';

// 服务账号配置（从JSON文件中提取）
const SERVICE_ACCOUNT = {
  client_email: 'aitoolcrux-bot@aitoolcrux-automation.iam.gserviceaccount.com',
  private_key: `-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDWE22AS07qBP0Q
NRWQTDgR3CaV4+eC2OyoXYUavhg+WRsfUN89EUM/DpuNx8bORyckHHAKm2zTmMLx
vP44bnsfPfsROBhB7etn9tMKIK7k6JIusoMoMhf7gIhzpyeel9zl/85dYmR+NtIu
HxiXrKXsjP4cIF9xw0G6GKKjTa01vYT1KD35Rj+Q4Zss2xFIjeBo2A2dPLopAdZ8
YYk1fdFgh+NqrNLg21tI+IfIQVhlaDlxfhGAgFq2GXKnu1X0TnWxUJay0WBtkhjI
69S0jE1DzQBnzombdLddwOxgP8sUEhOtQKXUiNflPe4zmsRaXqqBjEBKS6CfFtw3
Eu0OgP6xAgMBAAECggEANzi8uubyPNC7nNYssVPP9N92vpyTCEA/z/CL2MmnhFHE
+s+IPn74+0ef3bNmd6iIErsZNctBB9Y0l1oas+Df9r+sx5TSQROH8YIMj2S96MOL
jeszhQdjA1f1GuxH/pOLAnN5vsIWTS6ECiywUdPR21LFa+j35ecpycD4Fyr+3skC
5NcJcpY4T4DGcc4l+ySWkKvyDdavkassogQCiRHJRpk4rLf6zjP0XATXSQG6ygKL
pAa1F6QWI0RAcBM5udhLs790Ptgzp4oqf9dyIpubDA7sYg7gsW1GuDG7fYJ1Rbx+
DhWEneksz0rI3Bkz3GAX3BMji/g7zG1h/zcml3EANwKBgQD8xL92IJFoJ8gM0rU1
BPCkdLauPmuZzSS2UXCxWIBqUoum6O/sSgB7uQRGh4iPcm6HxrqvOeHbl0yAaE/f
J6PiTPcHeD/a1ZC0GFEwAtCZuH6JNA2yYbabmb6AaPrnc4goW4JwmZRIRhubSpj2
lMxJpIg+Txc+wmyfXCHM7xjV7wKBgQDY0AxAp86fu+KkCSOVqbzP0EOVsQweC06Q
m/Va5PkRAZsewl+atmbHTbsSAFs0TUKsZWz71AOh5/BsWS7hQuMsCGRAI9MPjti9
yJlXZWDovTIQ2dSHx+ASbjHemjGEWhrJs2BbLBKpdrF51kgi1h3AQQ7TWMTbiobP
0vtlNhMVXwKBgQDhv0oL0yxqLFVTdoAWGRJenkplNiRdWUT3e6a9DQCrdIt7B0D3
9GOYG/aAkx1Yl+e1ZbxnMLfRqb/OUts6vylzvC9HwZKt+9zfq3Qe//STxZ1lJlMx
RGmVcGsePiQPwDQTbx8BN3iiT9LqD2armtsUzlhL5dEp4PSoIt2hLM0uiwKBgHjH
DMxHrpbU92Ahpy0MLR4nCj8tLW7fJZjxCDDmNMkAeAUeiluJGKAV8QwKHsR39ZhL
t/ZhGNTse8YfuDnMJPi2hAIm8sBL9vlh8en5k46TNnykm/w3n98ke6thggwUla+e
uSKQ3qSAdkVE1VJyrIgYtcWOQbt647aJ9XlgMilJAoGBAOysdRlgHytyGAdRDE76
rG9YLJL1KiEy/HTRrPdc8zJFhtGQ0VHpynsXrfgo4Mg5fCXUA9uQJOdG/4c6po62
XTwinPMrtGoF6xhMlcifYrn/3wX5Cf6JTE6cb/505TCGNfOCx3+jnBZ/kbEl0sqT
6id/Ziv+s8NLDrfZYSKZiD7a
-----END PRIVATE KEY-----
`,
};

// GA4属性ID
const GA4_PROPERTY_ID = '549695344';

// 简单的API密钥验证（防止滥用）
const API_SECRET = 'aitoolcrux-ga4-proxy-2026';

export async function POST(request: NextRequest) {
  try {
    // 验证API密钥
    const authHeader = request.headers.get('authorization');
    if (!authHeader || authHeader !== `Bearer ${API_SECRET}`) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // 解析请求体
    const body = await request.json();
    const { startDate, endDate } = body;

    if (!startDate || !endDate) {
      return NextResponse.json({ error: 'startDate and endDate are required' }, { status: 400 });
    }

    // 创建JWT客户端
    const client = new JWT({
      email: SERVICE_ACCOUNT.client_email,
      key: SERVICE_ACCOUNT.private_key,
      scopes: ['https://www.googleapis.com/auth/analytics.readonly'],
    });

    // 获取访问令牌
    const token = await client.getAccessToken();

    // 调用Google Analytics Data API
    const response = await fetch(
      `https://analyticsdata.googleapis.com/v1beta/properties/${GA4_PROPERTY_ID}:runReport`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          dateRanges: [{ startDate, endDate }],
          dimensions: [{ name: 'date' }, { name: 'pagePath' }, { name: 'deviceCategory' }],
          metrics: [
            { name: 'activeUsers' },
            { name: 'screenPageViews' },
            { name: 'averageSessionDuration' },
            { name: 'bounceRate' },
            { name: 'conversions' },
          ],
          limit: 10000,
        }),
      },
    );

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: `GA4 API error: ${response.status}`, details: errorText },
        { status: response.status },
      );
    }

    const data = await response.json();

    // 处理和汇总数据
    const result = processGa4Data(data);

    return NextResponse.json(result);
  } catch (error: any) {
    console.error('GA4 Proxy Error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 },
    );
  }
}

function processGa4Data(data: any) {
  const rows = data.rows || [];

  let totalUsers = 0;
  let totalPageviews = 0;
  let totalSessionDuration = 0;
  let totalBounceRate = 0;
  let totalConversions = 0;
  let count = 0;

  const topPages: any[] = [];
  const devices: any[] = [];
  const dailyTrend: any[] = [];

  const pageMap = new Map<string, { users: number; pageviews: number }>();
  const deviceMap = new Map<string, { users: number; pageviews: number }>();
  const dateMap = new Map<string, { users: number; pageviews: number }>();

  for (const row of rows) {
    const dimensionValues = row.dimensionValues || [];
    const metricValues = row.metricValues || [];

    const date = dimensionValues[0]?.value || '';
    const pagePath = dimensionValues[1]?.value || '';
    const deviceCategory = dimensionValues[2]?.value || '';

    const users = parseInt(metricValues[0]?.value || '0');
    const pageviews = parseInt(metricValues[1]?.value || '0');
    const sessionDuration = parseFloat(metricValues[2]?.value || '0');
    const bounceRate = parseFloat(metricValues[3]?.value || '0');
    const conversions = parseInt(metricValues[4]?.value || '0');

    totalUsers += users;
    totalPageviews += pageviews;
    totalSessionDuration += sessionDuration;
    totalBounceRate += bounceRate;
    totalConversions += conversions;
    count++;

    // 按页面汇总
    if (pagePath) {
      const existing = pageMap.get(pagePath) || { users: 0, pageviews: 0 };
      existing.users += users;
      existing.pageviews += pageviews;
      pageMap.set(pagePath, existing);
    }

    // 按设备汇总
    if (deviceCategory) {
      const existing = deviceMap.get(deviceCategory) || { users: 0, pageviews: 0 };
      existing.users += users;
      existing.pageviews += pageviews;
      deviceMap.set(deviceCategory, existing);
    }

    // 按日期汇总
    if (date) {
      const existing = dateMap.get(date) || { users: 0, pageviews: 0 };
      existing.users += users;
      existing.pageviews += pageviews;
      dateMap.set(date, existing);
    }
  }

  // 转换为数组并排序
  for (const [path, data] of pageMap) {
    topPages.push({ pagePath: path, users: data.users, pageviews: data.pageviews });
  }
  topPages.sort((a, b) => b.pageviews - a.pageviews);

  for (const [device, data] of deviceMap) {
    devices.push({ deviceCategory: device, users: data.users, pageviews: data.pageviews });
  }

  for (const [date, data] of dateMap) {
    dailyTrend.push({ date, users: data.users, pageviews: data.pageviews });
  }
  dailyTrend.sort((a, b) => a.date.localeCompare(b.date));

  return {
    totalUsers,
    totalPageviews,
    avgSessionDuration: count > 0 ? totalSessionDuration / count : 0,
    avgBounceRate: count > 0 ? (totalBounceRate / count) * 100 : 0,
    totalConversions,
    topPages: topPages.slice(0, 20),
    devices,
    dailyTrend,
    totalRows: rows.length,
  };
}
