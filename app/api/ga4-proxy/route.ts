import { NextRequest, NextResponse } from 'next/server';
import { JWT } from 'google-auth-library';

// 服务账号配置（从JSON文件中提取）
const SERVICE_ACCOUNT = {
  client_email: 'ga4-api-access@aitoolcrux-analytics.iam.gserviceaccount.com',
  private_key: `-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6BrLVsKp/Yiq3
DdvHaV0OHhVgDG/nhLjgNsNnnBeRwjLwYUH1KhC/N+1izyj8BzS0HY4DlOGDkcDa
XJi0GjPLvfTMB7p1S8+WTCBKyixUy2mLgNfiqFRFrfxqufeZmtb0nmsnV2Yh7FNt
SHZMILQBXjRxawEVRRnSygIJgON5Gm4LePiTO6DQT0fd3Ya9NdEZ9zgB9Q+irUuH
z3F3BpRJbE+6WREbf8SQldF6gW2W8i37RIDsz90FlAuVxwIHQquXRAjhgUzoisI6
dyqc3OMhMRQftfW7R6PYWkdMpGQ74NXTeJ+7Q0CO2u5qj38h13KZNt5ApI4aRF+9
BNHxOAgPAgMBAAECggEADLzbrv0nV4yZvyoQRAHHcOmHbim72d8BJ70oOSZ7iKwC
/+mw8gAc4HMMaqkjtcoqhjDF4iHmJTOsQGd5v09R/5/0rKnUzyZPQwvYZDaevXmm
MvqyDZ+YEaNdttMgDKEJGfvk+28lG6qKdd+x1fmhSbyxG5kHnHS8VW4moI72RHr4
bkZol1Uyo6mnf1AK16vIehrwkxaAOKwAymJYRu0rUvrRSjx3ad6E3ALknb4r7Jhd
55dn9dGQlmNlw/zmtyxBSW/BQuPrG1L5lDxKN5I4OkjIVgxuJ4YWEcHRV+io2QRl
Oa+XNRXD3JuuHYbuC6XXPBy2iGAE4OGTfrkMBfLkrQKBgQDbEjikkuNZXi/EaWi0
INMlmCsAR7lv1jM+9r9lGzcvPzlHoHWuncmulUUyUMIXW/gbacOtV5f1rSR7C+S0
wl7H6u7/Q0lp3mtHVgteIW/gp2zn19amDGVG4bpmHemdVDLy4OmKVCz/rz7QTya/
35biR7IgYkhPI6G96CicNUe5MwKBgQDZYnStPPg90BA3Nod35LbdB86EkZUV2S99
ht88LWe5sIqVfWvVXYMLQUwxe1ZU5y+rJNa8oxRXC/5CgR4iBeIQ7efdvYbtGDWB
f20dEccZUqjlwFdTyw1JNJWa+QxBJbue/9yIDs7Gr25TCQJB5I70GNEBdvWEidHu
dSHhE3uNtQKBgEBdJyU7Pu7H3HLxoWCi8EZwYdnwOMxh+6Z5KpyTFXCdO8AOpeTK
2TGhC7aPwabJT6kGNwab4Lq+xyQbx3NQVDaakOOQqmYfghdwcWCTpGI17qpjYN5i
b/MWaQSNr1CZJ2ryp8sLljj9DRB44OKo15TeCbi4B5Sw3FmGd0AF62+/AoGAJ4qq
MIzjltLO8Ewh7iQTQzdVUHXuyW+dHNc4qgiUUomTW8fZopEE8jopcuK9fGolGJt1
2BBN9dt/n3c/FO8/BNdRktsTvPLnYKveHCiMr8WCZXBMMjjALO28vNjKattDOpPN
+I3A/RESH1aHK5c4jZwqAHs0A6zSG+8Af6F8mvUCgYEA0Lh9RhoUo9wlFkiqRlQM
fC0uwROd1tqz6+BsuJ7McJW467vgooI3ix5MKDOeBEquCIMYa/PEzxi6vLBWk+PY
zEYSiIvglFY1N7SV4ZoNezIPR290YNV71BDi8xypIRqwe3HZw408eyKl6LMaanW3
CuSUBvCIh/1qCJ3CkiNTM7U=
-----END PRIVATE KEY-----`,
};

// GA4属性ID
const GA4_PROPERTY_ID = '552513639';

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
          'Authorization': `Bearer ${token.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          dateRanges: [{ startDate, endDate }],
          dimensions: [
            { name: 'date' },
            { name: 'pagePath' },
            { name: 'deviceCategory' },
          ],
          metrics: [
            { name: 'activeUsers' },
            { name: 'screenPageViews' },
            { name: 'averageSessionDuration' },
            { name: 'bounceRate' },
            { name: 'conversions' },
          ],
          limit: 10000,
        }),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: `GA4 API error: ${response.status}`, details: errorText },
        { status: response.status }
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
      { status: 500 }
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
