import { test, expect } from "@playwright/test";

test("homepage loads", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/AIToolCrux/i);
});

test("tool page loads", async ({ page }) => {
  await page.goto("/tools/midjourney");
  await expect(page.locator("h1")).toBeVisible();
});

test("blog post loads", async ({ page }) => {
  await page.goto("/blog/perplexity-ai-review-2026");
  await expect(page.locator("article")).toBeVisible();
});
