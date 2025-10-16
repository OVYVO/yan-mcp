// Minimal MCP server (TypeScript) exposing a single tool: get_shanghai_weather
// Reference: modelcontextprotocol/typescript-sdk README
// https://github.com/modelcontextprotocol/typescript-sdk?tab=readme-ov-file

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

type WeatherCondition =
  | "sunny"
  | "cloudy"
  | "rainy"
  | "overcast"
  | "storm"
  | "windy";

function mockShanghaiWeather(date?: string) {
  const now = new Date();
  const seed = date ? new Date(date).getTime() : now.getTime();
  const rng = mulberry32(seed);

  const conditions: WeatherCondition[] = [
    "sunny",
    "cloudy",
    "rainy",
    "overcast",
    "windy",
  ];
  const condition = conditions[
    Math.floor(rng() * conditions.length)
  ] as WeatherCondition;
  const temperatureC = Math.round(10 + rng() * 20); // 10°C ~ 30°C
  const humidity = Math.round(40 + rng() * 50); // 40% ~ 90%
  const windKph = Math.round(5 + rng() * 25); // 5 ~ 30 kph

  return {
    city: "Shanghai",
    date: date ?? now.toISOString().slice(0, 10),
    condition,
    temperatureC,
    humidityPct: humidity,
    windKph,
    advisory: buildAdvisory(condition, temperatureC, humidity, windKph),
  };
}

function buildAdvisory(
  condition: WeatherCondition,
  temp: number,
  humidity: number,
  wind: number
): string {
  const tips: string[] = [];
  if (condition === "rainy" || condition === "overcast")
    tips.push("建议携带雨具");
  if (condition === "sunny" && temp >= 26) tips.push("注意防晒与补水");
  if (humidity >= 80) tips.push("闷热感较强，适当降温");
  if (wind >= 20) tips.push("风力较大，户外请注意安全");
  if (tips.length === 0) tips.push("天气整体舒适");
  return tips.join("；");
}

function mulberry32(seed: number) {
  let t = seed >>> 0;
  return function () {
    t += 0x6d2b79f5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

async function main() {
  const server = new McpServer({
    name: "shanghai-weather-mcp",
    version: "1.0.0",
  });

  server.tool(
    "get_shanghai_weather",
    {
      name: "get_shanghai_weather",
      description: "获取上海天气的 Mock 数据，可选按日期查询（YYYY-MM-DD）。",
      inputSchema: {
        type: "object",
        properties: {
          date: {
            type: "string",
            description: "可选，日期格式 YYYY-MM-DD",
          },
        },
      },
    },
    async ({ date }: { date?: string }) => {
      let normalizedDate: string | undefined = undefined;
      if (date) {
        const valid = /^\d{4}-\d{2}-\d{2}$/.test(date);
        if (!valid) {
          const error = {
            success: false,
            error: "Invalid date format, expected YYYY-MM-DD",
          };
          return {
            content: [{ type: "text", text: JSON.stringify(error) }],
            structuredContent: error,
          };
        }
        normalizedDate = date;
      }

      const data = mockShanghaiWeather(normalizedDate);
      const output = { success: true, data };
      return {
        content: [{ type: "text", text: JSON.stringify(output) }],
        structuredContent: output,
      };
    }
  );

  const transport = new StdioServerTransport();
  await server.connect(transport);

  const shutdown = async () => {
    try {
      await transport.close();
    } finally {
      process.exit(0);
    }
  };

  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
}

main().catch((err) => {
  console.error("[mcp] fatal:", err);
  process.exit(1);
});
