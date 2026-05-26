const { chromium } = require("playwright");
const path = require("node:path");

(async () => {
  const launchOptions = { headless: true };
  if (process.env.CHROME_PATH) {
    launchOptions.executablePath = process.env.CHROME_PATH;
  }
  const browser = await chromium.launch(launchOptions);
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.addInitScript(() => {
    window.API_BASE_URL = "http://mock.resume-ai.local";
  });
  await page.route("**/api/v1/analyze", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({
        score: 86,
        verdict: "Strong match. Your resume is closely aligned with the job description.",
        matched_keywords: ["python", "fastapi", "docker", "aws", "eks", "redis", "ci/cd", "prometheus"],
        missing_keywords: ["terraform", "argo", "helm"],
        skill_matches: [],
        strengths: ["Your resume already includes relevant backend and cloud keywords."],
        improvements: [
          "Add one bullet explaining how you used Terraform to provision AWS infrastructure.",
          "Mention Argo CD and Helm if you deployed the app through GitOps.",
          "Add numbers where possible, such as users, latency, cost, accuracy, or time saved."
        ],
        suggested_summary: "Backend developer with hands-on FastAPI, Docker, AWS, EKS, Redis, and CI/CD experience."
      }),
    });
  });

  const indexPath = path.resolve("apps/resume-ai-web/index.html");
  await page.goto(`file://${indexPath}`, { waitUntil: "domcontentloaded" });
  await page.click("text=Analyze Resume");
  await page.waitForFunction(() => document.querySelector("#score")?.textContent !== "--", null, {
    timeout: 10000,
  });
  await page.screenshot({ path: "docs/linkedin-screenshot-local.png", fullPage: true });
  await browser.close();
})();
